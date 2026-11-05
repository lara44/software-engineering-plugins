---
name: start
description: Usar para cualquier trabajo de arquitectura de software en un proyecto, que se conduce con el método ADD 3.0 (Attribute-Driven Design): iniciar, retomar o avanzar la arquitectura, abrir o cerrar una iteración o una ronda, revisar la arquitectura después de cambios (por ejemplo, en el anteproyecto, los requisitos o tras una visita al cliente), pedir o ajustar un diagrama, generar el documento de arquitectura o el registro de diseño ADD ("arranquemos la arquitectura", "en qué vamos", "sigamos con la iteración", "genera el documento", "cambió el anteproyecto", "qué preguntas tengo pendientes", "ya hablé con el cliente", /add:start). Sigue las secciones del caso FCAPS (caso de negocio, requisitos del sistema, proceso de diseño). Detecta la sección, la iteración y el paso por los archivos del proyecto y conduce cada uno con su skill, pidiendo aprobación en cada cierre.
---

# Orquestador del proceso de arquitectura (ADD 3.0)

Conduce al arquitecto por el proceso de arquitectura de un proyecto con el método **ADD 3.0 (Attribute-Driven Design)** de Cervantes y Kazman (2024, cap. 4). El arquitecto no invoca skills ni subagentes: habla con el orquestador, y el orquestador decide qué pieza usar en cada momento.

El orquestador **no hace el trabajo de las secciones**. Su responsabilidad es saber en qué sección, iteración y paso (y ronda, si hay más de una) está el proyecto, activar la pieza correcta, hacer respetar el orden de ADD y los puntos de aprobación, y mantener al arquitecto ubicado.

## Principios

1. **El modelo propone; el arquitecto decide.** Ninguna decisión de diseño, aprobación o cierre ocurre sin el arquitecto. El diseño que propone un modelo puede satisfacer los drivers solo en parte, y la supervisión del arquitecto es indispensable (Cervantes, Kazman y Cai, 2025).
2. **Las skills ejecutan; el orquestador gobierna.** Cada skill hace su trabajo dentro de su contrato; el orquestador decide cuál actúa, en qué estado y con qué condición (ver "Máquina de estados" y "Contratos").
3. **Los archivos demuestran el estado; la conversación no es la fuente de verdad.** Lo que no está en los archivos del proyecto no está decidido ni aprobado. Si la conversación y los archivos no coinciden, valen los archivos.

## El método

El proceso sigue la estructura del caso de estudio FCAPS de Cervantes y Kazman (2016, cap. 4): primero el **caso de negocio**, luego los **requisitos del sistema** y después el **proceso de diseño**, que es donde se aplican los pasos de ADD en iteraciones.

Dentro del proceso de diseño, cada iteración recorre los mismos pasos (Cervantes y Kazman, 2024, §4.2):

| Paso | Qué se hace |
|------|-------------|
| 1 | Revisar las entradas y elegir los drivers (una vez, antes de las iteraciones) |
| 2 | Establecer el objetivo de la iteración |
| 3 | Elegir los elementos a refinar |
| 4 | Elegir los conceptos de diseño |
| 5 | Instanciar elementos, asignar responsabilidades y definir interfaces |
| 6 | Bocetar vistas y registrar las decisiones |
| 7 | Analizar el diseño y revisar el objetivo de la iteración |

- El diseño termina cuando todos los drivers de prioridad alta están completamente abordados (CK24 §4.8).
- Una iteración cerrada **no se reabre**: revisar una de sus decisiones es una iteración nueva.
- **Rondas.** Si después de terminar el diseño llega información nueva (una visita, una revisión, un cambio de requisitos), se abre una **ronda nueva**: un nuevo paso 1 que toma la arquitectura existente como entrada, y sus iteraciones (CK24 §4.2.1). Mientras el diseño tenga una sola ronda, el plugin no las menciona: la sección 3 es solo "paso 1 e iteraciones". Desde la segunda ronda, la sección 3 se organiza por rondas.

Siempre que el orquestador o una pieza nombre un paso, lo nombra con su número y su nombre de ADD. En todo el plugin, **"paso" significa siempre un paso de ADD**; las etapas internas del orquestador no se numeran.

## Secciones del proceso

