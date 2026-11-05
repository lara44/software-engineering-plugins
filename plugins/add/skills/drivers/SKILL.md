---
name: drivers
description: Usar para las secciones 1 (caso de negocio) y 2 (requisitos del sistema) del proceso de arquitectura con ADD 3.0 - levantar o actualizar contexto, objetivos, actores, diagrama de contexto, casos de uso, escenarios de calidad con árbol de utilidad, restricciones, preocupaciones arquitectónicas y supuestos mediante una entrevista breve con el arquitecto, produciendo drivers.md.
---

# Caso de negocio y requisitos del sistema

Conduce las **secciones 1 y 2** del proceso de arquitectura, con la estructura del caso FCAPS de Cervantes y Kazman (2016, cap. 4): **1. Caso de negocio** y **2. Requisitos del sistema**. Produce `drivers.md` y el diagrama de contexto, que son las entradas del paso 1 de ADD (CK24 §4.2.1).

**Marco metodológico:** se diseña con ADD y se evalúa con ATAM. Los requisitos son los drivers de ADD (funcionalidad primaria, escenarios de calidad, restricciones y preocupaciones arquitectónicas) y los atributos de calidad se organizan con el árbol de utilidad de ATAM. Convención de IDs de ADD: UC-xx (casos de uso), QA-xx (escenarios de calidad), CON-x (restricciones), CRN-x (preocupaciones) y AS-x (supuestos).

Cada respuesta empieza con el bloque de estado de las secciones, con el formato exacto de `start` ("Bloque de estado"), con la sección 1 o la 2 en curso. Las decisiones y aprobaciones que se piden al arquitecto van al final, en el bloque "Necesito que decidas" (ver "Decisiones siempre visibles" en `start`).

## Principios (no negociables)

1. **El arquitecto decide; el asistente redacta.** El arquitecto responde en frases cortas y corrige. El asistente convierte eso en casos de uso, escenarios, restricciones, preocupaciones y supuestos. El arquitecto nunca llena formatos.
2. **Breve.** Meta: 20–30 minutos de conversación por sección y un `drivers.md` de 3–4 páginas. Mínimo suficiente, no exhaustivo.
3. **Proponer en vez de preguntar en abierto.** Mal: "¿Qué disponibilidad necesitas?". Bien: "Propongo 99,5 % en horario laboral porque la operación es de oficina. ¿Sí o ajusto?".
4. **De 2 a 3 preguntas por turno**, y solo sobre lo que falta.
5. **Nunca bloquear.** Si el arquitecto no sabe algo del proceso real, se ofrece dejarlo como pregunta para el interesado que corresponda en este proyecto ("¿lo sabes, o lo dejamos como pregunta para <interesado>?"). Se registra en `questions.md` con el formato de `start` (`references/questions.md`) y, si el diseño depende de ello, como supuesto AS-x por validar. Y se sigue.
6. **No inventar.** Lo que el asistente propone o infiere (y no dijo el arquitecto ni dicen explícitamente los insumos) se marca en línea con `[Propuesta]` mientras la sección está en borrador. La marca va al final de la frase que marca y nunca rompe el hilo del texto: un dato propuesto que no es parte del argumento va en su propia frase al final del párrafo. No se usan otras etiquetas de origen ni líneas "Origen:".
7. **Respetar lo que ya decidieron los insumos.** Si los documentos ya definen atributos de calidad, objetivos o alcance, se toman tal cual, con sus nombres. El asistente puede sugerir agregados, pero separados y marcados `[Propuesta]`, nunca mezclados ni reemplazando lo existente.
8. **No diseñar en estas secciones.** Si el arquitecto menciona estilo, patrones o tecnología: si es impuesto (cliente, normativa, plataforma obligatoria), va como restricción; si es una preferencia o conocimiento del equipo que conviene aprovechar, va como preocupación (CRN); si es una decisión candidata, va en "Notas para el diseño". Las decisiones se toman en el paso 4 de las iteraciones.
9. **Una sección a la vez.** La sección 2 empieza cuando la sección 1 está aprobada.

