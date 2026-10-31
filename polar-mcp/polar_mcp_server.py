"""
Conector MCP de Polar AccessLink para Claude Desktop.

Expone tus datos de la Polar Loop (sueño, recuperación, actividad diaria,
entrenamientos y frecuencia cardíaca continua) como herramientas para Claude.

Requiere haber corrido antes: python3 polar_auth.py
"""
import json
from pathlib import Path

import requests
from mcp.server.fastmcp import FastMCP

CONFIG_FILE = Path.home() / ".polar_mcp" / "credenciales.json"
API = "https://www.polaraccesslink.com/v3"

mcp = FastMCP("polar")


def _cred():
    if not CONFIG_FILE.exists():
        raise RuntimeError("No hay credenciales. Corre primero: python3 polar_auth.py")
    return json.loads(CONFIG_FILE.read_text())


def _get(path, params=None):
    c = _cred()
    r = requests.get(
        f"{API}{path}",
        headers={"Authorization": f"Bearer {c['access_token']}", "Accept": "application/json"},
        params=params,
        timeout=30,
    )
    if r.status_code == 204:
        return {"mensaje": "Sin datos para ese período."}
    if r.status_code == 404:
        return {"mensaje": "No hay datos (o el endpoint no está disponible para tu dispositivo)."}
    if r.status_code == 401:
        return {"error": "Token inválido o revocado. Vuelve a correr polar_auth.py"}
    r.raise_for_status()
    return r.json()


@mcp.tool()
def perfil() -> dict:
    """Datos básicos del usuario Polar (nombre, peso, altura, fecha de nacimiento)."""
    return _get(f"/users/{_cred()['user_id']}")


@mcp.tool()
def sueno(fecha: str = "") -> dict:
    """Sueño. Sin fecha: últimos 28 días. Con fecha (AAAA-MM-DD): detalle de esa noche."""
    return _get(f"/users/sleep/{fecha}" if fecha else "/users/sleep")


@mcp.tool()
def recuperacion_nocturna(fecha: str = "") -> dict:
    """Nightly Recharge (recuperación, HRV, estado del sistema nervioso).
    Sin fecha: últimos 28 días. Con fecha (AAAA-MM-DD): ese día."""
    return _get(f"/users/nightly-recharge/{fecha}" if fecha else "/users/nightly-recharge")


@mcp.tool()
def actividad_diaria(desde: str = "", hasta: str = "") -> dict:
    """Actividad diaria (pasos, calorías, tiempo activo). Fechas AAAA-MM-DD opcionales."""
    params = {k: v for k, v in {"from": desde, "to": hasta}.items() if v}
    return _get("/users/activities", params or None)


@mcp.tool()
def frecuencia_cardiaca(fecha: str) -> dict:
    """Frecuencia cardíaca continua de un día (AAAA-MM-DD)."""
    return _get(f"/users/continuous-heart-rate/{fecha}")


@mcp.tool()
def entrenamientos() -> list | dict:
    """Lista de entrenamientos de los últimos 30 días."""
    return _get("/exercises")


@mcp.tool()
def detalle_entrenamiento(id_entrenamiento: str, con_muestras: bool = False) -> dict:
    """Detalle de un entrenamiento. con_muestras=True incluye pulso segundo a segundo."""
    params = {"zones": "true"}
    if con_muestras:
        params["samples"] = "true"
    return _get(f"/exercises/{id_entrenamiento}", params)


if __name__ == "__main__":
    mcp.run()