| Sección | Contenido | Pieza que la ejecuta | Salida | Estado de la pieza |
|---------|-----------|----------------------|--------|--------------------|
| 1. Caso de negocio | Problema, contexto, objetivos e interesados; diagrama de contexto | skill `drivers` (+ subagente `extractor`, si está instalado y hay insumos) | `drivers.md`, sección 1, y `diagrams/c4-context.drawio` | Disponible |
| 2. Requisitos del sistema | Casos de uso, escenarios de calidad con árbol de utilidad, restricciones, supuestos y preocupaciones | skill `drivers` | `drivers.md`, sección 2 | Disponible |
| 3. Proceso de diseño | 3.1 Paso 1: revisar las entradas, propósito del diseño, drivers y hoja de ruta; 3.2 en adelante: una subsección por iteración (pasos 2 a 7) | skill `design` (carga las skills de estilo en los pasos 5 y 6) | `iterations/status.md`, `iterations/round-R/step-1.md`, `kanban.md`, `it-N/`, `adr/`, `diagrams/` | Disponible |
| 4. Análisis | Revisión del diseño contra los escenarios | subagente `analysis` | `analysis/`, `validation.md` | En construcción |
| 5. Documentos | Documento de arquitectura (diseño vigente) y registro de diseño ADD (iteraciones) | skill `document` y luego skill `record` | `document/Architecture-Document-vX.docx` y `document/ADD-Design-Record-vX.docx` | Disponible |

Las secciones 1 y 2 viven en el mismo archivo, `drivers.md`, y se aprueban por separado. La sección 5 no espera al final: se puede ejecutar al cierre de cualquier iteración (ver "Generar los documentos").

Antes de usar una pieza, verificar que realmente está instalada (que la skill o el subagente existe en esta sesión). Si no existe, tratarla como "En construcción" aunque la tabla diga otra cosa.

## Estado del proceso (`iterations/status.md`)

Es la única fuente de verdad sobre dónde va el proceso de diseño. Lo crea `design` al aprobar el paso 1; desde ahí lo actualizan el orquestador (sección, ronda, documento) y `design` (iteración y paso). Antes de que exista, el estado de las secciones 1 y 2 se lee de `drivers.md`.

```markdown
# Estado del proceso de arquitectura
Método: ADD 3.0 (Cervantes y Kazman, 2024)
Sección: 3 — Proceso de diseño
Ronda: 1 — Diseño inicial                ← desde la ronda 2: qué la abrió
Iteración en curso: 5 — <objetivo>        ← "ninguna" entre iteraciones
Paso en curso: 4 — Elegir los conceptos de diseño
Iteraciones cerradas: 4
Último documento generado: v1.4 (AAAA-MM-DD)
Actualizado: AAAA-MM-DD
```

### Bloque de estado

Mientras se trabaja en la arquitectura, **cada respuesta empieza con el bloque de estado**, dentro de un bloque de código para que la terminal respete la alineación. Va antes de cualquier otro texto, también cuando la respuesta empieza con un aviso o una corrección.

Muestra las cinco secciones. La sección en curso lleva `[>]` y, si es el proceso de diseño, debajo se despliegan los 7 pasos de ADD con más sangría:

```
ADD 3.0 · Proceso de diseño
  [✔] 1. Caso de negocio
  [✔] 2. Requisitos del sistema
  [>] 3. Proceso de diseño · iteración 5 de 6: Soporte a la decisión
        [✔] Paso 1: Revisar entradas
        [✔] Paso 2: Objetivo de la iteración
        [✔] Paso 3: Elegir elementos
        [>] Paso 4: Elegir conceptos de diseño · en curso
        [ ] Paso 5: Instanciar elementos, asignar responsabilidades e interfaces
        [ ] Paso 6: Bocetar vistas y registrar decisiones
        [ ] Paso 7: Analizar el diseño y revisar el objetivo
  [ ] 4. Análisis
  [ ] 5. Documentos
```

Fuera del proceso de diseño, la sección 3 va en una sola línea, sin pasos:

```
ADD 3.0 · Requisitos del sistema
  [✔] 1. Caso de negocio
  [>] 2. Requisitos del sistema · en curso
  [ ] 3. Proceso de diseño
  [ ] 4. Análisis
  [ ] 5. Documentos
```

- `[✔]` hecho, `[>]` en curso, `[ ]` pendiente. La línea más profunda en curso termina en ` · en curso`. Los nombres de las secciones y de los pasos son siempre los de arriba.
- La primera línea dice `ADD 3.0 · <nombre de la sección en curso>`.
- **Paso 1 en curso** (antes de la primera iteración de la ronda): la línea de la sección 3 no nombra iteración; el paso 1 lleva `[>]` y los demás `[ ]`.
- **Entre iteraciones:** la línea de la sección 3 dice `iteración N de M cerrada: <objetivo>` y los 7 pasos van con `[✔]`.
- **Desde la segunda ronda:** la línea de la sección 3 agrega `ronda R · ` antes de la iteración. Con una sola ronda no se nombra.
- **Sección 5 (documentos):** puede estar en curso con el diseño abierto; en ese caso la sección 3 queda `[>]` en una línea, sin pasos, y la 5 lleva ` · en curso`.

**Cuándo se muestra completo:** al retomar ("en qué vamos") y en la primera respuesta de cada paso o sección. En las demás respuestas del mismo paso o sección, solo la primera línea y la rama en curso:

```
ADD 3.0 · Proceso de diseño
  [>] 3. Proceso de diseño · iteración 5 de 6: Soporte a la decisión
        [>] Paso 4: Elegir conceptos de diseño · en curso
```

Sin caracteres de árbol (├──, └──), columnas, colores ni íconos: cada nivel va con sangría de espacios y el formato es exactamente este.

## Máquina de estados

Cada estado se demuestra con un archivo. El orquestador solo reconoce un estado si el archivo lo muestra, y solo la pieza indicada puede cambiarlo.

| Elemento | Estados | Dónde se demuestra | Transición | Quién | Condición |
|----------|---------|--------------------|------------|-------|-----------|
| Sección 1 | pendiente → borrador → aprobado | línea "Estado sección 1" de `drivers.md` | borrador → aprobado | `drivers` | criterio de cierre cumplido y aprobación explícita |
| Sección 2 | pendiente → borrador → aprobado | línea "Estado sección 2" de `drivers.md` | pendiente → borrador | `drivers` | sección 1 aprobada |
| | | | borrador → aprobado | `drivers` | criterio de cierre cumplido y aprobación explícita |
| Sección aprobada que cambia | aprobado → borrador | la misma línea y la tabla "Cambios después de la aprobación" | aprobado → borrador | `drivers` | cambio aprobado por el arquitecto |
| Paso 1 de una ronda | borrador → aprobado | `status: borrador \| aprobado` en `step-1.md` | borrador → aprobado | `design` | secciones 1 y 2 aprobadas, criterio de cierre del paso 1 y aprobación explícita |
| Iteración | abierta (paso 2…7) → cerrada | `status` y `step` en el encabezado de `it-N.md` | abrir | `design` | paso 1 aprobado y ninguna otra iteración abierta |
| | | | avanzar de paso | `design` | lo que exige el paso actual está escrito en `it-N.md` |
| | | | abierta → cerrada | `design` | paso 7 completo y aprobación explícita; en la misma operación copia los diagramas a `diagrams/` y actualiza el tablero |
| | | | abierta → descartada | `design` | el arquitecto la descarta; se borra su carpeta y nada más cambia |
| Diseño de la ronda | en curso → terminado | `kanban.md`: todos los drivers de prioridad alta completos | en curso → terminado | `design` al cerrar la iteración que lo logra | — |
| Ronda nueva | — → paso 1 en borrador | carpeta `round-R+1/` con su `step-1.md` | abrir | `design` | ronda anterior terminada y el arquitecto la pide |
| Sección 4 | pendiente → aprobado | `Estado:` de `validation.md` | pendiente → aprobado | `analysis` | diseño terminado y aprobación explícita |
| Documentos | — | archivos `vX` en `document/` y "Último documento generado" en `status.md` | generar | `document` y `record` | no depende de estados; usa solo lo cerrado y aprobado |

Lo cerrado no tiene transiciones de salida: una iteración cerrada, sus fotos y un ADR reemplazado no vuelven a ningún estado anterior.

## Contratos de las skills

| Pieza | Lee | Escribe | No toca nunca | Devuelve al orquestador |
|-------|-----|---------|---------------|-------------------------|
| `drivers` | `inputs/`, `drivers.md`, `questions.md` | `drivers.md`, `diagrams/c4-context.drawio` y su PNG, `questions.md` | `iterations/`, `adr/`, otras vistas, `document/` | estado de cada sección y resumen de cierre (máx. 5 líneas) |
| `design` | `drivers.md`, `iterations/`, `adr/`, `diagrams/`, `questions.md` | `iterations/` (incluido `status.md`), `adr/`, `diagrams/` (solo al cerrar una iteración), `analysis/walkthrough-*` (paso 7), `questions.md` | `drivers.md`, iteraciones cerradas y sus fotos, `document/` | ronda, iteración, paso, drivers que avanzaron y resumen de cierre (máx. 5 líneas) |
| `analysis` | todo lo anterior | `analysis/`, `validation.md`, `questions.md` | los demás archivos del proceso | hallazgos y estado |
| `document` | `drivers.md`, iteraciones cerradas (decisiones vigentes) y `kanban.md`, `adr/`, `diagrams/`, `validation.md` | `document/Architecture-Document-*`, `document/source/` (salvo `record.json`), "Último documento generado" de `status.md` | todo lo demás | versión y ruta del Word |
| `record` | `drivers.md`, `step-1.md` aprobados, iteraciones cerradas y sus fotos, `adr/`, `document/source/document.json` | `document/ADD-Design-Record-*`, `document/source/record.json` y `record-cover.*` | todo lo demás | versión y ruta del Word |
| Skills de estilo (C4, AWS, modelo de datos) | la especificación que reciben | el `.drawio` y el PNG en la ruta que se les indica | todo lo demás | ruta del archivo y verificación visual |

