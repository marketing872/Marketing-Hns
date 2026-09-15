"""Utilidades compartidas para exportar leads de WhatsApp Business a Excel.

Define el modelo de datos (Conversacion / Mensaje), la normalizacion de
telefonos chilenos y la escritura del archivo Excel final.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:  # zoneinfo necesita el paquete tzdata en algunos sistemas (Windows)
    from zoneinfo import ZoneInfo

    TZ_CHILE = ZoneInfo("America/Santiago")
except Exception:  # pragma: no cover - fallback sin base de datos de zonas
    TZ_CHILE = timezone(timedelta(hours=-3))

# Limite duro de caracteres por celda que impone Excel.
MAX_CELDA = 32767
# Margen de seguridad para la columna de transcripcion.
MAX_TRANSCRIPCION = 30000

_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_INVISIBLES = re.compile(r"[‎‏‪-‮﻿]")


def limpiar(texto: str | None) -> str:
    """Quita marcas invisibles y caracteres de control que Excel rechaza."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFC", str(texto))
    texto = _INVISIBLES.sub("", texto)
    return _CONTROL.sub("", texto).strip()


def normalizar_telefono(crudo: str | None, pais: str = "56") -> str:
    """Devuelve el numero en formato E.164 (+56912345678) o "" si no aplica."""
    if not crudo:
        return ""
    digitos = re.sub(r"\D", "", str(crudo))
    if not digitos:
        return ""
    # Numeros muy largos suelen ser IDs de grupo o de lista de difusion.
    if len(digitos) > 15:
        return ""
    if digitos.startswith("00"):
        digitos = digitos[2:]
    if len(digitos) == 9 and digitos.startswith("9"):  # movil chileno sin pais
        digitos = pais + digitos
    elif len(digitos) == 8:  # fijo de Santiago sin pais ni codigo de area
        digitos = pais + "2" + digitos
    if len(digitos) < 8:
        return ""
    return "+" + digitos


def telefono_desde_jid(jid: str | None) -> str:
    """Extrae el telefono de un JID tipo 56912345678@s.whatsapp.net."""
    if not jid:
        return ""
    usuario = str(jid).split("@", 1)[0]
    usuario = usuario.split(":", 1)[0]  # descarta sufijo de dispositivo
    if "-" in usuario:  # JID de grupo: creador-timestamp
        return ""
    return normalizar_telefono(usuario)


def es_grupo(jid: str | None) -> bool:
    j = (jid or "").lower()
    return j.endswith("@g.us") or j.endswith("@broadcast") or "status@" in j


def link_wame(telefono: str) -> str:
    return f"https://wa.me/{telefono.lstrip('+')}" if telefono else ""


@dataclass
class Mensaje:
    fecha: datetime | None
    de_mi: bool
    autor: str = ""
    texto: str = ""
    tipo: str = "texto"

    def linea(self) -> str:
        sello = self.fecha.strftime("%d-%m-%Y %H:%M") if self.fecha else "sin fecha"
        quien = "HNS" if self.de_mi else (self.autor or "Lead")
        cuerpo = self.texto or f"[{self.tipo}]"
        return f"[{sello}] {quien}: {cuerpo}"


@dataclass
class Conversacion:
    jid: str = ""
    telefono: str = ""
    nombre: str = ""
    etiquetas: list[str] = field(default_factory=list)
    no_leidos: int = 0
    archivado: bool = False
    mensajes: list[Mensaje] = field(default_factory=list)

    # --- metricas derivadas -------------------------------------------------
    @property
    def ordenados(self) -> list[Mensaje]:
        return sorted(self.mensajes, key=lambda m: (m.fecha or datetime.min.replace(tzinfo=TZ_CHILE)))

    @property
    def recibidos(self) -> int:
        return sum(1 for m in self.mensajes if not m.de_mi)

    @property
    def enviados(self) -> int:
        return sum(1 for m in self.mensajes if m.de_mi)

    @property
    def ultimo(self) -> Mensaje | None:
        ordenados = self.ordenados
        return ordenados[-1] if ordenados else None

    @property
    def primer_mensaje_lead(self) -> Mensaje | None:
        for m in self.ordenados:
            if not m.de_mi:
                return m
        return None

    @property
    def ultimo_mensaje_lead(self) -> Mensaje | None:
        for m in reversed(self.ordenados):
            if not m.de_mi:
                return m
        return None

    @property
    def fecha_ultimo(self) -> datetime | None:
        ultimo = self.ultimo
        return ultimo.fecha if ultimo else None

    @property
    def estado(self) -> str:
        """Clasifica la conversacion desde el punto de vista comercial."""
        if self.recibidos == 0:
            return "Sin mensajes del lead"
        if self.enviados == 0:
            return "Nunca contestado"
        ultimo = self.ultimo
        if ultimo is not None and not ultimo.de_mi:
            return "Esperando respuesta"
        return "Contestado"

    @property
    def sin_contestar(self) -> bool:
        return self.estado in ("Nunca contestado", "Esperando respuesta")

    def dias_de_espera(self, ahora: datetime | None = None) -> float | str:
        """Dias transcurridos desde el ultimo mensaje del lead sin responder."""
        if not self.sin_contestar:
            return ""
        referencia = self.ultimo_mensaje_lead
        if referencia is None or referencia.fecha is None:
            return ""
        ahora = ahora or datetime.now(TZ_CHILE)
        fecha = referencia.fecha
        if fecha.tzinfo is None:
            fecha = fecha.replace(tzinfo=TZ_CHILE)
        return round((ahora - fecha).total_seconds() / 86400, 1)

    def transcripcion(self, limite: int = MAX_TRANSCRIPCION) -> str:
        texto = "\n".join(m.linea() for m in self.ordenados)
        if len(texto) > limite:
            # Conserva el final: es lo mas util para retomar la conversacion.
            texto = "[...transcripcion recortada, ver archivo .txt adjunto...]\n" + texto[-limite:]
        return texto


