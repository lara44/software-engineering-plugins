---
name: "arch-document-style"
description: "Usar cuando se pida crear o actualizar un documento de arquitectura de software como archivo Word (.docx) — aplica su estructura, secciones, portada, control del documento, tabla de contenido y estilo de tablas estándar."
---

# Documento de arquitectura (Word)

Genera el documento de arquitectura en Word con una estructura y un estilo fijos, validados sobre documentos reales. Es la fase 5 del proceso: el contenido sale de los archivos aprobados (`drivers.md`, `decisiones.md`, `diagramas/`, `validacion.md`); esta skill no decide nada nuevo.

Si piden otro formato (PDF, Google Docs) o un documento distinto (un ADR suelto, un caso narrativo), esta skill no aplica.

## Generadores

En la carpeta `scripts/` de esta skill. Se ejecutan tal cual; no se leen, no se copian y no se reescriben:

```bash
node <carpeta-de-esta-skill>/scripts/make_cover.js portada.json portada.png
node <carpeta-de-esta-skill>/scripts/gen_doc.js documento.json documento/
```

- `make_cover.js`: portada como imagen a sangre completa (degradado oscuro, título, subtítulo, regla de color y bloques "Para" y "Por"). Requiere Playwright con Chromium.
- `gen_doc.js`: todo el documento a partir de un JSON de contenido. Ya implementa el estilo completo: fuente Segoe UI, encabezados negros (los de nivel 1 centrados), tablas limpias sin bordes con sombreado alterno, fichas de escenario, tablas de ADR, tabla de contenido estática numerada en dos pasadas e imágenes con su tamaño real. Requiere la librería `docx` (`npm install docx`), LibreOffice (`soffice`) y poppler (`pdftotext`).

- **Un archivo por versión:** `gen_doc.js` nombra el Word con la versión de la última fila de `control` (`documento/Documento-Arquitectura-v2.0.docx`). Las versiones anteriores no se borran ni se sobrescriben: son el historial que se entregó. Regenerar la misma versión mientras está en revisión la reemplaza; una vez entregada, cualquier cambio lleva una fila nueva en `control` y, con ella, un archivo nuevo. El PDF de verificación lleva el mismo nombre.

**No se modifican por proyecto.** Si el arquitecto pide un ajuste de estilo, se propone como cambio a los scripts del plugin.

## Herramientas (revisar al empezar)

Comprobar `node`, `docx`, Playwright, `soffice` y `pdftotext`. Si falta algo, pedir permiso para instalarlo en ese momento, no a mitad del documento:
- Mac: `brew install --cask libreoffice` y `brew install poppler`;
- en la carpeta del proyecto: `npm install docx playwright && npx playwright install chromium`.

Antes de instalar, buscar si ya están: en Mac, LibreOffice suele estar en `/Applications/LibreOffice.app/Contents/MacOS/soffice` aunque `soffice` no esté en el PATH, y poppler en `/opt/homebrew/bin`. `gen_doc.js` los busca solo en esas rutas. Sin `soffice` o `pdftotext`, el documento se genera igual, pero la tabla de contenido sale sin números de página: avisarlo.

## Estructura del documento y de dónde sale cada parte

| Sección | Contenido | Fuente |
|---|---|---|
| Portada | Título, subtítulo, Para, Por | Preguntar al arquitecto o tomarlo de `insumos/` (p. ej., un anteproyecto) |
| Control del Documento | Versión, fecha, autores, comentarios. Si hubo "Cambios posteriores a la aprobación", cada uno es una fila. Al actualizar un documento ya entregado, se agrega una fila con la versión nueva (preguntar al arquitecto el número) | Arquitecto y `decisiones.md` |
| Tabla de Contenido | Automática | — |
| Introducción | Un párrafo: qué sistema, para quién, qué cubre | `drivers.md` |
| 1. Contexto | 1.1 Situación actual, 1.2 Objetivo, 1.3 Vista de contexto C4 | `drivers.md` y `diagramas/` |
| 2. Drivers | 2.1 Funcionalidades, 2.2 Restricciones, 2.3 Supuestos, 2.4 Atributos de calidad | `drivers.md` |
| 3. Decisiones | 3.1 Estilo (con su diagrama), 3.2 Patrones (uno por subsección), Base de datos, Servicios cloud, Stack | `decisiones.md` y `diagramas/` |
| 4. Definición | 4.1 Vista funcional (contenedores y componentes), Información (modelo de datos), Despliegue, Desarrollo (árbol de carpetas) | `diagramas/` |
| 5. ADRs | Solo decisiones con alternativas reales | `decisiones.md` |
| 6. Validación | 6.1 Análisis por escenario, 6.2 Riesgos, 6.3 Temas de riesgo | `validacion.md` |