El orquestador escribe solo `status.md` (sección, ronda, documento), el bloque de `CLAUDE.md`/`AGENTS.md` con aprobación, los movimientos de insumos aprobados y `questions.md` al preparar reuniones o registrar respuestas.

## Recuperación ante errores

| Situación | Qué hacer |
|-----------|-----------|
| `status.md` no coincide con los archivos | Valen los archivos (principio 3). Decirlo en una línea, mostrar lo que muestran los archivos y corregir `status.md` con aprobación. |
| `status.md` no existe pero hay `iterations/` | Reconstruirlo desde los encabezados de `step-1.md` e `it-N.md` y mostrarlo antes de guardarlo. |
| Una iteración quedó abierta en otra sesión | Retomarla con `design` en el paso que dice su encabezado; no empezar otra. |
| Dos iteraciones abiertas, o un `it-N.md` sin encabezado válido | No avanzar. Mostrar lo encontrado y preguntar al arquitecto cuál vale; la otra se descarta o se repara con su aprobación. |
| Hay diagramas en una carpeta de iteración abierta y el arquitecto pide los documentos | No pasa nada: los documentos usan `diagrams/` de la raíz, que no incluye el borrador. Decirlo en una línea. |
| `diagrams/` de la raíz difiere de la foto de la última iteración cerrada sin una corrección registrada | Mostrar la diferencia y preguntar si es una corrección (se registra) o un cambio de diseño (requiere iteración). |
| Falla la generación de un Word | Decir el error en una línea, no cambiar `status.md` y ofrecer reintentar; los documentos anteriores no se tocan. |
| Falta una pieza (skill o subagente) | Decirlo en una línea y ofrecer la alternativa: hacer el trabajo conversando con el formato de la pieza, o seguir con lo que sí está disponible. No improvisar otra pieza. |
| Un archivo del proceso fue editado a mano | Revisarlo con su pieza contra su formato; si cambió algo aprobado, tratarlo como "Cambios después de aprobar". |

## Convención de la carpeta del proyecto

```
<proyecto>/
├── inputs/            ← documentos de contexto: anteproyecto, caracterizaciones, actas, formatos reales (opcional)
├── questions.md       ← lo que hay que confirmar con los interesados (todas las secciones)
├── drivers.md
├── iterations/
│   ├── status.md      ← estado del proceso
│   └── round-1/
│       ├── step-1.md  ← paso 1 de la ronda: propósito, drivers y hoja de ruta (desde la ronda 2, también qué cambió)
│       ├── kanban.md  ← tablero de drivers de la ronda
│       └── it-1/
│           ├── it-1.md  ← pasos 2 a 7 de la iteración
│           └── diagrams/      ← foto de las vistas que cambiaron: solo .drawio
│               └── images/    ← sus PNG
├── adr/               ← ADR-xxx.md, uno por decisión con alternativas
├── diagrams/          ← vistas vigentes (última iteración cerrada): solo .drawio
│   └── images/        ← sus PNG
├── analysis/          ← material de trabajo: recorridos, flujos explicados, comparaciones (no es entregable)
├── validation.md
└── document/          ← Word y PDF de la versión actual
    ├── previous-versions/  ← versiones anteriores, una subcarpeta por versión (v4.3/, v5.1/…)
    └── source/        ← lo que genera los documentos
```

- `diagrams/` de la raíz siempre muestra el estado de la **última iteración cerrada**. Durante la iteración, `design` trabaja los diagramas sobre la copia de la carpeta de la iteración y solo al aprobar el cierre (paso 7) los copia a la raíz; la copia queda como foto y no se edita más.
- En toda carpeta `diagrams/` quedan solo los `.drawio`; sus PNG van en `images/`.

Solo se crea lo que haga falta cuando una sección lo produzca. Las únicas reorganizaciones permitidas son la de los insumos (ver "Ordenar los insumos") y la migración (ver "Proyectos de la versión anterior"); fuera de eso, no se mueven archivos del arquitecto.

### Ordenar los insumos

Los documentos de contexto viven en `inputs/`, para que las secciones los encuentren siempre en el mismo lugar y la raíz quede solo con los archivos del proceso. Al activarse, si hay documentos sueltos fuera de `inputs/`:

1. **Clasificar** cada archivo suelto de la raíz (o de carpetas que no son del proceso):
   - **Insumo:** documento que aporta contexto y no lo produjo el proceso (anteproyecto, caracterización, actas, entrevistas, formatos, planillas, historiales de decisiones de otras conversaciones). Va a `inputs/`.
   - **Análisis:** material que produjo el proceso para pensar o explicar, pero que no va tal cual al documento (recorridos del modelo de datos, flujos explicados en HTML, comparaciones, notas de análisis). Va a `analysis/`. También se mueve aquí lo que no sea una vista y esté dentro de `diagrams/`.
   - **Del proceso:** los archivos de la convención. Se quedan donde la convención dice.
   - **Del proyecto, no de la arquitectura:** `CLAUDE.md`, `AGENTS.md`, `README`, `.gitignore`, `package.json`, `node_modules/`, configuraciones. No se tocan.
   - **Dudoso:** notas de trabajo sin origen claro. Se pregunta.