COLUMNAS = [
    ("Telefono", 17),
    ("Telefono sin +", 16),
    ("Nombre / Contacto", 26),
    ("Estado", 20),
    ("Dias sin responder", 11),
    ("Ultimo mensaje", 18),
    ("Quien escribio ultimo", 12),
    ("Mensajes del lead", 10),
    ("Mensajes nuestros", 10),
    ("No leidos", 9),
    ("Etiquetas", 20),
    ("Archivado", 10),
    ("Primer mensaje del lead", 45),
    ("Ultimo mensaje del lead", 45),
    ("Abrir chat", 30),
    ("Conversacion completa", 70),
]


def _fila(conv: Conversacion, ahora: datetime) -> list:
    ultimo = conv.ultimo
    primero_lead = conv.primer_mensaje_lead
    ultimo_lead = conv.ultimo_mensaje_lead
    fecha = conv.fecha_ultimo
    return [
        conv.telefono,
        conv.telefono.lstrip("+"),
        limpiar(conv.nombre),
        conv.estado,
        conv.dias_de_espera(ahora),
        fecha.replace(tzinfo=None) if fecha else "",
        ("HNS" if ultimo.de_mi else "Lead") if ultimo else "",
        conv.recibidos,
        conv.enviados,
        conv.no_leidos,
        ", ".join(conv.etiquetas),
        "Si" if conv.archivado else "No",
        limpiar(primero_lead.texto)[:500] if primero_lead else "",
        limpiar(ultimo_lead.texto)[:500] if ultimo_lead else "",
        link_wame(conv.telefono),
        conv.transcripcion(),
    ]


def escribir_excel(
    destino: Path,
    conversaciones: list[Conversacion],
    carpeta_transcripciones: Path | None = None,
) -> Path:
    """Genera el Excel con las hojas Resumen, Sin contestar y Todas."""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    ahora = datetime.now(TZ_CHILE)
    conversaciones = sorted(
        conversaciones,
        key=lambda c: c.fecha_ultimo or datetime.min.replace(tzinfo=TZ_CHILE),
        reverse=True,
    )
    pendientes = [c for c in conversaciones if c.sin_contestar]

    libro = Workbook()
    resumen = libro.active
    resumen.title = "Resumen"

    encabezado_fill = PatternFill("solid", fgColor="1F6F4A")
    encabezado_font = Font(bold=True, color="FFFFFF")

    def hoja_datos(nombre: str, datos: list[Conversacion]):
        hoja = libro.create_sheet(nombre)
        hoja.append([c[0] for c in COLUMNAS])
        for celda in hoja[1]:
            celda.fill = encabezado_fill
            celda.font = encabezado_font
            celda.alignment = Alignment(vertical="center", wrap_text=True)
        for conv in datos:
            hoja.append(_fila(conv, ahora))
        for indice, (_, ancho) in enumerate(COLUMNAS, start=1):
            hoja.column_dimensions[get_column_letter(indice)].width = ancho
        for fila in hoja.iter_rows(min_row=2, min_col=6, max_col=6):
            for celda in fila:
                celda.number_format = "DD-MM-YYYY HH:MM"
        hoja.freeze_panes = "A2"
        if hoja.max_row >= 1:
            hoja.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNAS))}{max(hoja.max_row, 1)}"
        return hoja

    hoja_datos("Leads sin contestar", pendientes)
    hoja_datos("Todas las conversaciones", conversaciones)

    nunca = sum(1 for c in conversaciones if c.estado == "Nunca contestado")
    esperando = sum(1 for c in conversaciones if c.estado == "Esperando respuesta")
    con_telefono = sum(1 for c in pendientes if c.telefono)
    resumen.append(["Exportacion de leads de WhatsApp Business - HNS"])
    resumen["A1"].font = Font(bold=True, size=14)
    resumen.append([])
    filas_resumen = [
        ("Fecha de exportacion", ahora.strftime("%d-%m-%Y %H:%M")),
        ("Conversaciones analizadas", len(conversaciones)),
        ("Leads sin contestar", len(pendientes)),
        ("  - Nunca contestados", nunca),
        ("  - Esperando respuesta (ya se habia contestado antes)", esperando),
        ("Sin contestar con telefono utilizable", con_telefono),
        ("Sin contestar sin telefono (contacto guardado sin numero)", len(pendientes) - con_telefono),
    ]
    for etiqueta, valor in filas_resumen:
        resumen.append([etiqueta, valor])
    resumen.append([])
    resumen.append(["Hoja 'Leads sin contestar': lo que el ejecutivo debe trabajar."])
    resumen.append(["Hoja 'Todas las conversaciones': respaldo completo del periodo exportado."])
    resumen.column_dimensions["A"].width = 55
    resumen.column_dimensions["B"].width = 24

    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    libro.save(destino)

    if carpeta_transcripciones:
        carpeta = Path(carpeta_transcripciones)
        carpeta.mkdir(parents=True, exist_ok=True)
        for conv in pendientes:
            base = conv.telefono.lstrip("+") or re.sub(r"\W+", "_", conv.nombre) or "sin_identificar"
            (carpeta / f"{base}.txt").write_text(
                f"{conv.nombre} ({conv.telefono})\n{'-' * 60}\n"
                + "\n".join(m.linea() for m in conv.ordenados),
                encoding="utf-8",
            )
    return destino