## Revisar qué existe

1. Si ya hay un `drivers.md`, retomarlo: revisarlo contra el formato y el criterio de cierre de esta skill y mostrar en 3–4 líneas qué está completo y qué falta. Si está en el formato anterior (una sola línea `Estado:`, sin secciones numeradas ni preocupaciones), convertirlo: reordenar en las secciones 1 y 2, poner una línea de estado por sección con el estado que tenía, agregar el bloque de preocupaciones con propuestas `[Propuesta]` y el caso de uso asociado de cada escenario. La conversión se escribe directamente en `drivers.md` con las secciones en `borrador` y se resume en la respuesta.
   Al retomar, revisar también si en `inputs/` hay documentos nuevos o cambiados desde la última aprobación (fecha de la línea de estado; `git log` si el proyecto usa git), como observaciones de un revisor o una versión nueva de la propuesta del proyecto, y proponer los cambios que traen, uno por observación.
2. Buscar insumos en `inputs/` (.md, .pdf, .docx, .xlsx, actas, transcripciones). Si hay documentos de contexto sueltos en la raíz, proponer moverlos a `inputs/` como indica `start` ("Ordenar los insumos") antes de leerlos. Si existe el subagente `extractor`, delegarle la lectura; si no, leerlos directamente.
3. Si hay un documento que fija el alcance del proyecto (propuesta, anteproyecto, contrato), sus definiciones de atributos, cotas (número de escenarios o atributos), restricciones y exclusiones de alcance son la referencia: cada propuesta se contrasta con ellas y, si se aparta, se dice en qué y por qué.
4. Pre-llenar con lo que digan los insumos y armar la lista de vacíos. Registrar los insumos una sola vez, en la línea "Insumos:" del encabezado.
5. Decir en 2–3 líneas qué se encontró y cuántas rondas de preguntas faltan aproximadamente. Si la carpeta está vacía, decirlo y arrancar por el bloque 1.

## Entrevista

El orden de los bloques importa: cada uno alimenta las propuestas del siguiente. Saltar un bloque si los insumos ya lo cubren. El orden de la entrevista no es el orden del documento: el archivo siempre sigue el formato de abajo.

Cada ronda de preguntas tiene esta forma:
- 1–2 líneas de lo entendido hasta ahora.
- 2–3 preguntas, cada una con una propuesta concreta para aceptar o ajustar.

### Sección 1: Caso de negocio

1. **Contexto.** De uno a tres párrafos cortos, en este orden: qué hace hoy la organización y cómo lo registra; qué no puede hacer por eso (las consecuencias, con su causa); a quién le duele, por qué ahora y cuál es el problema central. Frases cortas, una idea por frase, sin cifras de volumen (lo que importe de volumen o carga va como supuesto). No habla del proyecto ni de la oportunidad de diseñar: el propósito del diseño se registra en el paso 1 de ADD (CK24 §4.2.2).
2. **Objetivos.** Máximo 3, cada uno con cómo se sabría que se logró. Sin IDs.
3. **Actores y sistemas externos.** Proponer la lista a partir de lo dicho y pedir corrección. Formato "Nombre: qué hace" (dos puntos, no flechas).
4. **Diagrama de contexto.** Con los actores y sistemas externos aprobados, dibujarlo cargando la skill `c4` (nivel de contexto: el sistema como una sola caja, sin contenedores). Guardar `diagrams/c4-context.drawio` y su PNG en `diagrams/images/c4-context.png`, verificar visualmente la imagen, mostrarla e insertarla en `drivers.md` (1.3) para que se vea al abrir el archivo. Es la entrada del paso 3 de la primera iteración (CK24 §4.2.3).

Cerrar la sección 1 (ver "Cierre de cada sección") antes de pasar a la sección 2.

### Sección 2: Requisitos del sistema