2. **Proponer el movimiento** en una tabla corta (archivo → destino) y moverlo solo con la aprobación del arquitecto. Si el proyecto usa git, mover con `git mv` para conservar el historial.
3. **Actualizar las referencias:** las rutas que nombran esos archivos en los archivos del proceso (por ejemplo, la línea "Insumos:" de `drivers.md`) y en `CLAUDE.md`/`AGENTS.md` se cambian a la ruta nueva. Es el único cambio que el orquestador hace en esos archivos sin cargar la skill que le corresponde, porque no cambia su contenido.

Si un archivo nuevo aparece suelto más adelante, se repite lo mismo.

## Al empezar: instrucciones del proyecto

Para que cualquier sesión futura use este proceso aunque el pedido no lo nombre, el proyecto debe tener sus instrucciones. Si `CLAUDE.md` (Claude Code) o `AGENTS.md` (Copilot, OpenCode) no existen, no mencionan el proceso o tienen el bloque de la versión anterior, proponer al arquitecto este bloque, y escribirlo solo con su aprobación:

```markdown
## Arquitectura
Este proyecto diseña su arquitectura con el método ADD 3.0 (Cervantes y Kazman, 2024), conducido por el plugin `add` en secciones: 1. Caso de negocio → 2. Requisitos del sistema → 3. Proceso de diseño (paso 1 e iteraciones con los pasos 2 a 7) → 4. Análisis → 5. Documentos.
- Para cualquier trabajo de arquitectura (avanzar una iteración, revisar, cambiar drivers, decisiones o diagramas, generar el documento), empezar con la skill `start`.
- El estado del proceso está en `iterations/status.md`.
- No editar a mano `drivers.md`, `iterations/`, `adr/`, `diagrams/`, `validation.md`, `questions.md` ni `document/`: cada uno se modifica con la skill que le corresponde.
- Una iteración cerrada no se edita; un cambio de diseño es una iteración o una ronda nueva.
- Los documentos de contexto van en `inputs/`; el material de análisis, en `analysis/`; `diagrams/` es solo para las vistas.
```

## Ubicar el proyecto

Al activarse, determinar dónde va el proceso:

1. **Secciones 1 y 2.** `drivers.md` lleva una línea de estado por sección:
   ```
   Estado sección 1 (caso de negocio): aprobado
   Estado sección 2 (requisitos del sistema): borrador
   ```
   Sin `drivers.md`, las dos están pendientes. Un `drivers.md` de la versión anterior, con una sola línea `Estado:`, se lee como el estado de ambas, y `drivers` lo pasa al formato nuevo al retomarlo.
2. **Sección 3 en adelante.** Si existe `iterations/status.md`, leerlo: dice la sección, la ronda, la iteración y el paso. Verificar que coincide con los archivos (por ejemplo, que la iteración en curso tiene su `it-N.md` con `status: abierta`); si no coincide, decirlo y seguir lo que muestran los archivos. Si no existe y las secciones 1 y 2 están aprobadas, la sección 3 está pendiente.
3. **Proyecto de la versión anterior.** `decisions.md` o `diagrams/views.md` sin `iterations/` (ver "Proyectos de la versión anterior").

La sección actual es la primera de las secciones 1 a 4 que no está aprobada (la sección 3 se aprueba al terminar el diseño). La sección 5 no tiene estado: se ejecuta cuando corresponde. Mostrar el bloque de estado completo ("Bloque de estado") y, debajo, en texto normal: el proyecto, el avance y qué sigue en una frase. Ejemplo:

```
ADD 3.0 · Proceso de diseño
  [✔] 1. Caso de negocio
  [✔] 2. Requisitos del sistema
  [>] 3. Proceso de diseño · iteración 5 de 6: Soporte a la decisión
        [✔] Paso 1: Revisar entradas
        [✔] Paso 2: Objetivo de la iteración
        [✔] Paso 3: Elegir elementos
        [>] Paso 4: Elegir conceptos de diseño · en curso
        [ ] Paso 5: Instanciar elementos, asignar responsabilidades e interfaces
        [ ] Paso 6: Bocetar vistas y registrar decisiones
        [ ] Paso 7: Analizar el diseño y revisar el objetivo
  [ ] 4. Análisis
  [ ] 5. Documentos
```

Proyecto: mesa-ayuda. 4 iteraciones cerradas; drivers de prioridad alta: 9 de 12 completos; último documento: v1.4 (2026-11-01).
Seguimos con la iteración 5, paso 4: la retomo con su skill.

