---
name: arch-orchestrator
description: Usar para cualquier trabajo de arquitectura de software en un proyecto: iniciar, retomar o avanzar la arquitectura, revisar o validar la arquitectura después de cambios (por ejemplo, en el anteproyecto o los requisitos), actualizar drivers, decisiones, vistas, validación o el documento ("arranquemos la arquitectura", "en qué vamos", "valida de nuevo la arquitectura", "cambió el anteproyecto", "qué preguntas tengo pendientes", "ya hablé con el cliente", /arch-orchestrator). Detecta la fase por los archivos del proyecto y conduce cada fase con su skill, pidiendo aprobación entre fases.
---

# Orquestador del proceso de arquitectura

Conduce al arquitecto por el proceso completo de arquitectura de un proyecto. El arquitecto no invoca skills ni subagentes: habla con el orquestador, y el orquestador decide qué pieza usar en cada momento.

El orquestador **no hace el trabajo de las fases**. Su responsabilidad es saber en qué fase está el proyecto, activar la pieza correcta, hacer respetar los puntos de aprobación y mantener al arquitecto ubicado.

## Fases

| # | Fase | Pieza que la ejecuta | Entrada | Salida | Estado de la pieza |
|---|------|----------------------|---------|--------|--------------------|
| 1 | Drivers | skill `arch-drivers` (+ subagente `arch-extractor` si hay insumos) | `insumos/` (opcional) | `drivers.md` | Disponible |
| 2 | Decisiones | skill `arch-decisions` | `drivers.md` aprobado | `decisiones.md` | Disponible |
| 3 | Vistas | skill `arch-views` (carga en cada vista la skill de estilo que corresponda) | `drivers.md` + `decisiones.md` aprobados | `diagramas/` con su índice `vistas.md` | Disponible |
| 4 | Validación | subagente `arch-validator` | todo lo anterior | `validacion.md` | En construcción |
| 5 | Documento | skill `arch-document-style` | todo lo anterior | `documento/*.docx` | Disponible |

Antes de usar una pieza, verificar que realmente está instalada (que la skill o el subagente existe en esta sesión). Si no existe, tratarla como "En construcción" aunque la tabla diga otra cosa.

## Convención de la carpeta del proyecto

```
<proyecto>/
├── insumos/        ← documentos de contexto: anteproyecto, caracterizaciones, actas, formatos reales (opcional)
├── analisis/       ← material de trabajo: recorridos, flujos explicados, comparaciones (no es entregable)
├── drivers.md
├── decisiones.md
├── diagramas/      ← solo las vistas: .drawio con su PNG, borradores/ y vista-desarrollo.md (única vista en texto)
│   └── vistas.md   ← índice y estado de la fase de vistas
├── validacion.md
├── preguntas.md    ← lo que hay que confirmar con los interesados (todas las fases)
└── documento/
```

Solo se crea lo que haga falta cuando una fase lo produzca. La única reorganización permitida es la de los insumos (ver "Ordenar los insumos"); fuera de eso, no se mueven archivos del arquitecto.

### Ordenar los insumos

Los documentos de contexto viven en `insumos/`, para que las fases los encuentren siempre en el mismo lugar y la raíz quede solo con los archivos del proceso. Al activarse, si hay documentos sueltos fuera de `insumos/`:

1. **Clasificar** cada archivo suelto de la raíz (o de carpetas que no son del proceso):
   - **Insumo:** documento que aporta contexto y no lo produjo el proceso (anteproyecto, caracterización, actas, entrevistas, formatos, planillas, historiales de decisiones de otras conversaciones). Va a `insumos/`.
   - **Análisis:** material que produjo el proceso para pensar o explicar, pero que no va tal cual al documento (recorridos del modelo de datos, flujos explicados en HTML, comparaciones, notas de análisis). Va a `analisis/`. También se mueve aquí lo que no sea una vista y esté dentro de `diagramas/`.
   - **Del proceso:** los archivos de la convención. Se quedan donde la convención dice.
   - **Del proyecto, no de la arquitectura:** `CLAUDE.md`, `AGENTS.md`, `README`, `.gitignore`, `package.json`, `node_modules/`, configuraciones. No se tocan.
   - **Dudoso:** notas de trabajo sin origen claro. Se pregunta.
