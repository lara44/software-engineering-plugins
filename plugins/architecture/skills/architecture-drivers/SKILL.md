---
name: architecture-drivers
description: Usar para levantar los drivers arquitectónicos de un proyecto desde cero (contexto, objetivos, funcionalidades, restricciones, supuestos y árbol de utilidad con escenarios de calidad) mediante una entrevista breve con el arquitecto, produciendo drivers.md.
---

# Levantamiento de drivers arquitectónicos

Fase 1 del asistente de arquitectura. Produce `drivers.md`, la base de todas las fases siguientes (decisiones, vistas, validación, documento).

## Principios (no negociables)

1. **El arquitecto decide; Claude redacta.** El arquitecto responde en frases cortas y corrige. Claude convierte eso en funcionalidades, restricciones, supuestos y escenarios. El arquitecto nunca llena formatos.
2. **Breve.** Meta: 20–30 minutos de conversación y un `drivers.md` de 2–3 páginas. Mínimo suficiente, no exhaustivo.
3. **Proponer en vez de preguntar en abierto.** Mal: "¿Qué disponibilidad necesitas?". Bien: "Propongo 99,5 % en horario laboral porque la operación es de oficina. ¿Sí o ajusto?".
4. **De 2 a 3 preguntas por turno**, y solo sobre lo que falta.
5. **Nunca bloquear.** Si el arquitecto no sabe algo, se registra como supuesto (con su riesgo) o como pregunta abierta, y se sigue.
6. **No inventar.** Todo dato lleva su origen: `[Arquitecto]`, `[Doc: <nombre>]` o `[Propuesta]` (propuesto por Claude, pendiente de validar). Una inferencia hecha a partir de un documento es `[Propuesta]`, no `[Doc]`: `[Doc]` solo cuando el documento lo dice explícitamente.
7. **Respetar lo que ya decidieron los insumos.** Si los documentos ya definen atributos de calidad, objetivos o alcance, se toman tal cual. Claude puede sugerir agregados, pero separados y marcados como `[Propuesta]`, nunca mezclados ni reemplazando lo existente.
8. **No decidir arquitectura en esta fase.** Si el arquitecto menciona estilo, patrones o tecnología: si es impuesto (cliente, normativa, plataforma obligatoria), va como restricción; si es preferencia, va en "Preguntas abiertas" marcado `(para fase de decisiones)`.

## Paso 0: Revisar qué existe

1. Si ya hay un `drivers.md` en la carpeta del proyecto, retomarlo: mostrar en 3–4 líneas qué está completo y qué falta, y continuar desde ahí.
2. Buscar insumos en la carpeta (por ejemplo `insumos/`, o cualquier .md, .pdf, .docx, .xlsx, actas, transcripciones). Si existe un subagente `architecture-extractor`, delegarle la lectura. Si no existe, leerlos directamente.
3. Pre-llenar con lo que digan los insumos (origen `[Doc: …]`) y armar la lista de vacíos.
4. Decirle al arquitecto en 2–3 líneas qué se encontró y cuántas rondas de preguntas faltan aproximadamente. Si la carpeta está vacía, decirlo y arrancar la entrevista desde el bloque 1.

## Entrevista: orden de bloques

El orden importa: cada bloque alimenta las propuestas del siguiente. Saltar un bloque si los insumos ya lo cubren.