5. **Casos de uso (CK16 §4.2.1).** Pedir los principales (5–10) en lenguaje de negocio. Cada uno se nombra con verbo + objeto ("Registrar pedido") y se describe en una línea que nombra al actor ("El vendedor registra…"). Con la tabla aprobada, dibujar el **diagrama de casos de uso** con el generador de `c4` (`scripts/usecase_drawio.py`): solo los actores que usan el sistema o los sistemas externos que interactúan con él, sin los casos retirados, y con los casos coloreados por área funcional (el asistente propone las áreas a partir del dominio y el arquitecto las confirma). Guardar `diagrams/use-cases.drawio` y su PNG en `diagrams/images/use-cases.png`, verificar visualmente la imagen e insertarla en `drivers.md` (2.1), antes de la tabla, como en el caso FCAPS (CK16 §4.2.1, figura 4.1). Aquí no se marca cuáles son primarios: como en el caso FCAPS, el modelo de casos de uso solo los lista y describe, y la **funcionalidad primaria** se elige en el paso 1 de ADD con `design` (CK16 §4.2.1 y §4.3.1).
6. **Restricciones (CK16 §4.2.3).** Una restricción es una decisión ya tomada que el arquitecto no puede negociar. Preguntar por cliente, normativa, plataforma o tecnología obligatoria, presupuesto, plazos y equipo. Cada una se escribe como una frase que dice qué limita al diseño. No es restricción: un supuesto (se cree cierto pero puede no serlo), un atributo de calidad (tiene grados y se mide), una preferencia del equipo (es una preocupación) ni una regla de negocio que no limita la arquitectura.
7. **Preocupaciones arquitectónicas (CK16 §4.2.4).** Aspectos que el diseño debe atender aunque no sean requisitos del cliente. En un sistema nuevo, el asistente propone las generales, como en el caso FCAPS: establecer una estructura general del sistema, aprovechar el conocimiento del equipo (nombrando las tecnologías que domina) y repartir el trabajo entre los miembros del equipo. A esas suma las propias del proyecto que hayan salido en la entrevista. La de conocimiento del equipo nombra lo que el arquitecto dice que el equipo domina, nunca lo que usaba un diseño anterior. El arquitecto confirma, ajusta o descarta. Si descarta una de las generales, el asistente dice en una línea qué decisiones quedarán sin driver (por ejemplo, sin la de conocimiento del equipo, la elección de tecnologías solo podrá apoyarse en restricciones o escenarios; sin la de repartir el trabajo, la división en módulos no considerará el tamaño del equipo) y pide confirmación. Más preocupaciones pueden aparecer durante las iteraciones; esas las registra `design`.
8. **Supuestos.** Algo que se cree cierto pero no está confirmado, y que si resulta falso afecta el diseño. El asistente los propone a partir de todo lo anterior (volúmenes, usuarios, conectividad, datos existentes, disponibilidad de terceros), cada uno con su impacto si resulta falso. El arquitecto confirma, corrige o descarta. Si el dato lo sabe un interesado y no el arquitecto, el supuesto queda "Por validar con <interesado> (PA-xx)". No es supuesto una regla de cálculo o de negocio: eso va en "Notas para el diseño" marcado `(para el modelo de dominio)`. Un supuesto **condiciona** decisiones (se cita en su fundamentación, como en la tabla "Decisiones de diseño y ubicación | Fundamentación y supuestos" de ADD), pero **ninguna decisión existe para atenderlo**: en ADD los supuestos no son drivers. Si un supuesto describe algo que podría pedirse en el futuro (una proyección, como operar con más clientes o sedes), el asistente le pregunta al arquitecto con estas tres opciones, y en cada una dice qué casos de uso, actores y supuestos cambian:
   1. **Driver:** el diseño lo soporta. Se escribe como escenario de calidad (por ejemplo, de modificabilidad, con su medida y su prioridad), y los requisitos que dependen de él se quedan.
   2. **Fuera del diseño, como supuesto (recomendada):** se quitan los requisitos que solo existen para la proyección. El supuesto se reescribe como el estado presente (por ejemplo, "El sistema opera para un solo cliente"), y la proyección queda en "Fuera de alcance". El supuesto condiciona las decisiones, pero ninguna decisión existe para atenderlo.
   3. **Quitarlo del todo:** se quitan los requisitos y el supuesto, y la proyección queda solo en "Fuera de alcance".

   En las opciones 2 y 3, lo quitado se anota en "Cambios después de la aprobación". Diseñar para algo que no es driver es generalidad especulativa (Fowler, 1999).
