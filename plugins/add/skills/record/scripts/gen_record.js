#!/usr/bin/env node
/*
 * Genera el registro de diseno ADD en Word a partir de un JSON de contenido,
 * con la estructura del caso FCAPS (Cervantes y Kazman, 2016, cap. 4).
 *
 * Uso: node gen_record.js document/source/record.json document/
 *
 * Si el segundo argumento es una carpeta, el archivo se llama
 * ADD-Design-Record-v<version>.docx, con la version de la ultima fila de
 * "control" (la misma del documento de arquitectura). Las rutas de imagenes del
 * JSON son relativas a la carpeta del JSON.
 *
 * El estilo es el de document/scripts/doc_style.js. No se modifica
 * por proyecto.
 */
const fs = require('fs');
const path = require('path');

function loadStyle() {
  const candidates = [
    path.join(__dirname, '..', '..', 'document', 'scripts', 'doc_style.js'),
    path.join(__dirname, 'doc_style.js'),
  ];
  const f = candidates.find((c) => fs.existsSync(c));
  if (!f) { console.error('No encuentro doc_style.js de la skill document.'); process.exit(1); }
  return require(f);
}
const S = loadStyle();

const specPath = process.argv[2];
if (!specPath) { console.error('Uso: node gen_record.js document/source/record.json document/'); process.exit(1); }
const spec = S.readerText(JSON.parse(fs.readFileSync(specPath, 'utf8')));
const outPath = S.resolveOut(process.argv[3], spec.control, 'ADD-Design-Record');
const baseDir = path.dirname(path.resolve(specPath));

const CK16 = 'Cervantes y Kazman (2016), cap. 4, caso FCAPS';
const CK24 = 'Cervantes y Kazman (2024), cap. 4';
const FUENTES = {
  paso1: `${CK16}, sección 4.3.1; ${CK24}, secciones 4.2.1 y 4.3`,
  paso2: `${CK16}, sección 4.3.2.1; ${CK24}, sección 4.2.2`,
  paso3: `${CK16}, sección 4.3.2.2; ${CK24}, sección 4.2.3`,
  paso4: `${CK16}, sección 4.3.2.3; ${CK24}, sección 4.4`,
  paso5: `${CK16}, sección 4.3.2.4; ${CK24}, secciones 4.5 y 4.6`,
  paso6: `${CK16}, sección 4.3.2.5; ${CK24}, sección 4.7`,
  paso7: `${CK16}, sección 4.3.2.6; ${CK24}, sección 4.8`,
};
const DEC = ['Decisiones de diseño y ubicación', 'Fundamentación y supuestos'];

