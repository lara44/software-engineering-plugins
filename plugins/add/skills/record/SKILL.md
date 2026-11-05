---
name: "record"
description: "Usar para generar el registro de diseño ADD en Word (.docx): caso de negocio, requisitos del sistema, paso 1 y cada iteración cerrada con sus pasos 2 a 7, sus bocetos y su tablero, y la evolución del diseño, con la estructura del caso FCAPS de Cervantes y Kazman. Se genera junto con el documento de arquitectura y con su misma versión."
---

# Registro de diseño ADD (Word)

Genera `ADD-Design-Record-v<versión>.docx`: **cómo se llegó al diseño**, iteración por iteración, con la estructura del caso FCAPS (Cervantes y Kazman, 2016, cap. 4). Es el complemento del documento de arquitectura, que muestra solo el diseño vigente; los dos llevan la misma versión. Esta skill no decide nada nuevo ni resume: copia lo que quedó registrado al cierre de cada paso 1 y de cada iteración.

Cada respuesta empieza con el bloque de estado de las secciones, con el formato exacto de `start` ("Bloque de estado"), con la sección 5 en curso.

## Contrato

- **Lee:** `drivers.md`, `iterations/` (solo `step-1.md` con `status: aprobado` e iteraciones con `status: cerrada`), sus fotos en `iterations/round-R/it-N/diagrams/images/`, `adr/`, `diagrams/images/c4-context.png`, `document/source/document.json` y `cover.json`.
- **Escribe:** `document/ADD-Design-Record-v<versión>.docx` en la raíz de `document/` (las versiones anteriores ya las movió `document` a `document/previous-versions/v<X>/`), su PDF de verificación, `document/source/record.json`, `record-cover.json` y `record-cover.png`.
- **No toca nunca:** ningún otro archivo, incluido `document.json` (lo escribe `document`).
- **Devuelve al orquestador:** la versión y la ruta del Word.

## Generador

En `scripts/` de esta skill. Se ejecuta tal cual; no se lee, no se copia y no se reescribe:

```bash
node <carpeta-de-esta-skill>/scripts/gen_record.js document/source/record.json document/
```

Usa el estilo común de `document/scripts/doc_style.js` (portada, títulos, tablas, fichas de ADR, tabla de contenido con números de página), así que necesita las mismas herramientas: `node`, `docx`, `soffice` y `pdftotext` (ver "Herramientas" en `document`). La portada usa los mismos datos de `cover.json` ("Para", "Por" y el subtítulo), con `"kicker": "Registro de diseño · ADD 3.0"` y `"titulo": "Registro de diseño ADD"`: se escribe `document/source/record-cover.json` y se genera con el script de portada de `document`:

```bash
node <carpeta-de-document>/scripts/make_cover.js document/source/record-cover.json document/source/record-cover.png
```

## Versión y control del documento

Son los del documento de arquitectura: se toman de la tabla `control` de `document/source/document.json`. Si la versión que corresponde (ver `document`, "Versión y control del documento") todavía no está ahí, generar primero el documento de arquitectura con `document`. Así los dos documentos nunca tienen versiones ni historiales distintos.

## Estructura y de dónde sale cada parte

| Sección | Contenido | Fuente |
|---|---|---|
| Portada y Control del Documento | Portada con el título del registro; control igual al del documento de arquitectura | `cover.json` y `document.json` |
| Introducción | Una frase: qué sistema, método (ADD 3.0), cuántas rondas e iteraciones cerradas, y que el diseño vigente está en el documento de arquitectura de la misma versión | `drivers.md` e `iterations/` |
| 1. Caso de negocio | Contexto, objetivos, actores y sistemas externos, diagrama de contexto | `drivers.md` §1 |
| 2. Requisitos del sistema | 2.1 Casos de uso; 2.2 Escenarios de atributos de calidad (ID, atributo, escenario, caso de uso asociado); 2.3 Restricciones; 2.4 Preocupaciones arquitectónicas; 2.5 Supuestos | `drivers.md` §2, tal como está hoy (los elementos "Retirado" se muestran con esa marca) |
| 3. Proceso de diseño | Por cada ronda: el paso 1 y una subsección por iteración cerrada | `step-1.md` e `it-N.md` |
| 4. Evolución del diseño | Rondas y qué las abrió; ADR reemplazados o retirados y por cuál. El avance de los drivers no se repite aquí: lo muestra el tablero del paso 7 de cada iteración, como en el caso FCAPS. Los cambios a los requisitos tampoco van: quedan en `drivers.md`, y los que afectan al diseño abren una ronda nueva (CK24 §4.2.1) | `step-1.md` de cada ronda, `adr/` |
| Referencias | Las fuentes citadas | Fijas: CK16, CK24 y las demás que aparezcan |

