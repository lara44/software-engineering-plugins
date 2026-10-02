---
name: "architecture-document-style"
description: "Usar cuando se pida crear o actualizar un documento de arquitectura de software como archivo Word (.docx) — aplica su estructura, secciones, portada, control del documento, tabla de contenido y estilo de tablas estándar."
---

# Estilo de documento de arquitectura (Word / docx-js)

Esta skill define la estructura, el estilo visual y el script generador estándar para TODOS los documentos de arquitectura de software entregados en Word. Se construyó iterando sobre el documento de arquitectura de un caso de estudio real hasta llegar a una forma validada — de ahí en adelante, todo documento de arquitectura nuevo debe partir de esta misma forma, no reinventarla. El formato de los ADRs (sección 5) se actualizó después copiando exactamente el estilo de un documento de arquitectura real de un proyecto en producción (tabla de ficha con Alternativas, Ventajas y Desventajas), y es ahora el estándar para todos los documentos, no solo para ese caso.

## Cuándo usarla

Siempre que se pida un documento de arquitectura de software en Word — para un caso de estudio, un proyecto real, una actividad académica o cualquier sistema que se describa. Si se pide expresamente otro formato (PDF, Google Docs) o un tipo de documento distinto (un caso de estudio narrativo sin arquitectura, un ADR suelto), no se activa — solo aplica al documento de arquitectura completo.

## Regla de oro: reusar el script, no reescribir el estilo desde cero

El script generador de más abajo (basado en la librería `docx` de Node; si `require('docx')` falla, instalarla con `npm install docx`) ya implementa todas las reglas de estilo de esta skill. Al crear un documento nuevo:

1. Copia el script base de la sección "Script generador" a un archivo nuevo (p. ej. `gen_arq.js`).
2. Reemplaza únicamente el CONTENIDO marcado con `// TODO:` (título, portada, control del documento, secciones 1-5, ADRs, diagramas) — nunca cambies la lógica de estilo (fuentes, colores, bordes, el patrón de portada de dos secciones, la construcción de la TOC estática en dos pasadas, la tabla de ADR) a menos que el usuario lo pida explícitamente en ese mismo turno.
3. Si el usuario pide un ajuste de estilo (color, fuente, espaciado, bordes), aplícalo aquí Y considera si vale la pena proponer la actualización de esta skill al final de la conversación (usa la herramienta de propuesta de skills si está disponible), para que el próximo documento ya nazca con el ajuste.

## Estructura obligatoria del documento

1. **Portada** (sección de Word aparte, sin márgenes, imagen a sangre completa): fondo degradado oscuro, título del documento, subtítulo con el nombre del caso/proyecto, una regla de color, y un footer con dos bloques "Para:" (destinatario/cliente) y "Por:" (autor/programa). Se genera como imagen PNG (HTML + CSS + captura con Playwright), nunca como texto nativo de Word.
2. **Control del Documento** (su propia página): tabla con columnas Versión, Fecha, Cambiado por, Comentarios.
3. **Tabla de Contenido** (su propia página, separada de Control del Documento por un salto de página): ESTÁTICA (no un campo dinámico de Word `TableOfContents`, porque no se auto-actualiza de forma confiable al abrir el archivo) — ver la sección "Tabla de contenido estática" más abajo.
4. **Introducción**: un párrafo breve presentando el documento (qué sistema, para quién, qué cubre).
5. **1. Contexto de la Solución**: 1.1 Situación Actual, 1.2 Objetivo, 1.3 Vista de Contexto C4 (diagrama, tamaño moderado — ver "Diagramas").
6. **2. Drivers Arquitectónicos**: 2.1 Funcionalidades Principales (viñetas), 2.2 Restricciones (viñetas), 2.3 Supuestos (viñetas), 2.4 Atributos de Calidad — una tabla de ESCENARIO por cada atributo de calidad (no una tabla comparativa de varias filas), con exactamente estos campos verticales: ID (que incluye también un nombre descriptivo del escenario, p. ej. "QA-01 — Tiempo de Respuesta de Consultas"), Atributo de Calidad, Estímulo, Fuente del Estímulo, Ambiente, Artefacto, Response, Medida de la Respuesta.
7. **3. Decisiones de Arquitectura** — con esta forma y este orden exactos, sin referenciar ADRs dentro de cada decisión (los ADRs son un tema aparte, sección 5):
   - 3.1 Estilo Arquitectónico: <nombre del estilo> (p. ej. "Monolito Modular", "Microservicios") — el título usa dos puntos, nunca "y", porque el nombre del estilo ES el estilo, no algo adicional. Habla ÚNICAMENTE de la forma de despliegue/organización de alto nivel (monolito vs. microservicios, cuántos procesos, etc.), con su propio diagrama (ver "Diagramas").
   - 3.2 Patrones — una subsección (Heading 4) POR CADA patrón, nunca agrupados en un solo párrafo ni bajo un título compuesto (p. ej. Clean Architecture y Domain-Driven Design son DOS patrones distintos, van en dos subsecciones separadas aunque se usen juntos). Ejemplos típicos de subsecciones: Clean Architecture, Domain-Driven Design, CQRS, Comunicación entre Módulos mediante Contrato (u otro patrón de integración).
   - 3.3 Base de Datos
   - 3.4 Servicios Cloud Seleccionados
   - 3.5 Stack Tecnológico — un párrafo breve ("Lista de herramientas y tecnologías requeridas para la correcta implementación del sistema.") seguido de una tabla Categoría/Herramientas con el estilo limpio (ver "Estilo de tablas"), normalmente Frontend y Backend como filas.