9. **Escenarios de calidad con árbol de utilidad (CK16 §4.2.2; ATAM).** Tres niveles obligatorios: atributo → refinamiento → escenario.
   - **Atributos (el "qué").** Si los insumos ya los definen, se respetan tal cual. Si no, el asistente deriva candidatos de los bloques anteriores (por ejemplo, datos sensibles → seguridad; integración externa → interoperabilidad) y el arquitecto elige de 3 a 6.
   - **Refinamientos (obligatorios).** Cada atributo se descompone en uno o más refinamientos. El refinamiento nombra el **aspecto del atributo** que importa en este sistema: responde "¿trazabilidad de qué?", "¿disponibilidad de qué?". Se redacta como un sustantivo abstracto, no como un resumen del escenario. Bien: "Procedencia de los productos", "Aislamiento de fallos". Mal: "Origen de lo entregado en < 5 s" (eso es el escenario). Un aspecto que parezca otro atributo pero sirva al mismo propósito va como refinamiento de ese atributo.
   - **Escenarios (la prueba medible de cada refinamiento).** Al menos uno por refinamiento, con su **caso de uso asociado** (el caso de uso en que ocurre el estímulo; "transversal" si no hay uno). Proponer y que el arquitecto ajuste, siguiendo "Redacción de escenarios".
   - **Doble prioridad por escenario**, cada una Alta (A), Media (M) o Baja (B): **importancia para el negocio** y **dificultad o riesgo técnico**. El asistente propone ambas con una razón de una línea; el arquitecto las fija. Los (A, A) se señalan. En ATAM la importancia para el negocio la asignan los interesados (Kazman, Klein y Clements, 2000): si el arquitecto la fija sin ellos, queda provisional y se abre en `questions.md` una pregunta para la sesión de priorización con los interesados de la sección 1; cuando se hace, se anota en `drivers.md` la fecha y quiénes participaron. Si casi todos los escenarios tienen la misma importancia, el árbol no discrimina: decirlo y proponer cuáles bajar. Esta prioridad es la que usa el paso 1 para elegir los drivers del diseño.
   - **Normas de referencia.** ISO/IEC 25010 para atributos del producto. Si el atributo es sobre los datos (trazabilidad de registros, exactitud, completitud), ISO/IEC 25012. Si no encaja en ninguna, atributo propio del dominio con su justificación. No forzar mapeos.
   - **Medidas coherentes con las restricciones.** Si una restricción limita el alcance (por ejemplo, un prototipo), la medida debe ser realista para ese alcance o aclarar que aplica al diseño objetivo.

## Redacción de escenarios

Cada escenario se escribe dos veces, con el mismo contenido: como **frase completa** en el árbol de utilidad y como **ficha** debajo. El árbol debe poder leerse y evaluarse sin abrir las fichas.

**Frase del árbol.** Plantilla obligatoria:

> QA-xx: Cuando [fuente] [estímulo], en [ambiente], el sistema [respuesta] en/con [medida].

Nunca poner solo un título ("QA-01 Origen de un producto") en la columna Escenario.

