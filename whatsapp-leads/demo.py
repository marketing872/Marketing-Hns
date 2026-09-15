#!/usr/bin/env python3
"""Genera datos ficticios y produce un Excel de ejemplo.

Sirve para (a) ver el formato de salida antes de tocar datos reales y
(b) verificar que el entorno (Python + openpyxl) quedo bien instalado.

    python3 demo.py --salida ejemplo_leads.xlsx
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from desde_backup import EPOCA_APPLE, leer_conversaciones  # noqa: E402
from comun import TZ_CHILE, escribir_excel  # noqa: E402

ESQUEMA = """
CREATE TABLE ZWACHATSESSION (
    Z_PK INTEGER PRIMARY KEY, ZCONTACTJID TEXT, ZPARTNERNAME TEXT,
    ZUNREADCOUNT INTEGER, ZARCHIVED INTEGER, ZSESSIONTYPE INTEGER, ZLASTMESSAGEDATE REAL);
CREATE TABLE ZWAMESSAGE (
    Z_PK INTEGER PRIMARY KEY, ZCHATSESSION INTEGER, ZISFROMME INTEGER,
    ZMESSAGEDATE REAL, ZTEXT TEXT, ZMESSAGETYPE INTEGER, ZPUSHNAME TEXT);
CREATE TABLE ZWALABEL (Z_PK INTEGER PRIMARY KEY, ZLABELNAME TEXT);
CREATE TABLE ZWALABELCHATSESSION (Z_PK INTEGER PRIMARY KEY, ZCHATSESSION INTEGER, ZLABEL INTEGER);
"""

AHORA = datetime.now(TZ_CHILE)

CHATS = [
    # (jid, nombre, no_leidos, archivado, etiqueta, [(dias_atras, de_mi, texto)])
    ("56912345678@s.whatsapp.net", "Distribuidora Andes", 3, 0, 1, [
        (4.0, 0, "Hola, necesito cotizacion por mayor de Dy Nutrition proteina 2kg"),
        (4.0, 0, "Somos tienda en Rancagua, cual es el minimo de compra?"),
        (3.9, 0, "Quedo atento"),
    ]),
    ("56987654321@s.whatsapp.net", "Gimnasio Iron Buin", 1, 0, 2, [
        (11.0, 0, "Buenas, tienen stock de BSN Syntha-6?"),
        (10.9, 1, "Hola! Si, tenemos stock. Te envio lista de precios mayorista."),
        (10.5, 0, "Perfecto. Y precio por 12 unidades de Prosupps Hyde?"),
    ]),
    ("56911112222@s.whatsapp.net", "Nutricion Vina", 0, 0, None, [
        (2.0, 0, "Hola, quiero ser distribuidor de 4Active"),
        (1.9, 1, "Hola! Te envio el kit de distribuidor y condiciones."),
        (1.8, 0, "Gracias, lo reviso"),
        (1.7, 1, "Quedo atento a tus comentarios."),
    ]),
    ("56933334444@s.whatsapp.net", "+56 9 3333 4444", 2, 0, 1, [
        (0.6, 0, "Buenas tardes, venden Biotech USA al por mayor?"),
        (0.5, 0, "[imagen]"),
    ]),
    ("56955556666@s.whatsapp.net", "Suplementos Maipu", 0, 1, None, [
        (45.0, 0, "Hola, consulta por Swanson"),
        (44.0, 1, "Hola, te comparto catalogo."),
    ]),
]


def crear_db(ruta: Path) -> Path:
    con = sqlite3.connect(ruta)
    con.executescript(ESQUEMA)
    con.execute("INSERT INTO ZWALABEL VALUES (1, 'Nuevo cliente')")
    con.execute("INSERT INTO ZWALABEL VALUES (2, 'Cotizacion enviada')")
    mid = 1
    for pk, (jid, nombre, no_leidos, archivado, etiqueta, mensajes) in enumerate(CHATS, start=1):
        ultima = min(d for d, _, _ in mensajes)
        con.execute(
            "INSERT INTO ZWACHATSESSION VALUES (?,?,?,?,?,?,?)",
            (pk, jid, nombre, no_leidos, archivado, 0,
             ((AHORA - timedelta(days=ultima)).astimezone(timezone.utc) - EPOCA_APPLE).total_seconds()),
        )
        if etiqueta:
            con.execute("INSERT INTO ZWALABELCHATSESSION VALUES (?,?,?)", (pk, pk, etiqueta))
        for dias, de_mi, texto in mensajes:
            segundos = ((AHORA - timedelta(days=dias)).astimezone(timezone.utc) - EPOCA_APPLE).total_seconds()
            con.execute(
                "INSERT INTO ZWAMESSAGE VALUES (?,?,?,?,?,?,?)",
                (mid, pk, de_mi, segundos, texto, 1 if texto.startswith("[imagen]") else 0, nombre),
            )
            mid += 1
    # Mensaje de sistema: debe ser ignorado por el exportador.
    con.execute("INSERT INTO ZWAMESSAGE VALUES (?,?,?,?,?,?,?)",
                (mid, 1, 0, 0, "Los mensajes estan cifrados", 6, ""))
    con.commit()
    con.close()
    return ruta


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera un Excel de ejemplo con datos ficticios.")
    parser.add_argument("--salida", default="ejemplo_leads.xlsx")
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmp:
        db = crear_db(Path(tmp) / "ChatStorage.sqlite")
        conversaciones = leer_conversaciones(db)
        destino = escribir_excel(Path(args.salida), conversaciones)

    for conv in conversaciones:
        print(f"  {conv.telefono:<15} {conv.nombre:<24} {conv.estado:<22} {conv.dias_de_espera()}")
    print(f"\nExcel de ejemplo: {destino.resolve()}")


if __name__ == "__main__":
    main()