8. **4. Definición de Arquitectura**: 4.1 Vista Funcional (4.1.1 Diagrama de contenedores, 4.1.2 Diagrama de componentes), 4.2 Vista de Información/Base de Datos (con su diagrama entidad-relación), 4.3 Vista de Despliegue (con su diagrama AWS/cloud), 4.4 Vista de Desarrollo/Paquetes (árbol de carpetas en monoespaciada).
9. **5. ADRs**: un párrafo de introducción explicando que aquí solo van decisiones que implicaron un trade-off real entre alternativas viables (no decisiones impuestas por el contexto/restricciones, esas van en la sección 3). Cada ADR se presenta como una TABLA DE FICHA de 2 columnas (etiqueta/valor) — NO como un heading con viñetas — copiada del estilo del documento de arquitectura real de referencia. Ver "Estilo de tabla de ADR" para el detalle visual y de campos.

Esta estructura es el punto de partida por defecto. Si el proyecto del usuario no tiene, por ejemplo, componente cloud, omite esa subsección — pero mantén el resto del orden y la forma.

## Estilo tipográfico y de encabezados

- Fuente de todo el documento: **Segoe UI** (`styles.default.document.run.font`).
- Todos los niveles de encabezado (Heading 1 a 4) en **negro** (`color: '000000'`), nunca el azul por defecto de Word, y en negrita.
- Los títulos de nivel 1 dentro del cuerpo (Introducción, 1., 2., 3., 4., 5.) van **centrados**; sus subtítulos (1.1, 3.2, 4.1.1, etc.) van alineados a la izquierda. Los títulos de portada/front-matter ("Control del Documento", "Tabla de Contenido") NO se centran ni se cuentan en la tabla de contenido.
- Toda heading lleva `keepNext: true` para que nunca quede huérfana al final de una página justo antes de una imagen o tabla grande.

## Estilo de tablas ("tabla limpia")

Todas las tablas de contenido (Control del Documento, Stack Tecnológico, escenarios de atributos de calidad, etc.) comparten el mismo estilo — nunca la sombra azul (`D9E2F3`) ni los bordes por defecto de Word:

- Sin bordes exteriores ni de cuadrícula (`BorderStyle.NONE` en los cuatro lados de cada celda y en la tabla).
- Una única regla horizontal gris oscura (`404040`, grosor 6) bajo la fila de encabezado — o, si la tabla es de tipo "ficha" (una fila por campo, como Control del Documento o los escenarios de calidad), bajo la primera fila (el ID/nombre).
- Encabezado centrado y en negrita; el resto del texto alineado a la izquierda.
- Sombreado gris muy claro (`F2F2F2`) alternado en las filas de datos, empezando por la PRIMERA fila de datos (no la segunda) — así una tabla con una sola fila de datos (como Control del Documento con una sola versión) igual se ve con la banda gris, en vez de parecer sin estilo.
- Márgenes de celda de ~140 twips arriba/abajo y ~150 a los lados.
- Ninguna tabla lleva fila de encabezado repetible (`tableHeader`) — si una tabla se corta entre páginas, NO debe repetir el encabezado en la página siguiente.

## Estilo de tabla de ADR

Copiado exactamente (medido a pixel sobre capturas reales) del documento de arquitectura de un proyecto real que el usuario compartió. Cada ADR es una tabla de ficha de 2 columnas independiente (no comparte tabla con otros ADRs), separada de la siguiente por un párrafo en blanco:

- **Columna de etiqueta** (ancho ~2050 twips): texto alineado a la DERECHA, color morado/índigo `2B1A66` (nunca negro ni gris), sin negrita.
- **Columna de valor**: texto negro normal, alineado a la izquierda.
- **Campos, en este orden exacto**: ID, Contexto, Alternativas, Decisión, Consecuencias. (Los campos Estado/Fecha no forman parte del formato estándar; si algún proyecto sí los necesita, van entre ID y Contexto, mismo estilo.)
  - **ID**: primera fila. Valor = `ADR-00X: ` en negrita seguido del título descriptivo en texto normal, todo en una sola línea/párrafo. Esta fila lleva el bookmark que la registra en la Tabla de Contenido (el ID+título completo es el texto que aparece en la TOC).
  - **Contexto**: párrafo de texto normal.
  - **Alternativas**: SIEMPRE al menos 2 alternativas evaluadas (nunca una decisión sin alternativa real — si no hay alternativa real, la decisión no es un ADR, va en la sección 3). Para cada alternativa: un párrafo `Alternativa N: <título>` en negrita (con ` (elegida)` en cursiva al final de la alternativa que se adoptó), un párrafo de descripción, un párrafo `Ventajas` seguido de sus viñetas, y un párrafo `Desventajas` seguido de sus viñetas. Todo esto vive dentro de la MISMA celda/fila "Alternativas" (varios párrafos en una sola celda de tabla), no en filas separadas.
  - **Decisión**: párrafo de texto normal explicando qué se decidió (puede repetir/resumir la alternativa elegida).
  - **Consecuencias**: párrafo de texto normal (o viñetas si son varias) con las implicaciones de la decisión.
- **Sombreado**: alterna F2F2F2/blanco por FILA DE CAMPO empezando SOMBREADA en la fila 0 (ID) — fórmula `i % 2 === 0 → sombreado`, con `i` = índice 0-based de la fila dentro de esa tabla de ADR (ID=0 sombreado, Contexto=1 blanco, Alternativas=2 sombreado, Decisión=3 blanco, Consecuencias=4 sombreado). Es la MISMA regla de alternancia de `cleanTable`, solo que aquí no hay fila de encabezado que saltar.
- **Bordes**: sin bordes laterales ni internos entre filas (igual que el resto de tablas), pero con una regla NEGRA GRUESA (`BorderStyle.SINGLE`, grosor 12, color `000000`) arriba de la fila ID y abajo de la fila Consecuencias — enmarca cada ADR completo, a diferencia de la regla gris fina (`404040`, grosor 6) que usan las demás tablas bajo su encabezado.
- Cada ADR se registra en la Tabla de Contenido igual que un Heading 3 (mismo nivel de sangría), aunque visualmente no exista un heading separado — el bookmark vive dentro de la celda ID.

## Tabla de contenido estática

Nunca usar el campo dinámico `TableOfContents` de `docx` — no se autoactualiza en todos los visores y el usuario lo ha rechazado explícitamente por "no generarse". En su lugar:

1. Cada heading de nivel 2 a 4 que deba aparecer en la tabla de contenido se envuelve en un `Bookmark` con un id único (`bm1`, `bm2`, ...) y se registra en una lista `tocEntries` en el orden en que aparece. El ID de cada ADR se registra igual, aunque el bookmark viva dentro de una celda de tabla en vez de un `Paragraph` con `heading:`.
2. La página de Tabla de Contenido se construye con un párrafo por entrada: un `InternalHyperlink` (anchor = el id del bookmark) con el texto del título, sangría según el nivel (0 para H2, ~260 twips para H3, ~520 para H4), seguido de un `TextRun` con un tab (`'\t'`) y el número de página, usando un `tabStops` con `TabStopType.RIGHT` en `CONTENT_W` y `LeaderType.DOT` — esto da los puntos guía hasta el número, alineado a la derecha. NUNCA usar `PositionalTab` para esto (soporte de render inconsistente); un tab stop normal con líder de punto es el patrón validado.
3. Como el número de página real solo se conoce después de maquetar todo el documento, el script genera el `.docx` en DOS PASADAS: la primera con los números de página vacíos (solo para medir), se convierte a PDF, se extrae el texto por página (`pdftotext`, que separa páginas con `\f`), y para cada entrada se busca en qué página aparece su texto — usando la ÚLTIMA página donde aparece (porque la propia línea de la tabla de contenido también contiene ese texto, y siempre queda en una página anterior al cuerpo real). La segunda pasada reconstruye el documento con esos números de página reales embebidos como texto plano.

## Diagramas

