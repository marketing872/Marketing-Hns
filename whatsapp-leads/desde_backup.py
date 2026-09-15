#!/usr/bin/env python3
"""Exporta a Excel los leads de WhatsApp Business desde un backup del iPhone.

Lee la base de datos ChatStorage.sqlite que el iPhone guarda en el backup
local (Finder / Dispositivos Apple / iTunes) y genera un Excel con todas las
conversaciones y, en una hoja aparte, las que quedaron sin contestar.

Uso tipico:
    python3 desde_backup.py --backup "/ruta/al/backup" --salida leads.xlsx

Ver README.md para el paso a paso completo.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from comun import (  # noqa: E402
    TZ_CHILE,
    Conversacion,
    Mensaje,
    es_grupo,
    escribir_excel,
    limpiar,
    normalizar_telefono,
    telefono_desde_jid,
)

EPOCA_APPLE = datetime(2001, 1, 1, tzinfo=timezone.utc)

TIPOS = {
    0: "texto",
    1: "imagen",
    2: "video",
    3: "audio",
    4: "contacto",
    5: "ubicacion",
    6: "sistema",
    7: "enlace",
    8: "documento",
    10: "llamada",
    11: "gif",
    14: "mensaje eliminado",
    15: "sticker",
}


def fecha_apple(valor) -> datetime | None:
    if valor is None:
        return None
    try:
        return (EPOCA_APPLE + timedelta(seconds=float(valor))).astimezone(TZ_CHILE)
    except (TypeError, ValueError, OverflowError):
        return None


# --------------------------------------------------------------------------
# Localizacion de la base de datos dentro del backup del iPhone
# --------------------------------------------------------------------------

def buscar_en_backup(carpeta: Path) -> list[dict]:
    """Devuelve los ChatStorage.sqlite presentes en el backup, con su dominio."""
    manifest = carpeta / "Manifest.db"
    if not manifest.exists():
        raise SystemExit(
            f"No encontre Manifest.db en {carpeta}.\n"
            "Asegurate de apuntar a la carpeta del backup (la que tiene "
            "Manifest.db, Info.plist y subcarpetas de 2 caracteres)."
        )
    try:
        con = sqlite3.connect(f"file:{manifest}?mode=ro", uri=True)
        filas = con.execute(
            "SELECT fileID, domain, relativePath FROM Files "
            "WHERE relativePath LIKE '%ChatStorage.sqlite%' ORDER BY domain"
        ).fetchall()
        con.close()
    except sqlite3.DatabaseError:
        raise SystemExit(
            "Manifest.db no se pudo leer: el backup esta CIFRADO.\n"
            "Solucion: en Finder / Dispositivos Apple desmarca 'Encriptar backup "
            "local', vuelve a respaldar el iPhone y repite. (El backup sin cifrar "
            "igual incluye los chats de WhatsApp.)"
        )
    return [
        {"fileID": f, "domain": d, "relativePath": r}
        for f, d, r in filas
        if r.endswith((".sqlite", ".sqlite-wal", ".sqlite-shm"))
    ]


def extraer_db(carpeta: Path, entradas: list[dict], destino: Path, dominio: str | None) -> Path:
    """Copia ChatStorage.sqlite (+ -wal/-shm) del backup a una carpeta de trabajo."""
    principales = [e for e in entradas if e["relativePath"].endswith("ChatStorage.sqlite")]
    if dominio:
        principales = [e for e in principales if dominio.lower() in e["domain"].lower()]
    if not principales:
        raise SystemExit("No hay ChatStorage.sqlite en este backup con ese filtro de dominio.")
    if len(principales) > 1:
        # Prioriza WhatsApp Business (SMB) por sobre WhatsApp personal.
        negocio = [e for e in principales if "smb" in e["domain"].lower() or "business" in e["domain"].lower()]
        if negocio:
            print("Se encontraron varias bases; uso la de WhatsApp Business.")
            principales = negocio
        else:
            print("Se encontraron varias bases de WhatsApp:")
            for e in principales:
                print(f"  - {e['domain']}")
            print("Uso la primera. Usa --dominio para elegir otra.")
    elegida = principales[0]
    print(f"Base de datos: {elegida['domain']}")

    destino.mkdir(parents=True, exist_ok=True)
    salida = destino / "ChatStorage.sqlite"
    for sufijo in ("", "-wal", "-shm"):
        ruta_rel = elegida["relativePath"] + sufijo
        coincide = [
            e for e in entradas
            if e["relativePath"] == ruta_rel and e["domain"] == elegida["domain"]
        ]
        if not coincide:
            continue
        fid = coincide[0]["fileID"]
        origen = carpeta / fid[:2] / fid
        if not origen.exists():
            origen = carpeta / fid  # backups antiguos, sin subcarpetas
        if origen.exists():
            shutil.copy2(origen, str(salida) + sufijo)
    if not salida.exists():
        raise SystemExit("No pude copiar ChatStorage.sqlite desde el backup.")
    return salida


# --------------------------------------------------------------------------
# Lectura de ChatStorage.sqlite
# --------------------------------------------------------------------------

def columnas(con: sqlite3.Connection, tabla: str) -> set[str]:
    try:
        return {fila[1] for fila in con.execute(f"PRAGMA table_info({tabla})")}
    except sqlite3.DatabaseError:
        return set()


def tablas(con: sqlite3.Connection) -> set[str]:
    return {
        fila[0]
        for fila in con.execute("SELECT name FROM sqlite_master WHERE type IN ('table','view')")
    }


def leer_etiquetas(con: sqlite3.Connection) -> dict[int, list[str]]:
    """Etiquetas de WhatsApp Business por chat (Nuevo cliente, Pago pendiente...).

    El esquema cambia entre versiones, asi que se descubre en tiempo de
    ejecucion: se busca una tabla de etiquetas con nombre y una tabla puente
    que referencie a ZWACHATSESSION.
    """
    presentes = tablas(con)
    tabla_label = next(
        (t for t in presentes if "LABEL" in t.upper() and columnas(con, t) & {"ZLABELNAME", "ZNAME", "ZTITLE"}),
        None,
    )
    if not tabla_label:
        return {}
    col_nombre = next(c for c in ("ZLABELNAME", "ZNAME", "ZTITLE") if c in columnas(con, tabla_label))
    nombres = {
        pk: limpiar(nombre)
        for pk, nombre in con.execute(f"SELECT Z_PK, {col_nombre} FROM {tabla_label}")
    }

    resultado: dict[int, list[str]] = {}
    for tabla in presentes:
        if tabla == tabla_label:
            continue
        cols = columnas(con, tabla)
        col_chat = next((c for c in cols if "CHATSESSION" in c.upper()), None)
        col_label = next((c for c in cols if "LABEL" in c.upper() and c != col_chat), None)
        if not (col_chat and col_label and "LABEL" in tabla.upper()):
            continue
        try:
            filas = con.execute(f"SELECT {col_chat}, {col_label} FROM {tabla}").fetchall()
        except sqlite3.DatabaseError:
            continue
        for chat_pk, label_pk in filas:
            nombre = nombres.get(label_pk)
            if chat_pk and nombre:
                resultado.setdefault(chat_pk, []).append(nombre)
    return resultado


def leer_conversaciones(
    db: Path,
    incluir_grupos: bool = False,
    desde: datetime | None = None,
    incluir_archivados: bool = True,
) -> list[Conversacion]:
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    con.text_factory = lambda b: b.decode("utf-8", "replace")

    if "ZWACHATSESSION" not in tablas(con):
        raise SystemExit(
            "El archivo no parece un ChatStorage.sqlite de WhatsApp "
            "(falta la tabla ZWACHATSESSION)."
        )

    cols_sesion = columnas(con, "ZWACHATSESSION")
    campos = ["Z_PK", "ZCONTACTJID", "ZPARTNERNAME"]
    opcionales = ["ZUNREADCOUNT", "ZARCHIVED", "ZSESSIONTYPE", "ZLASTMESSAGEDATE"]
    campos += [c for c in opcionales if c in cols_sesion]
    filas = con.execute(f"SELECT {', '.join(campos)} FROM ZWACHATSESSION").fetchall()
    sesiones = [dict(zip(campos, f)) for f in filas]

    etiquetas = leer_etiquetas(con)

    cols_msg = columnas(con, "ZWAMESSAGE")
    campos_msg = ["ZCHATSESSION", "ZISFROMME", "ZMESSAGEDATE", "ZTEXT", "ZMESSAGETYPE"]
    campos_msg = [c for c in campos_msg if c in cols_msg]
    if "ZPUSHNAME" in cols_msg:
        campos_msg.append("ZPUSHNAME")

    condicion, parametros = "", []
    if desde is not None and "ZMESSAGEDATE" in cols_msg:
        condicion = " WHERE ZMESSAGEDATE >= ?"
        parametros = [(desde - EPOCA_APPLE).total_seconds()]

    mensajes: dict[int, list[Mensaje]] = {}
    consulta = f"SELECT {', '.join(campos_msg)} FROM ZWAMESSAGE{condicion}"
    for fila in con.execute(consulta, parametros):
        datos = dict(zip(campos_msg, fila))
        chat_pk = datos.get("ZCHATSESSION")
        if chat_pk is None:
            continue
        tipo_num = datos.get("ZMESSAGETYPE")
        tipo = TIPOS.get(tipo_num, f"tipo {tipo_num}")
        if tipo == "sistema":  # avisos de WhatsApp, no son del lead
            continue
        texto = limpiar(datos.get("ZTEXT"))
        if not texto and tipo != "texto":
            texto = f"[{tipo}]"
        mensajes.setdefault(chat_pk, []).append(
            Mensaje(
                fecha=fecha_apple(datos.get("ZMESSAGEDATE")),
                de_mi=bool(datos.get("ZISFROMME")),
                autor=limpiar(datos.get("ZPUSHNAME")),
                texto=texto,
                tipo=tipo,
            )
        )
    con.close()

    conversaciones: list[Conversacion] = []
    for sesion in sesiones:
        jid = sesion.get("ZCONTACTJID") or ""
        if not incluir_grupos and es_grupo(jid):
            continue
        archivado = bool(sesion.get("ZARCHIVED"))
        if not incluir_archivados and archivado:
            continue
        propios = mensajes.get(sesion["Z_PK"], [])
        if not propios:
            continue
        telefono = telefono_desde_jid(jid)
        conversaciones.append(
            Conversacion(
                jid=jid,
                telefono=telefono,
                nombre=limpiar(sesion.get("ZPARTNERNAME")) or telefono,
                etiquetas=sorted(set(etiquetas.get(sesion["Z_PK"], []))),
                no_leidos=int(sesion.get("ZUNREADCOUNT") or 0),
                archivado=archivado,
                mensajes=propios,
            )
        )
    return conversaciones


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Exporta a Excel los leads sin contestar de WhatsApp Business (backup de iPhone)."
    )
    origen = parser.add_mutually_exclusive_group(required=True)
    origen.add_argument("--backup", help="Carpeta del backup del iPhone (la que contiene Manifest.db)")
    origen.add_argument("--db", help="Ruta directa a un ChatStorage.sqlite ya extraido")
    parser.add_argument("--salida", default="leads_whatsapp_hns.xlsx", help="Archivo Excel de salida")
    parser.add_argument("--dominio", help="Filtra el dominio del backup (ej: WhatsAppSMB)")
    parser.add_argument("--dias", type=int, help="Considerar solo mensajes de los ultimos N dias")
    parser.add_argument("--incluir-grupos", action="store_true", help="Incluir chats grupales")
    parser.add_argument("--sin-archivados", action="store_true", help="Excluir chats archivados")
    parser.add_argument("--transcripciones", help="Carpeta donde guardar un .txt por lead sin contestar")
    parser.add_argument("--trabajo", default="_extraido", help="Carpeta temporal para la base extraida")
    parser.add_argument("--solo-listar", action="store_true", help="Solo lista las bases del backup y termina")
    args = parser.parse_args()

    if args.backup:
        carpeta = Path(args.backup).expanduser()
        entradas = buscar_en_backup(carpeta)
        if args.solo_listar:
            for e in entradas:
                print(f"{e['domain']}  ->  {e['relativePath']}")
            return
        db = extraer_db(carpeta, entradas, Path(args.trabajo).expanduser(), args.dominio)
    else:
        db = Path(args.db).expanduser()
        if not db.exists():
            raise SystemExit(f"No existe el archivo {db}")

    desde = datetime.now(TZ_CHILE) - timedelta(days=args.dias) if args.dias else None
    conversaciones = leer_conversaciones(
        db,
        incluir_grupos=args.incluir_grupos,
        desde=desde,
        incluir_archivados=not args.sin_archivados,
    )
    if not conversaciones:
        raise SystemExit("No se encontraron conversaciones con los filtros indicados.")

    destino = escribir_excel(
        Path(args.salida),
        conversaciones,
        Path(args.transcripciones) if args.transcripciones else None,
    )
    pendientes = [c for c in conversaciones if c.sin_contestar]
    print(f"Conversaciones leidas: {len(conversaciones)}")
    print(f"Leads sin contestar:   {len(pendientes)}")
    print(f"Excel generado en:     {destino.resolve()}")


if __name__ == "__main__":
    main()
