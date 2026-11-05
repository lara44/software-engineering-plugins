---
name: "document"
description: "Usar para generar el documento de arquitectura en Word (.docx) con el diseño vigente, en la sección 5 del proceso con ADD 3.0 o cuando el arquitecto lo pida: estructura, portada, control del documento automático, tabla de contenido y estilo de tablas estándar. El registro de las iteraciones de ADD lo genera record."
---

# Documento de arquitectura (Word)

Genera `Architecture-Document-v<versión>.docx`: **el diseño vigente** (contexto, requisitos, decisiones, vistas, ADR vigentes, validación y pendientes), a partir de los archivos del proceso. Esta skill no decide nada nuevo: solo toma lo aprobado o cerrado, y de las decisiones, solo las vigentes.

El registro de cómo se llegó al diseño (las iteraciones) es otro documento, `ADD-Design-Record-v<versión>.docx`, y lo genera la skill `record` con la misma versión. Cuando se piden "los documentos", el orquestador carga las dos.

Esta skill también define el estilo común (portada, títulos, tablas, fichas, tabla de contenido), que `record` reutiliza desde `scripts/doc_style.js`.

Cada respuesta empieza con el bloque de estado de las secciones, con el formato exacto de `start` ("Bloque de estado"), con la sección 5 en curso.

Si piden otro formato (PDF, Google Docs) o un documento distinto (un ADR suelto, un caso narrativo), esta skill no aplica.

## Contrato

- **Lee:** `drivers.md`, `iterations/` (solo iteraciones con `status: cerrada`, para las decisiones vigentes, y `kanban.md`), `adr/`, `diagrams/` y `diagrams/images/`, `development-view.md`, `validation.md`, `document/source/`.
- **Escribe:** `document/Architecture-Document-v<versión>.docx` y su PDF, `document/previous-versions/v<X>/` (solo para mover ahí las versiones anteriores), `document/source/document.json`, `cover.json`, `cover.png`, y la línea "Último documento generado" de `iterations/status.md`.
- **No toca nunca:** ningún otro archivo del proceso. Si algo falta o está mal en ellos, se dice; no se corrige aquí.
- **Devuelve al orquestador:** la versión y la ruta del Word.

## Generadores

En la carpeta `scripts/` de esta skill. Se ejecutan tal cual; no se leen, no se copian y no se reescriben:

```bash
node <carpeta-de-esta-skill>/scripts/make_cover.js document/source/cover.json document/source/cover.png
node <carpeta-de-esta-skill>/scripts/gen_doc.js document/source/document.json document/
```

```
document/
├── Architecture-Document-v<versión>.docx   ← un Word por versión, con su PDF
├── ADD-Design-Record-v<versión>.docx       ← lo genera record
└── source/
    ├── document.json                       ← contenido del documento de arquitectura
    ├── record.json                         ← lo escribe record
    ├── cover.json
    └── cover.png
```

- `make_cover.js`: portada como imagen a sangre completa. Requiere Playwright con Chromium. La misma portada la usa el registro de diseño ADD.
- `doc_style.js`: el estilo común (fuente, títulos, tablas, fichas, imágenes, portada, tabla de contenido en dos pasadas). Lo usan `gen_doc.js` y el generador de `record`; un cambio de estilo aquí cambia los dos documentos.
- `gen_doc.js`: todo el documento a partir de su JSON, con el estilo de `doc_style.js`: fuente Calibri de 11 pt con interlineado 1,15 (fijados en el estilo, para que Word y LibreOffice muestren lo mismo; donde no está Calibri, LibreOffice usa Carlito, que tiene sus mismas medidas), encabezados con espacio antes y después, párrafos justificados, tablas con encabezado negro y líneas grises finas, fichas de escenario y de ADR, tabla de contenido numerada en dos pasadas e imágenes con su tamaño real. Requieren la librería `docx`, LibreOffice (`soffice`) y poppler (`pdftotext`).
- Las imágenes se leen directamente de los PNG del proyecto (`diagrams/images/` y `iterations/.../diagrams/images/`), con rutas relativas al JSON. No se copian.
- El Word se nombra con la versión de la última fila de `control`. Las versiones anteriores no se borran ni se sobrescriben.

