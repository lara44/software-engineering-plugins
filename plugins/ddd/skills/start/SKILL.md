---
name: start
description: Usar para cualquier trabajo de Event Storming o de modelo de dominio en un proyecto - iniciar, retomar o avanzar el taller, revisar un paso después de cambios en los insumos, o registrar respuestas del negocio ("hagamos el Event Storming", "en qué vamos con el Event Storming", "modelo de dominio", "contextos delimitados", "cambió la caracterización", /ddd:start). Muestra en qué paso va el taller, conduce cada paso con su skill y pide aprobación antes de pasar al siguiente.
---

# Orquestador del taller de Event Storming

Conduce al arquitecto por los ocho pasos del taller de Event Storming. El arquitecto no invoca skills: habla con el orquestador, y el orquestador decide qué pieza usar en cada momento.

El orquestador **no hace el trabajo de los pasos**. Su responsabilidad es saber en qué paso va el taller, activar la pieza correcta, hacer respetar los puntos de aprobación, mover los borradores al aprobarse y mantener al arquitecto ubicado.

## Fases

Cada paso del taller es una fase, con su propia aprobación.

| # | Fase | Qué agrega al tablero |
|---|------|------------------------|
| 1 | Eventos | Todos los hechos del negocio, en pasado y sin orden |
| 2 | Línea de tiempo | Los eventos ordenados por recorrido del negocio, con caminos alternos |
| 3 | Comandos | La acción que origina cada evento |
| 4 | Usuarios y sistemas externos | Quién ejecuta cada comando y con qué sistemas se intercambia información |
| 5 | Políticas | Las reglas que validan un comando o reaccionan a un evento |
| 6 | Datos | La información que necesita cada evento |
| 7 | Agregados | Las unidades que protegen las invariantes |
| 8 | Contextos de negocio | Los contextos delimitados, sin línea de tiempo: un óvalo por contexto con sus agregados y sus relaciones |

Todas las fases las ejecuta la skill `storming`, que carga `board` para dibujar. Antes de usarlas, verificar que existen en esta sesión.

## Convención de la carpeta del proyecto

```
<proyecto>/
├── inputs/                       ← documentos de contexto: caracterización, entrevistas, actas, formatos
├── questions.md                  ← lo que hay que confirmar con el negocio
└── domain/
    ├── event-storming.md         ← índice: estado de cada paso y su resumen
    ├── event-storming.json       ← modelo aprobado
    ├── event-storming.drawio     ← tablero aprobado: un solo archivo, una página por paso
    ├── images/step-N.png         ← imagen de cada paso, exportada al aprobarlo
    └── drafts/                   ← solo el paso en curso
        ├── event-storming.json
        └── event-storming.drawio
```

- **El paso en curso vive en `drafts/`.** Al empezar un paso, el modelo y el tablero aprobados se copian a `drafts/`, y ahí se trabaja. Nada de la carpeta principal cambia hasta la aprobación.
- **Las imágenes se generan solo al aprobar.** Mientras el paso está en borrador, el arquitecto lo revisa abriendo `domain/drafts/event-storming.drawio` en su editor (draw.io o la extensión de draw.io para VS Code).
- Si el proyecto también usa el plugin `add`, `questions.md` y `inputs/` son los mismos de ese proceso.

Solo se crea lo que haga falta cuando un paso lo produzca. No se mueven archivos del arquitecto fuera de esta convención.

## Paso 0: Instrucciones del proyecto (la primera vez)

Si `CLAUDE.md` (Claude Code) o `AGENTS.md` (Copilot, OpenCode) no existen o no mencionan el taller, proponer agregar este bloque y escribirlo solo con aprobación:

```markdown
## Modelo de dominio
Este proyecto sigue el taller de Event Storming del plugin `ddd`.
- Para cualquier trabajo del modelo de dominio, empezar con la skill `start`.
- No editar a mano `domain/` ni `questions.md`: cada paso se modifica con su skill. El tablero `.drawio` sí se puede ajustar a mano en el editor.
```

## Paso 1: Detectar el estado

Leer `domain/event-storming.md` y su tabla de pasos. Cada paso está:

- **Pendiente:** no aparece o dice "Pendiente".
- **En curso:** dice "En curso" (su trabajo está en `drafts/`).
- **Aprobado:** dice "Aprobado" con fecha.
- **Por revisar:** estaba aprobado, pero cambió un paso anterior.

El paso actual es el primero que no está aprobado. Si no existe `domain/event-storming.md` pero hay archivos en `drafts/`, el paso 1 está en curso.

Mostrar un tablero corto y decir en una frase cuál es el paso actual:

```
Event Storming: <proyecto>
1. Eventos                        ✔ aprobado
2. Línea de tiempo                ✔ aprobado
3. Comandos                       ● en curso (borrador)
4. Usuarios y sistemas externos   ○ pendiente
5. Políticas                      ○ pendiente
6. Datos                          ○ pendiente
7. Agregados                      ○ pendiente
8. Contextos de negocio           ○ pendiente
Seguimos con los comandos: lo retomo con su skill para revisar qué falta.
```

Debajo, si existe `questions.md`, una línea: "Preguntas abiertas: N (para <interesado>: n)".

Si la carpeta está vacía, decirlo y proponer arrancar por el paso 1. Si hay archivos en `inputs/`, mencionarlos: son la base del paso 1.

El tablero solo informa el estado. **El orquestador no evalúa el contenido de un paso**: eso lo hace la skill del paso con su propio criterio de cierre.

## Paso 2: Ejecutar el paso actual

1. **Siempre cargar `storming`**, también al retomar un paso en curso. La skill revisa el borrador contra su formato, dice qué falta y conduce el paso.
2. Si el paso no tiene borrador, la skill lo abre: copia a `drafts/` el modelo y el tablero aprobados (o los crea en el paso 1).
3. No repetir lo que la skill ya hace: el orquestador no reescribe sus preguntas ni su formato.

## Paso 3: Punto de aprobación

Solo se pide aprobación cuando la skill del paso confirma que su criterio de cierre se cumple y que el tablero del borrador fue revisado visualmente.

1. Mostrar el resumen que entregue la skill y la ruta del borrador (`domain/drafts/event-storming.drawio`) para que el arquitecto lo abra. Decir cuántas preguntas abiertas afectan el paso.
2. Pedir aprobación explícita. Solo cuenta un "apruebo" o equivalente claro ("aprobado", "de acuerdo con el paso"). "Continuar" o "sigamos" no aprueban: se pregunta de nuevo en una línea. El silencio tampoco aprueba.
3. Con la aprobación:
   1. Mover `domain/drafts/event-storming.json` y `domain/drafts/event-storming.drawio` a `domain/`, reemplazando los aprobados (con `git mv` o un movimiento normal si el proyecto no usa git).
   2. Exportar la imagen del paso con la skill de estilo: `domain/images/step-N.png`. En el paso 6, generar también `domain/data.md`.
   3. Borrar `domain/drafts/` si quedó vacío.
   4. Marcar el paso "Aprobado AAAA-MM-DD" en `domain/event-storming.md`.
   5. Mostrar el tablero actualizado y proponer el paso siguiente.

Sin aprobación no se avanza. Si el arquitecto pide cambios, se vuelve a la skill del paso, sobre el mismo borrador.

Si no se puede exportar la imagen (no hay draw.io Desktop), el paso se aprueba igual y se dice en una línea cómo exportarla desde el editor; `event-storming.md` anota "imagen pendiente".

## Preguntas abiertas (`questions.md`)

Lo que solo sabe el negocio no se inventa ni se le pide al arquitecto que lo decida: se registra como pregunta, se avanza con un supuesto visible (en el tablero, con el borde de "por confirmar") y se vuelve sobre ello cuando haya respuesta.

```markdown
# Preguntas abiertas — <Sistema>
Actualizado: AAAA-MM-DD

## Abiertas
### PA-01 — <tema en pocas palabras>
- Pregunta: <en el lenguaje de quien responde>
- Para: <interesado del proyecto>
- Mientras tanto suponemos: <supuesto>
- Afecta: <paso y elementos del tablero>
- Surgió en: Event Storming, paso <n>, AAAA-MM-DD

## Respondidas
### PA-02 — <tema>
- Pregunta: …
- Respuesta (AAAA-MM-DD, <quién>): …
- Cambios: <qué se ajustó, o "Ninguno: se confirmó el supuesto">
```

- Si `questions.md` ya existe (por ejemplo, del plugin `add`), se usa ese mismo archivo y se sigue su numeración.
- Las preguntas abiertas no impiden aprobar un paso: al pedir la aprobación se dice cuántas lo afectan.
- Cuando llegan respuestas, se recorren de 2 a 3 por turno; por cada una se dice qué cambia en el modelo y qué pasos afecta, y se aplica con la skill del paso, según "Volver atrás".

## Reglas

- **El arquitecto decide.** El orquestador nunca aprueba un paso por su cuenta.
- **Un paso a la vez.** No se adelanta trabajo de pasos futuros.
- **Los borradores viven en el proyecto**, en `domain/drafts/`, nunca en una carpeta temporal.
- **Volver atrás está permitido.** Si el arquitecto cambia algo de un paso aprobado, ese paso vuelve a "En curso" con su borrador, y los pasos posteriores quedan "Por revisar": se revisan y se aprueban de nuevo en orden, cada uno con su borrador.
- **Conversación liviana.** Tableros cortos, sin repetir el contenido de los archivos.
- **Retomar siempre es posible.** Si el arquitecto vuelve otro día y pregunta en qué va, repetir el Paso 1.