function body(k) {
  const { p, paras, parasKeep, bullets, blank, hb, label, source, image, cleanTable, arr, H2, H3, H4, CONTENT_W, Paragraph, TextRun, richRuns } = k;
  // Celda de razón fundamental: párrafos y, aparte, las alternativas descartadas como lista
  // ("Alternativa: motivo"), o una frase si no hubo alternativas o fue una sola.
  const rp = (t) => new Paragraph({ spacing: { after: 80 }, children: richRuns(t) });
  const altP = ([a, m]) => new Paragraph({ numbering: { reference: 'bullets', level: 0 }, spacing: { after: 40 },
    children: [new TextRun({ text: `${a}: ` }), ...richRuns(String(m).replace(/^\p{Lu}(?=\p{Ll})/u, (c) => c.toLowerCase()))] });
  function razonCell(fund, alts) {
    const kids = arr(fund).map(rp);
    if (Array.isArray(alts) && alts.length && Array.isArray(alts[0])) {
      kids.push(new Paragraph({ keepNext: true, spacing: { before: 60, after: 40 }, children: [new TextRun({ text: 'Alternativas descartadas:', italics: true })] }));
      alts.forEach((x) => kids.push(altP(x)));
    } else if (alts) kids.push(rp(alts));
    return kids.length ? kids : [rp('')];
  }
  // La columna de la decisión va sin negritas.
  const plain = (t) => String(t ?? '').replace(/\*\*/g, '');
  const decRow = (d) => { const r = Array.isArray(d) ? d : [d.decision, d.fundamentacion, d.alternativas]; return [plain(r[0]), r[1], r[2]]; };
  const c = [];
  const W2 = (a) => [a, CONTENT_W - a];
  const imgs = (list) => arr(list).forEach((v) => c.push(image(v.imagen, CONTENT_W, 9500, v.titulo)));

  c.push(hb(H2, 'Introducción'), ...paras(spec.introduccion));

  // 1. Caso de negocio
  const cn = spec.caso_negocio || {};
  c.push(hb(H2, '1. Caso de Negocio'));
  c.push(...paras(cn.contexto));
  if (arr(cn.objetivos).length) c.push(label('Objetivos'), ...bullets(cn.objetivos));
  if (arr(cn.actores).length) c.push(label('Actores'), ...bullets(cn.actores));
  if (arr(cn.sistemas_externos).length) c.push(label('Sistemas externos'), ...bullets(cn.sistemas_externos));
  if (cn.diagrama) c.push(image(cn.diagrama, CONTENT_W, 8000, 'Diagrama de contexto del sistema'));
  c.push(source(`${CK16}, sección 4.1`));

  // 2. Requisitos del sistema
  const rq = spec.requisitos || {};
  c.push(hb(H2, '2. Requisitos del Sistema'));
  let rs = 1;
  if (arr(rq.casos_uso).length) {
    c.push(hb(H3, `2.${rs++} Casos de Uso`));
    if (rq.diagrama_casos_uso) c.push(image(rq.diagrama_casos_uso, CONTENT_W, 9500, 'Diagrama de casos de uso'));
    c.push(cleanTable([['ID', 'Caso de uso', 'Descripción'], ...rq.casos_uso.map((u) => [u.id, u.nombre, u.descripcion])], [900, 2600, CONTENT_W - 3500]));
    if (rq.funcionalidad_primaria) c.push(blank(120), ...paras(rq.funcionalidad_primaria));
    c.push(source(`${CK16}, sección 4.2.1`));
  }
  if (arr(rq.escenarios).length) {
    c.push(hb(H3, `2.${rs++} Escenarios de Atributos de Calidad`));
    c.push(cleanTable([['ID', 'Atributo de calidad', 'Escenario', 'Caso de uso asociado'],
      ...rq.escenarios.map((q) => [q.id, q.atributo, q.escenario, q.caso_uso || ''])], [900, 1700, 5060, 1700]));
    c.push(source(`${CK16}, sección 4.2.2`));
  }
  if (arr(rq.restricciones).length) {
    c.push(hb(H3, `2.${rs++} Restricciones`));
    c.push(cleanTable([['ID', 'Restricción'], ...rq.restricciones], W2(1000)), source(`${CK16}, sección 4.2.3`));
  }
  if (arr(rq.preocupaciones).length) {
    c.push(hb(H3, `2.${rs++} Preocupaciones Arquitectónicas`));
    c.push(cleanTable([['ID', 'Preocupación'], ...rq.preocupaciones], W2(1000)), source(`${CK16}, sección 4.2.4`));
  }
  if (arr(rq.supuestos).length) {
    c.push(hb(H3, `2.${rs++} Supuestos`));
    c.push(cleanTable([['ID', 'Supuesto', 'Impacto si es falso', 'Estado'], ...rq.supuestos], [800, 3400, 3000, 2160]), blank());
  }

  // 3. Proceso de diseno
  c.push(hb(H2, '3. Proceso de Diseño'));
  const rondas = arr(spec.rondas);
  const multi = rondas.length > 1;
  rondas.forEach((rd, ri) => {
    // Numeracion: con una ronda, 3.1 Paso 1, 3.2 Iteracion 1...; con varias, 3.R Ronda R, 3.R.1 Paso 1, 3.R.2 Iteracion 1...
    const pre = multi ? `3.${ri + 1}.` : '3.';
    const HL = multi ? H4 : H3;
    if (multi) c.push(hb(H3, `3.${ri + 1} Ronda ${rd.numero}${rd.titulo ? `: ${rd.titulo}` : ''}`));
    if (rd.motivo) c.push(...paras(rd.motivo));

    const p1 = rd.paso1 || {};
    c.push(hb(HL, `${pre}1 Paso 1: Revisar las Entradas`));
    const inner = arr(p1.prioridades).length
      ? cleanTable([['Escenario', 'Importancia para el negocio', 'Dificultad técnica'], ...p1.prioridades], [3200, 1470, 1470], { width: 6140 })
      : null;
    const rows = arr(p1.categorias).map(([cat, det]) => {
      const kids = arr(det).map((t) => new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: t })] }));
      if (inner && (p1.prioridades_en ? cat === p1.prioridades_en : /^Escenarios/.test(cat))) {
        kids.push(inner, new Paragraph({ spacing: { after: 60 }, children: [new TextRun({ text: p1.prioridades_nota || '' })] }));
      }
      return [cat, kids];
    });
    if (rows.length) c.push(cleanTable([['Categoría', 'Detalles'], ...rows], W2(2400), { labelCol: true }));
    if (p1.criterio) c.push(blank(120), p(`Criterio de "completamente abordado": ${p1.criterio}`));
    if (arr(p1.hoja_ruta).length) {
      c.push(label('Hoja de ruta'));
      c.push(cleanTable([['Iteración', 'Objetivo', 'Drivers'], ...p1.hoja_ruta], [1300, 3660, 4400]));
    }
    c.push(source(FUENTES.paso1));

    arr(rd.iteraciones).forEach((it, ii) => {
      c.push(hb(HL, `${pre}${ii + 2} Iteración ${it.numero}: ${it.titulo}`));
      c.push(p(`Abierta: ${it.abierta || '—'} · Cerrada: ${it.cerrada || '—'}`));

      const s2 = it.paso2 || {};
      c.push(label('Paso 2: establecer el objetivo de la iteración'), ...paras(s2.texto));
      arr(s2.drivers).forEach((g) => { if (arr(g.items).length) c.push(new Paragraph({ keepNext: true, spacing: { before: 60, after: 40 }, children: [new TextRun({ text: g.grupo, italics: true })] }), ...bullets(g.items)); });
      c.push(source(FUENTES.paso2));

      const s3 = it.paso3 || {};
      c.push(label('Paso 3: elegir los elementos a refinar'), ...(s3.diagrama ? parasKeep : paras)(s3.texto));
      if (s3.diagrama) c.push(image(s3.diagrama, CONTENT_W, 8000, 'Diagrama de contexto, punto de partida del refinamiento'));
      c.push(source(FUENTES.paso3));

      const s4 = it.paso4 || {};
      c.push(label('Paso 4: elegir los conceptos de diseño'), ...paras(s4.intro));
      if (arr(s4.decisiones).length) {
        const w = W2(3000);
        c.push(cleanTable([DEC, ...s4.decisiones.map(decRow).map(([d, f, a]) => [d, razonCell(f, a)])], w));
      }
      c.push(...paras(s4.texto), source(FUENTES.paso4));

      const s5 = it.paso5 || {};
      c.push(label('Paso 5: instanciar elementos, asignar responsabilidades y definir interfaces'));
      c.push(...paras(s5.intro));
      if (arr(s5.decisiones).length) {
        const w = W2(3000);
        c.push(cleanTable([['Decisión de diseño y ubicación', 'Razón fundamental'], ...s5.decisiones.map(decRow).map(([d, f, a]) => [d, razonCell(f, a)])], w), blank(120));
      }
      c.push(...paras(s5.texto));
      if (s5.preocupaciones_nuevas) c.push(p(`Preocupaciones nuevas: ${s5.preocupaciones_nuevas}`));
      c.push(source(FUENTES.paso5));

      const s6 = it.paso6 || {};
      c.push(label('Paso 6: bocetar vistas y registrar las decisiones'), ...paras(s6.texto));
      imgs(s6.vistas);
      if (arr(s6.responsabilidades).length) c.push(cleanTable([['Elemento', 'Responsabilidad'], ...s6.responsabilidades], W2(3000)), blank(120));
      if (arr(s6.relaciones).length) c.push(cleanTable([['Relación', 'Descripción'], ...s6.relaciones], W2(3600)), blank(120));
      // Interfaces: se identifican en el paso 5 y se registran en el 6 (CK16 4.3.3.4 y 4.3.3.5).
      imgs(arr(s6.secuencias).length ? s6.secuencias : s5.secuencias);
      arr(arr(s6.interfaces).length ? s6.interfaces : s5.interfaces).forEach((g) => {
        c.push(cleanTable([['Nombre del método', 'Descripción'], [`Elemento: ${g.elemento}`, ''], ...arr(g.metodos)], W2(3000)), blank(120));
      });
      c.push(source(FUENTES.paso6));

      const s7 = it.paso7 || {};
      c.push(label('Paso 7: analizar el diseño y revisar el objetivo de la iteración'), ...paras(s7.texto));
      if (arr(s7.tablero).length) {
        c.push(cleanTable([['No abordado', 'Parcialmente abordado', 'Completamente abordado', 'Decisiones de diseño tomadas durante la iteración'], ...s7.tablero], [1300, 1850, 1950, 4260]));
      }
      if (s7.recorrido) c.push(blank(120), p(`Recorrido del modelo de datos: ${s7.recorrido}`));
      if (s7.revision) c.push(p(`Revisión: ${s7.revision}`));
      c.push(source(FUENTES.paso7));
    });
  });

  // 4. Evolucion
  const ev = spec.evolucion;
  if (ev) {
    c.push(hb(H2, '4. Evolución del Diseño'), ...paras(ev.texto));
    if (arr(ev.rondas).length) c.push(label('Rondas'), cleanTable([['Ronda', 'Fecha', 'Qué la abrió'], ...ev.rondas], [1100, 1500, CONTENT_W - 2600]));
    if (arr(ev.adrs_reemplazados).length) c.push(label('ADR reemplazados o retirados'), cleanTable([['ADR', 'Estado', 'Reemplazado por', 'Fecha'], ...ev.adrs_reemplazados], [1600, 2600, 3260, 1900]));
    c.push(blank());
  }

  const refs = arr(spec.referencias).length ? spec.referencias : [
    'Cervantes, H., & Kazman, R. (2016). Designing software architectures: A practical approach. Addison-Wesley.',
    'Cervantes, H., & Kazman, R. (2024). Designing software architectures: A practical approach (2.ª ed.). Addison-Wesley.',
  ];
  c.push(hb(H2, `${ev ? 5 : 4}. Referencias`), ...paras(refs));
  return c;
}

S.generate({
  baseDir, cover: spec.portada, control: spec.control, outPath,
  controlDefault: ['1.0', '', '', 'Versión inicial del registro de diseño ADD.'],
  buildBody: body,
}).catch((e) => { console.error(e); process.exit(1); });