**No se modifican por proyecto.** Si el arquitecto pide un ajuste de estilo, se propone como cambio a los scripts del plugin.

## Herramientas (revisar al empezar)

Comprobar `node`, `docx`, Playwright, `soffice` y `pdftotext`. Si falta algo, pedir permiso para instalarlo en ese momento:
- Mac: `brew install --cask libreoffice` y `brew install poppler`;
- en la carpeta del proyecto: `npm install docx playwright && npx playwright install chromium`.

Antes de instalar, buscar si ya están: en Mac, LibreOffice suele estar en `/Applications/LibreOffice.app/Contents/MacOS/soffice` y poppler en `/opt/homebrew/bin`. Sin `soffice` o `pdftotext`, el documento se genera igual, pero la tabla de contenido sale sin números de página: avisarlo.

## Versión y control del documento

**Versión:** `<ronda>.<última iteración cerrada>`, tomada de `iterations/status.md` y de los encabezados de las iteraciones. Si `status.md` tiene "Número mayor de la ronda 1: M" (proyecto migrado con documentos anteriores), el número mayor es `M + ronda − 1`.
- Antes de cerrar la primera iteración de la ronda: `<ronda>.0` (por ejemplo, 1.0 con solo las secciones 1 y 2 y el paso 1).
- Si esa versión ya existe en `document/` y desde entonces hubo correcciones sin iteración nueva, se agrega un tercer número (1.5.1, 1.5.2).
- Si la versión ya existe y no cambió nada, decirlo y no generar.

**Control del documento:** es el mismo en los dos documentos (`record` lo copia de `document.json`). Se conservan todas las filas anteriores (de `document/source/document.json`, si existe) y se agrega una por versión nueva. El comentario no se le pide al arquitecto: sale de los archivos.
- Una iteración cerrada: "Iteración N: <objetivo>. ADR nuevos: <IDs>. Vistas: <las que cambiaron>."
- Varias iteraciones cerradas desde la última versión: una fila con todas.
- La primera versión de una ronda nueva: "Ronda R: <qué la abrió>."
- Una corrección: lo que se corrigió, tomado de "Cambios después de la aprobación" de `drivers.md` o de lo que pidió el arquitecto.
- "Cambiado por": los autores de `cover.json` ("Por"), salvo que el arquitecto diga otra cosa.

## Documento de arquitectura: de dónde sale cada parte

| Sección | Contenido | Fuente |
|---|---|---|
| Portada | Título, subtítulo, Para, Por | `cover.json` (se pide una vez al arquitecto o se toma de `inputs/`) |
| Control del Documento | Ver arriba | Automático |
| Introducción | Qué sistema, para quién, qué cubre, y una frase del método: "El diseño se elaboró con ADD 3.0 (Cervantes y Kazman, 2024) en R rondas y N iteraciones; el detalle está en el registro de diseño ADD v<versión>." | `drivers.md` y `iterations/` |
| 1. Contexto | 1.1 Situación actual, 1.2 Objetivo, 1.3 Vista de contexto C4 | `drivers.md` §1 y `diagrams/images/c4-context.png` |
| 2. Drivers | 2.1 Funcionalidades, 2.2 Restricciones, 2.3 Supuestos, 2.4 Atributos de calidad, 2.5 Preocupaciones arquitectónicas | `drivers.md` §2 (sin los elementos "Retirado") y las preocupaciones nuevas de las iteraciones |
| 3. Decisiones | 3.1 Estilo, 3.2 Patrones, Base de datos, Servicios cloud, Stack | Decisiones vigentes de las iteraciones cerradas (pasos 4 y 5) |
| 4. Definición | Contenedores, componentes, información, despliegue, desarrollo | `diagrams/` vigente y `development-view.md` |
| 5. ADRs | Solo los ADR en `Estado: aprobado` | `adr/` (los reemplazados no van; su historia está en el registro) |
| 6. Validación | Si existe | `validation.md` aprobado |
| 7. Pendientes del Diseño | Drivers que no están completamente abordados, con su estado y qué falta | `kanban.md` de la última ronda |