**Reglas por campo de la ficha:**
- **Fuente:** quién o qué origina el estímulo, concreto (un rol, un sistema, "falla interna", "ente externo", "equipo de desarrollo").
- **Estímulo:** un evento puntual, con verbo ("consulta", "corrige", "deja de responder", "cambia la estructura"). No un estado. **Un solo estímulo por escenario**: si hay varios (o uno queda escondido en el ambiente), se separan en escenarios distintos, cada uno con su medida, o el arquitecto elige cuál se queda.
- **Ambiente:** la condición del sistema cuando llega el estímulo: "operación normal", "carga pico", "falla de un componente", "puesta en marcha", "mantenimiento". Para modificabilidad usar "mantenimiento" o "tiempo de diseño", no "desarrollo".
- **Artefacto:** la parte específica del sistema que recibe el estímulo (un componente, un módulo, un conjunto de datos). Nunca "sistema completo" ni "el sistema".
- **Respuesta:** lo que el sistema hace, observable y verificable. Nunca respuestas vacías como "el servicio responde" o "funciona correctamente". Dice **qué** hace el sistema, nunca **cómo** lo logra: un mecanismo, patrón, táctica, tecnología o forma de cálculo ("porque el riesgo se calcula al consultar", "con reintentos", "en una cola") es una decisión del paso 4. Se quita del escenario y se anota en "Notas para el diseño" como decisión candidata (Bass, Clements y Kazman, 2021, cap. 3).
- **Medida:** cómo se mide **esa respuesta a ese estímulo** (tiempo, porcentaje, conteo, esfuerzo). No mezclar con la meta de un objetivo de negocio. Una sola medida principal; si hay dos, deben medir la misma respuesta.
- **Caso de uso asociado:** UC-xx, o "transversal".

## Escritura incremental

Actualizar `drivers.md` al cerrar cada bloque, no solo al final, para que nada se pierda si la sesión se interrumpe y para que el arquitecto vea los requisitos mientras avanzan. Todo cambio se escribe directamente en `drivers.md`, en el proyecto, nunca en una copia temporal. Guardar no aprueba nada: la sección queda en `borrador` hasta su aprobación, y lo que espera una decisión del arquitecto queda marcado `[Propuesta]` o `[Pendiente]`. "Mostrar antes de guardar" significa resumir los cambios en la respuesta con el archivo ya actualizado.

## Formato de drivers.md

```markdown
# Drivers — <Sistema>
Estado sección 1 (caso de negocio): borrador | aprobado · AAAA-MM-DD
Estado sección 2 (requisitos del sistema): pendiente | borrador | aprobado · AAAA-MM-DD

Insumos: <archivo 1> · <archivo 2>

## 1. Caso de negocio

### 1.1 Contexto
<Uno a tres párrafos cortos: cómo opera hoy; qué no puede hacer por eso; a quién le duele, por qué ahora y el problema central.>

### 1.2 Objetivos
- <Objetivo>. Medida: <cómo se sabe que se logró>.

### 1.3 Actores y sistemas externos
Actores:
- <Actor>: <qué hace con el sistema>.

Sistemas externos:
- <Sistema>: <para qué se relaciona>.

Diagrama de contexto (editable en `diagrams/c4-context.drawio`):

![Diagrama de contexto](diagrams/images/c4-context.png)

## 2. Requisitos del sistema

### 2.1 Casos de uso
Diagrama de casos de uso (editable en `diagrams/use-cases.drawio`):

![Diagrama de casos de uso](diagrams/images/use-cases.png)

| ID | Caso de uso | Descripción |
|----|-------------|-------------|
| UC-01 | <Verbo + objeto> | <Actor> <qué hace>, en una línea. |
| UC-0n | <Verbo + objeto> | … |

Fuera de alcance: <si aplica>.

### 2.2 Escenarios de atributos de calidad
Prioridad: (importancia para el negocio, dificultad técnica) · A = alta, M = media, B = baja

| Atributo | Refinamiento | Escenario | Caso de uso | Prioridad |
|----------|--------------|-----------|-------------|-----------|
| **<Atributo 1>** (ISO/IEC 25010 – … / ISO/IEC 25012 / propio del dominio) | <Refinamiento 1.1> | QA-01: Cuando [fuente] [estímulo], en [ambiente], el sistema [respuesta] en/con [medida]. | UC-0x | (A, A) |
| | <Refinamiento 1.2> | QA-02: Cuando … | UC-0x | (A, M) |
| **<Atributo 2>** (…) | <Refinamiento 2.1> | QA-03: Cuando … | transversal | (M, M) |

Escenarios que guían el diseño (A, A): QA-xx

#### QA-01 — <nombre descriptivo>
- Atributo: <atributo> › <refinamiento> · (A, A)
- Fuente:
- Estímulo:
- Ambiente:
- Artefacto:
- Respuesta:
- Medida:
- Caso de uso asociado: UC-0x

### 2.3 Restricciones
| ID | Restricción |
|----|-------------|
| CON-1 | <Qué limita al diseño, en una frase>. |

### 2.4 Preocupaciones arquitectónicas
| ID | Preocupación |
|----|--------------|
| CRN-1 | Establecer una estructura general del sistema. |
| CRN-2 | <Aprovechar el conocimiento del equipo en …>. |

Las preocupaciones que surjan durante el diseño se registran en la iteración donde aparecen y en el tablero.

### 2.5 Supuestos
| ID | Supuesto | Impacto si es falso | Estado |
|----|----------|---------------------|--------|
| AS-1 | <Lo que se cree cierto>. | <Qué pasa con el diseño si no lo es>. | Validado / Por validar con <interesado> (PA-xx) |

## Notas para el diseño
Las preguntas para los interesados están en `questions.md`. Aquí solo quedan las que resuelve el propio proceso:
- (para el modelo de dominio) <Regla de negocio o de cálculo que no es driver>
- (para el proceso de diseño) <Decisión candidata que mencionó el arquitecto>

## Cambios después de la aprobación
| Fecha | Sección | Cambio | Motivo | Se atiende en |
|-------|---------|--------|--------|---------------|
```