- Los diagramas se generan como `.drawio` editables (con la skill de estilo C4, AWS o base de datos que corresponda) y se renderizan a PNG con draw.io Desktop (`drawio -x -f png archivo.drawio`) o con Playwright + `viewer-static.min.js` de draw.io, nunca a mano ni con otra herramienta de dibujo.
- El diagrama de Vista de Contexto (1.3) va en tamaño MODERADO, no ocupando casi toda la página — usar un límite de ancho/alto notablemente menor al ancho de contenido (p. ej. `diagramImage(path, 5600, 6000)` en vez de `diagramImage(path, maxW, 9500)`).
- Los diagramas de contenedores, componentes, despliegue y modelo de datos sí pueden usar el ancho completo de contenido (`maxW`) con una altura máxima de ~9500 twips.
- El diagrama de Estilo Arquitectónico (3.1) debe mostrar: el punto de entrada del cliente/actor arriba, el proceso/contenedor único (o los servicios, si es microservicios) con sus módulos internos y el contrato o mecanismo de comunicación entre ellos, y la capa de persistencia abajo — igual que cualquier otro diagrama de arquitectura, nunca solo los módulos sueltos sin entrada ni persistencia.
- Todas las imágenes se centran (`AlignmentType.CENTER`) y llevan `keepNext` en el heading que las precede para que el heading nunca quede solo al final de una página.

## Flujo de trabajo para un documento nuevo

1. Reunir el contenido (contexto, drivers, decisiones, vistas, ADRs con sus alternativas reales) con el usuario o del material que comparta — igual que para cualquier documento de arquitectura.
2. Generar/actualizar los diagramas `.drawio` → PNG con las skills de estilo correspondientes (C4, AWS, base de datos) y, si aplica, uno nuevo de estilo arquitectónico siguiendo la nota de arriba.
3. Copiar el script base de más abajo, ajustar el `// TODO:` de cada sección con el contenido real del proyecto, incluidas las Alternativas (mínimo 2 por ADR, marcando la elegida).
4. Ejecutar el script (dos pasadas, automatizado dentro del propio script — ver "Script generador").
5. Verificar SIEMPRE antes de entregar: convertir a PDF con LibreOffice (`soffice --headless --convert-to pdf`) y `pdftoppm` a JPEG, y mirar con la herramienta de lectura de imágenes al menos: la portada, Control del Documento, la Tabla de Contenido (que los números coincidan con las páginas reales), cualquier página con una tabla o diagrama nuevo, y al menos un ADR completo (etiquetas moradas, sombreado alterno, regla negra arriba/abajo, alternativas con viñetas).
6. Entregar el `.docx` con la herramienta de envío de archivos.

## Script generador

Guarda esto como `gen_arq.js` y ajusta los bloques marcados `// TODO:`. Requiere `docx` (`npm install docx` si no está disponible) y, para la portada, un HTML/CSS renderizado a PNG con Playwright (ver notas al final).

