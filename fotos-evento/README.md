# Tu Foto Nutrend — buscador de fotografías de evento

Aplicación de una sola página para que los corredores encuentren y descarguen
gratis sus fotos del evento. El acceso queda detrás del registro con el correo
de suscripción de Nutrend.cl.

**Evento cargado:** MTB Carlo de Gavardo · La Vacada — Huelquén, 30 de agosto de 2026
**Fotografía:** Ofront Audiovisual Studio
**Artifact publicado:** https://claude.ai/code/artifact/b9f5bd45-4f69-4919-b173-d6324df87947

## Estado

La aplicación ya trae las 83 fotografías que hay hoy en la carpeta de Drive del
fotógrafo, cada una con su enlace de descarga. Falta el etiquetado de dorsales:
mientras no exista, la página lo dice de frente, el campo de dorsal queda en
espera y se ocultan los filtros que todavía no tienen datos, en lugar de
devolver búsquedas vacías.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `tu-foto-nutrend.html` | La aplicación completa. Un solo archivo, sin dependencias. |
| `fotos-drive.json` | Índice de la carpeta de Drive: `[nombre de archivo, ID en Drive]`. Es lo que convierte cada foto en un enlace de descarga. |
| `detectar-dorsales.py` | Lee los dorsales de las fotos con Claude y escribe `planilla.csv`. |
| `csv-a-datos.py` | Convierte la planilla en el bloque de datos que consume la aplicación. |
| `planilla-ejemplo.csv` | La estructura de la planilla, por si prefieres etiquetar a mano. |

## Cargar los dorsales

El etiquetado corre en el computador donde estén las fotos: los originales pesan
entre 17 y 25 MB cada uno, así que se trabajan en local, no desde la nube.

1. Descarga la carpeta de Drive a tu computador (botón *Descargar* de Google
   Drive, o la aplicación Drive para escritorio).
2. Instala lo necesario y deja tu clave de API a mano:

   ```bash
   pip install anthropic pillow
   export ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. Prueba primero con unas pocas fotos, para ver la calidad de lectura y el costo:

   ```bash
   python3 detectar-dorsales.py /ruta/a/las/fotos --limite 10
   ```

4. Si el resultado convence, corre el resto. El avance se guarda a medida que
   avanza, así que puedes cortar y retomar sin repetir lo ya leído:

   ```bash
   python3 detectar-dorsales.py /ruta/a/las/fotos
   ```

5. Revisa a mano las filas marcadas en la columna `revisar`: son las fotos donde
   el número se distingue apenas. Aprovecha de rellenar `tramo`, `categoria` y
   `hora` si los tienes; la aplicación activa un filtro por cada columna que
   traiga datos.
6. Genera el bloque de datos y pégalo en la aplicación, reemplazando desde
   `const ARCHIVOS = [` hasta el cierre de `let FOTOS = ...;`:

   ```bash
   python3 csv-a-datos.py planilla.csv > datos.js
   ```

Al abrir la página con dorsales cargados, el buscador se activa solo: no hay
ningún interruptor que tocar.

### Cómo lee los dorsales

Cada foto pasa por dos etapas. Primero se reduce a 1568 px por el lado largo y
se lee entera. Si así no aparece ningún número, se recorta en cuatro cuadrantes
solapados y se lee cada uno: un dorsal de 40 px en una foto de 6000 px se pierde
al reducir la imagen completa, pero sobrevive en el recorte.

El modelo tiene instrucción explícita de no adivinar dígitos y de declarar su
nivel de certeza. Las lecturas dudosas quedan marcadas para revisión humana en
vez de colarse como buenas: un dorsal equivocado le manda a un corredor las
fotos de otro, que es peor que no encontrar nada.

Ajustables al comienzo de `detectar-dorsales.py`: `ESFUERZO` (`low` abarata,
`high` afina en fotos difíciles) y `MODELO`.

## Configurar otro evento

Todo lo editable está en el bloque `CONFIG`, al comienzo del `<script>`: nombre,
fecha y lugar del evento, fotógrafo, carpeta de Drive, página de suscripción y
sitio web. `modoDemo: true` llena la galería con fichas de ejemplo para probar
el buscador sin datos reales.

Sube las fotos a Drive compartidas como **cualquier persona con el enlace puede
ver**. Sin ese permiso, los corredores chocan con una pantalla de solicitud de
acceso en vez de con su foto.

## Límites de la plataforma que conviene conocer

- **Un Artifact no puede mostrar imágenes alojadas fuera de la página.** La
  política de seguridad del visor bloquea las peticiones a Drive, Dropbox o
  cualquier servidor. Por eso cada tarjeta muestra el código de archivo y los
  dorsales detectados, y enlaza a la foto. Si quieres miniaturas visibles dentro
  de la galería hay dos caminos: incrustarlas en el propio archivo como `data:`
  URI, que caben unas cuantas cientos dentro del límite de 16 MB de la página, o
  publicar la galería como sitio web real en un hosting propio.
- **La descarga la ejecuta Drive, no la aplicación.** El botón *Descargar* abre
  `https://drive.google.com/uc?export=download&id=...`, que entrega el archivo
  original en resolución completa.
- **El registro por correo es declarativo.** Un Artifact no puede consultar la
  base de suscriptores de Nutrend.cl, así que el correo no se verifica contra
  ella. Funciona como filtro y como incentivo, no como control estricto, y los
  correos quedan en el navegador del corredor: para capturarlos de verdad, la
  suscripción tiene que ocurrir en Nutrend.cl.

## Búsqueda por rostro (v2)

La sección está construida y visible, en estado *en preparación*. Para activarla
hay que calcular fuera de la aplicación un vector facial por rostro detectado,
guardarlo junto a cada foto y comparar en el navegador contra la selfie que sube
el corredor. Antes de encenderla conviene revisar el tratamiento de datos
biométricos bajo la Ley 21.719: son datos sensibles y requieren consentimiento
explícito e informado.
