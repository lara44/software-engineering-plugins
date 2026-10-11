---
name: architecture-drivers
description: Usar para levantar los drivers arquitectónicos de un proyecto desde cero (contexto, objetivos, casos de uso, restricciones, supuestos y árbol de utilidad con escenarios de calidad) mediante una entrevista breve con el arquitecto, produciendo drivers.md según ADD y ATAM.
---

# Levantamiento de drivers arquitectónicos

Fase 1 del asistente de arquitectura. Produce `drivers.md`, la base de todas las fases siguientes (decisiones, vistas, validación, documento).

**Marco metodológico:** se diseña con ADD y se evalúa con ATAM. Los drivers son los insumos de ADD (funcionalidad primaria, escenarios de calidad, restricciones) y los atributos de calidad se organizan con el árbol de utilidad de ATAM, que luego reutiliza la fase de validación. Se usa la convención de IDs de ADD: UC-xx (casos de uso), QA-xx (escenarios de calidad), CON-x (restricciones) y AS-x (supuestos).

## Principios (no negociables)

1. **El arquitecto decide; Claude redacta.** El arquitecto responde en frases cortas y corrige. Claude convierte eso en casos de uso, restricciones, supuestos y escenarios. El arquitecto nunca llena formatos.
2. **Breve.** Meta: 20–30 minutos de conversación y un `drivers.md` de 2–3 páginas. Mínimo suficiente, no exhaustivo.
3. **Proponer en vez de preguntar en abierto.** Mal: "¿Qué disponibilidad necesitas?". Bien: "Propongo 99,5 % en horario laboral porque la operación es de oficina. ¿Sí o ajusto?".
4. **De 2 a 3 preguntas por turno**, y solo sobre lo que falta.
5. **Nunca bloquear.** Si el arquitecto no sabe algo, se registra como supuesto por validar o como pregunta abierta, y se sigue.
6. **No inventar.** Lo que Claude propone o infiere (y no dijo el arquitecto ni dicen explícitamente los insumos) se marca en línea con `[Propuesta]` mientras el archivo está en borrador. No se usan otras etiquetas de origen ni líneas "Origen:".
7. **Respetar lo que ya decidieron los insumos.** Si los documentos ya definen atributos de calidad, objetivos o alcance, se toman tal cual, con sus nombres. Claude puede sugerir agregados, pero separados y marcados `[Propuesta]`, nunca mezclados ni reemplazando lo existente.
8. **No decidir arquitectura en esta fase.** Si el arquitecto menciona estilo, patrones o tecnología: si es impuesto (cliente, normativa, plataforma obligatoria), va como restricción; si es preferencia, va en "Preguntas abiertas" marcado `(para fase de decisiones)`.

## Paso 0: Revisar qué existe

1. Si ya hay un `drivers.md` en la carpeta del proyecto, retomarlo: revisarlo contra el formato y el criterio de cierre de esta skill, convertirlo si está en un formato anterior, y mostrar en 3–4 líneas qué está completo y qué falta.
2. Buscar insumos en la carpeta (por ejemplo `insumos/`, o cualquier .md, .pdf, .docx, .xlsx, actas, transcripciones). Si existe un subagente `architecture-extractor`, delegarle la lectura. Si no existe, leerlos directamente.
3. Pre-llenar con lo que digan los insumos y armar la lista de vacíos. Registrar los insumos una sola vez, en la línea "Insumos:" del encabezado.
4. Decirle al arquitecto en 2–3 líneas qué se encontró y cuántas rondas de preguntas faltan aproximadamente. Si la carpeta está vacía, decirlo y arrancar la entrevista desde el bloque 1.

## Entrevista: orden de bloques

El orden importa: cada bloque alimenta las propuestas del siguiente. Saltar un bloque si los insumos ya lo cubren.

Cada ronda tiene esta forma:
- 1–2 líneas de lo entendido hasta ahora.
- 2–3 preguntas, cada una con una propuesta concreta para aceptar o ajustar.

