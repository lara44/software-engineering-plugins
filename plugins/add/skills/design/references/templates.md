# Formatos de la sección 3

Referencia de `design`. Leer la plantilla antes de crear o actualizar el archivo correspondiente.

Contenido:
- `iterations/status.md`: estado del proceso
- `iterations/round-R/step-1.md`: paso 1 y hoja de ruta
- `iterations/round-R/kanban.md`: tablero de drivers
- Encabezado de `step-1.md` e `it-N.md`: estado oculto y líneas visibles
- `iterations/round-R/it-N/it-N.md`: pasos 2 a 7
- `adr/ADR-xxx.md`: registro de decisión

## `iterations/status.md`

```markdown
# Estado del proceso de arquitectura
Método: ADD 3.0 (Cervantes y Kazman, 2024)
Sección: 3 — Proceso de diseño
Ronda: 1 — Diseño inicial
Iteración en curso: 2 — Identificar estructuras para la funcionalidad primaria   ← "ninguna" entre iteraciones
Paso en curso: 4 — Elegir los conceptos de diseño                                ← vacío entre iteraciones
Iteraciones cerradas: 1
Último documento generado: v1.1 (AAAA-MM-DD)
Número mayor de la ronda 1: 1                 ← solo en proyectos migrados con documentos anteriores
Actualizado: AAAA-MM-DD
```

## `iterations/round-R/step-1.md`

```markdown
<!-- estado
method: ADD 3.0
round: 1
status: borrador
approved:
-->
# Paso 1: revisar las entradas

**Borrador** · Ronda 1                ← aprobado: **Aprobado** · Ronda 1 · 4 nov 2026

---

<Solo desde la ronda 2:>
## Motivo de la ronda
<Qué la abrió (visita, revisión, cambio) y cuándo.>
Drivers que cambiaron: <IDs, con una frase cada uno>. Afectan decisiones de: <iteraciones y ADR>.

| Categoría | Detalles |
|-----------|----------|
| Propósito del diseño | Se trata de un sistema <nuevo en un dominio conocido / nuevo en un dominio desconocido / existente>. El objetivo es <un diseño suficiente para…>. |
| Requisitos funcionales principales | De los casos de uso de la sección 2.1, se determinó que los principales son:<br>UC-01: <razón en pocas palabras>.<br>UC-03: <razón>. |
| Escenarios de atributos de calidad | Los escenarios se describieron en la sección 2.2. Su prioridad es la siguiente: (tabla de prioridad). Se seleccionan como drivers <QA-01, QA-02… / los N>. |
| Restricciones | Todas las restricciones de la sección 2.3 se incluyen como drivers. <O: todas, salvo CON-x, porque…> |
| Preocupaciones arquitectónicas | Todas las preocupaciones de la sección 2.4 se incluyen como drivers. <O: todas, salvo CRN-x, porque…> |

| Escenario | Importancia para el negocio | Dificultad técnica |
|-----------|-----------------------------|--------------------|
| QA-01 | Alta | Alta |

Criterio de "completamente abordado": <una frase>.

## Hoja de ruta
| Iteración | Objetivo | Drivers |
|-----------|----------|---------|
| 1 | Establecer una estructura general del sistema | CRN-1, QA-xx, CON-x |
| 2 | Identificar estructuras para la funcionalidad primaria | UC-xx, CRN-x |
| 3 | <…> | <…> |
```

Reglas de la tabla del paso 1 (como el caso FCAPS, CK16 §4.3.1):
- Solo esas cinco categorías, con esos nombres. No se agregan filas (ni "Entradas", ni "Tipo de sistema": el tipo de sistema va en la primera frase del propósito).
- Cada celda es corta: una o dos frases que remiten a la sección de requisitos. Cada caso de uso principal va en una línea, `UC-xx: <razón en pocas palabras>`, sin repetir su nombre ni su descripción. Los no principales no se listan ni se justifican.
- Si se incluyen todas las restricciones o todas las preocupaciones, basta una frase. Solo se explica lo que se excluye.
- El criterio y la hoja de ruta van después de la tabla, cortos: el criterio en una frase y la hoja de ruta en su tabla, con el objetivo de cada iteración en pocas palabras.

## `iterations/round-R/kanban.md`

