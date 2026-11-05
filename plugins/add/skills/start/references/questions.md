# Preguntas abiertas (`questions.md`)

Referencia de `start`. Se lee cuando una sección registra una pregunta, cuando el arquitecto prepara una reunión o cuando trae respuestas.

La arquitectura se diseña sobre cómo funciona realmente el proceso, y eso no siempre lo sabe el arquitecto: lo saben quienes lo operan. Lo que no se sabe todavía no se inventa ni se le pide al arquitecto que lo decida: se registra como pregunta, se avanza con un supuesto provisional visible y se vuelve sobre ello cuando haya respuesta. Todas las secciones escriben en el mismo archivo, para que el arquitecto tenga una sola lista para llevar a la reunión.

**A quién se pregunta: siempre según el proyecto en curso.** Los interesados salen de `drivers.md` (actores, contexto, restricciones) o del arquitecto: el cliente, un área de negocio, el equipo legal, el proveedor, el usuario final. Nunca se usa un nombre genérico ni el de otro proyecto. Si no está claro quién tiene la respuesta, se le pregunta al arquitecto.

**Qué es pregunta y qué es decisión:**
- **Hecho del dominio**: cómo se trabaja hoy, reglas de negocio, volúmenes, formatos, normas internas, excepciones. Lo sabe un interesado. Si el arquitecto no lo sabe con certeza, se ofrece: "¿Lo sabes, o lo dejamos como pregunta para <interesado del proyecto>?". Con la segunda, se registra y se sigue.
- **Decisión de arquitectura**: cómo resuelve el sistema ese hecho. La toma el arquitecto con alternativas, en el paso 4 de una iteración. Si la decisión depende de un hecho sin confirmar, se toma con el supuesto provisional y se anota en "Afecta" de la pregunta.

Formato de `questions.md` (redactado en el lenguaje de quien va a responder, sin términos técnicos, para que el arquitecto lo pueda imprimir y llevar):

```markdown
# Preguntas abiertas — <Sistema>
Actualizado: AAAA-MM-DD

Mientras no haya respuesta, el diseño avanza con el supuesto indicado en cada pregunta.

## Abiertas
### PA-01 — <tema en pocas palabras>
- Pregunta: <en el lenguaje del interesado>
- Para: <interesado del proyecto>
- Mientras tanto suponemos: <supuesto provisional>
- Afecta: <AS-x, ADR-00x, iteración, vista o entidad>
- Surgió en: <sección, o iteración y paso>, AAAA-MM-DD

## Respondidas
### PA-02 — <tema>
- Pregunta: …
- Respuesta (AAAA-MM-DD, <quién>): …
- Cambios: <qué se ajustó y en qué iteración o ronda, o "Ninguno: se confirmó el supuesto">
```

Reglas:
- Una pregunta por tema; si dos secciones preguntan lo mismo, se suma a "Afecta" de la que ya existe.
- Los supuestos de `drivers.md` que dependen de una pregunta llevan su ID en el estado: "Por validar con <interesado> (PA-01)".
- Las preguntas abiertas no impiden aprobar una sección ni cerrar una iteración: al pedir la aprobación se dice cuántas la afectan, y el arquitecto aprueba sabiendo que esos puntos son provisionales.
- **Proyectos con preguntas dispersas.** Si no existe `questions.md` pero hay preguntas en otros archivos, proponer reunirlas en `questions.md` y dejar en su lugar solo la referencia al ID. Hacerlo solo con aprobación.

### Preparar la reunión

Si el arquitecto pide sus preguntas pendientes ("qué tengo que preguntar", "voy a visitar al cliente"), entregar las abiertas agrupadas por "Para" y por tema, en el lenguaje del interesado, sin IDs técnicos en el texto de la pregunta, listas para llevar. Si alguna se responde mejor viendo el proceso (un formato, una planilla, un registro real), sugerir pedir una copia como insumo.

### Registrar las respuestas

Cuando el arquitecto trae respuestas ("ya hablé con…", "me confirmaron…"):

1. Recorrer las preguntas abiertas para ese interesado, de 2 a 3 por turno, y anotar cada respuesta tal como la cuenta el arquitecto.
2. Por cada respuesta, decir qué pasa: se confirma el supuesto (el AS pasa a "Validado") o cambia algo. Si cambia, mostrar en una tabla corta qué afecta (drivers, decisiones de qué iteraciones, vistas) antes de tocar nada.
3. Decidir con el arquitecto cómo se atiende según "Cambios después de aprobar" de SKILL.md: corrección, iteración nueva o ronda nueva. Nunca se editan iteraciones cerradas.
4. Mover la pregunta a "Respondidas" con su respuesta y sus cambios. Si la respuesta abre una pregunta nueva, se registra como otra PA.
