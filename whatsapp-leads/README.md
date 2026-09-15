# Exportar leads sin contestar de WhatsApp Business → Excel

Herramienta interna de HNS para rescatar los leads que escribieron al WhatsApp
Business (iPhone 13) y **quedaron sin respuesta**, con su número de teléfono y
la conversación completa, para que el ejecutivo pueda retomar el contacto.

## Lo primero: qué se puede y qué no

WhatsApp **no tiene** una función de "exportar todos los chats" en iPhone. Solo
existen dos caminos reales, y esta carpeta automatiza los dos:

| | Ruta A — Backup del iPhone | Ruta B — Exportar chat uno por uno |
|---|---|---|
| Trae **todos** los chats de una vez | Sí | No, hay que exportar cada chat a mano |
| Trae el **número de teléfono** | Siempre | Solo si el contacto **no** está guardado en la agenda |
| Trae etiquetas de WhatsApp Business | Sí | No |
| Necesita computador + cable | Sí | No (se puede hacer desde el iPhone) |
| Esfuerzo | ~20 min una sola vez | ~1 min por chat |

**Recomendación: usar la Ruta A.** La Ruta B sirve solo si son pocos chats o si
no hay acceso al computador.

---

## Requisitos (una sola vez)

1. Un computador Mac o Windows y el cable del iPhone.
2. Python 3.9 o superior (`python3 --version`). En Windows se instala desde
   [python.org](https://www.python.org/downloads/) marcando "Add Python to PATH".
3. Instalar la librería que genera el Excel:

   ```bash
   pip install -r requirements.txt
   ```

4. Probar que todo quedó bien, generando un Excel de ejemplo con datos ficticios:

   ```bash
   python3 demo.py --salida ejemplo_leads.xlsx
   ```

---

## Ruta A — Desde el backup del iPhone (recomendada)

### Paso 1. Hacer un backup **sin cifrar** en el computador

> ⚠️ El backup **no puede estar encriptado**. Si lo está, el script no puede
> leerlo (así lo diseñó Apple). Si necesitas mantener la encriptación activada,
> salta al apartado "Alternativas con software pagado".

- **Mac (macOS Catalina o superior):** conecta el iPhone → abre **Finder** → haz
  clic en el iPhone en la barra lateral → pestaña **General** → elige
  *"Hacer copia de seguridad de todos los datos del iPhone en esta Mac"* →
  **desmarca "Encriptar copia de seguridad local"** → **Hacer copia ahora**.
- **Windows:** conecta el iPhone → abre **Dispositivos Apple** (o iTunes) →
  **Resumen / General** → *"Este computador"* → **desmarca "Encriptar copia
  local"** → **Hacer copia de seguridad ahora**.

Deja que termine (puede tardar 10–30 minutos la primera vez).

### Paso 2. Ubicar la carpeta del backup

- **Mac:** `~/Library/Application Support/MobileSync/Backup/`
- **Windows (app Dispositivos Apple / iTunes de Microsoft Store):**
  `C:\Users\TU_USUARIO\Apple\MobileSync\Backup\`
- **Windows (iTunes clásico):**
  `C:\Users\TU_USUARIO\AppData\Roaming\Apple Computer\MobileSync\Backup\`

Dentro hay una carpeta con nombre largo (el identificador del iPhone). Esa es la
que se le pasa al script: debe contener `Manifest.db` e `Info.plist`.

### Paso 3. Verificar que el backup trae WhatsApp Business

```bash
python3 desde_backup.py --backup "/ruta/a/la/carpeta/del/backup" --solo-listar
```

Debería aparecer una línea con `WhatsAppSMB` (WhatsApp Business). Si solo
aparece `net.whatsapp.WhatsApp`, ese es el WhatsApp personal: revisa que el
backup sea del iPhone correcto.

### Paso 4. Generar el Excel

```bash
python3 desde_backup.py \
  --backup "/ruta/a/la/carpeta/del/backup" \
  --salida "leads_sin_contestar_HNS.xlsx" \
  --transcripciones "conversaciones"
```

Opciones útiles:

| Opción | Para qué sirve |
|---|---|
| `--dias 90` | Considerar solo los últimos 90 días (recomendado para no arrastrar chats viejos) |
| `--sin-archivados` | Ignorar los chats archivados |
| `--incluir-grupos` | Incluir chats grupales (por defecto se excluyen, no son leads) |
| `--transcripciones CARPETA` | Además del Excel, guarda un `.txt` por cada lead sin contestar |
| `--dominio WhatsAppSMB` | Forzar la base de WhatsApp Business si el backup tiene las dos apps |
| `--db archivo.sqlite` | Usar un `ChatStorage.sqlite` ya extraído en vez de un backup |

---

## Ruta B — Exportando cada chat desde el iPhone

### Paso 1. Exportar los chats

En el iPhone, dentro de WhatsApp Business, por cada chat:
**abrir el chat → tocar el nombre arriba → bajar hasta "Exportar chat" →
"Sin archivos adjuntos"** → enviarlo por correo a `marketing@hnsnutrition.cl`
o guardarlo en Archivos / Drive.

> Truco: usa las **etiquetas** de WhatsApp Business (ej. "Sin responder") para
> filtrar primero qué chats exportar y no tener que revisarlos todos.

### Paso 2. Juntar los archivos

Descarga todos los `.txt` o `.zip` en una sola carpeta del computador, por
ejemplo `chats/`. No hace falta descomprimir los `.zip`.

### Paso 3. Generar el Excel

```bash
python3 desde_txt.py \
  --carpeta "chats" \
  --yo "HNS Nutrition" \
  --salida "leads_sin_contestar_HNS.xlsx" \
  --transcripciones "conversaciones"
```

- `--yo` es el nombre **tal como aparece la cuenta de HNS dentro del chat**.
  Si no se indica, el script intenta deducirlo solo (es el nombre que aparece en
  todos los chats).
- Los contactos **guardados en la agenda** salen sin número. Para recuperarlos,
  crea un CSV `nombre,telefono` y pásalo con `--mapa mapa.csv`.

---

## Qué contiene el Excel

**Hoja `Resumen`** — totales: cuántas conversaciones se leyeron, cuántas quedaron
sin contestar y cuántas tienen teléfono utilizable.

**Hoja `Leads sin contestar`** — lo que el ejecutivo tiene que trabajar.

**Hoja `Todas las conversaciones`** — respaldo completo del período exportado.

Columnas de ambas hojas de datos:

| Columna | Descripción |
|---|---|
| Teléfono | Formato internacional `+56912345678` |
| Teléfono sin + | Para importar a CRM o planillas que rechazan el `+` |
| Nombre / Contacto | Nombre guardado o el número si no está en la agenda |
| **Estado** | `Nunca contestado` · `Esperando respuesta` · `Contestado` · `Sin mensajes del lead` |
| Días sin responder | Días desde el último mensaje del lead que quedó sin respuesta |
| Último mensaje | Fecha y hora del último mensaje del chat |
| Quién escribió último | `Lead` o `HNS` |
| Mensajes del lead / nuestros | Volumen de la conversación |
| No leídos | Contador de no leídos de WhatsApp (solo Ruta A) |
| Etiquetas | Etiquetas de WhatsApp Business (solo Ruta A) |
| Primer / Último mensaje del lead | Para entender el contexto sin abrir la conversación |
| Abrir chat | Link `wa.me` — un clic y se abre la conversación |
| Conversación completa | Transcripción completa del chat |

### Criterio de "sin contestar"

- **Nunca contestado:** el lead escribió y nunca hubo respuesta desde HNS. *Máxima prioridad.*
- **Esperando respuesta:** hubo conversación, pero el último mensaje es del lead
  y quedó sin responder.

Ambos casos aparecen en la hoja `Leads sin contestar`, ordenados del más
reciente al más antiguo. Se pueden reordenar por "Días sin responder" con el
filtro que ya viene activado en la planilla.

---

## Alternativas con software pagado

Si no se puede desactivar la encriptación del backup o se prefiere no usar
línea de comandos:

- **iMazing** (Mac/Windows) — abre el backup incluso encriptado y exporta
  WhatsApp a Excel/CSV/PDF. Licencia paga.
- **Decipher WhatsApp Exporter** (Mac/Windows) — similar, exporta a PDF/CSV.

Si se usa una de estas, se puede exportar el `ChatStorage.sqlite` y procesarlo
igual con `python3 desde_backup.py --db ChatStorage.sqlite` para obtener este
mismo formato de Excel.

---

## Para que esto no vuelva a pasar

Esta exportación es un rescate puntual. Para que los leads dejen de perderse:

1. **Etiquetas de WhatsApp Business** — crear "Nuevo lead", "Cotización enviada",
   "Sin respuesta" y usarlas de forma obligatoria. Es gratis y es lo más rápido de implementar.
2. **Respuestas rápidas + mensaje de ausencia** — configurar en
   *Herramientas para la empresa* para que nadie quede sin al menos un acuse de recibo.
3. **WhatsApp Business API / plataforma multiagente** (Callbell, Wati, Chatwoot,
   360dialog) — permite varios ejecutivos en un mismo número, asignación de
   conversaciones, historial exportable y reportes de tiempo de respuesta.
   Es el paso lógico si el volumen de leads de HNS ya justifica tener un equipo
   comercial atendiendo el mismo WhatsApp.

---

## Privacidad

El Excel y las transcripciones contienen datos personales de clientes (números
de teléfono y conversaciones). Se aplican la Ley 19.628 sobre protección de la
vida privada y las políticas internas de HNS:

- Guardar el archivo solo en el Drive corporativo, no en computadores personales.
- Compartirlo únicamente con el equipo comercial que va a contactar a los leads.
- No subir el archivo a este repositorio ni a herramientas externas.

El archivo `.gitignore` de esta carpeta ya bloquea los `.xlsx`, los `.sqlite`
y las transcripciones para evitar subirlos por accidente.
