# Conector Polar Loop → Claude (MCP)

1. Crea la app en https://admin.polaraccesslink.com con Redirect URL `http://localhost:5000/oauth2_callback`.
2. `pip install -r requirements.txt`
3. `python3 polar_auth.py` (pide Client ID y Secret, abre el navegador para autorizar).
4. Agrega a `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "polar": {
      "command": "python3",
      "args": ["/RUTA/COMPLETA/polar-mcp/polar_mcp_server.py"]
    }
  }
}
```

5. Reinicia Claude Desktop.

Herramientas: `perfil`, `sueno`, `recuperacion_nocturna`, `actividad_diaria`,
`frecuencia_cardiaca`, `entrenamientos`, `detalle_entrenamiento`.

Las credenciales quedan solo en `~/.polar_mcp/credenciales.json` de tu computador.