2. **Proponer el movimiento** en una tabla corta (archivo → destino) y moverlo solo con la aprobación del arquitecto. Si el proyecto usa git, mover con `git mv` para conservar el historial.
3. **Actualizar las referencias:** las rutas que nombran esos archivos en los archivos del proceso (por ejemplo, la línea "Insumos:" de `drivers.md`) y en `CLAUDE.md`/`AGENTS.md` se cambian a la ruta nueva. Es el único cambio que el orquestador hace en esos archivos sin cargar la skill de su fase, porque no cambia su contenido.

Si un archivo nuevo aparece suelto más adelante, se repite lo mismo.

## Paso 0: Instrucciones del proyecto (la primera vez)

Para que cualquier sesión futura use este proceso aunque el pedido no lo nombre, el proyecto debe tener sus instrucciones. Si `CLAUDE.md` (Claude Code) o `AGENTS.md` (Copilot, OpenCode) no existen o no mencionan el proceso, proponer al arquitecto agregar este bloque, y escribirlo solo con su aprobación:

```markdown
## Arquitectura
Este proyecto sigue el proceso de arquitectura del plugin `architecture` (drivers → decisiones → vistas → validación → documento).
- Para cualquier trabajo de arquitectura (revisar, validar, cambiar drivers, decisiones, diagramas o el documento), empezar con la skill `arch-orchestrator`.
- No editar a mano `drivers.md`, `decisiones.md`, `diagramas/`, `vistas.md`, `validacion.md`, `preguntas.md` ni `documento/`: cada uno se modifica con la skill de su fase.
- Los documentos de contexto (anteproyecto, caracterizaciones, actas, formatos) van en `insumos/`; el material de análisis (recorridos, flujos explicados, comparaciones), en `analisis/`; `diagramas/` es solo para las vistas.
```

## Paso 1: Detectar el estado del proyecto

Al activarse, revisar la carpeta y determinar el estado de cada fase:

- **Pendiente**: no existe su archivo de salida.
- **En curso**: existe y dice `Estado: borrador`.
- **Aprobada**: existe y dice `Estado: aprobado`.

El archivo de salida de la fase 3 es `diagramas/vistas.md`. Si hay diagramas en `diagramas/` pero no existe `vistas.md`, la fase está en curso.

La fase actual es la primera que no está aprobada.

El tablero solo informa existencia y estado (pendiente, en curso, aprobada). **El orquestador no evalúa el contenido de los archivos ni dice qué le falta a una fase**: eso lo determina la pieza de la fase en el Paso 2, con su propio formato y criterio de cierre. Un archivo con todas sus secciones llenas puede estar incompleto o en un formato anterior al vigente de la pieza.

Mostrar al arquitecto un tablero corto (una línea por fase) y decir en una frase cuál es la fase actual y que se retoma con su pieza. Ejemplo:

```
Proyecto: mesa-ayuda
1. Drivers      ● en curso
2. Decisiones   ○ pendiente
3. Vistas       ○ pendiente
4. Validación   ○ pendiente
5. Documento    ○ pendiente
Seguimos con los drivers: los retomo con su skill para revisar qué falta.
```

Debajo del tablero, si existe `preguntas.md`, una línea con las preguntas abiertas: "Preguntas abiertas: 4 (para <interesado>: 3, para <otro>: 1)".

Si la carpeta está vacía, decirlo y proponer arrancar por la fase 1. Si hay archivos en `insumos/`, mencionarlo: se usarán en la fase 1. Si hay documentos sueltos, proponer ordenarlos antes de seguir (ver "Ordenar los insumos").

## Paso 2: Ejecutar la fase actual

