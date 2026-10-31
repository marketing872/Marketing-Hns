"""
Paso único de autorización con Polar AccessLink.

1. Abre el navegador para que inicies sesión en Polar Flow y autorices la app.
2. Recibe el código en http://localhost:5000/oauth2_callback
3. Lo cambia por un access token y registra tu usuario en AccessLink.
4. Guarda todo en ~/.polar_mcp/credenciales.json (solo en tu computador).

Uso:
    python3 polar_auth.py
"""
import json
import os
import sys
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlencode, urlparse

import requests

CONFIG_DIR = Path.home() / ".polar_mcp"
CONFIG_FILE = CONFIG_DIR / "credenciales.json"

AUTH_URL = "https://flow.polar.com/oauth2/authorization"
TOKEN_URL = "https://polarremote.com/v2/oauth2/token"
API = "https://www.polaraccesslink.com/v3"
REDIRECT_URI = "http://localhost:5000/oauth2_callback"

_code_holder = {}


class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "code" in query:
            _code_holder["code"] = query["code"][0]
            msg = "Listo. Ya puedes cerrar esta ventana y volver a la terminal."
        else:
            _code_holder["error"] = query.get("error", ["desconocido"])[0]
            msg = f"Error de autorizacion: {_code_holder['error']}"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"<h2>{msg}</h2>".encode("utf-8"))

    def log_message(self, *args):
        pass


def main():
    client_id = os.environ.get("POLAR_CLIENT_ID") or input("Client ID: ").strip()
    client_secret = os.environ.get("POLAR_CLIENT_SECRET") or input("Client Secret: ").strip()

    server = HTTPServer(("localhost", 5000), CallbackHandler)
    threading.Thread(target=server.handle_request, daemon=True).start()

    url = AUTH_URL + "?" + urlencode(
        {"response_type": "code", "client_id": client_id, "redirect_uri": REDIRECT_URI}
    )
    print("\nAbriendo el navegador para autorizar en Polar Flow...")
    print("Si no se abre, copia esta URL en tu navegador:\n", url, "\n")
    webbrowser.open(url)

    while "code" not in _code_holder and "error" not in _code_holder:
        threading.Event().wait(0.5)
    server.server_close()

    if "error" in _code_holder:
        sys.exit(f"Autorización cancelada o fallida: {_code_holder['error']}")

    # Cambiar el código por el token
    r = requests.post(
        TOKEN_URL,
        auth=(client_id, client_secret),
        headers={"Accept": "application/json;charset=UTF-8"},
        data={
            "grant_type": "authorization_code",
            "code": _code_holder["code"],
            "redirect_uri": REDIRECT_URI,
        },
        timeout=30,
    )
    r.raise_for_status()
    token = r.json()
    access_token = token["access_token"]
    user_id = token["x_user_id"]

    # Registrar el usuario en AccessLink (409 = ya estaba registrado, está OK)
    reg = requests.post(
        f"{API}/users",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        json={"member-id": f"hns-{user_id}"},
        timeout=30,
    )
    if reg.status_code not in (200, 409):
        sys.exit(f"No se pudo registrar el usuario: {reg.status_code} {reg.text}")

    CONFIG_DIR.mkdir(exist_ok=True)
    CONFIG_FILE.write_text(
        json.dumps(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "access_token": access_token,
                "user_id": user_id,
            },
            indent=2,
        )
    )
    os.chmod(CONFIG_FILE, 0o600)
    print(f"✅ Conectado. Usuario Polar {user_id}. Credenciales guardadas en {CONFIG_FILE}")


if __name__ == "__main__":
    main()