**Decisión vigente:** una decisión de una iteración cerrada que ninguna iteración posterior reemplazó. Para armar la sección 3, recorrer las iteraciones cerradas en orden y, si una revisó una decisión anterior (paso 2 o ADR "Reemplaza a"), quedarse con la nueva.

Reglas de contenido:
- **2.4 Atributos de calidad:** tabla del árbol de utilidad y una ficha por escenario, en orden SEI, copiadas de `drivers.md`.
- **3.1:** el título lleva dos puntos ("Estilo Arquitectónico: Monolito Modular") y el texto habla solo de la organización de alto nivel.
- **3.2:** un patrón por subsección, nunca agrupados.
- **Sección 3 sin ADRs:** las decisiones no citan ADRs; los ADRs son la sección 5.
- **Secciones opcionales:** si no hay nube, componentes, validación o pendientes, se omiten esas claves del JSON y el script ajusta la numeración.
- **No inventar.** Si falta algo, se marca como pendiente o se pide; no se crea en esta sección.

## Formato de document.json

Las rutas de imágenes son relativas al JSON (por ejemplo, `../../diagrams/images/c4-containers.png`). Los textos aceptan un string o una lista de párrafos. El formato completo de `document.json` está en `references/document-json.md`; leerlo antes de escribirlo.

## Flujo de trabajo

1. Revisar las herramientas.
2. Calcular la versión y las filas nuevas de control (ver "Versión y control del documento"). Si hay una iteración abierta, decir en una línea que no entra.
3. Si no existe `cover.json`, pedir los datos de portada una vez y generar la portada.
4. Verificar que existan los PNG de todas las vistas que se van a usar. Si falta uno, convertir su `.drawio` (`drawio -x -f png -s 2 -o <images>/<nombre>.png <nombre>.drawio`); si no se puede, decirlo y seguir sin esa imagen, marcada como pendiente.
5. Archivar las versiones anteriores: mover cada `Architecture-Document-v<X>` y `ADD-Design-Record-v<X>` (Word y PDF) que haya en la raíz de `document/` a `document/previous-versions/v<X>/`, una subcarpeta por versión con los documentos de esa versión. Se mueven sin pedir aprobación; nunca se borran ni se sobrescriben. En la raíz de `document/` queda solo la versión que se genera. Nada más de `document/` se mueve.
6. Escribir `document.json` desde los archivos del proceso y generar el Word.
7. Verificar (abajo), actualizar "Último documento generado" en `status.md` y devolver la versión y las rutas. El resumen para el arquitecto: versión, qué incluye y qué quedó pendiente, en máximo cinco líneas.

Si falla un generador, decir el error en una línea, no cambiar `status.md` y ofrecer reintentar.

## Verificación antes de entregar

Convertir el Word a PDF y mirar **todas** las páginas, no una muestra:

```bash
soffice --headless --convert-to pdf document/<archivo>.docx --outdir document
pdftoppm -jpeg -r 60 document/<archivo>.pdf <carpeta-temporal>/pagina
```

- [ ] Portada completa; control del documento con todas las filas anteriores y la nueva.
- [ ] Tabla de contenido con número en cada entrada y números que coinciden con las páginas.
- [ ] Títulos separados del texto; párrafos justificados; ningún título ni encabezado de tabla solo al pie de una página; ningún diagrama cortado ni ilegible.
- [ ] **Fuente:** Calibri 11 pt, interlineado 1,15. Si no están ni Calibri ni Carlito, LibreOffice usa otra fuente al numerar y la paginación puede variar en Word. Avisarlo.

- [ ] Sección 3 solo con decisiones vigentes; sección 5 solo con ADR aprobados.
- [ ] Diagramas de `diagrams/` (vigentes), no fotos de iteraciones.
- [ ] Sección 7 coincide con el tablero.