```js
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, LevelFormat, PageBreak, SectionType, Bookmark, InternalHyperlink,
  TabStopType, LeaderType,
} = require('docx');
const fs = require('fs');
const { execSync } = require('child_process');

// TODO: tamaños reales (px) de cada PNG de diagrama y de la portada.
const KNOWN_SIZES = {
  'render/cover.png': [2550, 3300],
  // 'render/page0.png': [w, h], ...
};
function sizeOf(path) { const [width, height] = KNOWN_SIZES[path]; return { width, height }; }

const PAGE_W = 12240, PAGE_H = 15840; // US Letter
const MARGIN = 1440; // 1"
const CONTENT_W = PAGE_W - 2 * MARGIN;

const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const HEADER_RULE = { style: BorderStyle.SINGLE, size: 6, color: '404040' };

// Estilo de tabla de ADR (calcado del documento de arquitectura de un proyecto real):
// etiqueta morada a la derecha, sombreado alterno desde la fila ID, regla negra
// gruesa arriba/abajo de cada ADR.
const ADR_LABEL_COLOR = '2B1A66';
const ADR_THICK_RULE = { style: BorderStyle.SINGLE, size: 12, color: '000000' };

function buildDoc(pageNumbers) {
  let bmCounter = 0;
  function nextBm() { return 'bm' + (++bmCounter); }
  const tocEntries = [];

  function bullet(text) {
    return new Paragraph({ numbering: { reference: 'bullets', level: 0 }, children: [new TextRun({ text })], spacing: { after: 120 } });
  }
  // Heading de front-matter, NO va en la tabla de contenido.
  function h(level, text) {
    return new Paragraph({ heading: level, keepNext: true, children: [new TextRun({ text })] });
  }
  // Heading del cuerpo: se registra en tocEntries y se centra si es nivel 2.
  function hb(level, text) {
    const id = nextBm();
    tocEntries.push({ id, level, text });
    return new Paragraph({
      heading: level,
      keepNext: true,
      alignment: level === HeadingLevel.HEADING_2 ? AlignmentType.CENTER : undefined,
      children: [new Bookmark({ id, children: [new TextRun({ text })] })],
    });
  }
  // Registra un bookmark para la TOC sin necesidad de un HeadingLevel (usado para
  // el ID de cada ADR, que vive dentro de una celda de tabla).
  function bmRegister(level, text) {
    const id = nextBm();
    tocEntries.push({ id, level, text });
    return id;
  }
  function p(text, opts = {}) {
    return new Paragraph({ children: [new TextRun({ text })], spacing: { after: 200 }, ...opts });
  }
  function mono(text) {
    return new Paragraph({ children: [new TextRun({ text, font: 'Consolas', size: 18 })], spacing: { after: 0 } });
  }
  function diagramImage(path, maxWidthTwip, maxHeightTwip) {
    const dim = sizeOf(path);
    const twipPerPx = 15;
    let wTwip = dim.width * twipPerPx, hTwip = dim.height * twipPerPx;
    const scale = Math.min(maxWidthTwip / wTwip, maxHeightTwip / hTwip, 1);
    wTwip *= scale; hTwip *= scale;
    return new Paragraph({
      alignment: AlignmentType.CENTER,
      children: [new ImageRun({ type: 'png', data: fs.readFileSync(path), transformation: { width: wTwip / 15, height: hTwip / 15 } })],
      spacing: { after: 300 },
    });
  }

  // Tabla "limpia": sin bordes, regla bajo la primera fila, sombreado alterno desde la 1a fila de datos.
  function cleanTable(rows, colWidths) {
    const trows = rows.map((row, i) => new TableRow({
      tableHeader: false,
      children: row.map((cell, ci) => new TableCell({
        width: { size: colWidths[ci], type: WidthType.DXA },
        margins: { top: 140, bottom: 140, left: 150, right: 150 },
        shading: i === 0 ? undefined : (i % 2 === 1 ? { type: ShadingType.CLEAR, fill: 'F2F2F2' } : undefined),
        borders: i === 0
          ? { top: NO_BORDER, left: NO_BORDER, right: NO_BORDER, bottom: HEADER_RULE }
          : { top: NO_BORDER, left: NO_BORDER, right: NO_BORDER, bottom: NO_BORDER },
        children: [new Paragraph({
          alignment: i === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
          children: [new TextRun({ text: cell, bold: i === 0 })],
        })],
      })),
    }));
    return new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: colWidths,
      borders: { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER, insideHorizontal: NO_BORDER, insideVertical: NO_BORDER },
      rows: trows,
    });
  }

  // Tabla "ficha" de escenario de atributo de calidad (una tabla por atributo).
  function qaScenarioTable(qa) {
    const fieldRows = [
      ['ID', `${qa.id} — ${qa.nombre}`],
      ['Atributo de Calidad', qa.atributo],
      ['Estímulo', qa.estimulo],
      ['Fuente del Estímulo', qa.fuente],
      ['Ambiente', qa.ambiente],
      ['Artefacto', qa.artefacto],
      ['Response', qa.response],
      ['Medida de la Respuesta', qa.medida],
    ];
    return cleanTable(fieldRows, [2500, 6860]);
  }

  // Tabla de ADR estilo de referencia: ficha de 2 columnas (etiqueta/valor), con
  // soporte para un campo "Alternativas" estructurado (array de {titulo, elegida,
  // descripcion, ventajas[], desventajas[]}).
  // `adr` = { id: 'ADR-001', titulo: '...', campos: [['Contexto', '...'], ['Alternativas', [...]], ['Decisión', '...'], ['Consecuencias', '...']] }
  function adrTable(adr) {
    const bmId = bmRegister(HeadingLevel.HEADING_3, `${adr.id}: ${adr.titulo}`);
    const labelColW = 2050;
    const valueColW = CONTENT_W - labelColW;
    const rows = [['ID', null], ...adr.campos];
    const trows = rows.map((row, i) => {
      const [label, value] = row;
      const shaded = i % 2 === 0; // ID(0) sombreado, alterna desde ahí
      const shading = shaded ? { type: ShadingType.CLEAR, fill: 'F2F2F2' } : undefined;
      const isFirst = i === 0;
      const isLast = i === rows.length - 1;
      const borders = {
        top: isFirst ? ADR_THICK_RULE : NO_BORDER,
        bottom: isLast ? ADR_THICK_RULE : NO_BORDER,
        left: NO_BORDER,
        right: NO_BORDER,
      };
      let valueChildren;
      if (value === null) {
        valueChildren = [new Paragraph({
          children: [
            new Bookmark({ id: bmId, children: [new TextRun({ text: adr.id + ': ', bold: true })] }),
            new TextRun({ text: adr.titulo }),
          ],
        })];
      } else if (Array.isArray(value)) {
        // Campo "Alternativas": una o más alternativas evaluadas, cada una con
        // descripción y listas de Ventajas / Desventajas.
        valueChildren = [];
        value.forEach((alt, ai) => {
          valueChildren.push(new Paragraph({
            spacing: { before: ai === 0 ? 0 : 200, after: 100 },
            children: [
              new TextRun({ text: `Alternativa ${ai + 1}: `, bold: true }),
              new TextRun({ text: alt.titulo, bold: true }),
              ...(alt.elegida ? [new TextRun({ text: '  (elegida)', italics: true })] : []),
            ],
          }));
          valueChildren.push(new Paragraph({ text: alt.descripcion, spacing: { after: 100 } }));
          valueChildren.push(new Paragraph({ text: 'Ventajas', spacing: { after: 60 } }));
          alt.ventajas.forEach((v) => valueChildren.push(new Paragraph({
            numbering: { reference: 'bullets', level: 0 },
            children: [new TextRun({ text: v })],
            spacing: { after: 60 },
          })));
          valueChildren.push(new Paragraph({ text: 'Desventajas', spacing: { before: 60, after: 60 } }));
          alt.desventajas.forEach((v, vi) => valueChildren.push(new Paragraph({
            numbering: { reference: 'bullets', level: 0 },
            children: [new TextRun({ text: v })],
            spacing: { after: vi === alt.desventajas.length - 1 ? 0 : 60 },
          })));
        });
      } else {
        valueChildren = [new Paragraph({ children: [new TextRun({ text: value })] })];
      }
      return new TableRow({
        tableHeader: false,
        children: [
          new TableCell({
            width: { size: labelColW, type: WidthType.DXA },
            margins: { top: 140, bottom: 140, left: 150, right: 150 },
            shading, borders,
            children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ text: label, color: ADR_LABEL_COLOR })] })],
          }),
          new TableCell({
            width: { size: valueColW, type: WidthType.DXA },
            margins: { top: 140, bottom: 140, left: 150, right: 150 },
            shading, borders,
            children: valueChildren,
          }),
        ],
      });
    });
    return new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [labelColW, valueColW],
      borders: { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER, insideHorizontal: NO_BORDER, insideVertical: NO_BORDER },
      rows: trows,
    });
  }

  // TODO: Portada (imagen a sangre completa, generada aparte con HTML+Playwright).
  const coverChildren = [
    new Paragraph({
      spacing: { before: 0, after: 0 },
      children: [new ImageRun({ type: 'png', data: fs.readFileSync('render/cover.png'), transformation: { width: PAGE_W / 15, height: PAGE_H / 15 } })],
    }),
  ];

  // TODO: Control del Documento — filas reales del proyecto.
  const controlDocRows = [
    ['Versión', 'Fecha', 'Cambiado por', 'Comentarios'],
    ['1.0', 'YYYY-MM-DD', 'Nombre Apellido', 'Versión inicial del documento de arquitectura.'],
  ];

  // ===================== CUERPO =====================
  const children = [];
  children.push(hb(HeadingLevel.HEADING_2, 'Introducción'));
  children.push(p('TODO: párrafo de introducción del documento.'));

  children.push(hb(HeadingLevel.HEADING_2, '1. Contexto de la Solución'));
  children.push(hb(HeadingLevel.HEADING_3, '1.1 Situación Actual'));
  children.push(p('TODO'));
  children.push(hb(HeadingLevel.HEADING_3, '1.2 Objetivo'));
  children.push(p('TODO'));
  children.push(hb(HeadingLevel.HEADING_3, '1.3 Vista de Contexto C4'));
  children.push(diagramImage('render/page0.png', 5600, 6000)); // tamaño moderado, no maxW

  children.push(hb(HeadingLevel.HEADING_2, '2. Drivers Arquitectónicos'));
  children.push(hb(HeadingLevel.HEADING_3, '2.1 Funcionalidades Principales'));
  children.push(bullet('TODO'));
  children.push(hb(HeadingLevel.HEADING_3, '2.2 Restricciones'));
  children.push(bullet('TODO'));
  children.push(hb(HeadingLevel.HEADING_3, '2.3 Supuestos'));
  children.push(bullet('TODO'));
  children.push(hb(HeadingLevel.HEADING_3, '2.4 Atributos de Calidad'));
  const qaScenarios = [
    // TODO: uno por atributo. { id: 'QA-01', nombre: '...', atributo: '...', estimulo: '...', fuente: '...', ambiente: '...', artefacto: '...', response: '...', medida: '...' }
  ];
  qaScenarios.forEach((qa, i) => {
    children.push(qaScenarioTable(qa));
    children.push(new Paragraph({ text: '', spacing: { after: i === qaScenarios.length - 1 ? 200 : 240 } }));
  });

  children.push(hb(HeadingLevel.HEADING_2, '3. Decisiones de Arquitectura'));
  children.push(hb(HeadingLevel.HEADING_3, '3.1 Estilo Arquitectónico: TODO_NOMBRE_DEL_ESTILO'));
  children.push(p('TODO: solo la forma de despliegue/organización de alto nivel.'));
  children.push(diagramImage('render/page_estilo.png', CONTENT_W, 9500)); // actor + módulos/servicios + contrato + persistencia

  children.push(hb(HeadingLevel.HEADING_3, '3.2 Patrones'));
  children.push(hb(HeadingLevel.HEADING_4, '3.2.1 TODO_PATRON_1'));
  children.push(p('TODO'));
  children.push(hb(HeadingLevel.HEADING_4, '3.2.2 TODO_PATRON_2'));
  children.push(p('TODO')); // un patrón por subsección, nunca agrupados

  children.push(hb(HeadingLevel.HEADING_3, '3.3 Base de Datos'));
  children.push(p('TODO'));
  children.push(hb(HeadingLevel.HEADING_3, '3.4 Servicios Cloud Seleccionados'));
  children.push(p('TODO'));
  children.push(hb(HeadingLevel.HEADING_3, '3.5 Stack Tecnológico'));
  children.push(p('Lista de herramientas y tecnologías requeridas para la correcta implementación del sistema.'));
  children.push(cleanTable([['Categoría', 'Herramientas'], ['Frontend', 'TODO'], ['Backend', 'TODO']], [1800, 7560]));
  children.push(new Paragraph({ text: '', spacing: { after: 200 } }));

  children.push(hb(HeadingLevel.HEADING_2, '4. Definición de Arquitectura'));
  children.push(hb(HeadingLevel.HEADING_3, '4.1 Vista Funcional'));
  children.push(hb(HeadingLevel.HEADING_4, '4.1.1 Diagrama de contenedores'));
  children.push(diagramImage('render/page1.png', CONTENT_W, 11000));
  children.push(hb(HeadingLevel.HEADING_4, '4.1.2 Diagrama de componentes'));
  children.push(diagramImage('render/page2.png', CONTENT_W, 9500));
  children.push(hb(HeadingLevel.HEADING_3, '4.2 Vista de Información (Base de Datos)'));
  children.push(p('TODO'));
  children.push(diagramImage('render/page4.png', CONTENT_W, 9500));
  children.push(hb(HeadingLevel.HEADING_3, '4.3 Vista de Despliegue'));
  children.push(p('TODO'));
  children.push(diagramImage('render/page3.png', CONTENT_W, 9500));
  children.push(hb(HeadingLevel.HEADING_3, '4.4 Vista de Desarrollo (Paquetes)'));
  children.push(p('TODO'));
  'TODO/carpeta\n  arbol.txt'.split('\n').forEach((line) => children.push(mono(line)));
  children.push(new Paragraph({ text: '', spacing: { after: 200 } }));

  children.push(hb(HeadingLevel.HEADING_2, '5. ADRs'));
  children.push(p('Se documentan aquí únicamente las decisiones que implicaron un trade-off real entre alternativas viables. Otras decisiones (impuestas por el contexto o restricciones) están en la sección 3.'));
  const adrs = [
    // TODO: uno por decisión con trade-off real, mínimo 2 alternativas cada uno:
    // {
    //   id: 'ADR-001', titulo: 'Título de la decisión',
    //   campos: [
    //     ['Contexto', '...'],
    //     ['Alternativas', [
    //       { titulo: 'Opción A', descripcion: '...', ventajas: ['...'], desventajas: ['...'] },
    //       { titulo: 'Opción B', elegida: true, descripcion: '...', ventajas: ['...'], desventajas: ['...'] },
    //     ]],
    //     ['Decisión', '...'],
    //     ['Consecuencias', '...'],
    //   ],
    // },
  ];
  adrs.forEach((adr, i) => {
    children.push(adrTable(adr));
    children.push(new Paragraph({ text: '', spacing: { after: i === adrs.length - 1 ? 200 : 260 } }));
  });

  // ===================== TABLA DE CONTENIDO ESTÁTICA =====================
  function tocParagraph(entry) {
    const indent = entry.level === HeadingLevel.HEADING_2 ? 0 : entry.level === HeadingLevel.HEADING_3 ? 260 : 520;
    const bold = entry.level === HeadingLevel.HEADING_2;
    const pageNum = pageNumbers ? String(pageNumbers[entry.id] || '') : '';
    return new Paragraph({
      indent: { left: indent },
      spacing: { after: 110 },
      tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W, leader: LeaderType.DOT }],
      children: [
        new InternalHyperlink({ anchor: entry.id, children: [new TextRun({ text: entry.text, bold, style: 'Hyperlink' })] }),
        new TextRun({ text: '\t' + pageNum }),
      ],
    });
  }

  const frontMatterChildren = [
    h(HeadingLevel.HEADING_1, 'Control del Documento'),
    cleanTable(controlDocRows, [1200, 1500, 2760, 3900]),
    new Paragraph({ children: [new PageBreak()] }),
    h(HeadingLevel.HEADING_1, 'Tabla de Contenido'),
    ...tocEntries.map(tocParagraph),
    new Paragraph({ children: [new PageBreak()] }),
  ];

  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: 'Segoe UI' } },
        heading1: { run: { font: 'Segoe UI', color: '000000', bold: true } },
        heading2: { run: { font: 'Segoe UI', color: '000000', bold: true } },
        heading3: { run: { font: 'Segoe UI', color: '000000', bold: true } },
        heading4: { run: { font: 'Segoe UI', color: '000000', bold: true } },
      },
    },
    numbering: {
      config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }],
    },
    sections: [
      { properties: { type: SectionType.NEXT_PAGE, page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 0, bottom: 0, left: 0, right: 0 } } }, children: coverChildren },
      { properties: { type: SectionType.NEXT_PAGE, page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } }, children: [...frontMatterChildren, ...children] },
    ],
  });

  return { doc, tocEntries };
}

// Dos pasadas: la primera mide la paginación real, la segunda embebe los números de página reales en la TOC estática.
async function main() {
  const pass1 = buildDoc(null);
  fs.writeFileSync('doc_pass1.docx', await Packer.toBuffer(pass1.doc));
  execSync('soffice --headless --convert-to pdf doc_pass1.docx', { stdio: 'inherit' }); // requiere LibreOffice en el PATH
  const pages = execSync('pdftotext doc_pass1.pdf -').toString().split('\f');
  const norm = (s) => s.replace(/\s+/g, ' ').trim();
  const normPages = pages.map(norm);
  const pageNumbers = {};
  pass1.tocEntries.forEach((entry) => {
    const needle = norm(entry.text);
    let lastPage = null;
    normPages.forEach((t, idx) => { if (t.includes(needle)) lastPage = idx + 1; }); // última ocurrencia = la del cuerpo, no la de la TOC
    pageNumbers[entry.id] = lastPage || '';
  });
  const pass2 = buildDoc(pageNumbers);
  fs.writeFileSync('documento_arquitectura.docx', await Packer.toBuffer(pass2.doc));
  fs.unlinkSync('doc_pass1.docx'); fs.unlinkSync('doc_pass1.pdf');
  console.log('done');
}
main().catch((e) => { console.error(e); process.exit(1); });
```

### Notas sobre la portada (imagen)

La portada NO se escribe como texto nativo de Word — se construye como una pieza de diseño (HTML/CSS con degradado oscuro, título, subtítulo, footer Para/Por) y se captura como PNG con Playwright a 2550×3300px (2x de una carta 8.5×11in), servida por un `python3 -m http.server` local. Patrón: un `cover.html` y un script de captura con Playwright: viewport 1275×1650, `deviceScaleFactor: 2`, screenshot del `<body>` completo.

### Verificación obligatoria antes de entregar

```bash
soffice --headless --convert-to pdf documento_arquitectura.docx
pdftoppm -jpeg -r 100 documento_arquitectura.pdf page
```
Luego leer con la herramienta de imágenes al menos la portada, Control del Documento, la Tabla de Contenido (números de página correctos), cualquier tabla o diagrama nuevo, y al menos un ADR completo.