Reglas del formato:
- Las secciones siguen el orden del caso FCAPS: 1. Caso de negocio; 2. Requisitos del sistema (casos de uso, escenarios de calidad, restricciones, preocupaciones). Los supuestos van al final de la sección 2.
- IDs de ADD: UC-xx, QA-xx, CON-x, CRN-x, AS-x. Los objetivos no llevan ID.
- Contexto: un párrafo, sin etiquetas ("Problema:") ni cifras de volumen. Listas con "Nombre: descripción", nunca flechas.
- Casos de uso en lenguaje de negocio, sin términos técnicos, en tres columnas (ID, Caso de uso, Descripción): el actor va dentro de la descripción. Sin marcar primarios: eso se hace en el paso 1 de ADD.
- Árbol de utilidad: atributo y refinamiento se escriben una sola vez, en la primera fila de su grupo (en Word se combinan verticalmente); la norma va junto al atributo; dentro de cada atributo, (A, A) primero; la columna Escenario lleva la frase completa.
- Restricciones y preocupaciones en dos columnas (ID, texto), sin columna de tipo.
- Supuestos en cuatro columnas; el estado dice con quién se valida y con qué pregunta (PA-xx).
- Cuando un texto cita un driver, escribe el ID con su nombre corto ("UC-03 Emitir remisión", "QA-05 Recuperación sin pérdida de registros"), nunca el ID solo. Las tablas con columna de ID y de nombre quedan como están.
- Sin líneas "Origen:" ni etiquetas de documento. Solo `[Propuesta]`, en línea, mientras la sección está en borrador. Si refinamientos o normas son propuesta, una línea "Refinamientos y normas de referencia: [Propuesta]" debajo de la tabla.
- Una línea por campo; nada de párrafos largos fuera del contexto.

## Criterio de cierre

**Sección 1:**
- [ ] Contexto en un párrafo; objetivos (máx. 3, con medida).
- [ ] Actores y sistemas externos definidos.
- [ ] Diagrama de contexto con exactamente esos actores y sistemas externos, verificado visualmente.
- [ ] Todos los elementos `[Propuesta]` de la sección fueron mostrados al arquitecto.