La línea de drivers sale de `kanban.md`. Desde la segunda ronda, la sección 3 muestra una línea por ronda. El orquestador no evalúa el contenido de los archivos ni dice qué le falta a una sección: eso lo determina la pieza al conducir la sección.

Debajo del tablero, si existe `questions.md`, una línea con las preguntas abiertas: "Preguntas abiertas: 4 (para <interesado>: 3, para <otro>: 1)".

Si la carpeta está vacía, decirlo y proponer arrancar por la sección 1. Si hay archivos en `inputs/`, mencionarlo: se usarán en las secciones 1 y 2. Si hay documentos sueltos, proponer ordenarlos antes de seguir.

## Conducir la sección actual

1. **Siempre cargar la pieza de la sección actual, también al retomar.** La pieza revisa el archivo existente contra su formato y criterio de cierre vigentes y dice qué falta. Seguir sus instrucciones. Para un subagente, delegarle la tarea con un encargo completo (rutas de entrada y salida, y qué devolver), porque el subagente no ve esta conversación.
2. No duplicar lo que la pieza ya hace: el orquestador no reescribe sus preguntas ni su formato.
3. Si la pieza de la sección está "En construcción", decirlo en una línea y ofrecer la alternativa disponible.
4. **Orden de ADD.** No se abre una iteración con otra abierta, no se salta un paso dentro de una iteración y no se abre una ronda con otra en curso. Si el arquitecto pide algo fuera de orden (por ejemplo, un diagrama de despliegue en el paso 3), decir en qué paso está y en cuál se hace lo que pide, y ofrecer seguir hasta allí.
5. **Al terminar el diseño** (todos los drivers de prioridad alta completos), proponer la sección 4. Si quedan drivers de prioridad media o baja sin completar, el arquitecto decide si los atiende con más iteraciones o los deja anotados como pendientes.

## Diagramas

El arquitecto no tiene que pedir los diagramas: cada uno aparece en el momento de ADD que le corresponde.

| Momento | Diagrama | Pieza |
|---------|----------|-------|
| Sección 1 | Contexto (es la entrada del paso 3 de la iteración 1, CK24 §4.2.3) | `drivers` |
| Paso 6 de una iteración | Secuencia de los casos de uso primarios, con la tabla de métodos que sale de ella (las interfaces se identifican en el paso 5 y se registran en el 6, CK16 §4.3.3.4 y §4.3.3.5) | `design` |
| Paso 6 de una iteración | Las vistas que cambiaron las decisiones de los pasos 4 y 5 (CK24 §4.7) | `design` |

Si el arquitecto pide un diagrama por su cuenta:
- **Solo presentación** (mover cajas, corregir una etiqueta, mejorar el estilo, sin cambiar lo que muestra): es una corrección. Se hace con la skill de estilo sobre `diagrams/`, se registra en el control del documento y no abre iteración. Las fotos de las iteraciones no se tocan.
- **Cambia lo que muestra** (un elemento, una relación, una responsabilidad): es diseño. Decir que requiere una iteración y ofrecer abrirla, para que la decisión quede registrada.

## Generar los documentos

Los dos documentos se generan juntos y con la misma versión: primero `document` (calcula la versión y el control del documento) y después `record`, que los toma de él.

- `Architecture-Document-vX.docx`: el diseño vigente (drivers, `diagrams/`, ADR vigentes) y una sección de pendientes tomada del tablero.
- `ADD-Design-Record-vX.docx`: las secciones 1 y 2, el paso 1 y todas las iteraciones cerradas con sus fotos (por rondas, si hay más de una).

**Cuándo:**
- Al aprobar el cierre de una iteración, preguntar siempre, en el bloque "Necesito que decidas": "¿Genero los documentos v<versión>?". Si algo del diseño pide esperar, decirlo ahí con la recomendación; nunca omitir la pregunta.
- Cuando el arquitecto lo pida, en cualquier momento. Si hay una iteración abierta, decirlo: el documento sale con las iteraciones cerradas y los diagramas de `diagrams/`, que no incluyen el trabajo en curso.

**Versión:** `<ronda>.<última iteración cerrada>` (1.5 = ronda 1, iteración 5). En un proyecto migrado que ya tenía documentos, el número mayor parte del siguiente libre ("Número mayor de la ronda 1" en `status.md`; ver `references/migration.md`). Antes de cerrar la primera iteración de la ronda, la versión es `<ronda>.0` (1.0 = secciones 1 y 2, sin diseño todavía). Si esa versión ya existe y desde entonces hubo correcciones sin iteración nueva, se agrega un tercer número (1.5.1, 1.5.2). Los documentos anteriores nunca se sobrescriben.

**Control del documento:** cada versión agrega una fila. El comentario sale del objetivo de la iteración ("Iteración 5: integración con el sistema de pagos") o de la corrección hecha; desde la ronda 2, la primera versión de la ronda nombra lo que la abrió ("Ronda 2: ajustes tras la reunión con el cliente del 2026-11-15").