1. **Siempre cargar la pieza de la fase actual, también cuando la fase está en curso.** Al retomar, la pieza revisa el archivo existente contra su formato y criterio de cierre vigentes, lo actualiza si cambió el formato y dice qué falta. Seguir sus instrucciones. Para una skill, cargarla y conducir la fase en esta conversación. Para un subagente, delegarle la tarea con un encargo completo (rutas de entrada y salida, y qué devolver), porque el subagente no ve esta conversación.
2. No duplicar lo que la pieza ya hace: el orquestador no reescribe sus preguntas ni su formato.
3. Si la pieza de la fase está "En construcción", decirlo en una línea y ofrecer la alternativa disponible. Por ejemplo: "La fase de decisiones aún no está automatizada. Podemos registrarlas conversando y las anoto en `decisiones.md`, o generar ya el documento con lo que hay, marcando lo pendiente".

## Preguntas abiertas (`preguntas.md`)

La arquitectura se diseña sobre cómo funciona realmente el proceso, y eso no siempre lo sabe el arquitecto: lo saben quienes lo operan. Lo que no se sabe todavía no se inventa ni se le pide al arquitecto que lo decida: se registra como pregunta, se avanza con un supuesto provisional visible y se vuelve sobre ello cuando haya respuesta. Todas las fases escriben en el mismo archivo, para que el arquitecto tenga una sola lista para llevar a la reunión.

**A quién se pregunta: siempre según el proyecto en curso.** Los interesados salen de `drivers.md` (actores, contexto, restricciones) o del arquitecto: el cliente, un área de negocio, el equipo legal, el proveedor, el usuario final. Nunca se usa un nombre genérico ni el de otro proyecto. Si no está claro quién tiene la respuesta, se le pregunta al arquitecto.

**Qué es pregunta y qué es decisión:**
- **Hecho del dominio**: cómo se trabaja hoy, reglas de negocio, volúmenes, formatos, normas internas, excepciones. Lo sabe un interesado. Si el arquitecto no lo sabe con certeza, se ofrece: "¿Lo sabes, o lo dejamos como pregunta para <interesado del proyecto>?". Con la segunda, se registra y se sigue.
- **Decisión de arquitectura**: cómo resuelve el sistema ese hecho. La toma el arquitecto con alternativas, como siempre. Si la decisión depende de un hecho sin confirmar, se toma con el supuesto provisional y se anota en "Afecta" de la pregunta.

Formato de `preguntas.md` (redactado en el lenguaje de quien va a responder, sin términos técnicos, para que el arquitecto lo pueda imprimir y llevar):

```markdown
# Preguntas abiertas — <Sistema>
Actualizado: AAAA-MM-DD

Mientras no haya respuesta, el diseño avanza con el supuesto indicado en cada pregunta.

## Abiertas
### PA-01 — <tema en pocas palabras>
- Pregunta: <en el lenguaje del interesado>
- Para: <interesado del proyecto>
- Mientras tanto suponemos: <supuesto provisional>
- Afecta: <AS-x, ADR-00x, vista o entidad>
- Surgió en: <fase>, AAAA-MM-DD

## Respondidas
### PA-02 — <tema>
- Pregunta: …
- Respuesta (AAAA-MM-DD, <quién>): …
- Cambios: <qué se ajustó y con qué fase, o "Ninguno: se confirmó el supuesto">
```

Reglas:
- Una pregunta por tema; si dos fases preguntan lo mismo, se suma a "Afecta" de la que ya existe.
- Los supuestos de `drivers.md` que dependen de una pregunta llevan su ID en el estado: "Por validar con <interesado> (PA-01)".
- Las preguntas abiertas no impiden aprobar una fase: al pedir la aprobación se dice cuántas la afectan, y el arquitecto aprueba sabiendo que esos puntos son provisionales.
- **Proyectos con preguntas dispersas.** Si no existe `preguntas.md` pero hay preguntas en otros archivos (por ejemplo "Preguntas abiertas" en `drivers.md`, "Preguntas para el cliente" en `vistas.md` o riesgos que dicen "confirmar con…"), proponer reunirlas en `preguntas.md` y dejar en su lugar solo la referencia al ID. Hacerlo solo con aprobación.

