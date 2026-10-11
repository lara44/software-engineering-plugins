---
name: architect
description: Usar cuando el arquitecto quiera iniciar, retomar o avanzar la arquitectura de un proyecto ("arranquemos la arquitectura", "en qué vamos", "sigamos con la arquitectura", /architect). Detecta la fase actual por los archivos del proyecto y conduce cada fase con la skill o subagente que corresponde, pidiendo aprobación entre fases.
---

# Architect — orquestador del proceso de arquitectura

Conduce al arquitecto por el proceso completo de arquitectura de un proyecto. El arquitecto no invoca skills ni subagentes: habla con el orquestador, y el orquestador decide qué pieza usar en cada momento.

El orquestador **no hace el trabajo de las fases**. Su responsabilidad es saber en qué fase está el proyecto, activar la pieza correcta, hacer respetar los puntos de aprobación y mantener al arquitecto ubicado.

## Fases

| # | Fase | Pieza que la ejecuta | Entrada | Salida | Estado de la pieza |
|---|------|----------------------|---------|--------|--------------------|
| 1 | Drivers | skill `architecture-drivers` (+ subagente `architecture-extractor` si hay insumos) | `insumos/` (opcional) | `drivers.md` | Disponible |
| 2 | Decisiones | skill `architecture-decisions` | `drivers.md` aprobado | `decisiones.md` | Disponible |
| 3 | Vistas | subagente `architecture-views` (usa `c4-diagram-style`, `database-diagram-style`, `aws-deployment-diagram-style`) | `drivers.md` + `decisiones.md` aprobados | `diagramas/` | En construcción |
| 4 | Validación | subagente `architecture-validator` | todo lo anterior | `validacion.md` | En construcción |
| 5 | Documento | skill `architecture-document-style` | todo lo anterior | `documento/*.docx` | Disponible |

Antes de usar una pieza, verificar que realmente está instalada (que la skill o el subagente existe en esta sesión). Si no existe, tratarla como "En construcción" aunque la tabla diga otra cosa.

## Convención de la carpeta del proyecto

```
<proyecto>/
├── insumos/        ← documentos que aporte el arquitecto (opcional)
├── drivers.md
├── decisiones.md
├── diagramas/
├── validacion.md
└── documento/
```

Si la carpeta no tiene esta estructura, no reorganizar archivos del arquitecto. Solo crear lo que haga falta cuando una fase lo produzca.

## Paso 1: Detectar el estado del proyecto

Al activarse, revisar la carpeta y determinar el estado de cada fase:

- **Pendiente**: no existe su archivo de salida.
- **En curso**: existe y dice `Estado: borrador`.
- **Aprobada**: existe y dice `Estado: aprobado`.

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

Si la carpeta está vacía, decirlo y proponer arrancar por la fase 1. Si hay archivos en `insumos/` (o documentos sueltos), mencionarlo: se usarán en la fase 1.

## Paso 2: Ejecutar la fase actual

1. **Siempre cargar la pieza de la fase actual, también cuando la fase está en curso.** Al retomar, la pieza revisa el archivo existente contra su formato y criterio de cierre vigentes, lo actualiza si cambió el formato y dice qué falta. Seguir sus instrucciones. Para una skill, cargarla y conducir la fase en esta conversación. Para un subagente, delegarle la tarea con un encargo completo (rutas de entrada y salida, y qué devolver), porque el subagente no ve esta conversación.
2. No duplicar lo que la pieza ya hace: el orquestador no reescribe sus preguntas ni su formato.
3. Si la pieza de la fase está "En construcción", decirlo en una línea y ofrecer la alternativa disponible. Por ejemplo: "La fase de decisiones aún no está automatizada. Podemos registrarlas conversando y las anoto en `decisiones.md`, o generar ya el documento con lo que hay, marcando lo pendiente".

## Paso 3: Punto de aprobación

Solo se pide aprobación cuando la pieza de la fase confirma que su criterio de cierre se cumple. El orquestador nunca ofrece aprobar una fase que no fue revisada por su pieza en esta sesión.

Al terminar una fase:

1. Mostrar el resumen que entregue la pieza (no repetir el archivo completo).
2. Pedir aprobación explícita del arquitecto.
3. Con la aprobación, verificar que el archivo quedó en `Estado: aprobado`, mostrar el tablero actualizado y proponer la siguiente fase.

Sin aprobación no se avanza. Si el arquitecto quiere corregir algo, se vuelve a la pieza de esa fase.

## Reglas

- **El arquitecto decide.** El orquestador nunca toma decisiones de arquitectura ni aprueba fases por su cuenta.
- **Una fase a la vez.** No adelantar trabajo de fases futuras.
- **Volver atrás está permitido.** Si el arquitecto cambia algo de una fase ya aprobada (por ejemplo, un driver), esa fase vuelve a `Estado: borrador` y las fases posteriores que dependen de ella se marcan para revisión.
- **Conversación liviana.** Tableros cortos, sin repetir contenido de los archivos, sin narrar cada paso interno.
- **Retomar siempre es posible.** Si el arquitecto vuelve otro día y dice "en qué vamos", repetir el Paso 1.
