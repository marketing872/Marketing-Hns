#!/usr/bin/env python3
"""Exporta a Excel los leads a partir de los .txt de "Exportar chat" de WhatsApp.

Sirve cuando no se puede hacer un backup del iPhone: se exporta cada chat
desde la app (Exportar chat > Sin archivos adjuntos), se juntan los .txt o
.zip en una carpeta y este script los convierte en un solo Excel.

Uso tipico:
    python3 desde_txt.py --carpeta ./chats --yo "HNS Nutrition" --salida leads.xlsx

Limitacion importante: si el contacto esta guardado en la agenda del iPhone,
el .txt trae el nombre y NO el numero. Para esos casos usa --mapa con un CSV
de "nombre,telefono", o usa mejor desde_backup.py.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import (  # noqa: E402
    TZ_CHILE,
    Conversacion,
    Mensaje,
    escribir_excel,
    limpiar,
    normalizar_telefono,
)

# iOS:     [15/9/26, 10:32:11] Juan Perez: Hola
# Android: 15/9/26, 10:32 - Juan Perez: Hola
LINEA_IOS = re.compile(r"^\[(?P<fecha>[^\]]+)\]\s*(?P<autor>[^:]{1,80}?):\s?(?P<texto>.*)$")
LINEA_ANDROID = re.compile(r"^(?P<fecha>\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4},?\s+\d{1,2}:\d{2}(?::\d{2})?(?:\s*[ap]\.?\s?m\.?)?)\s+-\s+(?P<autor>[^:]{1,80}?):\s?(?P<texto>.*)$", re.IGNORECASE)

FORMATOS_FECHA = [
    "%d/%m/%Y, %H:%M:%S", "%d/%m/%y, %H:%M:%S", "%d/%m/%Y %H:%M:%S", "%d/%m/%y %H:%M:%S",
    "%d/%m/%Y, %H:%M", "%d/%m/%y, %H:%M", "%d-%m-%Y, %H:%M:%S", "%d-%m-%y, %H:%M:%S",
    "%d-%m-%Y %H:%M:%S", "%d-%m-%y %H:%M:%S", "%d-%m-%Y, %H:%M", "%d-%m-%y, %H:%M",
    "%m/%d/%y, %I:%M:%S %p", "%m/%d/%Y, %I:%M:%S %p", "%d/%m/%Y, %I:%M:%S %p",
    "%d/%m/%y, %I:%M:%S %p", "%d/%m/%y, %I:%M %p", "%Y-%m-%d %H:%M:%S",
]

ADJUNTOS = re.compile(
    r"(imagen omitida|video omitido|audio omitido|sticker omitido|GIF omitido|"
    r"documento omitido|archivo adjunto|image omitted|video omitted|audio omitted)",
    re.IGNORECASE,
)
SISTEMA = re.compile(
    r"(cifrados de extremo a extremo|end-to-end encrypted|creo el grupo|created group|"
    r"cambio su numero|changed their phone number|Los mensajes y las llamadas)",
    re.IGNORECASE,
)


def parsear_fecha(crudo: str) -> datetime | None:
    crudo = limpiar(crudo).replace(" ", " ").replace("a. m.", "AM").replace("p. m.", "PM")
    crudo = crudo.replace("a.m.", "AM").replace("p.m.", "PM")
    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(crudo, formato).replace(tzinfo=TZ_CHILE)
        except ValueError:
            continue
    return None


def parsear_txt(contenido: str) -> list[tuple[datetime | None, str, str]]:
    """Devuelve (fecha, autor, texto) por mensaje, uniendo lineas continuadas."""
    mensajes: list[list] = []
    for linea_cruda in contenido.splitlines():
        linea = limpiar(linea_cruda)
        if not linea:
            continue
        coincidencia = LINEA_IOS.match(linea) or LINEA_ANDROID.match(linea)
        if coincidencia:
            mensajes.append([
                parsear_fecha(coincidencia.group("fecha")),
                limpiar(coincidencia.group("autor")),
                limpiar(coincidencia.group("texto")),
            ])
        elif mensajes:  # continuacion de un mensaje multilinea
            mensajes[-1][2] = (mensajes[-1][2] + "\n" + linea).strip()
    return [(f, a, t) for f, a, t in mensajes if not SISTEMA.search(t)]


def cargar_archivos(carpeta: Path) -> list[tuple[str, str]]:
    """Lee .txt sueltos y .zip exportados por WhatsApp. Devuelve (etiqueta, contenido)."""
    salida: list[tuple[str, str]] = []
    for ruta in sorted(carpeta.rglob("*")):
        if ruta.suffix.lower() == ".txt":
            etiqueta = ruta.stem
            if etiqueta.lower() in ("_chat", "chat"):
                etiqueta = ruta.parent.name
            salida.append((etiqueta, ruta.read_text(encoding="utf-8", errors="replace")))
        elif ruta.suffix.lower() == ".zip":
            with zipfile.ZipFile(ruta) as z:
                for interno in z.namelist():
                    if interno.lower().endswith(".txt"):
                        salida.append((ruta.stem, z.read(interno).decode("utf-8", "replace")))
    return salida


def parece_telefono(texto: str) -> bool:
    """True si el texto es un numero, aunque venga espaciado: '+56 9 4444 5555'."""
    texto = limpiar(texto)
    if not re.fullmatch(r"[+\d\s().\-]{7,}", texto or ""):
        return False
    return len(re.sub(r"\D", "", texto)) >= 8


def nombre_desde_etiqueta(etiqueta: str) -> str:
    """'Chat de WhatsApp con Juan Perez' -> 'Juan Perez'."""
    limpio = re.sub(
        r"^(chat de whatsapp con|whatsapp chat with|chat con)\s+", "", etiqueta, flags=re.IGNORECASE
    )
    return limpiar(limpio)


def detectar_mi_nombre(archivos: list[tuple[str, str]]) -> str:
    """El autor que aparece en mas chats distintos es, casi seguro, la cuenta HNS."""
    apariciones: dict[str, int] = {}
    for _, contenido in archivos:
        autores = {a for _, a, _ in parsear_txt(contenido)}
        for autor in autores:
            apariciones[autor] = apariciones.get(autor, 0) + 1
    if not apariciones:
        return ""
    autor, veces = max(apariciones.items(), key=lambda kv: kv[1])
    return autor if veces > 1 else ""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convierte exportaciones .txt/.zip de WhatsApp en un Excel de leads."
    )
    parser.add_argument("--carpeta", required=True, help="Carpeta con los .txt o .zip exportados")
    parser.add_argument("--salida", default="leads_whatsapp_hns.xlsx", help="Archivo Excel de salida")
    parser.add_argument("--yo", help="Nombre exacto con que aparece la cuenta de HNS en los chats")
    parser.add_argument("--mapa", help="CSV 'nombre,telefono' para contactos guardados sin numero")
    parser.add_argument("--transcripciones", help="Carpeta donde guardar un .txt por lead sin contestar")
    args = parser.parse_args()

    carpeta = Path(args.carpeta).expanduser()
    if not carpeta.is_dir():
        raise SystemExit(f"No existe la carpeta {carpeta}")
    archivos = cargar_archivos(carpeta)
    if not archivos:
        raise SystemExit(f"No encontre .txt ni .zip dentro de {carpeta}")

    mapa: dict[str, str] = {}
    if args.mapa:
        with open(Path(args.mapa).expanduser(), newline="", encoding="utf-8-sig") as fh:
            for fila in csv.reader(fh):
                if len(fila) >= 2:
                    mapa[limpiar(fila[0]).lower()] = normalizar_telefono(fila[1])

    mi_nombre = limpiar(args.yo) if args.yo else detectar_mi_nombre(archivos)
    if not mi_nombre:
        raise SystemExit(
            "No pude deducir con que nombre aparece la cuenta de HNS en los chats.\n"
            "Indicalo con --yo \"Nombre tal como sale en el chat\"."
        )
    print(f"Cuenta propia detectada como: {mi_nombre}")

    conversaciones: list[Conversacion] = []
    for etiqueta, contenido in archivos:
        crudos = parsear_txt(contenido)
        if not crudos:
            continue
        nombre_chat = nombre_desde_etiqueta(etiqueta)
        telefono = normalizar_telefono(nombre_chat) if parece_telefono(nombre_chat) else ""
        mensajes = []
        for fecha, autor, texto in crudos:
            de_mi = autor == mi_nombre
            if not de_mi and not telefono:
                telefono = normalizar_telefono(autor) if parece_telefono(autor) else telefono
            mensajes.append(
                Mensaje(
                    fecha=fecha,
                    de_mi=de_mi,
                    autor=autor,
                    texto=texto,
                    tipo="adjunto" if ADJUNTOS.search(texto) else "texto",
                )
            )
        if not telefono:
            telefono = mapa.get(nombre_chat.lower(), "")
        conversaciones.append(
            Conversacion(
                jid="",
                telefono=telefono,
                nombre=nombre_chat or telefono,
                mensajes=mensajes,
            )
        )

    destino = escribir_excel(
        Path(args.salida),
        conversaciones,
        Path(args.transcripciones) if args.transcripciones else None,
    )
    pendientes = [c for c in conversaciones if c.sin_contestar]
    sin_tel = sum(1 for c in pendientes if not c.telefono)
    print(f"Chats procesados:    {len(conversaciones)}")
    print(f"Leads sin contestar: {len(pendientes)}")
    if sin_tel:
        print(f"Aviso: {sin_tel} leads sin telefono (contacto guardado). Usa --mapa o desde_backup.py.")
    print(f"Excel generado en:   {destino.resolve()}")


if __name__ == "__main__":
    main()
