---
name: "arch-document-style"
description: "Usar cuando se pida crear o actualizar un documento de arquitectura de software como archivo Word (.docx) — aplica su estructura, secciones, portada, control del documento, tabla de contenido y estilo de tablas estándar."
---

# Documento de arquitectura (Word)

Genera el documento de arquitectura en Word con una estructura y un estilo fijos, validados sobre documentos reales. Es la fase 5 del proceso: el contenido sale de los archivos aprobados (`drivers.md`, `decisions.md`, `diagrams/`, `validation.md`); esta skill no decide nada nuevo.

Si piden otro formato (PDF, Google Docs) o un documento distinto (un ADR suelto, un caso narrativo), esta skill no aplica.

## Generadores

En la carpeta `scripts/` de esta skill. Se ejecutan tal cual; no se leen, no se copian y no se reescriben:

```bash
node <carpeta-de-esta-skill>/scripts/make_cover.js document/source/cover.json document/source/cover.png
node <carpeta-de-esta-skill>/scripts/gen_doc.js document/source/document.json document/
```

Estructura de `document/` (no se crean otras carpetas):

```
document/
├── Architecture-Document-v<versión>.docx   ← un Word por versión, con su PDF
└── source/                                 ← lo que genera el Word
    ├── document.json
    ├── cover.json
    ├── cover.png
    └── png/                                ← diagramas exportados para el documento
```

- `make_cover.js`: portada como imagen a sangre completa (degradado oscuro, título, subtítulo, regla de color y bloques "Para" y "Por"). Requiere Playwright con Chromium.
- `gen_doc.js`: todo el documento a partir de un JSON de contenido. Ya implementa el estilo completo: fuente Segoe UI, encabezados negros con espacio antes y después (los de nivel 1 centrados), párrafos justificados, tablas compactas con encabezado negro y letra blanca, líneas grises finas entre filas y sombreado alterno, fichas de escenario y de ADR con la columna de etiquetas en negrita sobre gris, tabla de contenido estática numerada en dos pasadas e imágenes con su tamaño real. Requiere la librería `docx` (`npm install docx`), LibreOffice (`soffice`) y poppler (`pdftotext`).

- **Un archivo por versión:** `gen_doc.js` nombra el Word con la versión de la última fila de `control` (`document/Architecture-Document-v2.0.docx`). Las versiones anteriores no se borran ni se sobrescriben: son el historial que se entregó. Regenerar la misma versión mientras está en revisión la reemplaza; una vez entregada, cualquier cambio lleva una fila nueva en `control` y, con ella, un archivo nuevo. El PDF de verificación lleva el mismo nombre.

**No se modifican por proyecto.** Si el arquitecto pide un ajuste de estilo, se propone como cambio a los scripts del plugin.

## Herramientas (revisar al empezar)

Comprobar `node`, `docx`, Playwright, `soffice` y `pdftotext`. Si falta algo, pedir permiso para instalarlo en ese momento, no a mitad del documento:
- Mac: `brew install --cask libreoffice` y `brew install poppler`;
- en la carpeta del proyecto: `npm install docx playwright && npx playwright install chromium`.

Antes de instalar, buscar si ya están: en Mac, LibreOffice suele estar en `/Applications/LibreOffice.app/Contents/MacOS/soffice` aunque `soffice` no esté en el PATH, y poppler en `/opt/homebrew/bin`. `gen_doc.js` los busca solo en esas rutas. Sin `soffice` o `pdftotext`, el documento se genera igual, pero la tabla de contenido sale sin números de página: avisarlo.

## Estructura del documento y de dónde sale cada parte

| Sección | Contenido | Fuente |
|---|---|---|
| Portada | Título, subtítulo, Para, Por | Preguntar al arquitecto o tomarlo de `inputs/` (p. ej., un anteproyecto) |
| Control del Documento | Versión, fecha, autores, comentarios. Si hubo "Cambios posteriores a la aprobación", cada uno es una fila. Al actualizar un documento ya entregado, se agrega una fila con la versión nueva (preguntar al arquitecto el número) | Arquitecto y `decisions.md` |
| Tabla de Contenido | Automática | — |
| Introducción | Un párrafo: qué sistema, para quién, qué cubre | `drivers.md` |
| 1. Contexto | 1.1 Situación actual, 1.2 Objetivo, 1.3 Vista de contexto C4 | `drivers.md` y `diagrams/` |
| 2. Drivers | 2.1 Funcionalidades, 2.2 Restricciones, 2.3 Supuestos, 2.4 Atributos de calidad | `drivers.md` |
| 3. Decisiones | 3.1 Estilo (con su diagrama), 3.2 Patrones (uno por subsección), Base de datos, Servicios cloud, Stack | `decisions.md` y `diagrams/` |
| 4. Definición | 4.1 Vista funcional (contenedores y componentes), Información (modelo de datos), Despliegue, Desarrollo (árbol de carpetas) | `diagrams/` |
| 5. ADRs | Solo decisiones con alternativas reales | `decisions.md` |
| 6. Validación | 6.1 Análisis por escenario, 6.2 Riesgos, 6.3 Temas de riesgo | `validation.md` |

