/*
 * Estilo comun de los documentos Word de la arquitectura.
 *
 * Lo usan gen_doc.js (documento de arquitectura) y gen_record.js de la skill
 * record (registro de diseno ADD). Un cambio de estilo aqui cambia
 * los dos documentos. No se modifica por proyecto.
 *
 * Uso:
 *   const S = require('./doc_style');
 *   S.generate({ baseDir, cover, control, outPath, buildBody: (k) => [ ...parrafos y tablas ] });
 *
 * buildBody recibe un "kit" con los bloques de construccion (p, hb, cleanTable,
 * image, adrTable, ...). Se llama dos veces: la primera mide la paginacion real
 * con LibreOffice y la segunda escribe los numeros en la tabla de contenido.
 */
const fs = require('fs');
const path = require('path');
const os = require('os');
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
const D = loadDocx();
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  ImageRun, LevelFormat, PageBreak, SectionType, Bookmark, InternalHyperlink,
  TabStopType, LeaderType, NoBreakHyphen,
} = D;

// Texto de una celda con los IDs (UC-01, QA-05, ADR-003…) unidos por un guion que no se parte al final de la linea.
function idChildren(text) {
  const parts = String(text).split(/\b([A-Z]{1,4})-(?=\d)/);
  const out = [];
  for (let i = 0; i < parts.length; i++) {
    if (i % 2 === 1) { out.push(parts[i], new NoBreakHyphen()); } else if (parts[i]) out.push(parts[i]);
  }
  return out.length ? out : [''];
}

// Runs de un texto con **negrita** y los IDs sin partir.
function richRuns(text, opts = {}) {
  return String(text ?? '').split(/\*\*(.+?)\*\*/).filter((s, i) => s !== '' || i === 0)
    .map((seg, i) => new TextRun({ ...opts, bold: opts.bold || i % 2 === 1, children: idChildren(seg) }));
}

const PAGE_W = 12240, PAGE_H = 15840; // carta
const MARGIN = 1440;
const CONTENT_W = PAGE_W - 2 * MARGIN;
const FONT = 'Calibri';
const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };
const GRAY = { type: ShadingType.CLEAR, fill: 'F2F2F2' };
// Tablas limpias: encabezado oscuro con letra blanca, celdas compactas y lineas grises finas entre filas.
const TABLE_HEAD = { type: ShadingType.CLEAR, fill: '262626' };
const ROW_RULE = { style: BorderStyle.SINGLE, size: 4, color: 'D9D9D9' };
const TABLE_MARGINS = { top: 70, bottom: 70, left: 120, right: 120 };
const H1 = HeadingLevel.HEADING_1, H2 = HeadingLevel.HEADING_2, H3 = HeadingLevel.HEADING_3, H4 = HeadingLevel.HEADING_4;

const arr = (x) => (x == null ? [] : Array.isArray(x) ? x : [x]);

// Tamano real de un PNG leyendo su cabecera (sin tablas de tamanos a mano).
function pngSize(file) {
  const b = fs.readFileSync(file);
  if (b.toString('ascii', 1, 4) !== 'PNG') throw new Error(`No es PNG: ${file}`);
  return { width: b.readUInt32BE(16), height: b.readUInt32BE(20) };
}

// Nombre del archivo de salida: si el destino es una carpeta, <prefijo>-v<version>.docx
// con la version de la ultima fila de "control".
function resolveOut(arg, control, prefix) {
  const target = arg || 'document';
  if (target.toLowerCase().endsWith('.docx')) return path.resolve(target);
  const rows = Array.isArray(control) ? control : [];
  const version = String((rows.length ? rows[rows.length - 1][0] : '1.0') || '1.0').trim().replace(/[^\w.-]+/g, '-');
  fs.mkdirSync(path.resolve(target), { recursive: true });
  return path.resolve(target, `${prefix}-v${version}.docx`);
}

