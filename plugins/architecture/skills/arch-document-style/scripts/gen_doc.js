#!/usr/bin/env node
/*
 * Genera el documento de arquitectura en Word a partir de un JSON de contenido.
 *
 * Uso: node gen_doc.js documento.json documento/
 *
 * Si el segundo argumento es una carpeta (o se omite: "documento/"), el archivo
 * se llama Documento-Arquitectura-v<version>.docx, con la version de la ultima
 * fila de "control". Asi cada version queda en su propio archivo y las
 * anteriores se conservan. Tambien acepta una ruta .docx explicita.
 *
 * Requiere la libreria `docx` (npm install docx, en la carpeta del proyecto o
 * global), LibreOffice (`soffice`) y poppler (`pdftotext`) para numerar la
 * tabla de contenido en dos pasadas. Las rutas de imagenes del JSON son
 * relativas a la carpeta del JSON.
 *
 * Todo el estilo vive aqui (fuentes, tablas limpias, fichas de escenario, ADR,
 * TOC estatica). El contenido vive en el JSON. No se modifica por proyecto.
 */
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function loadDocx() {
  const tries = [
    () => require('docx'),
    () => require(path.join(process.cwd(), 'node_modules', 'docx')),
    () => require(path.join(execSync('npm root -g').toString().trim(), 'docx')),
  ];
  for (const t of tries) { try { return t(); } catch (e) { /* siguiente */ } }
  console.error('No encuentro la libreria "docx". Instalala con: npm install docx');
  process.exit(1);
}
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, LevelFormat, PageBreak, SectionType, Bookmark, InternalHyperlink,
  TabStopType, LeaderType,
} = loadDocx();