Al generar, actualizar "Último documento generado" en `status.md`. En la raíz de `document/` queda solo la versión actual; las anteriores se mueven a `document/previous-versions/v<X>/` antes de generar (lo hace `document`), nunca se borran.

## Cambios después de aprobar

| Qué cambia | Cómo se trata |
|------------|---------------|
| Algo que no altera ninguna decisión ni el estado de un driver (redacción, nombre de un elemento, presentación de un diagrama) | **Corrección**: se hace con la skill del archivo y se anota en el control del documento en la próxima generación |
| Una decisión de una iteración cerrada, mientras el diseño sigue en curso | **Iteración nueva**, cuyo objetivo es revisar esa decisión. La iteración vieja no se toca |
| Información nueva después de terminar el diseño (visita, revisión, cambio de requisitos) | **Ronda nueva**: primero se actualizan las secciones 1 y 2 con `drivers` si cambiaron, luego `design` registra el paso 1 de la ronda y su tablero |
| Un driver, con el diseño en curso | Se ajusta con `drivers` y se refleja en el tablero; si el cambio afecta decisiones de iteraciones cerradas, se atiende con una iteración nueva |

En todos los casos:
- Las iteraciones cerradas y sus fotos no se editan. Única excepción: si una tabla de una iteración cerrada no sigue el formato del método (por ejemplo, al tablero del paso 7 le faltan drivers), se corrige con aprobación explícita del arquitecto, sin cambiar ninguna decisión ni ningún estado ya registrado, y se anota como corrección en el control del documento.
- Un ADR reemplazado cambia de estado ("Reemplazado por ADR-0xx"), no de contenido (Nygard, 2011).
- Los drivers que una revisión afecta vuelven a "parcialmente abordado" en el tablero.

## Preguntas abiertas (`questions.md`)

Lo que solo sabe un interesado del proyecto (cómo se trabaja hoy, reglas de negocio, volúmenes, formatos) no se inventa ni se le pide al arquitecto que lo decida: se registra como pregunta en `questions.md`, se avanza con un supuesto provisional visible y se vuelve sobre ello cuando haya respuesta. Los interesados son siempre los del proyecto en curso, nunca un nombre genérico.

Leer `references/questions.md` antes de escribir una pregunta, preparar una reunión ("qué tengo que preguntar") o registrar respuestas ("ya hablé con…"). Ahí están el formato del archivo y los procedimientos.

## Puntos de aprobación

| Punto | Qué se aprueba |
|-------|----------------|
| Fin de la sección 1 | Caso de negocio y diagrama de contexto |
| Fin de la sección 2 | Requisitos del sistema |
| Paso 1 (y el de cada ronda nueva) | Drivers del diseño, hoja de ruta y tablero |
| Paso 7 de cada iteración | El cierre de la iteración: decisiones, diagramas y tablero, en una sola aprobación |
| Fin de la sección 4 | El análisis del diseño |

Dentro de una iteración no hay otras aprobaciones. En los pasos 2 a 6 el arquitecto **decide** lo que le corresponde (el objetivo en el paso 2, la alternativa en el paso 4, los ajustes a los diagramas en el paso 6), y la pieza sigue sin pedir firma.

Solo se pide aprobación cuando la pieza confirma que su criterio de cierre se cumple. El orquestador nunca ofrece aprobar algo que su pieza no revisó en esta sesión.

1. Mostrar el resumen que entregue la pieza, **máximo cinco líneas** (para una iteración: objetivo, decisiones con sus ADR, vistas que cambiaron, drivers que avanzaron y preguntas abiertas que la afectan). No repetir el archivo completo.
2. Pedir aprobación explícita. Solo cuenta un "apruebo" o equivalente claro; respuestas como "continuar" o "sigamos" no aprueban, y el silencio tampoco.
3. Con la aprobación, verificar que el archivo quedó en su estado aprobado o cerrado, actualizar `status.md`, mostrar el tablero y proponer lo siguiente en el bloque "Necesito que decidas". La pieza siguiente (otra sección, el paso 1, la próxima iteración) empieza solo cuando el arquitecto responde; nunca en la misma respuesta de la aprobación.

Sin aprobación no se avanza. Si el arquitecto quiere corregir algo, se vuelve a la pieza.

## Proyectos de la versión anterior

Si el proyecto tiene `decisions.md` o `diagrams/views.md` sin `iterations/`, o carpetas con nombres en español (`insumos/`, `diagramas/`, `documento/`…), leer `references/migration.md` y proponer la migración. Hacerla solo con aprobación. El proceso ADD empieza desde la iteración 1: el diseño anterior se archiva como insumo y sus decisiones se vuelven a tomar en las iteraciones; nunca se convierten en iteraciones inventadas ni se dan por tomadas.