Reglas de contenido:
- **2.4 Atributos de calidad:** el script dibuja primero la tabla del árbol de utilidad (atributo → refinamiento → escenario, con prioridad de negocio y dificultad) y después una ficha por escenario, con los campos en orden SEI: fuente, estímulo, ambiente, artefacto, respuesta y medida. Copiar los escenarios de `drivers.md` tal cual, con su refinamiento y su prioridad.
- **3.1:** el título lleva dos puntos ("Estilo Arquitectónico: Monolito Modular") y el texto habla solo de la organización de alto nivel.
- **3.2:** un patrón por subsección, nunca agrupados (Clean Architecture y DDD son dos).
- **Sección 3 sin ADRs:** las decisiones no citan ADRs; los ADRs son la sección 5.
- **ADRs:** mínimo 2 alternativas, con la elegida marcada. Si una decisión no tuvo alternativa real, no es ADR: va en la sección 3.
- **Secciones opcionales:** si el sistema no tiene nube, componentes o validación, se omiten esas claves del JSON y el script ajusta la numeración.
- **No inventar.** Todo sale de los archivos aprobados. Si falta algo (por ejemplo, la vista de desarrollo), se pide o se marca como pendiente; no se crea en esta fase.

## Formato de document.json

Las rutas de imágenes son relativas al JSON (`cover.png`, `png/<nombre>.png`). Los textos aceptan un string o una lista de párrafos.

```json
{
  "portada": "cover.png",
  "control": [["1.0", "2026-10-11", "Autor", "Versión inicial."]],
  "introduccion": "…",
  "contexto": {"situacion": ["…"], "objetivo": ["…"], "diagrama": "png/c4-context.png"},
  "drivers": {
    "funcionalidades": ["UC-01 …"], "restricciones": ["CON-1: …"], "supuestos": ["AS-1: …"],
    "escenarios": [{"id": "QA-01", "nombre": "…", "atributo": "Trazabilidad", "refinamiento": "Procedencia", "negocio": "A", "dificultad": "A",
                    "fuente": "…", "estimulo": "…", "ambiente": "…", "artefacto": "…", "respuesta": "…", "medida": "…"}]
  },
  "decisiones": {
    "estilo": {"nombre": "Monolito Modular", "texto": ["…"], "diagrama": "png/architectural-style.png"},
    "patrones": [{"nombre": "Clean Architecture", "texto": "…"}],
    "base_datos": ["…"],
    "cloud": {"texto": "…", "servicios": [["Amazon ECS Fargate", "…"]]},
    "stack": [["Frontend", "…"], ["Backend", "…"]]
  },
  "vistas": {
    "contenedores": {"texto": "…", "diagrama": "…png"}, "componentes": {"texto": "…", "diagrama": "…png"},
    "informacion": {"texto": "…", "diagrama": "…png"}, "despliegue": {"texto": "…", "diagrama": "…png"},
    "desarrollo": {"texto": "…", "arbol": "carpeta/\n├── …"}
  },
  "adrs": [{"id": "ADR-001", "titulo": "…", "contexto": "…",
            "alternativas": [{"titulo": "…", "descripcion": "…", "ventajas": ["…"], "desventajas": ["…"]},
                             {"titulo": "…", "elegida": true, "descripcion": "…", "ventajas": ["…"], "desventajas": ["…"]}],
            "decision": "…", "consecuencias": ["…"]}],
  "validacion": {
    "escenarios": [{"id": "QA-01", "enfoque": "…", "sensibilidad": "…", "prueba": "…"}],
    "riesgos": [{"id": "R-01", "riesgo": "…", "impacto": "…", "mitigacion": "…", "estado": "…"}],
    "temas": ["…"]
  }
}
```

`cover.json`: `{"titulo": "…", "subtitulo": "…", "para": ["Destinatario", "…"], "por": ["Autores", "Programa"]}`.

## Flujo de trabajo

1. Revisar las herramientas.
2. Confirmar que `drivers.md`, `decisions.md`, `views.md` y `validation.md` están aprobados. Si alguno no lo está, decirlo antes de generar.
3. Convertir cada `.drawio` de `diagrams/` a PNG en `document/source/png/`, con el mismo nombre (draw.io Desktop: `drawio -x -f png -s 2 -o document/source/png/<nombre>.png diagrams/<nombre>.drawio`).
4. Pedir o tomar los datos de portada y control, y generar la portada.
5. Escribir `document/source/document.json` desde los archivos aprobados y generar el `.docx` en `document/`. Nunca borrar versiones anteriores; si hay un Word viejo con otro nombre, proponer renombrarlo como `Architecture-Document-v<su versión>.docx` (según su control del documento) en vez de borrarlo.
6. Verificar (ver abajo) y entregar con un resumen de qué contiene y qué falta.

## Verificación antes de entregar

Convertir a PDF y mirar **todas** las páginas, no una muestra:

```bash
soffice --headless --convert-to pdf document/Architecture-Document-v<version>.docx --outdir document
pdftoppm -jpeg -r 60 document/Architecture-Document-v<version>.pdf <carpeta-temporal>/pagina
```

- [ ] Portada completa, con Para y Por legibles.
- [ ] Tabla de contenido con número en cada entrada y números que coinciden con las páginas.
- [ ] 2.4 con la tabla del árbol y una ficha por escenario, en español y en orden SEI.
- [ ] Títulos separados del texto; párrafos justificados.
- [ ] Ningún título ni fila de títulos de tabla solo al pie de una página, ningún diagrama cortado ni ilegible.
- [ ] ADRs con el estilo de las fichas (franja negra con ID y título, etiquetas en negrita sobre gris) y cada alternativa con descripción, ventajas y desventajas; la elegida, marcada.
- [ ] Sección 6 con los riesgos de `validation.md`.
- [ ] **Fuente:** si Segoe UI no está instalada (normal en Mac y Linux), LibreOffice la reemplaza al numerar y la paginación puede variar en Word. Avisarlo y ofrecer regenerar si un número no coincide al abrirlo en Windows.