// Kit de bloques de construccion para una pasada.
function makeKit(baseDir) {
  let bm = 0;
  const tocEntries = [];
  const nextBm = () => 'bm' + (++bm);
  const rel = (f) => path.resolve(baseDir, f);

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
  // Titulo con marcador: entra en la tabla de contenido. Los de nivel 2 van centrados.
  function hb(level, text) {
    const id = nextBm();
    tocEntries.push({ id, level, text });
    return new Paragraph({
      heading: level, keepNext: true,
      alignment: level === H2 ? AlignmentType.CENTER : undefined,
      children: [new Bookmark({ id, children: [new TextRun({ text })] })],
    });
  }
  // Etiqueta en negrita que abre un bloque (por ejemplo, un paso de ADD), sin entrar en la tabla de contenido.
  const label = (text) => new Paragraph({ keepNext: true, spacing: { before: 200, after: 100 }, children: [new TextRun({ text, bold: true })] });
  // Linea de fuente: cursiva gris pequena debajo de un bloque.
  const source = (text) => new Paragraph({ spacing: { before: 40, after: 200 }, children: [new TextRun({ text: `Fuente: ${text}`, italics: true, size: 16, color: '595959' })] });
  function image(file, maxW, maxH, caption) {
    const f = rel(file);
    if (!fs.existsSync(f)) { console.error(`AVISO: falta la imagen ${file}; se omite.`); return p(`[Falta la imagen: ${file}]`); }
    const d = pngSize(f);
    let w = d.width * 15, hh = d.height * 15;
    const s = Math.min(maxW / w, maxH / hh, 1);
    w *= s; hh *= s;
    const img = new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: caption ? 80 : 300 }, keepNext: !!caption,
      children: [new ImageRun({ type: 'png', data: fs.readFileSync(f), transformation: { width: w / 15, height: hh / 15 } })],
    });
    if (!caption) return img;
    return [img, new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 300 }, children: [new TextRun({ text: caption, italics: true, size: 17, color: '595959' })] })];
  }

  // Tabla limpia: encabezado (fila 0) en franja oscura con letra blanca en negrita;
  // filas de datos con linea gris fina debajo y sombreado alterno. Con labelCol
  // (fichas de dos columnas), la primera columna va en negrita sobre gris en vez
  // del sombreado alterno. El encabezado se repite en cada pagina y nunca queda
  // solo al pie: va junto a la primera fila de datos. Las filas cortas no se
  // parten entre dos paginas; las largas si, para no dejar huecos en blanco. Una celda puede ser texto o una lista de parrafos/tablas.
  function rowLength(row) {
    const walk = (x) => typeof x === 'string' ? x.length : Array.isArray(x) ? x.reduce((n, y) => n + walk(y), 0) : (x && typeof x === 'object' ? 250 : 0);
    return walk(row);
  }
  function cleanTable(rows, colWidths, { labelCol = false, width = CONTENT_W } = {}) {
    return new Table({
      width: { size: width, type: WidthType.DXA }, columnWidths: colWidths,
      borders: { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER, insideHorizontal: NO_BORDER, insideVertical: NO_BORDER },
      rows: rows.map((row, i) => new TableRow({
        tableHeader: i === 0,
        cantSplit: i === 0 || rowLength(row) < 700,
        children: row.map((cell, ci) => {
          const head = i === 0, lab = labelCol && ci === 0 && !head;
          const shading = head ? TABLE_HEAD : lab ? GRAY : (!labelCol && i % 2 === 0 ? GRAY : undefined);
          const children = Array.isArray(cell) && cell.length && typeof cell[0] === 'object'
            ? cell
            : [new Paragraph({ keepNext: head, children: richRuns(cell, { bold: head || lab, color: head ? 'FFFFFF' : undefined }) })];
          return new TableCell({
            width: { size: colWidths[ci], type: WidthType.DXA }, margins: TABLE_MARGINS, shading,
            borders: { top: NO_BORDER, left: NO_BORDER, right: NO_BORDER, bottom: head ? NO_BORDER : ROW_RULE },
            children,
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
    if (q.caso_uso) rows.push(['Caso de uso asociado', q.caso_uso]);
    return cleanTable(rows, [2500, CONTENT_W - 2500], { labelCol: true });
  }

  // ADR con el mismo estilo de las fichas de escenario: franja negra con el ID y
  // el titulo, etiquetas en negrita sobre gris y lineas grises finas entre filas.
  // Cada alternativa es un bloque con su titulo; la elegida lleva la marca
  // "(elegida)". La franja se repite si el ADR sigue en otra pagina.
  function adrTable(adr, { toc = true } = {}) {
    const bmId = nextBm();
    if (toc) tocEntries.push({ id: bmId, level: H3, text: `${adr.id}: ${adr.titulo}` });
    const labelW = 2500, valueW = CONTENT_W - labelW;
    const rows = [['ID', null]];
    if (adr.estado) rows.push(['Estado', adr.estado]);
    if (adr.fecha) rows.push(['Fecha', adr.fecha]);
    if (adr.decidio) rows.push(['Decidió', adr.decidio]);
    if (adr.evidencia) rows.push(['Evidencia', adr.evidencia]);
    rows.push(['Contexto', adr.contexto], ['Alternativas', adr.alternativas], ['Decisión', adr.decision], ['Consecuencias', adr.consecuencias]);
    const bulletP = (v) => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, children: [new TextRun({ text: v })], spacing: { after: 40 } });
    const textP = (v, after = 0) => new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after }, children: [new TextRun({ text: v || '' })] });
    return new Table({
      width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [labelW, valueW],
      borders: { top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER, insideHorizontal: NO_BORDER, insideVertical: NO_BORDER },
      rows: rows.map(([lab, value], i) => {
        const head = i === 0;
        let kids;
        if (head) {
          kids = [new Paragraph({ keepNext: true, children: [new Bookmark({ id: bmId, children: [new TextRun({ text: `${adr.id}: ${adr.titulo}`, bold: true, color: 'FFFFFF' })] })] })];
        } else if (lab === 'Alternativas') {
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
        return new TableRow({ tableHeader: head, cantSplit: lab !== 'Alternativas', children: [
          cell(labelW, [new Paragraph({ keepNext: head, children: [new TextRun({ text: lab, bold: true, color: head ? 'FFFFFF' : undefined })] })], head ? TABLE_HEAD : GRAY),
          cell(valueW, kids, head ? TABLE_HEAD : undefined)] });
      }),
    });
  }

  return {
    p, paras, parasKeep, bullet, bullets, blank, mono, h, hb, label, source, image, cleanTable, scenarioTable, adrTable,
    rel, tocEntries, arr, H1, H2, H3, H4, CONTENT_W, Paragraph, TextRun, PageBreak, richRuns,
  };
}

// Arma el documento completo de una pasada: portada (imagen a sangre), control
// del documento, tabla de contenido y cuerpo.
function buildDoc({ baseDir, cover, control, controlDefault, buildBody }, pageNumbers) {
  const k = makeKit(baseDir);
  const body = buildBody(k).flat();
  const tocP = (e) => new Paragraph({
    indent: { left: e.level === H2 ? 0 : e.level === H3 ? 260 : 520 }, spacing: { after: 110 },
    tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W, leader: LeaderType.DOT }],
    children: [
      new InternalHyperlink({ anchor: e.id, children: [new TextRun({ text: e.text, bold: e.level === H2, style: 'Hyperlink' })] }),
      new TextRun({ text: '\t' + (pageNumbers ? String(pageNumbers[e.id] || '') : '') }),
    ],
  });
  const rows = arr(control).length ? control : [controlDefault || ['1.0', '', '', 'Versión inicial.']];
  const front = [
    k.h(H1, 'Control del Documento'),
    k.cleanTable([['Versión', 'Fecha', 'Cambiado por', 'Comentarios'], ...rows], [1200, 1500, 2760, 3900]),
    new Paragraph({ children: [new PageBreak()] }),
    k.h(H1, 'Tabla de Contenido'),
    ...k.tocEntries.map(tocP),
    new Paragraph({ children: [new PageBreak()] }),
  ];

  const sections = [];
  if (cover) {
    const f = k.rel(cover);
    if (fs.existsSync(f)) {
      sections.push({ properties: { type: SectionType.NEXT_PAGE, page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: 0, bottom: 0, left: 0, right: 0 } } },
        children: [new Paragraph({ spacing: { before: 0, after: 0 }, children: [new ImageRun({ type: 'png', data: fs.readFileSync(f), transformation: { width: PAGE_W / 15, height: PAGE_H / 15 } })] })] });
    } else console.error(`AVISO: falta la portada ${cover}; el documento sale sin portada.`);
  }
  sections.push({ properties: { type: SectionType.NEXT_PAGE, page: { size: { width: PAGE_W, height: PAGE_H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } } }, children: [...front, ...body] });

  // Espacio antes y despues de cada titulo (en veinteavos de punto), para que no quede pegado al texto.
  const hs = (before, after) => ({ run: { font: FONT, color: '000000', bold: true }, paragraph: { spacing: { before, after } } });
  const doc = new Document({
    styles: { default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { line: 276 } } }, heading1: hs(360, 240), heading2: hs(360, 200), heading3: hs(280, 160), heading4: hs(240, 120) } },
    numbering: { config: [{ reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•', alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] }] },
    sections,
  });
  return { doc, tocEntries: k.tocEntries };
}