1. **Problema y contexto.** Qué pasa hoy, a quién le duele y por qué ahora.
2. **Objetivos.** Máximo 3, con cómo se sabría que se lograron.
3. **Actores y sistemas externos.** Proponer la lista a partir de lo dicho y pedir corrección.
4. **Funcionalidades (casos de uso, según ADD).** Pedir los principales casos de uso (5–10) en lenguaje de negocio. Cada uno se nombra con verbo + objeto ("Registrar recepción") y se describe en una línea que nombra al actor ("El personal de bodega registra…"). Luego Claude propone cuáles son **funcionalidad primaria** (los que condicionan la arquitectura), con su porqué, y pide confirmación. Criterios para ser primario: integración externa, volumen o frecuencia alta, lógica de negocio crítica o compleja, datos sensibles o normativa, disponibilidad crítica, cambio frecuente, origen de un atributo de calidad.
5. **Restricciones.** Preguntar por cliente, normativa, plataforma o tecnología obligatoria, presupuesto, plazos y equipo. Clasificar cada una como técnica, de negocio o normativa.
6. **Supuestos.** Claude los propone a partir de todo lo anterior (volúmenes, usuarios, conectividad, disponibilidad de terceros), cada uno con su riesgo si resulta falso. El arquitecto confirma, corrige o descarta. Si el dato lo sabe el cliente y no el arquitecto ("no sé"), el supuesto queda sin validar y se agrega a "Preguntas abiertas" como pregunta para el cliente.
7. **Árbol de utilidad (ATAM).** Los atributos de calidad se organizan como árbol de utilidad con tres niveles obligatorios: atributo → refinamiento → escenario. Se presenta como tabla (ver formato). Se construye en este orden:
   - **Atributos (el "qué").** Si los insumos ya los definen, se respetan tal cual, con sus nombres. Si no, Claude deriva candidatos de los bloques anteriores (por ejemplo, datos sensibles → seguridad; integración externa → interoperabilidad) y el arquitecto elige de 3 a 6.
   - **Refinamientos (obligatorios).** Cada atributo se descompone en uno o más refinamientos. El refinamiento nombra el **aspecto del atributo** que importa en este sistema: responde "¿trazabilidad de qué?", "¿disponibilidad de qué?". Se redacta como un sustantivo abstracto, no como un resumen del escenario. Bien: "Procedencia de los productos", "Aislamiento de fallos", "Configurabilidad de reglas de negocio". Mal: "Origen de lo entregado en < 5 s" (eso es el escenario). Un aspecto que parezca otro atributo pero sirva al mismo propósito va como refinamiento de ese atributo, no como atributo nuevo (por ejemplo, "Integridad del historial" bajo trazabilidad). Claude los propone; el arquitecto los ajusta.
   - **Escenarios (la prueba medible de cada refinamiento).** Al menos un escenario por refinamiento. No preguntar en abstracto: proponer el escenario y que el arquitecto ajuste. Redactarlo siguiendo las reglas de "Redacción de escenarios".
   - **Doble prioridad por escenario**, cada una Alta (A), Media (M) o Baja (B): **importancia para el negocio** y **dificultad o riesgo técnico**. Claude propone ambas con una razón de una línea; el arquitecto las fija. Los escenarios (A, A) son los que más guían el diseño y se señalan como tales.
   - **Normas de referencia.** Usar los nombres de ISO/IEC 25010 para atributos del producto. Si el atributo es sobre los datos (por ejemplo, trazabilidad de registros, exactitud, completitud), anclarlo en ISO/IEC 25012. Si no encaja en ninguna, dejarlo como atributo propio del dominio con su justificación. No forzar mapeos.
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
- **Medida:** cómo se mide **esa respuesta a ese estímulo** (tiempo, porcentaje, conteo, esfuerzo). No mezclar con la meta de un objetivo de negocio: por ejemplo, "100 % de los kg entregados vinculados a una entrada" es la medida del objetivo O2 y va en Contexto, no en el escenario de consulta. Una sola medida principal; si hay dos, deben medir la misma respuesta.

Cada ronda tiene esta forma:
- 1–2 líneas de lo entendido hasta ahora.
- 2–3 preguntas, cada una con una propuesta concreta para aceptar o ajustar.

## Escritura incremental

Actualizar `drivers.md` al cerrar cada bloque, no solo al final, para que nada se pierda si la sesión se interrumpe. Mantener `Estado: borrador` hasta la aprobación.

## Formato de drivers.md