const PAGE_W = 12240, PAGE_H = 15840; // carta
const MARGIN = 1440;
const CONTENT_W = PAGE_W - 2 * MARGIN;
const FONT = 'Segoe UI';
const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const GRAY = { type: ShadingType.CLEAR, fill: 'F2F2F2' };
// Tablas limpias: encabezado oscuro con letra blanca, celdas compactas y lineas grises finas entre filas.
const TABLE_HEAD = { type: ShadingType.CLEAR, fill: '262626' };
const ROW_RULE = { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' };
const TABLE_MARGINS = { top: 70, bottom: 70, left: 120, right: 120 };

const specPath = process.argv[2];
if (!specPath) { console.error('Uso: node gen_doc.js documento.json documento/'); process.exit(1); }
const spec = JSON.parse(fs.readFileSync(specPath, 'utf8'));
function resolveOut(arg) {
  const target = arg || 'documento';
  if (target.toLowerCase().endsWith('.docx')) return path.resolve(target);
  const rows = Array.isArray(spec.control) ? spec.control : [];
  const version = String((rows.length ? rows[rows.length - 1][0] : '1.0') || '1.0').trim().replace(/[^\w.-]+/g, '-');
  fs.mkdirSync(path.resolve(target), { recursive: true });
  return path.resolve(target, `Documento-Arquitectura-v${version}.docx`);
}
const outPath = resolveOut(process.argv[3]);
const baseDir = path.dirname(path.resolve(specPath));
const rel = (p) => path.resolve(baseDir, p);

// Tamano real de un PNG leyendo su cabecera (sin tablas de tamanos a mano).
function pngSize(file) {
  const b = fs.readFileSync(file);
  if (b.toString('ascii', 1, 4) !== 'PNG') throw new Error(`No es PNG: ${file}`);
  return { width: b.readUInt32BE(16), height: b.readUInt32BE(20) };
}
const arr = (x) => (x == null ? [] : Array.isArray(x) ? x : [x]);

function buildDoc(pageNumbers) {
  let bm = 0;
  const tocEntries = [];
  const nextBm = () => 'bm' + (++bm);

  // Parrafos de cuerpo justificados.
  const p = (text, opts = {}) => new Paragraph({ children: [new TextRun({ text })], alignment: AlignmentType.JUSTIFIED, spacing: { after: 200 }, ...opts });
  const paras = (x) => arr(x).map((t) => p(t));
  // Parrafos que preceden a una imagen: se mantienen con ella en la misma pagina.
  const parasKeep = (x) => arr(x).map((t) => p(t, { keepNext: true }));
  const bullet = (text) => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, children: [new TextRun({ text })], spacing: { after: 120 } });
  const bullets = (x) => arr(x).map(bullet);
  const blank = (after = 200) => new Paragraph({ text: '', spacing: { after } });
  const mono = (text) => new Paragraph({ children: [new TextRun({ text, font: 'Consolas', size: 18 })], spacing: { after: 0 } });
  const h = (level, text) => new Paragraph({ heading: level, keepNext: true, children: [new TextRun({ text })] });
  function hb(level, text) {
    const id = nextBm();
    tocEntries.push({ id, level, text });
    return new Paragraph({
      heading: level, keepNext: true,
      alignment: level === HeadingLevel.HEADING_2 ? AlignmentType.CENTER : undefined,
      children: [new Bookmark({ id, children: [new TextRun({ text })] })],
    });
  }
  function image(file, maxW, maxH) {
    const f = rel(file);
    if (!fs.existsSync(f)) { console.error(`AVISO: falta la imagen ${file}; se omite.`); return p(`[Falta la imagen: ${file}]`); }
    const d = pngSize(f);
    let w = d.width * 15, hh = d.height * 15;
    const s = Math.min(maxW / w, maxH / hh, 1);
    w *= s; hh *= s;
    return new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 300 },
      children: [new ImageRun({ type: 'png', data: fs.readFileSync(f), transformation: { width: w / 15, height: hh / 15 } })],
    });
  }

  // Tabla limpia: encabezado (fila 0) en franja oscura con letra blanca en negrita;
  // filas de datos con linea gris fina debajo y sombreado alterno. Con labelCol
  // (fichas de dos columnas), la primera columna va en negrita sobre gris en vez
  // del sombreado alterno. El encabezado se repite en cada pagina y nunca queda
  // solo al pie: va junto a la primera fila de datos. Ninguna fila se parte
  // entre dos paginas.
  function cleanTable(rows, colWidths, { labelCol = false } = {}) {
    return new Table({
      width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: colWidths,
      borders: { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER, insideHorizontal: NO_BORDER, insideVertical: NO_BORDER },
      rows: rows.map((row, i) => new TableRow({
        tableHeader: i === 0,
        cantSplit: true,
        children: row.map((cell, ci) => {
          const head = i === 0, label = labelCol && ci === 0 && !head;
          const shading = head ? TABLE_HEAD : label ? GRAY : (!labelCol && i % 2 === 0 ? GRAY : undefined);
          return new TableCell({
            width: { size: colWidths[ci], type: WidthType.DXA }, margins: TABLE_MARGINS, shading,
            borders: { top: NO_BORDER, left: NO_BORDER, right: NO_BORDER, bottom: head ? NO_BORDER : ROW_RULE },
            children: [new Paragraph({ keepNext: head, children: [new TextRun({ text: String(cell ?? ''), bold: head || label, color: head ? 'FFFFFF' : undefined })] })],
          });
        }),
      })),
    });
  }

  // Ficha de escenario de calidad: campos en orden SEI, en espanol.
  function scenarioTable(q) {
    const rows = [
      ['ID', `${q.id} — ${q.nombre}`],
      ['Atributo de calidad', q.refinamiento ? `${q.atributo} › ${q.refinamiento}` : q.atributo],
    ];
    if (q.negocio || q.dificultad) rows.push(['Prioridad', `Negocio ${q.negocio || '—'} · Dificultad ${q.dificultad || '—'}`]);
    rows.push(['Fuente del estímulo', q.fuente], ['Estímulo', q.estimulo], ['Ambiente', q.ambiente],
      ['Artefacto', q.artefacto], ['Respuesta', q.respuesta], ['Medida de la respuesta', q.medida]);
    return cleanTable(rows, [2500, CONTENT_W - 2500], { labelCol: true });
  }

  // ADR con el mismo estilo de las fichas de escenario: franja negra con el ID y
  // el titulo, etiquetas en negrita sobre gris y lineas grises finas entre filas.
  // Cada alternativa es un bloque con su titulo; la elegida lleva la marca
  // "(elegida)". La franja se repite si el ADR sigue en otra pagina.
  function adrTable(adr) {
    const bmId = nextBm();
    tocEntries.push({ id: bmId, level: HeadingLevel.HEADING_3, text: `${adr.id}: ${adr.titulo}` });
    const labelW = 2500, valueW = CONTENT_W - labelW;
    const rows = [['ID', null], ['Contexto', adr.contexto], ['Alternativas', adr.alternativas], ['Decisión', adr.decision], ['Consecuencias', adr.consecuencias]];
    const bulletP = (v) => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, children: [new TextRun({ text: v })], spacing: { after: 40 } });
    const textP = (v, after = 0) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after }, children: [new TextRun({ text: v || '' })] });
    return new Table({
      width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [labelW, valueW],
      borders: { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER, insideHorizontal: NO_BORDER, insideVertical: NO_BORDER },
      rows: rows.map(([label, value], i) => {
        const head = i === 0;
        let kids;
        if (head) {
          kids = [new Paragraph({ keepNext: true, children: [new Bookmark({ id: bmId, children: [new TextRun({ text: `${adr.id}: ${adr.titulo}`, bold: true, color: 'FFFFFF' })] })] })];
        } else if (label === 'Alternativas') {
          kids = [];
          arr(value).forEach((a, ai) => {
            kids.push(new Paragraph({ keepNext: true, spacing: { before: ai === 0 ? 0 : 160, after: 60 }, children: [
              new TextRun({ text: `${ai + 1}. ${a.titulo}`, bold: true }),
              ...(a.elegida ? [new TextRun({ text: ' (elegida)', bold: true })] : [])] }));
            if (a.descripcion) kids.push(textP(a.descripcion, 60));
            if (arr(a.ventajas).length) { kids.push(new Paragraph({ keepNext: true, spacing: { after: 20 }, children: [new TextRun({ text: 'Ventajas', bold: true, size: 18, color: '595959' })] })); arr(a.ventajas).forEach((v) => kids.push(bulletP(v))); }
            if (arr(a.desventajas).length) { kids.push(new Paragraph({ keepNext: true, spacing: { before: 40, after: 20 }, children: [new TextRun({ text: 'Desventajas', bold: true, size: 18, color: '595959' })] })); arr(a.desventajas).forEach((v) => kids.push(bulletP(v))); }
          });
        } else if (Array.isArray(value)) {
          kids = value.map(bulletP);
        } else {
          kids = [textP(value)];
        }
        const cell = (w, children, shading) => new TableCell({
          width: { size: w, type: WidthType.DXA }, margins: TABLE_MARGINS, shading,
          borders: { top: NO_BORDER, left: NO_BORDER, right: NO_BORDER, bottom: head ? NO_BORDER : ROW_RULE }, children });
        return new TableRow({ tableHeader: head, cantSplit: label !== 'Alternativas', children: [
          cell(labelW, [new Paragraph({ keepNext: head, children: [new TextRun({ text: label, bold: true, color: head ? 'FFFFFF' : undefined })] })], head ? TABLE_HEAD : GRAY),
          cell(valueW, kids, head ? TABLE_HEAD : undefined)] });
      }),
    });
  }

  // ===================== CUERPO =====================
  const c = [];
  const H2 = HeadingLevel.HEADING_2, H3 = HeadingLevel.HEADING_3, H4 = HeadingLevel.HEADING_4;

  c.push(hb(H2, 'Introducción'), ...paras(spec.introduccion));

  const ctx = spec.contexto || {};
  c.push(hb(H2, '1. Contexto de la Solución'));
  c.push(hb(H3, '1.1 Situación Actual'), ...paras(ctx.situacion));
  c.push(hb(H3, '1.2 Objetivo'), ...paras(ctx.objetivo));
  if (ctx.diagrama) c.push(hb(H3, '1.3 Vista de Contexto C4'), image(ctx.diagrama, 5600, 6000));

  const dr = spec.drivers || {};
  c.push(hb(H2, '2. Drivers Arquitectónicos'));
  c.push(hb(H3, '2.1 Funcionalidades Principales'), ...bullets(dr.funcionalidades));
  c.push(hb(H3, '2.2 Restricciones'), ...bullets(dr.restricciones));
  c.push(hb(H3, '2.3 Supuestos'), ...bullets(dr.supuestos));
  c.push(hb(H3, '2.4 Atributos de Calidad'));
  const esc = arr(dr.escenarios);
  if (esc.length) {
    c.push(p('El árbol de utilidad resume los atributos de calidad, sus refinamientos y los escenarios que los concretan, con su prioridad para el negocio y su dificultad técnica (A = alta, M = media, B = baja).'));
    c.push(cleanTable([['Atributo', 'Refinamiento', 'Escenario', 'Prioridad (N, D)'],
      ...esc.map((q) => [q.atributo, q.refinamiento || '', `${q.id} — ${q.nombre}`, `(${q.negocio || '—'}, ${q.dificultad || '—'})`])],
      [1900, 2300, 3660, 1500]));
    c.push(blank(240));
    esc.forEach((q, i) => { c.push(scenarioTable(q), blank(i === esc.length - 1 ? 200 : 240)); });
  }

  const de = spec.decisiones || {};
  c.push(hb(H2, '3. Decisiones de Arquitectura'));
  if (de.estilo) {
    c.push(hb(H3, `3.1 Estilo Arquitectónico: ${de.estilo.nombre}`), ...(de.estilo.diagrama ? parasKeep : paras)(de.estilo.texto));
    if (de.estilo.diagrama) c.push(image(de.estilo.diagrama, CONTENT_W, 9500));
  }
  c.push(hb(H3, '3.2 Patrones'));
  arr(de.patrones).forEach((pt, i) => c.push(hb(H4, `3.2.${i + 1} ${pt.nombre}`), ...paras(pt.texto)));
  let sub = 3;
  if (de.base_datos) c.push(hb(H3, `3.${sub++} Base de Datos`), ...paras(de.base_datos));
  if (de.cloud) {
    c.push(hb(H3, `3.${sub++} Servicios Cloud Seleccionados`), ...paras(de.cloud.texto));
    if (de.cloud.servicios) c.push(cleanTable([['Servicio', 'Uso'], ...de.cloud.servicios], [3000, CONTENT_W - 3000]), blank());
  }
  if (de.stack) {
    c.push(hb(H3, `3.${sub++} Stack Tecnológico`), p('Lista de herramientas y tecnologías requeridas para la correcta implementación del sistema.'));
    c.push(cleanTable([['Categoría', 'Herramientas'], ...de.stack], [1800, CONTENT_W - 1800]), blank());
  }

  const vi = spec.vistas || {};
  c.push(hb(H2, '4. Definición de Arquitectura'));
  c.push(hb(H3, '4.1 Vista Funcional'));
  if (vi.contenedores) c.push(hb(H4, '4.1.1 Diagrama de contenedores'), ...parasKeep(vi.contenedores.texto), image(vi.contenedores.diagrama, CONTENT_W, 11000));
  if (vi.componentes) c.push(hb(H4, '4.1.2 Diagrama de componentes'), ...parasKeep(vi.componentes.texto), image(vi.componentes.diagrama, CONTENT_W, 9500));
  let vsub = 2;
  if (vi.informacion) c.push(hb(H3, `4.${vsub++} Vista de Información (Base de Datos)`), ...parasKeep(vi.informacion.texto), image(vi.informacion.diagrama, CONTENT_W, 9500));
  if (vi.despliegue) c.push(hb(H3, `4.${vsub++} Vista de Despliegue`), ...parasKeep(vi.despliegue.texto), image(vi.despliegue.diagrama, CONTENT_W, 9500));
  if (vi.desarrollo) {
    c.push(hb(H3, `4.${vsub++} Vista de Desarrollo (Paquetes)`), ...paras(vi.desarrollo.texto));
    String(vi.desarrollo.arbol || '').split('\n').forEach((l) => c.push(mono(l)));
    c.push(blank());
  }

  const adrs = arr(spec.adrs);
  c.push(hb(H2, '5. ADRs'));
  c.push(p('Se documentan aquí únicamente las decisiones que implicaron un trade-off real entre alternativas viables. Las decisiones impuestas por el contexto o por restricciones están en la sección 3.'));
  adrs.forEach((a, i) => c.push(adrTable(a), blank(i === adrs.length - 1 ? 200 : 260)));

  const va = spec.validacion;
  if (va) {
    c.push(hb(H2, '6. Validación de la Arquitectura'));
    c.push(...paras(va.metodo || 'La arquitectura se evaluó contra los escenarios de calidad con un análisis inspirado en ATAM: para cada escenario se revisaron el enfoque que lo atiende, los puntos de sensibilidad, los compromisos y la prueba con que se validará.'));
    if (arr(va.escenarios).length) {
      c.push(hb(H3, '6.1 Análisis por Escenario'));
      c.push(cleanTable([['Escenario', 'Enfoque', 'Sensibilidad y compromisos', 'Prueba'],
        ...va.escenarios.map((e) => [e.id, e.enfoque, e.sensibilidad, e.prueba])], [1300, 2700, 2800, 2560]), blank());
    }
    if (arr(va.riesgos).length) {
      c.push(hb(H3, '6.2 Riesgos'));
      c.push(cleanTable([['ID', 'Riesgo', 'Impacto', 'Mitigación', 'Estado'],
        ...va.riesgos.map((r) => [r.id, r.riesgo, r.impacto, r.mitigacion, r.estado])], [800, 3100, 1300, 2700, 1460]), blank());
    }
    if (arr(va.temas).length) c.push(hb(H3, '6.3 Temas de Riesgo'), ...bullets(va.temas));
  }

  // ===================== TABLA DE CONTENIDO ESTATICA =====================
  const tocP = (e) => new Paragraph({
    indent: { left: e.level === H2 ? 0 : e.level === H3 ? 260 : 520 }, spacing: { after: 110 },
    tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W, leader: LeaderType.DOT }],
    children: [
      new InternalHyperlink({ anchor: e.id, children: [new TextRun({ text: e.text, bold: e.level === H2, style: 'Hyperlink' })] }),
      new TextRun({ text: '\t' + (pageNumbers ? String(pageNumbers[e.id] || '') : '') }),
    ],
  });
  const control = arr(spec.control).length ? spec.control : [['1.0', '', '', 'Versión inicial del documento de arquitectura.']];
  const front = [
    h(HeadingLevel.HEADING_1, 'Control del Documento'),
    cleanTable([['Versión', 'Fecha', 'Cambiado por', 'Comentarios'], ...control], [1200, 1500, 2760, 3900]),
    new Paragraph({ children: [new PageBreak()] }),
    h(HeadingLevel.HEADING_1, 'Tabla de Contenido'),
    ...tocEntries.map(tocP),
    new Paragraph({ children: [new PageBreak()] }),
  ];

  const sections = [];
  if (spec.portada) {
    const f = rel(spec.portada);
    if (fs.existsSync(f)) {
      sections.push({ properties: { type: SectionType.NEXT_PAGE, page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
        children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f), transformation: { width: PAGE_W / 15, height: PAGE_H / 15 } })] })] });
    } else console.error(`AVISO: falta la portada ${spec.portada}; el documento sale sin portada.`);
  }
  sections.push({ properties: { type: SectionType.NEXT_PAGE, page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } }, children: [...front, ...c] });

  // Espacio antes y despues de cada titulo (en veinteavos de punto), para que no quede pegado al texto.
  const hs = (before, after) => ({ run: { font: FONT, color: '000000', bold: true }, paragraph: { spacing: { before, after } } });
  const doc = new Document({
    styles: { default: { document: { run: { font: FONT } }, heading1: hs(360, 240), heading2: hs(360, 200), heading3: hs(280, 160), heading4: hs(240, 120) } },
    numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
    sections,
  });
  return { doc, tocEntries };
}