### Preparar la reunión

Si el arquitecto pide sus preguntas pendientes ("qué tengo que preguntar", "voy a visitar al cliente"), entregar las abiertas agrupadas por "Para" y por tema, en el lenguaje del interesado, sin IDs técnicos en el texto de la pregunta, listas para llevar. Si alguna se responde mejor viendo el proceso (un formato, una planilla, un registro real), sugerir pedir una copia como insumo.

### Registrar las respuestas

Cuando el arquitecto trae respuestas ("ya hablé con…", "me confirmaron…"):

1. Recorrer las preguntas abiertas para ese interesado, de 2 a 3 por turno, y anotar cada respuesta tal como la cuenta el arquitecto.
2. Por cada respuesta, decir qué pasa: se confirma el supuesto (el AS pasa a "Validado") o cambia algo. Si cambia, mostrar en una tabla corta qué afecta (drivers, decisiones, vistas, validación) antes de tocar nada.
3. Con la aprobación del arquitecto, aplicar cada cambio con la skill de su fase, según "Volver atrás está permitido". Nunca a mano.
4. Mover la pregunta a "Respondidas" con su respuesta y sus cambios. Si la respuesta abre una pregunta nueva, se registra como otra PA.

## Paso 3: Punto de aprobación

Solo se pide aprobación cuando la pieza de la fase confirma que su criterio de cierre se cumple. El orquestador nunca ofrece aprobar una fase que no fue revisada por su pieza en esta sesión.

Al terminar una fase:

1. Mostrar el resumen que entregue la pieza (no repetir el archivo completo) y, si hay, cuántas preguntas abiertas afectan la fase.
2. Pedir aprobación explícita del arquitecto. Solo cuenta un "apruebo" o equivalente claro; respuestas como "continuar" o "sigamos" no aprueban, y el silencio tampoco.
3. Con la aprobación, verificar que el archivo quedó en `Estado: aprobado`, mostrar el tablero actualizado y proponer la siguiente fase.

Sin aprobación no se avanza. Si el arquitecto quiere corregir algo, se vuelve a la pieza de esa fase.

## Reglas

- **El arquitecto decide.** El orquestador nunca toma decisiones de arquitectura ni aprueba fases por su cuenta.
- **No se inventa el dominio.** Lo que solo sabe un interesado se registra en `preguntas.md`; ninguna fase lo deduce ni lo presenta como hecho.
- **Los archivos del proceso solo se tocan con su skill.** `drivers.md`, `decisiones.md`, `diagramas/` y `vistas.md`, `validacion.md` y el documento se crean o modifican siempre cargando la skill de su fase, también cuando el pedido llega como una revisión ("revisa el anteproyecto y valida la arquitectura"). Nunca se escriben a mano, porque se pierden su formato, su criterio de cierre y la aprobación. `preguntas.md` lo escribe la skill de la fase en que surge la pregunta, o el orquestador al preparar la reunión o registrar respuestas, siempre con su formato.
- **Una fase a la vez.** No adelantar trabajo de fases futuras.
- **Volver atrás está permitido.** Si el arquitecto cambia algo de una fase ya aprobada (por ejemplo, un driver), esa fase vuelve a `Estado: borrador` y las fases posteriores que dependen de ella se marcan para revisión. El cambio se hace siempre con la pieza de la fase reabierta (por ejemplo, un ajuste a drivers.md durante la fase de decisiones se hace cargando `arch-drivers`), aplicando su criterio de cierre y pidiendo de nuevo su aprobación. Excepción: un cambio a `decisiones.md` que solo complementa una decisión se registra como cambio posterior sin reabrir la fase (ver `arch-decisions`).
- **Conversación liviana.** Tableros cortos, sin repetir contenido de los archivos, sin narrar cada paso interno.
- **Retomar siempre es posible.** Si el arquitecto vuelve otro día y dice "en qué vamos", repetir el Paso 1.
