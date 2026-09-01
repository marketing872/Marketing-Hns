#!/usr/bin/env python3
"""
Lee los números de dorsal de las fotografías de un evento y arma la planilla
que consume la aplicación Tu Foto Nutrend.

Este script corre en el computador donde están las fotos: la carpeta de Drive
se descarga primero (botón Descargar de Google Drive, o la app Drive para
escritorio) y luego se le pasa la ruta local.

    pip install anthropic pillow
    export ANTHROPIC_API_KEY="sk-ant-..."
    python3 detectar-dorsales.py /ruta/a/las/fotos

Salida: planilla.csv, con una fila por fotografía, lista para

    python3 csv-a-datos.py planilla.csv > datos.js

Cómo trabaja cada foto:

  1. La reduce a 1568 px por el lado largo y se la manda a Claude, que informa
     los dorsales que alcanza a leer.
  2. Si en esa pasada no aparece ninguno, recorta la imagen en cuatro cuadrantes
     solapados y repite la lectura sobre cada uno. Un dorsal de 40 px en una foto
     de 6000 px se pierde al reducirla entera, pero sobrevive en el recorte.

El trabajo se guarda a medida que avanza en avance.jsonl, así que el script se
puede cortar y retomar sin repetir lo ya leído ni volver a pagarlo.
"""

import argparse
import base64
import csv
import io
import json
import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import anthropic
    from PIL import Image
except ImportError:
    sys.exit("Faltan dependencias. Instálalas con:  pip install anthropic pillow")


MODELO = "claude-opus-5"
# Sube a "high" si las fotos son difíciles; baja a "low" si quieres abaratar.
ESFUERZO = "medium"
LADO_MAXIMO = 1568          # resolución que aprovecha el modelo sin desperdiciar
CALIDAD_JPEG = 82
HILOS = 4
EXTENSIONES = (".jpg", ".jpeg", ".png")

INSTRUCCIONES = """Eres el asistente de un fotógrafo de carreras de ciclismo de montaña.

Tu tarea es leer los NÚMEROS DE DORSAL de los corredores que aparecen en la
fotografía. En MTB el dorsal va normalmente en una placa rígida sujeta al manubrio
de la bicicleta, y a veces también impreso en el maillot o en un adhesivo del casco.

Reglas:
- Informa únicamente números que puedas LEER de verdad en la imagen. Si un número
  está tapado, movido o demasiado lejos, no lo informes. Nunca adivines ni completes
  dígitos que no ves.
- Si la misma persona lleva el número en la placa y en el maillot, infórmalo una vez.
- Si hay varios corredores con dorsal legible, infórmalos todos.
- No confundas el dorsal con otros números de la escena: patentes de vehículos,
  marcas de bicicletas, tallas de ropa, publicidad, cronómetros o señalética.
- Conserva los ceros a la izquierda tal como aparecen impresos.

Devuelve además tu nivel de certeza:
- "alta": los dígitos se leen sin esfuerzo.
- "media": se leen, pero hay desenfoque, ángulo o sombra que dejan margen de duda.
- "baja": crees distinguir un número pero no lo afirmarías. Estas fotos se revisan a mano.

Si no hay ningún dorsal legible, devuelve la lista vacía y certeza "alta"."""

ESQUEMA = {
    "type": "object",
    "properties": {
        "dorsales": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Números de dorsal legibles en la imagen"
        },
        "certeza": {"type": "string", "enum": ["alta", "media", "baja"]}
    },
    "required": ["dorsales", "certeza"],
    "additionalProperties": False
}

candado = threading.Lock()


# ------------------------------------------------------------------ imágenes

def a_jpeg_base64(imagen):
    """Reduce la imagen al lado máximo útil y la codifica para la API."""
    imagen = imagen.convert("RGB")
    imagen.thumbnail((LADO_MAXIMO, LADO_MAXIMO), Image.LANCZOS)
    memoria = io.BytesIO()
    imagen.save(memoria, format="JPEG", quality=CALIDAD_JPEG)
    return base64.standard_b64encode(memoria.getvalue()).decode("utf-8")