// Busca un ejecutable en el PATH y, si no esta, en las rutas tipicas de Mac
// (LibreOffice instalado como app, Homebrew en Apple Silicon o Intel).
function findBin(name, extra = []) {
  try { return execSync(`command -v ${name}`, { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch (e) { /* sigue */ }
  const candidates = [...extra, `/opt/homebrew/bin/${name}`, `/usr/local/bin/${name}`];
  return candidates.find((c) => fs.existsSync(c)) || null;
}
const SOFFICE = findBin('soffice', ['/Applications/LibreOffice.app/Contents/MacOS/soffice']);
const PDFTOTEXT = findBin('pdftotext');

// Dos pasadas: la primera mide la paginacion real con LibreOffice; la segunda
// escribe los numeros de pagina en la tabla de contenido.
async function main() {
  const out = outPath;
  if (fs.existsSync(out)) {
    console.error(`AVISO: ya existe ${path.basename(out)} y se reemplaza. Si esa version ya se entrego, agrega una fila nueva en "control" para generar otro archivo.`);
  }
  const tmpDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'gen_doc_'));
  const pass1 = buildDoc(null);
  const tmpDocx = path.join(tmpDir, 'pass1.docx');
  fs.writeFileSync(tmpDocx, await Packer.toBuffer(pass1.doc));
  let pageNumbers = null;
  try {
    if (!SOFFICE || !PDFTOTEXT) throw new Error('faltan herramientas');
    execSync(`"${SOFFICE}" --headless --convert-to pdf --outdir "${tmpDir}" "${tmpDocx}"`, { stdio: 'ignore' });
    const pages = execSync(`"${PDFTOTEXT}" "${path.join(tmpDir, 'pass1.pdf')}" -`).toString().split('\f');
    const norm = (s) => s.replace(/\s+/g, ' ').trim();
    const np = pages.map(norm);
    pageNumbers = {};
    pass1.tocEntries.forEach((e) => {
      const needle = norm(e.text);
      let last = null;
      np.forEach((t, i) => { if (t.includes(needle)) last = i + 1; }); // ultima aparicion = cuerpo, no la TOC
      pageNumbers[e.id] = last || '';
    });
  } catch (e) {
    console.error(`AVISO: no pude numerar la tabla de contenido (soffice: ${SOFFICE || 'no encontrado'}, pdftotext: ${PDFTOTEXT || 'no encontrado'}); sale sin números de página.`);
  }
  const pass2 = buildDoc(pageNumbers);
  fs.writeFileSync(out, await Packer.toBuffer(pass2.doc));
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log('OK ->', out);
}
main().catch((e) => { console.error(e); process.exit(1); });