// Busca un ejecutable en el PATH y, si no esta, en las rutas tipicas de Mac
// (LibreOffice instalado como app, Homebrew en Apple Silicon o Intel).
function findBin(name, extra = []) {
  try { return execSync(`command -v ${name}`, { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch (e) { /* sigue */ }
  const candidates = [...extra, `/opt/homebrew/bin/${name}`, `/usr/local/bin/${name}`];
  return candidates.find((c) => fs.existsSync(c)) || null;
}

// Dos pasadas: la primera mide la paginacion real con LibreOffice; la segunda
// escribe los numeros de pagina en la tabla de contenido.
async function generate(opts) {
  const out = opts.outPath;
  if (fs.existsSync(out)) {
    console.error(`AVISO: ya existe ${path.basename(out)} y se reemplaza. Si esa version ya se entrego, agrega una fila nueva en "control" para generar otro archivo.`);
  }
  const SOFFICE = findBin('soffice', ['/Applications/LibreOffice.app/Contents/MacOS/soffice']);
  const PDFTOTEXT = findBin('pdftotext');
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'gen_doc_'));
  const pass1 = buildDoc(opts, null);
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
  const pass2 = buildDoc(opts, pageNumbers);
  fs.writeFileSync(out, await Packer.toBuffer(pass2.doc));
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log('OK ->', out);
}

// Texto para el lector: convierte las abreviaturas internas del proceso (CK16, CK24, §, nombres de archivo)
// en citas legibles antes de escribir el documento. No cambia el contenido.
function readerText(v) {
  if (Array.isArray(v)) return v.map(readerText);
  if (v && typeof v === 'object') { const o = {}; for (const k of Object.keys(v)) o[k] = readerText(v[k]); return o; }
  if (typeof v !== 'string') return v;
  return v
    .replace(/`?drivers\.md`?\s*§\s*([\d.]*\d)/g, 'la sección $1')
    .replace(/\bCK(16|24)\s*§\s*([\d.]*\d)/g, (m, y, s) => `Cervantes y Kazman, 20${y}, sección ${s}`)
    .replace(/\bCK(16|24)\b/g, (m, y) => `Cervantes y Kazman, 20${y}`)
    .replace(/§§\s*/g, 'secciones ')
    .replace(/§\s*/g, 'sección ');
}

module.exports = { generate, resolveOut, arr, readerText, CONTENT_W, H1, H2, H3, H4 };