**Sección 2:**
- [ ] Casos de uso en formato ADD (ID, caso de uso y descripción de una línea).
- [ ] Cada objetivo tiene al menos un caso de uso que lo soporta.
- [ ] Todo actor nombrado en una descripción está en la lista de actores de la sección 1, y viceversa.
- [ ] Árbol de utilidad con 3 a 6 atributos; si los insumos ya los definían, se respetaron.
- [ ] Cada atributo tiene al menos un refinamiento, y cada refinamiento al menos un escenario.
- [ ] Los refinamientos nombran un aspecto del atributo, no resumen el escenario.
- [ ] Cada escenario aparece como frase completa en el árbol y como ficha con el mismo contenido, con su caso de uso asociado.
- [ ] Ninguna ficha tiene artefacto genérico, respuesta vacía ni una medida que en realidad es la meta de un objetivo.
- [ ] Cada escenario tiene su doble prioridad fijada por el arquitecto, y los (A, A) están señalados.
- [ ] Las medidas son coherentes con las restricciones.
- [ ] Restricciones (CON-x) sin supuestos, preferencias ni reglas de negocio mezclados.
- [ ] Preocupaciones (CRN-x) confirmadas por el arquitecto; al menos la de estructura general si el sistema es nuevo.
- [ ] Supuestos (AS-x) con impacto y estado.
- [ ] Todos los elementos `[Propuesta]` de la sección fueron mostrados al arquitecto.

Si algo falla, decirlo en una línea y preguntar si se resuelve ahora o se deja como pregunta abierta.

## Cierre de cada sección

1. Mostrar un resumen de máximo cinco líneas.
   - Sección 1: problema, objetivos, actores y sistemas externos, y el diagrama de contexto.
   - Sección 2: casos de uso, escenarios (A, A), restricciones clave, preocupaciones, y supuestos y preguntas abiertas que la afectan.
2. Pedir aprobación explícita de esa sección.
3. Con la aprobación: quitar las marcas `[Propuesta]` de lo aceptado en esa sección, sacar (o pasar a "Notas para el diseño") lo que el arquitecto no aceptó, poner su línea de estado en `aprobado` con la fecha.
4. Indicar lo que sigue: tras la sección 1, la sección 2; tras la sección 2, el paso 1 del proceso de diseño, que conduce `design`.

## Cambios después de la aprobación

Cuando las secciones ya están aprobadas y algo cambia (una respuesta de un interesado, una revisión, un requisito nuevo):

1. Mostrar en una tabla corta qué cambia y qué afecta (escenarios, restricciones, decisiones de qué iteraciones) antes de tocar nada.
2. Con la aprobación del arquitecto, aplicar el cambio y anotarlo en "Cambios después de la aprobación", con la fecha, el motivo y dónde se atiende: "Corrección" si no altera ninguna decisión ni driver del diseño en curso; si no, la iteración o la ronda nueva que lo atiende (lo decide el arquitecto con `start`, "Cambios después de aprobar").
3. La sección cambiada vuelve a `borrador` hasta que el arquitecto la apruebe de nuevo con el mismo cierre.

Un caso de uso, escenario, restricción o supuesto que se elimina sale de su tabla. Si todavía no lo cita ninguna iteración cerrada ni un documento generado con ADD (por ejemplo, en la ronda 1 antes de cerrar la primera iteración), se borra sin dejar rastro en `drivers.md`; el cambio queda solo en "Cambios después de la aprobación" (si la sección ya estaba aprobada) y en git. Si ya lo citan, queda en una línea "Retirados (AAAA-MM-DD): <ID> (<nombre>), <motivo>" debajo de su tabla, para que esas iteraciones y documentos sigan teniendo sentido. En ambos casos su ID no se reutiliza.

## Fuentes

- Cervantes, H., & Kazman, R. (2016). *Designing software architectures: A practical approach*. Addison-Wesley. Cap. 4, caso FCAPS (CK16).
- Cervantes, H., & Kazman, R. (2024). *Designing software architectures: A practical approach* (2.ª ed.). Addison-Wesley. Cap. 4 (CK24).
- Bass, L., Clements, P., & Kazman, R. (2021). *Software architecture in practice* (4.ª ed.). Addison-Wesley. Cap. 3 (escenarios de atributos de calidad).
- Fowler, M. (1999). *Refactoring: Improving the design of existing code*. Addison-Wesley (generalidad especulativa).
- ISO/IEC 25010 e ISO/IEC 25012, para los atributos de calidad.
- Kazman, R., Klein, M., & Clements, P. (2000). *ATAM: Method for architecture evaluation* (CMU/SEI-2000-TR-004). Software Engineering Institute.