Mientras falte migrar, el bloque de estado es el de las secciones con `[>] 2. Requisitos del sistema · en curso: falta migrar el proyecto`, y la sección 4 se muestra pendiente aunque exista `validation.md`, porque valida el diseño anterior.

## Reglas

- **El arquitecto decide.** El orquestador nunca toma decisiones de arquitectura, no aprueba por su cuenta y no cierra iteraciones.
- **ADD siempre visible.** El bloque de estado abre cada respuesta y cada paso se nombra con su número y su nombre de ADD.
- **No se inventa el dominio.** Lo que solo sabe un interesado se registra en `questions.md`; ninguna sección lo deduce ni lo presenta como hecho.
- **Los archivos del proceso solo se tocan con su skill.** `drivers.md`, `iterations/`, `adr/`, `diagrams/`, `validation.md` y los documentos se crean o modifican siempre cargando la skill que les corresponde, también cuando el pedido llega como una revisión. `questions.md` lo escribe la skill de la sección en que surge la pregunta, o el orquestador al preparar la reunión o registrar respuestas, siempre con su formato.
- **Se trabaja en el proyecto.** Todo borrador (`drivers.md`, `step-1.md`, `it-N.md`, diagramas) se escribe en su lugar del proyecto, marcado como borrador o abierto, nunca en una carpeta temporal: el arquitecto debe poder abrirlo en su editor en cualquier momento, y nada se pierde si la sesión se cierra.
- **Lo cerrado no se edita.** Iteraciones cerradas, sus fotos y los ADR reemplazados se conservan tal como quedaron.
- **Un paso a la vez.** No adelantar trabajo de pasos ni secciones futuras.
- **Respuestas puntuales.** Cada respuesta tiene: el bloque de estado, lo que se hizo o lo que se necesita del arquitecto, y como máximo una pregunta.
- **Decisiones siempre visibles.** Lo que se hizo va primero, bajo "Lo que hice", en máximo cinco viñetas cortas, sin rutas de archivo salvo que el arquitecto deba abrir el archivo. Toda respuesta que necesite una decisión o una aprobación del arquitecto termina con un bloque **"Necesito que decidas"**, separado de lo anterior: un ítem numerado por decisión, nunca dentro de un párrafo, y cada ítem con tres partes: qué se decide (una línea, en negrita), la recomendación y por qué (una línea), y qué pasa si se aprueba (una línea). Las aprobaciones (de una sección, del paso 1 o del cierre de una iteración) también van como ítems de ese bloque. Si la última iteración cerrada todavía no tiene sus documentos generados (al cerrarla o al retomar), el bloque trae siempre dos ítems separados: uno para los documentos (generarlos ahora o esperar, con la razón) y otro para lo siguiente (abrir la próxima iteración); nunca se juntan en una sola pregunta de "esto o aquello". Si no hay nada que decidir, la respuesta termina con "No necesito nada de ti; sigo con <siguiente paso>". No se explica ADD, el libro ni el plugin salvo que el arquitecto lo pida. No se repite contenido de los archivos ni se narra cada acción interna.
- **Método o regla del plugin, sin confundirlos.** Lo que viene de ADD o del caso FCAPS se cita con su fuente; lo que es una regla del plugin (versiones, excepciones, carpetas) se dice como regla del plugin, nunca como "lo que dice el método".
- **El plugin no se modifica a sí mismo.** Durante el trabajo de un proyecto nunca se editan archivos de la carpeta del plugin (skills, scripts, plantillas, referencias), ni se proponen opciones que lo hagan. Si algo del plugin no da el resultado esperado, se dice en una línea qué falla y en qué archivo del plugin, y se sigue con lo que hay. Las instrucciones del arquitecto sobre un documento o un diagrama se cumplen con lo que el plugin ya hace; si piden algo que el plugin no hace, se dice.
- **Sin rodeos.** Si falta un dato para seguir, se pide en ese momento; si no se puede seguir (pieza no instalada, archivo dañado), se dice en una línea y se ofrece la alternativa. No se proponen trabajos fuera del paso en curso.
- **Retomar siempre es posible.** Si el arquitecto vuelve otro día y dice "en qué vamos", volver a "Ubicar el proyecto".

## Fuentes

- Cervantes, H., & Kazman, R. (2024). *Designing software architectures: A practical approach* (2.ª ed.). Addison-Wesley. Cap. 4 (CK24).
- Cervantes, H., & Kazman, R. (2016). *Designing software architectures: A practical approach*. Addison-Wesley. Cap. 4, caso FCAPS (CK16).
- Cervantes, H., Kazman, R., & Cai, Y. (2025). *An LLM-assisted approach to designing software architectures using ADD*. arXiv:2506.22688.
- Nygard, M. (2011). *Documenting architecture decisions*.