def cuadrantes(imagen):
    """Cuatro recortes solapados, para que un dorsal en el borde no se parta."""
    ancho, alto = imagen.size
    solape = 0.12
    medio_x, medio_y = ancho / 2, alto / 2
    margen_x, margen_y = ancho * solape, alto * solape
    cajas = [
        (0, 0, medio_x + margen_x, medio_y + margen_y),
        (medio_x - margen_x, 0, ancho, medio_y + margen_y),
        (0, medio_y - margen_y, medio_x + margen_x, alto),
        (medio_x - margen_x, medio_y - margen_y, ancho, alto),
    ]
    return [imagen.crop(tuple(int(v) for v in caja)) for caja in cajas]


# ------------------------------------------------------------------ API

def preguntar(cliente, imagen_b64):
    """Una lectura. Devuelve (dorsales, certeza)."""
    parametros = dict(
        model=MODELO,
        max_tokens=4000,
        thinking={"type": "adaptive"},
        output_config={"effort": ESFUERZO, "format": {"type": "json_schema", "schema": ESQUEMA}},
        system=INSTRUCCIONES,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64", "media_type": "image/jpeg", "data": imagen_b64}},
                {"type": "text", "text": "¿Qué números de dorsal se leen en esta fotografía?"}
            ]
        }]
    )

    try:
        respuesta = cliente.beta.messages.create(
            betas=["server-side-fallback-2026-07-01"], fallbacks="default", **parametros)
    except anthropic.BadRequestError:
        # Cuenta sin el respaldo del lado del servidor: seguimos sin él.
        respuesta = cliente.messages.create(**parametros)

    if respuesta.stop_reason == "refusal":
        return [], "baja"

    texto = next((b.text for b in respuesta.content if b.type == "text"), "")
    if not texto:
        return [], "baja"

    datos = json.loads(texto)
    dorsales = [d.strip() for d in datos.get("dorsales", []) if str(d).strip()]
    # Sin duplicados, conservando el orden de lectura
    vistos, limpios = set(), []
    for d in dorsales:
        if d not in vistos:
            vistos.add(d)
            limpios.append(d)
    return limpios, datos.get("certeza", "media")


def leer_foto(cliente, ruta):
    """Pasada completa sobre una fotografía: entera y, si hace falta, por cuadrantes."""
    with Image.open(ruta) as original:
        original.load()
        entera = a_jpeg_base64(original.copy())
        dorsales, certeza = preguntar(cliente, entera)

        if dorsales:
            return {"dorsales": dorsales, "certeza": certeza, "pasada": "completa"}

        # Segunda pasada: los dorsales pequeños se pierden al reducir la foto entera
        encontrados, certezas = [], []
        for recorte in cuadrantes(original):
            parciales, certeza_parcial = preguntar(cliente, a_jpeg_base64(recorte))
            for d in parciales:
                if d not in encontrados:
                    encontrados.append(d)
                    certezas.append(certeza_parcial)

    if not encontrados:
        return {"dorsales": [], "certeza": "alta", "pasada": "cuadrantes"}

    peor = "baja" if "baja" in certezas else ("media" if "media" in certezas else "alta")
    return {"dorsales": encontrados, "certeza": peor, "pasada": "cuadrantes"}


# ------------------------------------------------------------------ avance

def cargar_avance(ruta):
    hechos = {}
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as archivo:
            for linea in archivo:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    fila = json.loads(linea)
                    hechos[fila["archivo"]] = fila
                except (ValueError, KeyError):
                    continue
    return hechos