**Sección 3, en detalle:**
- **Rondas:** si hay una sola, la sección 3 no la menciona (3.1 Paso 1, 3.2 Iteración 1, …). Desde la segunda, cada ronda es una subsección (3.1 Ronda 1, 3.1.1 Paso 1, 3.1.2 Iteración 1, …), y el paso 1 de cada ronda nueva empieza con su motivo.
- **Paso 1:** la tabla "Categoría | Detalles" del caso FCAPS, con la tabla de prioridad de los escenarios dentro de la fila de escenarios; el criterio de "completamente abordado" y la hoja de ruta.
- **Cada iteración:** fecha de apertura y de cierre; los pasos 2 a 7 en orden, con sus tablas tal como quedaron en `it-N.md`; en el paso 3 de la primera iteración, el diagrama de contexto; en el paso 6, las fotos de la iteración (nunca las vistas vigentes); en el paso 7, el tablero de la iteración y la revisión del objetivo.
- **Fuente por paso:** debajo de cada paso, una línea "Fuente:" con la sección del libro, como en el formato del caso FCAPS: paso 2, CK16 §4.3.2.1 y CK24 §4.2.2; paso 3, CK16 §4.3.2.2 y CK24 §4.2.3; paso 4, CK16 §4.3.2.3 y CK24 §4.4; paso 5, CK16 §4.3.2.4 y CK24 §4.5–4.6; paso 6, CK16 §4.3.2.5 y CK24 §4.7; paso 7, CK16 §4.3.2.6 y CK24 §4.8.

Reglas:
- **Solo lo cerrado.** Una iteración abierta no aparece, ni siquiera parcial. Si hay una, decirlo en una línea.
- **Copiar, no reescribir.** Los textos y tablas de cada paso se copian de `it-N.md`; si algo está mal, se dice, y se corrige en su archivo con `design`, no aquí.
- **Las decisiones reemplazadas se quedan.** En la iteración donde se tomaron aparecen tal cual; la evolución dice qué las reemplazó.
- **Sin "[Propuesta]".** Si quedó alguna marca en un archivo cerrado, decirlo: es un error del cierre.

## Formato de record.json

El formato completo está en `references/record-json.md`; leerlo antes de escribirlo. Las rutas de imágenes son relativas al JSON (por ejemplo, `../../iterations/round-1/it-2/diagrams/images/c4-containers.png`).

## Flujo de trabajo

1. Confirmar que `document/source/document.json` tiene la versión que corresponde; si no, generar primero el documento de arquitectura.
2. Generar la portada del registro si no existe o si cambió `cover.json`.
3. Verificar que existan los PNG de las fotos de cada iteración cerrada. Si falta uno, convertir su `.drawio` de la carpeta de la iteración; si no se puede, decirlo y seguir sin esa imagen, marcada como faltante.
4. Escribir `record.json` desde los archivos del proceso y generar el Word.
5. Verificar (abajo) y devolver la versión y la ruta. Si falla el generador, decir el error en una línea y ofrecer reintentar.

## Verificación antes de entregar

Convertir a PDF y mirar **todas** las páginas:

```bash
soffice --headless --convert-to pdf document/ADD-Design-Record-v<version>.docx --outdir document
pdftoppm -jpeg -r 60 document/ADD-Design-Record-v<version>.pdf <carpeta-temporal>/pagina
```

- [ ] Portada con el título "Registro de diseño ADD"; control del documento igual al del documento de arquitectura de la misma versión.
- [ ] Tabla de contenido con número en cada entrada y números que coinciden con las páginas.
- [ ] Secciones 1 y 2 en el orden del caso FCAPS.
- [ ] Una subsección por iteración cerrada, en orden, con los pasos 2 a 7 completos y su línea "Fuente:".
- [ ] Las fotos de cada iteración tomadas de su propia carpeta; ningún diagrama cortado ni ilegible.
- [ ] Evolución con las rondas y los ADR reemplazados, sin tabla de cambios a los requisitos.
- [ ] Ningún título ni encabezado de tabla solo al pie de una página.

## Fuentes

- Cervantes, H., & Kazman, R. (2016). *Designing software architectures: A practical approach*. Addison-Wesley. Cap. 4, caso FCAPS (CK16).
- Cervantes, H., & Kazman, R. (2024). *Designing software architectures: A practical approach* (2.ª ed.). Addison-Wesley. Cap. 4 (CK24).