1. **Contexto.** Qué pasa hoy, a quién le duele y por qué ahora. Se escribe como un solo párrafo, sin cifras de volumen (lo que importe de volumen o carga va como supuesto).
2. **Objetivos.** Máximo 3, cada uno con cómo se sabría que se logró. Sin IDs.
3. **Actores y sistemas externos.** Proponer la lista a partir de lo dicho y pedir corrección. Formato "Nombre: qué hace" (dos puntos, no flechas).
4. **Casos de uso (según ADD).** Pedir los principales (5–10) en lenguaje de negocio. Cada uno se nombra con verbo + objeto ("Registrar recepción") y se describe en una línea que nombra al actor ("El personal de bodega registra…"). Luego Claude propone cuáles son **funcionalidad primaria** (los que condicionan la arquitectura), con su porqué, y pide confirmación. Criterios para ser primario: integración externa, volumen o frecuencia alta, lógica de negocio crítica o compleja, datos sensibles o normativa, disponibilidad crítica, cambio frecuente, origen de un atributo de calidad.
5. **Restricciones (según ADD).** Una restricción es una decisión ya tomada que el arquitecto no puede negociar. Preguntar por cliente, normativa, plataforma o tecnología obligatoria, presupuesto, plazos y equipo. Cada una se escribe como una frase que dice qué limita al diseño. No es restricción: un supuesto (se cree cierto pero puede no serlo), un atributo de calidad (tiene grados y se mide) ni una regla de negocio que no limita la arquitectura.
6. **Supuestos.** Un supuesto es algo que se cree cierto pero no está confirmado, y que si resulta falso afecta el diseño. Claude los propone a partir de todo lo anterior (volúmenes, usuarios, conectividad, datos existentes, disponibilidad de terceros), cada uno con su impacto si resulta falso. El arquitecto confirma, corrige o descarta. Si el dato lo sabe el cliente y no el arquitecto ("no sé"), el supuesto queda con estado "Por validar con <quién>"; no se duplica en "Preguntas abiertas". No es supuesto una regla de cálculo o de negocio (por ejemplo, cómo se convierte una unidad): eso va en "Preguntas abiertas" marcado `(para el modelo de dominio)`.
7. **Árbol de utilidad (ATAM).** Los atributos de calidad se organizan con tres niveles obligatorios: atributo → refinamiento → escenario. Se construye en este orden:
   - **Atributos (el "qué").** Si los insumos ya los definen, se respetan tal cual. Si no, Claude deriva candidatos de los bloques anteriores (por ejemplo, datos sensibles → seguridad; integración externa → interoperabilidad) y el arquitecto elige de 3 a 6.
   - **Refinamientos (obligatorios).** Cada atributo se descompone en uno o más refinamientos. El refinamiento nombra el **aspecto del atributo** que importa en este sistema: responde "¿trazabilidad de qué?", "¿disponibilidad de qué?". Se redacta como un sustantivo abstracto, no como un resumen del escenario. Bien: "Procedencia de los productos", "Aislamiento de fallos", "Configurabilidad de reglas de negocio". Mal: "Origen de lo entregado en < 5 s" (eso es el escenario). Un aspecto que parezca otro atributo pero sirva al mismo propósito va como refinamiento de ese atributo, no como atributo nuevo (por ejemplo, "Integridad del historial" bajo trazabilidad).
   - **Escenarios (la prueba medible de cada refinamiento).** Al menos uno por refinamiento. Proponer el escenario y que el arquitecto ajuste, siguiendo "Redacción de escenarios".
   - **Doble prioridad por escenario**, cada una Alta (A), Media (M) o Baja (B): **importancia para el negocio** y **dificultad o riesgo técnico**. Claude propone ambas con una razón de una línea; el arquitecto las fija. Los escenarios (A, A) son los que más guían el diseño y se señalan.
   - **Normas de referencia.** ISO/IEC 25010 para atributos del producto. Si el atributo es sobre los datos (trazabilidad de registros, exactitud, completitud), ISO/IEC 25012. Si no encaja en ninguna, atributo propio del dominio con su justificación. No forzar mapeos.
   - **Medidas coherentes con las restricciones.** Si una restricción limita el alcance (por ejemplo, un prototipo), la medida debe ser realista para ese alcance o aclarar que aplica al diseño objetivo.

## Redacción de escenarios

