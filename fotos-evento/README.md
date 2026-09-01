# Tu Foto Nutrend — buscador de fotografías de evento

Aplicación de una sola página para que los corredores encuentren y descarguen
gratis sus fotos del evento. El acceso queda detrás del registro con el correo
de suscripción de Nutrend.cl.

Artifact publicado: https://claude.ai/code/artifact/b9f5bd45-4f69-4919-b173-d6324df87947

## Qué hace

- Búsqueda por número de dorsal, en un campo con forma de placa de bicicleta.
  Coincidencia exacta primero, luego parcial.
- Búsqueda por nombre del corredor, sin distinguir tildes ni mayúsculas.
- Filtros por tramo del recorrido y por categoría.
- Filtro **solo fotos sin dorsal legible**, para las tomas donde el número
  salió tapado o movido. En un evento de 700 fotos suelen ser entre 30 y 60.
- Selección múltiple: copiar todos los enlaces, compartirlos por WhatsApp o
  descargar la lista en un archivo de texto.
- Carga por tandas de 48 fotos, de modo que 700 fichas no traban el teléfono.
- Recuerda el acceso en el navegador del corredor: se registra una sola vez.

## Cómo cargar el evento real

Todo lo editable está en el bloque `CONFIG`, al comienzo del `<script>`:

```js
const CONFIG = {
  evento: {
    nombre: "Gran Fondo Nutrend 2026",
    lugar: "Buin, Región Metropolitana",
    fecha: "Domingo 24 de agosto de 2026",
    fotografo: "Equipo HNS Nutrition"
  },
  carpetaDrive: "https://drive.google.com/drive/folders/REEMPLAZAR_ID_CARPETA",
  urlSuscripcion: "https://nutrend.cl/suscribete",
  urlWeb: "https://nutrend.cl",
  modoDemo: true,
  porTanda: 48
};
```

Pasos:

1. Sube las 700 fotos a una carpeta de Google Drive y compártela como
   **cualquier persona con el enlace puede ver**. Sin ese permiso, los
   corredores reciben una pantalla de solicitud de acceso.
2. Etiqueta los dorsales en `planilla-ejemplo.csv` (misma estructura, una fila
   por foto). Varios dorsales en una misma foto van separados por `|`.
3. Genera el bloque de datos:

   ```bash
   python3 csv-a-datos.py planilla.csv > datos.js
   ```

4. Reemplaza en `tu-foto-nutrend.html` la línea `let FOTOS = [];` por el
   contenido de `datos.js`, y cambia `modoDemo: true` por `modoDemo: false`.
   El aviso amarillo de demostración desaparece solo.

## Límites de la plataforma que conviene conocer

- **Un Artifact no puede mostrar imágenes alojadas fuera de la página.** La
  política de seguridad del visor bloquea las peticiones a Drive, Dropbox o
  cualquier servidor. Por eso cada tarjeta muestra el código de archivo y los
  dorsales detectados, y enlaza a la foto en Drive. Si en el futuro quieres
  miniaturas visibles dentro de la app, hay dos caminos: incrustarlas en el
  propio archivo como `data:` URI —caben unas 700 miniaturas pequeñas dentro
  del límite de 16 MB de la página— o publicar la galería como sitio web real
  en un hosting propio.
- **La descarga la ejecuta Drive, no la aplicación.** El botón *Descargar*
  abre `https://drive.google.com/uc?export=download&id=...`, que entrega el
  archivo original en resolución completa.
- **La detección de dorsales con IA se procesa fuera de la página**, contra
  los archivos de fotos, y su resultado es la planilla del paso 2.

## Búsqueda por rostro (v2)

La sección está construida y visible, en estado *en preparación*. Para
activarla hay que calcular fuera de la aplicación un vector facial por rostro
detectado, guardarlo junto a cada foto y comparar en el navegador contra la
selfie que sube el corredor. Antes de encenderla conviene revisar el
tratamiento de datos biométricos bajo la Ley 21.719: son datos sensibles y
requieren consentimiento explícito e informado.