```markdown
# Tablero de drivers — Ronda R
Actualizado: AAAA-MM-DD · después de la iteración N

| Driver | Prioridad | Estado | Iteración | Justificación |
|--------|-----------|--------|-----------|---------------|
| UC-01 Registrar pedido | Primario | Completamente abordado | 2 | <frase> |
| QA-01 <nombre corto> | (A, A) | Parcialmente abordado | 3 | <qué falta> |
| CON-1 <nombre corto> | — | No abordado | — | |
| CRN-4 <nombre corto> | — | No abordado | — | Nueva en la iteración 2 |

Drivers de prioridad alta completos: X de Y.

## Decisiones sin driver
| Decisión | Dónde está | Qué se hace |
|----------|------------|-------------|
| <decisión> | <ADR-xxx o software existente> | <Agregar driver con drivers / revisar en la iteración N / pendiente de decidir> |
```

La sección "Decisiones sin driver" solo aparece si hay alguna.

Estados: No abordado · Parcialmente abordado · Completamente abordado · Descartado (con su razón). Prioridad alta = casos de uso primarios, escenarios de importancia alta, restricciones y las preocupaciones que el paso 1 marcó así.

## Encabezado de `step-1.md` e `it-N.md`

El estado va en un comentario HTML (`<!-- estado … -->`) antes del título: el plugin lo lee y ningún visor lo muestra. Nunca usar un encabezado YAML (`---` … `---`), porque GitHub y otros visores lo muestran como tabla. Los valores posibles: `status` en `step-1.md`, `borrador` o `aprobado`; en `it-N.md`, `abierta` o `cerrada`; `step` es el paso en curso mientras la iteración está abierta.

Debajo del título van las líneas que lee el arquitecto, cada una en su párrafo, y una línea horizontal (`---`) antes del primer paso:

1. Estado: `**En curso · paso N de 7** · Ronda R · desde el <fecha>` o `**Cerrada** · Ronda R · <fecha de cierre>`. En `step-1.md`: `**Borrador** · Ronda R` o `**Aprobado** · Ronda R · <fecha>`.
2. Solo en `it-N.md`: `**Decisiones:** ADR-xxx · ADR-yyy`, o `**Decisiones:** ninguna por ahora`.
3. Solo en `it-N.md`: los seis pasos (Objetivo, Elementos, Conceptos, Instanciación, Vistas, Análisis) con `[✔]`, `[>]` o `[ ]`. Los pasos con contenido enlazan a su sección; el paso en curso va en negrita; los que no han empezado van sin enlace.

Fechas como `4 nov 2026`. El método no se muestra (queda en el comentario). Cada vez que cambian el paso, el estado o los ADR, se actualizan el comentario y las líneas visibles. Si un archivo tiene el encabezado YAML anterior, se convierte a este formato la próxima vez que se escriba, sin pedir aprobación y sin cambiar los datos.

## `iterations/round-R/it-N/it-N.md`