def anotar(ruta, fila):
    with candado:
        with open(ruta, "a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(fila, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------ principal

def main():
    analizador = argparse.ArgumentParser(
        description="Lee los dorsales de las fotos de un evento y arma la planilla.")
    analizador.add_argument("carpeta", help="Carpeta local con las fotografías")
    analizador.add_argument("--salida", default="planilla.csv", help="Archivo CSV de salida")
    analizador.add_argument("--indice", default="fotos-drive.json",
                            help="Índice [nombre de archivo, ID de Drive]")
    analizador.add_argument("--avance", default="avance.jsonl",
                            help="Registro de trabajo ya hecho, para poder retomar")
    analizador.add_argument("--hilos", type=int, default=HILOS,
                            help="Fotografías leídas en paralelo")
    analizador.add_argument("--limite", type=int,
                            help="Procesa solo las primeras N fotos, para probar el costo")
    opciones = analizador.parse_args()

    if not os.path.isdir(opciones.carpeta):
        sys.exit("No existe la carpeta: " + opciones.carpeta)

    ids_drive = {}
    if os.path.exists(opciones.indice):
        with open(opciones.indice, encoding="utf-8") as archivo:
            ids_drive = {nombre: identificador for nombre, identificador in json.load(archivo)}
        print("Índice de Drive: %d archivos" % len(ids_drive))
    else:
        print("Sin índice de Drive: la planilla saldrá sin los ID de archivo.")

    fotos = sorted(
        f for f in os.listdir(opciones.carpeta)
        if f.lower().endswith(EXTENSIONES) and not f.startswith(".")
    )
    if not fotos:
        sys.exit("No hay fotografías en " + opciones.carpeta)

    if opciones.limite:
        fotos = fotos[:opciones.limite]

    hechos = cargar_avance(opciones.avance)
    pendientes = [f for f in fotos if f not in hechos]
    print("%d fotografías · %d ya leídas · %d por leer"
          % (len(fotos), len(fotos) - len(pendientes), len(pendientes)))

    cliente = anthropic.Anthropic()
    fallidas = []

    if pendientes:
        with ThreadPoolExecutor(max_workers=opciones.hilos) as grupo:
            tareas = {
                grupo.submit(leer_foto, cliente, os.path.join(opciones.carpeta, nombre)): nombre
                for nombre in pendientes
            }
            for indice, tarea in enumerate(as_completed(tareas), 1):
                nombre = tareas[tarea]
                try:
                    fila = tarea.result()
                except anthropic.RateLimitError:
                    fallidas.append((nombre, "límite de solicitudes alcanzado"))
                    continue
                except anthropic.APIStatusError as error:
                    fallidas.append((nombre, "error %s de la API" % error.status_code))
                    continue
                except anthropic.APIConnectionError:
                    fallidas.append((nombre, "no se pudo conectar"))
                    continue
                except (OSError, ValueError) as error:
                    fallidas.append((nombre, "no se pudo leer la imagen: %s" % error))
                    continue

                fila["archivo"] = nombre
                hechos[nombre] = fila
                anotar(opciones.avance, fila)
                print("[%d/%d] %s → %s (%s)" % (
                    indice, len(pendientes), nombre,
                    ", ".join(fila["dorsales"]) or "sin dorsal legible",
                    fila["certeza"]))

    with open(opciones.salida, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["codigo", "driveId", "dorsales", "nombres",
                           "tramo", "categoria", "hora", "revisar"])
        for nombre in fotos:
            fila = hechos.get(nombre)
            if not fila:
                continue
            revisar = "si" if fila["certeza"] == "baja" else ""
            escritor.writerow([
                nombre,
                ids_drive.get(nombre, ""),
                "|".join(fila["dorsales"]),
                "", "", "", "",
                revisar,
            ])

    con_dorsal = sum(1 for n in fotos if hechos.get(n, {}).get("dorsales"))
    por_revisar = sum(1 for n in fotos if hechos.get(n, {}).get("certeza") == "baja")
    print("\nPlanilla escrita en %s" % opciones.salida)
    print("  %d fotografías con dorsal identificado" % con_dorsal)
    print("  %d sin dorsal legible" % (len(hechos) - con_dorsal))
    print("  %d marcadas para revisar a mano (columna revisar)" % por_revisar)

    if fallidas:
        print("\n%d fotografías quedaron pendientes:" % len(fallidas))
        for nombre, motivo in fallidas[:10]:
            print("  %s: %s" % (nombre, motivo))
        print("Vuelve a ejecutar el script: retoma solo lo que falta.")


if __name__ == "__main__":
    main()