```markdown
# Drivers — <Sistema>
Estado: borrador | aprobado · Fecha: AAAA-MM-DD

## Contexto
- Problema: (2–3 líneas)
- Objetivos: (máx. 3, con cómo se mide si aplica)
- Actores: rol → qué hace
- Sistemas externos: sistema → para qué

## Funcionalidades
| Caso de uso | Descripción |
|-------------|-------------|
| **UC-01** <Verbo + objeto> | <Actor> <qué hace>, en una línea. |
| **UC-02** <Verbo + objeto> | … |
| UC-0n <Verbo + objeto> | … (no primario: sin negrita) |

**Funcionalidad primaria:** UC-01 a UC-0x. <Una o dos frases que agrupan los casos por la razón por la que son primarios, por ejemplo: "originan la trazabilidad (UC-01, UC-05), concentran la lógica de negocio crítica (UC-02, UC-03) o están sujetos a cambios frecuentes (UC-06)">. <Casos no primarios> no son primarios.

Origen: <de dónde salen los casos de uso>.

## Restricciones
| ID | Restricción | Tipo (técnica/negocio/normativa) | Origen |
|----|-------------|----------------------------------|--------|
| R-01 | | | |

## Supuestos
| ID | Supuesto | Riesgo si es falso | Validado |
|----|----------|--------------------|----------|
| S-01 | | | Sí/No |

## Árbol de utilidad
Prioridad: (importancia para el negocio, dificultad técnica) · A = alta, M = media, B = baja

| Atributo | Refinamiento | Escenario | Prioridad |
|----------|--------------|-----------|-----------|
| **<Atributo 1>** (ISO/IEC 25010 – … / ISO/IEC 25012 – … / propio del dominio) | <Refinamiento 1.1> | QA-01: Cuando [fuente] [estímulo], en [ambiente], el sistema [respuesta] en/con [medida]. | (A, A) |
| | <Refinamiento 1.2> | QA-02: Cuando … | (A, M) |
| **<Atributo 2>** (…) | <Refinamiento 2.1> | QA-03: Cuando … | (M, M) |

Escenarios que guían el diseño (A, A): QA-xx
Origen: <de dónde salen atributos y escenarios>; refinamientos y normas <origen>; prioridades [Arquitecto].

Reglas de la tabla:
- Atributo y refinamiento se escriben una sola vez, en la primera fila de su grupo; las filas siguientes del mismo grupo dejan la celda vacía (en Word se combinan verticalmente).
- La norma se nombra junto al atributo, una vez.
- Dentro de cada atributo, ordenar por prioridad, (A, A) primero.
- La columna Escenario lleva la frase completa, nunca solo un título.

Atributos sugeridos no definidos por el arquitecto ni por los insumos: (lista aparte, marcados `[Propuesta]`)

## Escenarios de calidad
### QA-01 — <nombre descriptivo>
- Atributo: <atributo> › <refinamiento> · (A, A)
- Fuente:
- Estímulo:
- Ambiente:
- Artefacto:
- Respuesta:
- Medida:

(El origen no se repite en cada ficha: va una vez debajo de la tabla. Solo se anota en una ficha si difiere del general.)

## Preguntas abiertas
- 
```

Reglas del formato:
- Casos de uso en lenguaje de negocio, sin términos técnicos. Solo dos columnas (Caso de uso, Descripción), como en ADD: el actor va dentro de la descripción y la razón de ser primario va en el párrafo "Funcionalidad primaria", no en columnas. Los casos primarios van en negrita.
- Cada escenario de calidad tiene una medida concreta (número, umbral o condición verificable) y sigue las reglas de "Redacción de escenarios".
- Una línea por campo; nada de párrafos largos.

## Criterio de cierre

Antes de pedir aprobación, verificar:
- [ ] Problema, objetivos y actores definidos.
- [ ] Casos de uso en formato ADD (Caso de uso, Descripción) y párrafo de funcionalidad primaria con su porqué.
- [ ] Cada objetivo tiene al menos un caso de uso primario que lo soporta.
- [ ] Todo actor nombrado en una descripción está en la lista de actores de Contexto, y viceversa.
- [ ] Restricciones separadas de supuestos.
- [ ] Árbol de utilidad con 3 a 6 atributos; si los insumos ya los definían, se respetaron.
- [ ] Cada atributo tiene al menos un refinamiento, y cada refinamiento al menos un escenario.
- [ ] Los refinamientos nombran un aspecto del atributo, no resumen el escenario.
- [ ] Cada escenario aparece como frase completa en el árbol ("Cuando…, en…, el sistema… en/con…") y como ficha de 6 partes con el mismo contenido.
- [ ] Ninguna ficha tiene artefacto genérico ("sistema completo"), respuesta vacía ("el servicio responde") ni una medida que en realidad es la meta de un objetivo.
- [ ] La tabla no repite atributo ni refinamiento en cada fila.
- [ ] Cada escenario tiene su doble prioridad (negocio, dificultad) fijada por el arquitecto, y los (A, A) están señalados.
- [ ] Las medidas son coherentes con las restricciones (por ejemplo, el alcance de un prototipo).
- [ ] Ningún supuesto de riesgo alto sin validar; si queda alguno, está en "Preguntas abiertas".
- [ ] Los datos con origen `[Propuesta]` fueron mostrados al arquitecto.

Si algo falla, decirlo en una línea y preguntar si se resuelve ahora o se deja como pregunta abierta.

## Cierre

1. Mostrar un resumen de 5–8 líneas: objetivos, funcionalidad primaria, restricciones clave, atributos del árbol de utilidad y los escenarios (A, A), más el número de preguntas abiertas.
2. Pedir aprobación explícita. Con la aprobación, cambiar a `Estado: aprobado` y poner la fecha.
3. Indicar que la siguiente fase es la de decisiones de arquitectura, que parte de este archivo.