Cada escenario se escribe dos veces, con el mismo contenido: como **frase completa** en el árbol de utilidad y como **ficha de 6 partes** debajo. El árbol debe poder leerse y evaluarse sin abrir las fichas.

**Frase del árbol.** Plantilla obligatoria:

> QA-xx: Cuando [fuente] [estímulo], en [ambiente], el sistema [respuesta] en/con [medida].

Ejemplo: "QA-01: Cuando el coordinador consulta el origen de un producto entregado, en operación normal, el sistema muestra donante, fecha de recepción, soporte y remisión en menos de 5 s."

Nunca poner solo un título ("QA-01 Origen de un producto") en la columna Escenario.

**Reglas por campo de la ficha:**
- **Fuente:** quién o qué origina el estímulo, concreto (un rol, un sistema, "falla interna", "ente externo", "equipo de desarrollo").
- **Estímulo:** un evento puntual, con verbo ("consulta", "corrige", "deja de responder", "cambia la estructura"). No un estado.
- **Ambiente:** la condición del sistema cuando llega el estímulo: "operación normal", "carga pico", "jornada de recepción", "falla de un componente", "puesta en marcha", "mantenimiento". Para modificabilidad usar "mantenimiento" o "tiempo de diseño", no "desarrollo".
- **Artefacto:** la parte específica del sistema que recibe el estímulo (un componente, un módulo, un conjunto de datos). Nunca "sistema completo" ni "el sistema".
- **Respuesta:** lo que el sistema hace, observable y verificable. Nunca respuestas vacías como "el servicio responde" o "funciona correctamente".
- **Medida:** cómo se mide **esa respuesta a ese estímulo** (tiempo, porcentaje, conteo, esfuerzo). No mezclar con la meta de un objetivo de negocio: por ejemplo, "100 % de los kg entregados vinculados a una entrada" es la medida de un objetivo y va en Objetivos, no en el escenario de consulta. Una sola medida principal; si hay dos, deben medir la misma respuesta.

## Escritura incremental

Actualizar `drivers.md` al cerrar cada bloque, no solo al final, para que nada se pierda si la sesión se interrumpe. Mantener `Estado: borrador` hasta la aprobación.

## Formato de drivers.md

```markdown
# Drivers — <Sistema>
Estado: borrador | aprobado · Fecha: AAAA-MM-DD

Insumos: <archivo 1> · <archivo 2>

## Contexto
<Un solo párrafo: qué pasa hoy, a quién le duele y por qué ahora.>

Objetivos:
- <Objetivo>. Medida: <cómo se sabe que se logró>.

Actores:
- <Actor>: <qué hace con el sistema>.

Sistemas externos:
- <Sistema>: <para qué se relaciona>.

## Funcionalidades
| Caso de uso | Descripción |
|-------------|-------------|
| **UC-01** <Verbo + objeto> | <Actor> <qué hace>, en una línea. |
| UC-0n <Verbo + objeto> | … (no primario: sin negrita) |

**Funcionalidad primaria:** UC-01 a UC-0x. <Una o dos frases que agrupan los casos por la razón por la que son primarios>. <Casos no primarios> no son primarios.

Fuera de alcance: <si aplica>.

## Restricciones
| ID | Restricción |
|----|-------------|
| CON-1 | <Qué limita al diseño, en una frase>. |

## Supuestos
| ID | Supuesto | Impacto si es falso | Estado |
|----|----------|---------------------|--------|
| AS-1 | <Lo que se cree cierto>. | <Qué pasa con el diseño si no lo es>. | Validado / Por validar con <quién> |

## Árbol de utilidad
Prioridad: (importancia para el negocio, dificultad técnica) · A = alta, M = media, B = baja

| Atributo | Refinamiento | Escenario | Prioridad |
|----------|--------------|-----------|-----------|
| **<Atributo 1>** (ISO/IEC 25010 – … / ISO/IEC 25012 / propio del dominio) | <Refinamiento 1.1> | QA-01: Cuando [fuente] [estímulo], en [ambiente], el sistema [respuesta] en/con [medida]. | (A, A) |
| | <Refinamiento 1.2> | QA-02: Cuando … | (A, M) |
| **<Atributo 2>** (…) | <Refinamiento 2.1> | QA-03: Cuando … | (M, M) |

Escenarios que guían el diseño (A, A): QA-xx

## Escenarios de calidad
### QA-01 — <nombre descriptivo>
- Atributo: <atributo> › <refinamiento> · (A, A)
- Fuente:
- Estímulo:
- Ambiente:
- Artefacto:
- Respuesta:
- Medida:

## Preguntas abiertas
- <Pregunta para el cliente o para el equipo>
- (para el modelo de dominio) <Regla de negocio o de cálculo que no es driver>
- (para fase de decisiones) <Preferencia técnica o candidata a ADR>
```

