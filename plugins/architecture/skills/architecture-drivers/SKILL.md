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
4. **Funcionalidades.** Pedir las principales (5–10) en lenguaje de negocio. Luego Claude marca cuáles son arquitectónicamente significativas, con su porqué, y pide confirmación. Criterios de significancia: integración externa, volumen o tiempo real, lógica de negocio crítica o compleja, datos sensibles o normativa, alta disponibilidad, crecimiento o multi-tenant.
5. **Restricciones.** Preguntar por cliente, normativa, plataforma o tecnología obligatoria, presupuesto, plazos y equipo. Clasificar cada una como técnica, de negocio o normativa.
6. **Supuestos.** Claude los propone a partir de todo lo anterior (volúmenes, usuarios, conectividad, disponibilidad de terceros), cada uno con su riesgo si resulta falso. El arquitecto confirma, corrige o descarta. Si el dato lo sabe el cliente y no el arquitecto ("no sé"), el supuesto queda sin validar y se agrega a "Preguntas abiertas" como pregunta para el cliente.
7. **Árbol de utilidad (ATAM).** Los atributos de calidad se organizan como árbol de utilidad: Utilidad → atributo → refinamiento → escenario. Se construye en este orden:
   - **Atributos (el "qué").** Si los insumos ya los definen, se respetan tal cual. Si no, Claude deriva candidatos de los bloques anteriores (por ejemplo, datos sensibles → seguridad; integración externa → interoperabilidad) y el arquitecto elige de 3 a 6.
   - **Refinamientos (qué aspecto concreto del atributo).** Claude los propone a partir de las funcionalidades significativas. Un aspecto que parezca otro atributo pero sirva al mismo propósito va como refinamiento, no como atributo nuevo (por ejemplo, "no sobrescribir registros" como refinamiento de trazabilidad).
   - **Escenarios (la prueba medible de cada refinamiento).** Al menos un escenario por refinamiento, con medida concreta. No preguntar en abstracto: proponer el escenario y que el arquitecto ajuste.
   - **Doble prioridad por escenario**, cada una Alta (A), Media (M) o Baja (B): **importancia para el negocio** y **dificultad o riesgo técnico**. Claude propone ambas con una razón de una línea; el arquitecto las fija. Los escenarios (A, A) son los que más guían el diseño y se señalan como tales.
   - **Normas de referencia.** Usar los nombres de ISO/IEC 25010 para atributos del producto. Si el atributo es sobre los datos (por ejemplo, trazabilidad de registros, exactitud, completitud), anclarlo en ISO/IEC 25012. Si no encaja en ninguna, dejarlo como atributo propio del dominio con su justificación. No forzar mapeos.
   - **Medidas coherentes con las restricciones.** Si una restricción limita el alcance (por ejemplo, un prototipo), la medida debe ser realista para ese alcance o aclarar que aplica al diseño objetivo.

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
| ID | Funcionalidad | ¿Significativa? | Por qué | Origen |
|----|---------------|-----------------|---------|--------|
| F-01 | | Sí/No | | [Arquitecto] |

## Restricciones
| ID | Restricción | Tipo (técnica/negocio/normativa) | Origen |
|----|-------------|----------------------------------|--------|
| R-01 | | | |

## Supuestos
| ID | Supuesto | Riesgo si es falso | Validado |
|----|----------|--------------------|----------|
| S-01 | | | Sí/No |

## Árbol de utilidad
Prioridad de cada escenario: (importancia para el negocio, dificultad técnica), con A/M/B.

| Atributo | Norma de referencia | Refinamiento | Escenario | Prioridad | Origen |
|----------|---------------------|--------------|-----------|-----------|--------|
| <atributo> | ISO 25010 – <característica/subcaracterística> · ISO 25012 – <característica> · o propio del dominio | <aspecto concreto> | QA-01 — <resumen en una línea> | (A, A) | |

Escenarios (A, A): QA-xx, QA-yy

Atributos sugeridos no definidos por el arquitecto ni por los insumos: (lista aparte, marcados `[Propuesta]`)

## Escenarios de calidad
### QA-01 — <nombre descriptivo> · Atributo: <atributo> › <refinamiento> · Prioridad: (A, A)
- Estímulo:
- Fuente:
- Ambiente:
- Artefacto:
- Respuesta:
- Medida:
- Origen:

## Preguntas abiertas
- 
```

Reglas del formato:
- Funcionalidades en lenguaje de negocio, sin términos técnicos.
- Cada escenario de calidad tiene una medida concreta (número, umbral o condición verificable).
- Cada funcionalidad significativa se puede vincular a un objetivo.
- Una línea por campo; nada de párrafos largos.

## Criterio de cierre

Antes de pedir aprobación, verificar:
- [ ] Problema, objetivos y actores definidos.
- [ ] Al menos una funcionalidad significativa, cada una vinculada a un objetivo.
- [ ] Restricciones separadas de supuestos.
- [ ] Árbol de utilidad con 3 a 6 atributos; si los insumos ya los definían, se respetaron.
- [ ] Cada atributo tiene al menos un refinamiento y cada refinamiento al menos un escenario con medida concreta.
- [ ] Cada escenario tiene su doble prioridad (negocio, dificultad) fijada por el arquitecto, y los (A, A) están señalados.
- [ ] Las medidas son coherentes con las restricciones (por ejemplo, el alcance de un prototipo).
- [ ] Ningún supuesto de riesgo alto sin validar; si queda alguno, está en "Preguntas abiertas".
- [ ] Los datos con origen `[Propuesta]` fueron mostrados al arquitecto.

Si algo falla, decirlo en una línea y preguntar si se resuelve ahora o se deja como pregunta abierta.

## Cierre

1. Mostrar un resumen de 5–8 líneas: objetivos, funcionalidades significativas, restricciones clave, atributos del árbol de utilidad y los escenarios (A, A), más el número de preguntas abiertas.
2. Pedir aprobación explícita. Con la aprobación, cambiar a `Estado: aprobado` y poner la fecha.
3. Indicar que la siguiente fase es la de decisiones de arquitectura, que parte de este archivo.
