#!/usr/bin/env python3
"""
Convierte la planilla de etiquetado en el bloque FOTOS que consume
tu-foto-nutrend.html.

Uso:
    python3 csv-a-datos.py planilla.csv > datos.js

Columnas esperadas (el orden no importa, los nombres sí):
    codigo     nombre del archivo original          HNS_0231.jpg
    driveId    ID del archivo en Google Drive       1aBcDeFg...
    dorsales   uno o varios, separados por |        231|87
    nombres    uno o varios, separados por |        Camila Rojas
    tramo      punto del recorrido                  Subida El Peral
    categoria  categoría de carrera                 Master A
    hora       hora de captura                      10:42

Las columnas vacías se aceptan: una foto sin dorsal legible aparece en el
filtro "Solo fotos sin dorsal legible" de la aplicación.

Después de generar el bloque, pégalo en tu-foto-nutrend.html reemplazando
la línea  let FOTOS = [];  y cambia  modoDemo: true  por  modoDemo: false.
"""

import csv
import json
import sys


def separar(valor):
    if not valor:
        return []
    return [parte.strip() for parte in valor.split("|") if parte.strip()]


def main():
    if len(sys.argv) < 2:
        sys.exit("Uso: python3 csv-a-datos.py planilla.csv > datos.js")

    fotos = []
    with open(sys.argv[1], newline="", encoding="utf-8-sig") as archivo:
        for fila in csv.DictReader(archivo):
            dorsales = []
            for numero in separar(fila.get("dorsales", "")):
                try:
                    dorsales.append(int(numero))
                except ValueError:
                    dorsales.append(numero)

            fotos.append({
                "codigo": (fila.get("codigo") or "").strip(),
                "driveId": (fila.get("driveId") or "").strip(),
                "dorsales": dorsales,
                "nombres": separar(fila.get("nombres", "")),
                "tramo": (fila.get("tramo") or "").strip(),
                "categoria": (fila.get("categoria") or "").strip(),
                "hora": (fila.get("hora") or "").strip(),
            })

    fotos.sort(key=lambda f: (f["hora"], f["codigo"]))

    sin_dorsal = sum(1 for f in fotos if not f["dorsales"])
    print("  // %d fotografías · %d sin dorsal legible" % (len(fotos), sin_dorsal))
    print("  let FOTOS = " + json.dumps(fotos, ensure_ascii=False, indent=2) + ";")


if __name__ == "__main__":
    main()