Reglas del formato:
- Convención de IDs de ADD: UC-xx, QA-xx, CON-x, AS-x. Los objetivos no llevan ID.
- Contexto: un párrafo, sin etiquetas ("Problema:") ni cifras de volumen. Listas con "Nombre: descripción", nunca flechas.
- Casos de uso en lenguaje de negocio, sin términos técnicos. Solo dos columnas (Caso de uso, Descripción), como en ADD: el actor va dentro de la descripción y la razón de ser primario va en el párrafo "Funcionalidad primaria". Los primarios en negrita.
- Restricciones en dos columnas (ID, Restricción), sin columna de tipo.
- Supuestos en cuatro columnas; el estado dice con quién se valida. No se repiten en "Preguntas abiertas".
- Árbol de utilidad: atributo y refinamiento se escriben una sola vez, en la primera fila de su grupo (en Word se combinan verticalmente); la norma va junto al atributo; dentro de cada atributo, (A, A) primero; la columna Escenario lleva la frase completa.
- Sin líneas "Origen:" ni etiquetas de documento. Solo `[Propuesta]`, en línea, mientras el archivo está en borrador. Si refinamientos o normas son propuesta, una línea "Refinamientos y normas de referencia: [Propuesta]" debajo de la tabla.
- Una línea por campo; nada de párrafos largos fuera del contexto.

## Criterio de cierre

Antes de pedir aprobación, verificar:
- [ ] Contexto en un párrafo; objetivos (máx. 3, con medida) y actores definidos.
- [ ] Casos de uso en formato ADD y párrafo de funcionalidad primaria con su porqué.
- [ ] Cada objetivo tiene al menos un caso de uso primario que lo soporta.
- [ ] Todo actor nombrado en una descripción está en la lista de actores, y viceversa.
- [ ] Restricciones en formato ADD (CON-x), sin supuestos ni reglas de negocio mezclados.
- [ ] Supuestos en formato AS-x con impacto y estado; sin reglas de cálculo o de negocio mezcladas.
- [ ] Árbol de utilidad con 3 a 6 atributos; si los insumos ya los definían, se respetaron.
- [ ] Cada atributo tiene al menos un refinamiento, y cada refinamiento al menos un escenario.
- [ ] Los refinamientos nombran un aspecto del atributo, no resumen el escenario.
- [ ] Cada escenario aparece como frase completa en el árbol y como ficha de 6 partes con el mismo contenido.
- [ ] Ninguna ficha tiene artefacto genérico, respuesta vacía ni una medida que en realidad es la meta de un objetivo.
- [ ] Cada escenario tiene su doble prioridad fijada por el arquitecto, y los (A, A) están señalados.
- [ ] Las medidas son coherentes con las restricciones.
- [ ] Todos los elementos `[Propuesta]` fueron mostrados al arquitecto.

Si algo falla, decirlo en una línea y preguntar si se resuelve ahora o se deja como pregunta abierta.

## Cierre

1. Mostrar un resumen de 5–8 líneas: objetivos, funcionalidad primaria, restricciones clave, atributos del árbol de utilidad y escenarios (A, A), supuestos por validar y número de preguntas abiertas.
2. Pedir aprobación explícita.
3. Con la aprobación: quitar las marcas `[Propuesta]` de lo aceptado, sacar (o pasar a "Preguntas abiertas") lo que el arquitecto no aceptó, cambiar a `Estado: aprobado` y poner la fecha.
4. Indicar que la siguiente fase es la de decisiones de arquitectura, que parte de este archivo. Los supuestos que queden "Por validar" serán riesgos candidatos en la fase de validación.
