#!/usr/bin/env node
/*
 * Genera el documento de arquitectura en Word a partir de un JSON de contenido.
 *
 * Uso: node gen_doc.js document/source/document.json document/
 *
 * Si el segundo argumento es una carpeta (o se omite: "document/"), el archivo
 * se llama Architecture-Document-v<version>.docx, con la version de la ultima
 * fila de "control". Asi cada version queda en su propio archivo y las
 * anteriores se conservan. Tambien acepta una ruta .docx explicita.
 *
 * El estilo vive en doc_style.js (comun con el registro de diseno ADD); aqui
 * solo la estructura del documento. El contenido vive en el JSON. Las rutas de
 * imagenes del JSON son relativas a la carpeta del JSON. No se modifica por
 * proyecto.
 */
const fs = require('fs');
const path = require('path');
const S = require('./doc_style');

const specPath = process.argv[2];
if (!specPath) { console.error('Uso: node gen_doc.js document/source/document.json document/'); process.exit(1); }
const spec = S.readerText(JSON.parse(fs.readFileSync(specPath, 'utf8')));
const outPath = S.resolveOut(process.argv[3], spec.control, 'Architecture-Document');
const baseDir = path.dirname(path.resolve(specPath));

function body(k) {
  const { p, paras, parasKeep, bullets, blank, mono, hb, image, cleanTable, scenarioTable, adrTable, arr, H2, H3, H4, CONTENT_W } = k;
  const c = [];

  c.push(hb(H2, 'Introducción'), ...paras(spec.introduccion));

  const ctx = spec.contexto || {};
  c.push(hb(H2, '1. Contexto de la Solución'));
  c.push(hb(H3, '1.1 Situación Actual'), ...paras(ctx.situacion));
  c.push(hb(H3, '1.2 Objetivo'), ...paras(ctx.objetivo));
  if (ctx.diagrama) c.push(hb(H3, '1.3 Vista de Contexto C4'), image(ctx.diagrama, CONTENT_W, 8000));

  const dr = spec.drivers || {};
  c.push(hb(H2, '2. Drivers Arquitectónicos'));
  c.push(hb(H3, '2.1 Funcionalidades Principales'));
  if (dr.diagrama_casos_uso) c.push(image(dr.diagrama_casos_uso, CONTENT_W, 9500, 'Diagrama de casos de uso'));
  c.push(...bullets(dr.funcionalidades));
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
  if (arr(dr.preocupaciones).length) c.push(hb(H3, '2.5 Preocupaciones Arquitectónicas'), ...bullets(dr.preocupaciones));

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

  if (arr(spec.tacticas).length) {
    c.push(hb(H3, `3.${sub++} Tácticas por Atributo`), p('Tácticas de calidad aplicadas en el diseño, agrupadas por el atributo que atienden.'));
    c.push(cleanTable([['Atributo', 'Táctica', 'Escenarios', 'ADR'], ...spec.tacticas], [2200, 3200, 2000, CONTENT_W - 7400]), blank());
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

  let sec = 6;
  if (arr(spec.trazabilidad).length) {
    c.push(hb(H2, `${sec++}. Trazabilidad de los Drivers`));
    c.push(p('Relación de cada driver con las decisiones, los elementos y las vistas que lo atienden.'));
    c.push(cleanTable([['Driver', 'Decisiones', 'Elementos', 'Vistas'], ...spec.trazabilidad], [2300, 3300, 2100, CONTENT_W - 7700]), blank());
  }
  const va = spec.validacion;
  if (va) {
    const n = sec++;
    c.push(hb(H2, `${n}. Validación de la Arquitectura`));
    c.push(...paras(va.metodo || 'La arquitectura se evaluó contra los escenarios de calidad con un análisis inspirado en ATAM: para cada escenario se revisaron el enfoque que lo atiende, los puntos de sensibilidad, los compromisos y la prueba con que se validará.'));
    let vs = 1;
    if (arr(va.escenarios).length) {
      c.push(hb(H3, `${n}.${vs++} Análisis por Escenario`));
      c.push(cleanTable([['Escenario', 'Enfoque', 'Sensibilidad y compromisos', 'Prueba'],
        ...va.escenarios.map((e) => [e.id, e.enfoque, e.sensibilidad, e.prueba])], [1300, 2700, 2800, 2560]), blank());
    }
    if (arr(va.riesgos).length) {
      c.push(hb(H3, `${n}.${vs++} Riesgos`));
      c.push(cleanTable([['ID', 'Riesgo', 'Impacto', 'Mitigación', 'Estado'],
        ...va.riesgos.map((r) => [r.id, r.riesgo, r.impacto, r.mitigacion, r.estado])], [800, 3100, 1300, 2700, 1460]), blank());
    }
    if (arr(va.temas).length) c.push(hb(H3, `${n}.${vs++} Temas de Riesgo`), ...bullets(va.temas));
  }

  const pe = spec.pendientes;
  if (pe && arr(pe.drivers).length) {
    c.push(hb(H2, `${sec++}. Pendientes del Diseño`));
    c.push(...paras(pe.texto || 'Drivers que el diseño todavía no aborda por completo, según el tablero del proceso de diseño a la fecha de esta versión.'));
    c.push(cleanTable([['Driver', 'Estado', 'Qué falta'], ...pe.drivers.map((d) => [d.id, d.estado, d.falta])], [2600, 2000, CONTENT_W - 4600]), blank());
  }
  return c;
}

S.generate({
  baseDir, cover: spec.portada, control: spec.control, outPath,
  controlDefault: ['1.0', '', '', 'Versión inicial del documento de arquitectura.'],
  buildBody: body,
}).catch((e) => { console.error(e); process.exit(1); });
