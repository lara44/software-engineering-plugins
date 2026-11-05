# Proyectos de la versión anterior

Referencia de `start`. Se lee solo cuando el proyecto tiene archivos de la versión 1.x o nombres en español.

Un proyecto de la versión 1.x tiene `decisions.md` o `diagrams/views.md` y no tiene `iterations/`.

**Regla:** el proceso ADD empieza siempre desde la iteración 1. El diseño anterior se hizo sin ADD y sirve como **insumo**, no como decisiones tomadas: cada decisión se vuelve a tomar en su iteración, con el arquitecto. Una decisión anterior se puede proponer como alternativa solo si atiende un driver vigente de la iteración; si depende de algo que está en "Fuera de alcance" o de un supuesto que se quitó, no se propone. Al proponerla se dice que viene del diseño anterior, y el arquitecto elige entre al menos dos alternativas. Tampoco se copian iteraciones de registros hechos fuera del plugin (un Word, un PDF): si existen, son insumos como cualquier otro documento. La única continuidad que el plugin respeta son sus propias iteraciones: un proyecto que ya tiene `iterations/` no se migra, sigue con iteraciones o rondas nuevas.

Mientras no haya iteraciones cerradas con el plugin, no hay nada cerrado que proteger: empezar desde la iteración 1 no borra historia del proceso, y lo anterior sigue en git y en los documentos ya entregados.

Proponer estos pasos en una sola respuesta y hacerlos solo con aprobación (con `git mv` si el proyecto usa git):

1. **Archivar el diseño anterior como insumo.** `decisions.md`, `diagrams/views.md`, `validation.md` y las vistas de `diagrams/` (con sus PNG) se mueven a `inputs/previous-design/`. En `diagrams/` queda solo el diagrama de contexto, que es parte de la sección 1. Si hay un registro de iteraciones hecho fuera del plugin, también va a `inputs/previous-design/`.
2. **Convertir `drivers.md`** al formato vigente cargando `drivers` (secciones 1 y 2 con una línea de estado cada una, preocupaciones CRN, caso de uso asociado en cada escenario). La conversión se escribe directamente en `drivers.md` (nunca en una copia temporal) y se resume en la respuesta; las secciones quedan en `borrador` y lo nuevo marcado `[Propuesta]` hasta que el arquitecto lo apruebe. Es el momento de revisar si algo de los requisitos depende de lo que está "Fuera de alcance" o de un supuesto que no es driver (actores, casos de uso o supuestos que solo existen para ello) y proponer quitarlo; lo que se quite se registra en "Cambios después de la aprobación".
3. **No crear ADR desde los anteriores.** `adr/` empieza vacía; los ADR nacen en las iteraciones, numerados desde ADR-001. Las decisiones anteriores no entran en bloque como alternativas: el diseño anterior es un insumo para consultar, y cada una se propone solo con la regla de arriba.
4. **Ronda 1 de un sistema nuevo** (si el software no se ha construido): el paso 1 toma los drivers y el tablero empieza con todos en "No abordado". Solo si hay software construido que se modifica es un sistema existente (CK24 §4.3.3); aun así, el diseño anterior en documentos sigue siendo insumo.
5. **La validación** se hace de nuevo en la sección 4, sobre el diseño nuevo.
6. **Actualizar el bloque** de `CLAUDE.md`/`AGENTS.md` ("Al empezar: instrucciones del proyecto" en SKILL.md).
7. **Numerar los documentos** a partir del siguiente número mayor libre, si `document/` ya tiene versiones (ver abajo).

**Artefactos del diseño anterior que tienen su propio lugar** (código, contratos de API, una demo): no se mueven ni se copian. Se registran en la línea "Insumos" de `drivers.md` y en el bloque de `CLAUDE.md`/`AGENTS.md` como insumo del diseño anterior: no cuentan como decisiones tomadas y se revisan en las iteraciones con la misma regla de alternativas.

**Documentos ya generados.** Los Word y PDF del diseño anterior se quedan en `document/` sin cambios. Para que las versiones nuevas no choquen con ellas, la ronda 1 toma como número mayor el siguiente libre (si la última fue 2.4, la ronda 1 se numera 3: 3.0, 3.1…), y cada ronda nueva suma uno. Se anota en `status.md` con la línea "Número mayor de la ronda 1: 3". El control del documento conserva las filas anteriores y la primera fila nueva dice "Migración a ADD 3.0: el diseño se rehace por iteraciones".

`diagrams/drafts/` se revisa con el arquitecto (lo que sirva va a `analysis/` o a `inputs/previous-design/`, el resto se descarta con su aprobación).

### Nombres en inglés

Los nombres de carpetas y archivos del proceso van en inglés; su contenido sigue en el idioma del proyecto. Si el proyecto usa nombres en español de versiones anteriores, proponer renombrarlos antes de migrar, con la aprobación del arquitecto y con `git mv` si el proyecto usa git:

| Anterior | Actual |
|---|---|
| `insumos/`, `analisis/` | `inputs/`, `analysis/` |
| `diagramas/` | `diagrams/` (sus PNG en `diagrams/images/`) |
| `diagramas/borradores/`, `diagrams/drafts/` | Se revisa con el arquitecto (punto 3) |
| `documento/` | `document/` |
| `documento/png/` (imágenes del generador anterior) | No se migra: los Word ya traen sus imágenes. Se propone borrarla, con aprobación del arquitecto (queda en el historial de git) |
| `documento/fuentes/` y los JSON y PNG de portada sueltos en `documento/` | `document/source/` |
| `Documento-Arquitectura-v<versión>.docx` y su PDF | `document/previous-versions/v<versión>/Architecture-Document-v<versión>.docx` y su PDF (con el nombre nuevo) |
| `decisiones.md`, `validacion.md`, `preguntas.md` | `decisions.md`, `validation.md`, `questions.md` |
| `vistas.md`, `vista-desarrollo.md` | `views.md`, `development-view.md` |
| `c4-contexto`, `c4-contenedores`, `c4-componentes` | `c4-context`, `c4-containers`, `c4-components` |
| `estilo-arquitectonico`, `modelo-datos`, `despliegue-<nube>` | `architectural-style`, `data-model`, `deployment-<cloud>` |
| `recorrido-<caso>` | `walkthrough-<case>` |
| `documento.json`, `portada.json`, `portada.png` | `document.json`, `cover.json`, `cover.png` |

- Después de renombrar, actualizar las rutas que los nombran: enlaces entre archivos del proceso, `CLAUDE.md`/`AGENTS.md` y las rutas de imágenes de `document.json` (sus claves internas no cambian).
- Los Word ya generados se renombran con su misma versión; su contenido no cambia.
- Si el arquitecto prefiere no renombrar, las secciones trabajan con los nombres que ya tiene el proyecto.