Reglas de contenido:
- **2.4 Atributos de calidad:** el script dibuja primero la tabla del árbol de utilidad (atributo → refinamiento → escenario, con prioridad de negocio y dificultad) y después una ficha por escenario, con los campos en orden SEI: fuente, estímulo, ambiente, artefacto, respuesta y medida. Copiar los escenarios de `drivers.md` tal cual, con su refinamiento y su prioridad.
- **3.1:** el título lleva dos puntos ("Estilo Arquitectónico: Monolito Modular") y el texto habla solo de la organización de alto nivel.
- **3.2:** un patrón por subsección, nunca agrupados (Clean Architecture y DDD son dos).
- **Sección 3 sin ADRs:** las decisiones no citan ADRs; los ADRs son la sección 5.
- **ADRs:** mínimo 2 alternativas, con la elegida marcada. Si una decisión no tuvo alternativa real, no es ADR: va en la sección 3.
- **Secciones opcionales:** si el sistema no tiene nube, componentes o validación, se omiten esas claves del JSON y el script ajusta la numeración.
- **No inventar.** Todo sale de los archivos aprobados. Si falta algo (por ejemplo, la vista de desarrollo), se pide o se marca como pendiente; no se crea en esta fase.

## Formato de documento.json

Las rutas de imágenes son relativas al JSON. Los textos aceptan un string o una lista de párrafos.

```json
{
  "portada": "portada.png",
  "control": [["1.0", "2026-10-11", "Autor", "Versión inicial."]],
  "introduccion": "…",
  "contexto": {"situacion": ["…"], "objetivo": ["…"], "diagrama": "diagramas/c4-contexto.png"},
  "drivers": {
    "funcionalidades": ["UC-01 …"], "restricciones": ["CON-1: …"], "supuestos": ["AS-1: …"],
    "escenarios": [{"id": "QA-01", "nombre": "…", "atributo": "Trazabilidad", "refinamiento": "Procedencia", "negocio": "A", "dificultad": "A",
                    "fuente": "…", "estimulo": "…", "ambiente": "…", "artefacto": "…", "respuesta": "…", "medida": "…"}]
  },
  "decisiones": {
    "estilo": {"nombre": "Monolito Modular", "texto": ["…"], "diagrama": "diagramas/estilo.png"},
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

`portada.json`: `{"titulo": "…", "subtitulo": "…", "para": ["Destinatario", "…"], "por": ["Autores", "Programa"]}`.

## Flujo de trabajo

1. Revisar las herramientas.
2. Confirmar que `drivers.md`, `decisiones.md`, `vistas.md` y `validacion.md` están aprobados. Si alguno no lo está, decirlo antes de generar.
3. Convertir cada `.drawio` de `diagramas/` a PNG (draw.io Desktop: `drawio -x -f png -s 2 -o salida.png entrada.drawio`).
4. Pedir o tomar los datos de portada y control, y generar la portada.
5. Escribir `documento.json` desde los archivos aprobados y generar el `.docx` en `documento/`. Nunca borrar versiones anteriores; si hay un Word viejo sin versión en el nombre, proponer renombrarlo con la suya (según su control del documento) en vez de borrarlo.
6. Verificar (ver abajo) y entregar con un resumen de qué contiene y qué falta.

## Verificación antes de entregar

Convertir a PDF y mirar **todas** las páginas, no una muestra:

```bash
soffice --headless --convert-to pdf documento/Documento-Arquitectura-v<version>.docx --outdir documento
pdftoppm -jpeg -r 60 documento/Documento-Arquitectura-v<version>.pdf pagina
```

- [ ] Portada completa, con Para y Por legibles.
- [ ] Tabla de contenido con número en cada entrada y números que coinciden con las páginas.
- [ ] 2.4 con la tabla del árbol y una ficha por escenario, en español y en orden SEI.
- [ ] Ningún título solo al pie de una página, ningún diagrama cortado ni ilegible.
- [ ] ADRs con etiquetas moradas, sombreado alterno, regla negra arriba y abajo, y alternativas con ventajas y desventajas.
- [ ] Sección 6 con los riesgos de `validacion.md`.
- [ ] **Fuente:** si Segoe UI no está instalada (normal en Mac y Linux), LibreOffice la reemplaza al numerar y la paginación puede variar en Word. Avisarlo y ofrecer regenerar si un número no coincide al abrirlo en Windows.