```markdown
<!-- estado
method: ADD 3.0
round: 1
iteration: 2
status: abierta
step: 4
opened: AAAA-MM-DD
closed:
adrs: [ADR-003, ADR-004]
-->
# Iteración 2: <objetivo en pocas palabras>

**En curso · paso 4 de 7** · Ronda 1 · desde el 5 nov 2026

**Decisiones:** ADR-003 · ADR-004

[✔] [Objetivo](#paso-2-establecer-el-objetivo-de-la-iteración) · [✔] [Elementos](#paso-3-elegir-los-elementos-a-refinar) · [>] **[Conceptos](#paso-4-elegir-los-conceptos-de-diseño)** · [ ] Instanciación · [ ] Vistas · [ ] Análisis

---

## Paso 2: establecer el objetivo de la iteración
<Objetivo en una o dos frases: qué se busca, de qué tipo es y por qué ahora.>

- Funcionalidad primaria: UC-xx <nombre corto>, UC-yy <nombre corto>
- Escenarios de calidad: QA-xx <nombre corto> <si entra en parte: (solo <qué parte>)>
- Restricciones: CON-x <nombre corto>, CON-y <nombre corto>
- Preocupaciones arquitectónicas: CRN-x <nombre corto>

## Paso 3: elegir los elementos a refinar
<Una o dos frases: el elemento a refinar y el tipo de refinamiento.> <En la iteración 1 de un sistema nuevo: ![Contexto](../../../diagrams/images/c4-context.png)>

## Paso 4: elegir los conceptos de diseño
<Una frase: cómo se eligieron los conceptos (en la primera iteración, según la hoja de ruta).> La siguiente tabla resume las decisiones de diseño.

| Decisiones de diseño y ubicación | Fundamentación y supuestos |
|----------------------------------|----------------------------|
| <Frase en imperativo que nombra el concepto, sin negritas; si es una táctica: "Táctica de <atributo>: <nombre>"> | <Prosa de dos a cuatro frases con el porqué y los drivers entre paréntesis (CON-x, QA-y); supuestos (AS-x).> Ver ADR-00x.<br>*Alternativas descartadas:*<br>- <alternativa>: <motivo en una frase><br>- <alternativa>: <motivo> |
| <Decisión sin alternativas reales> | <Prosa con el porqué (CRN-x).><br>No se consideraron otras alternativas, ya que <razón>. |

## Paso 5: instanciar elementos, asignar responsabilidades y definir interfaces
Las decisiones de instanciación tomadas en esta iteración se resumen en la siguiente tabla:

| Decisión de diseño y ubicación | Razón fundamental |
|--------------------------------|-------------------|
| <Una decisión corta: un elemento, una responsabilidad o una relación> | <Prosa de una a tres frases con el porqué y los drivers entre paréntesis (QA-x, CON-y).> |

Los resultados de estas decisiones de instanciación se registran en el siguiente paso. <En la iteración de estructura general: los sistemas externos con su protocolo.>

Preocupaciones nuevas: <CRN-x: frase, o "Ninguna">

## Paso 6: bocetar vistas y registrar las decisiones
Vistas que cambiaron: <lista; o "Ninguna: las decisiones no cambian las vistas">
![<Vista>](diagrams/images/<vista>.png)

| Elemento | Responsabilidad |
|----------|-----------------|
| <Elemento> | <Responsabilidad> |

| Relación | Descripción |
|----------|-------------|
| <A y B> | <Cómo se comunican> |

<Solo si la iteración define interfaces (no en la de estructura general):>
![Secuencia UC-xx](diagrams/images/seq-uc-xx.png)

| Nombre del método | Descripción |
|-------------------|-------------|
| **Elemento: <nombre>** | |
| <operación> | <qué hace, quién la llama> |

## Paso 7: analizar el diseño y revisar el objetivo
<Una o dos frases sobre lo que logró la iteración.>

| No abordado | Parcialmente abordado | Completamente abordado | Decisiones de diseño tomadas durante la iteración |
|-------------|-----------------------|------------------------|---------------------------------------------------|
| | QA-xx | | <frase> |
| | | UC-xx | <frase> |
| QA-yy | | | No se han tomado decisiones relevantes. |

En las columnas de estado, solo el ID (como el libro).

Todos los drivers del tablero, salvo los completamente abordados en iteraciones anteriores (CK16 §4.3.3.6), en el orden UC, QA, CON, CRN, cada grupo por número.

Recorrido del modelo de datos: <`analysis/walkthrough-<case>.md`, o "No aplica: el modelo no cambió">

Revisión: <Se logró el objetivo / qué queda y para qué iteración.>
```

Rutas de imágenes: relativas al archivo. Las de la iteración apuntan a su propia carpeta `diagrams/images/`, nunca a `diagrams/` de la raíz (salvo el contexto en la iteración 1, que es entrada y no se modifica).

## `adr/ADR-xxx.md`

```markdown
# ADR-xxx — <Título de la decisión>
Estado: propuesto | aprobado | reemplazado por ADR-yyy (AAAA-MM-DD)
Fecha: AAAA-MM-DD · Iteración: <ronda.iteración> · Reemplaza a: <ADR-zzz, si aplica>
Decidió: <arquitecto o equipo, con nombres>
Evidencia: <drivers, visita, formato del cliente, PA-xx respondida>

## Contexto
<Qué drivers fuerzan esta decisión, citando sus IDs, y los supuestos que la condicionan.>

## Alternativas
### 1. <Título>
- Descripción:
- Ventajas:
- Desventajas:

### 2. <Título> (elegida)
- Descripción:
- Ventajas:
- Desventajas:

## Decisión
<Qué se decidió.>

## Consecuencias
<Implicaciones, incluidas las que dejan algo pendiente.>
```

Reglas: mínimo 2 alternativas, cada una con descripción, ventajas y desventajas; la elegida marcada "(elegida)"; campos en este orden. Un ADR aprobado no se reescribe: solo cambia su línea de estado cuando otro lo reemplaza.
