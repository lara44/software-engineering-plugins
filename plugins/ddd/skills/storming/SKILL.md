---
name: "storming"
description: "Usar para conducir cada paso del taller de Event Storming (eventos, línea de tiempo, comandos, usuarios y sistemas externos, políticas, datos, agregados y contextos de negocio) a partir de la caracterización del negocio en inputs/, trabajando el paso en curso en domain/drafts/ hasta su aprobación. La activa start; también aplica a 'agrega los comandos', 'revisa las políticas', 'cambia los contextos'."
---

# Taller de Event Storming

Conduce con el arquitecto cada uno de los ocho pasos del taller, cada uno sobre el anterior, y deja el modelo de dominio listo para diseñar: contextos delimitados, agregados con sus invariantes y reglas de negocio. El orquestador (`start`) lleva el estado y la aprobación; esta skill hace el trabajo del paso.

El arquitecto decide; Claude propone desde la evidencia, pregunta y verifica la coherencia.

## Principios

1. **Desde la evidencia.** Todo elemento sale de lo que hay en `inputs/` (caracterización, entrevistas, formatos, actas). Cada evento, política y dato dice de qué hallazgo sale.
2. **No inventar.** Lo que Claude propone sin respaldo en los insumos se marca `[Propuesta]` en `event-storming.md`. Una regla del negocio que nadie confirmó se marca como punto por confirmar (`hotspot`) en el tablero y su pregunta va a `questions.md`.
3. **Entrevista breve.** Por ronda: 1–2 líneas de lo entendido y 2–3 preguntas, siempre con una propuesta concreta para aceptar o ajustar.
4. **Un paso a la vez.** Cada paso agrega un solo tipo de elemento y tiene su propia aprobación. No se adelantan elementos de pasos futuros.
5. **Lenguaje del negocio.** Los nombres salen de cómo habla el negocio y de sus formatos, no de la tecnología.
6. **El orden del proceso manda.** El tablero cuenta el flujo del negocio tal como ocurre: cada evento va en el momento (columna) y en el recorrido (línea) en que pasa, y cada flecha muestra qué sigue a qué. Nunca se mueve un evento, se parte un recorrido o se quita una flecha de secuencia para ahorrar espacio o para que el tablero se vea mejor. Si el orden y el espacio chocan, gana el orden. Todo cambio de posición o de flecha se justifica con una razón del proceso, y se le dice al arquitecto cuál es.

## Archivos

```
domain/
├── event-storming.md         ← índice: estado de cada paso y su resumen (lo actualiza esta skill)
├── event-storming.json       ← modelo aprobado
├── event-storming.drawio     ← tablero aprobado: un solo archivo, una página por paso
├── images/step-N.png         ← imagen de cada paso aprobado (la exporta el orquestador)
└── drafts/                   ← el paso en curso
    ├── event-storming.json
    └── event-storming.drawio
```

El tablero lo genera la skill `board`, que se carga en cada paso. Es **un solo `.drawio`**: cada paso en su propia página, con el panel de terminología y del proceso a la izquierda y el tablero del paso a la derecha.

## Ciclo de un paso

1. **Abrir el borrador.** Si `domain/drafts/` no tiene el paso en curso, copiar ahí `domain/event-storming.json` (en el paso 1, crearlo) y trabajar solo sobre esa copia. Marcar el paso "En curso" en `event-storming.md`.
2. **Proponer y preguntar.** Con la entrevista breve, agregar al modelo del borrador solo los elementos de este paso.
3. **Dibujar** con la skill de estilo, sobre el tablero aprobado, para conservar las páginas de los pasos anteriores tal como quedaron (incluidos los ajustes que el arquitecto haya hecho a mano en draw.io):
   ```bash
   python3 <skill de estilo>/scripts/es_drawio.py build domain/drafts/event-storming.json --paso N \
       --base domain/event-storming.drawio --out domain/drafts/event-storming.drawio
   ```
   En el paso 1 no hay base: se omite `--base`.
4. **Verificar antes de mostrar.** Si el script da un `AVISO` (flechas que se cruzan, contextos que se superponen), reorganizar el modelo según las reglas de disposición de la skill de estilo y volver a dibujar: un tablero con avisos no se presenta. Luego exportar el tablero del paso a un PNG **fuera del proyecto** (en una carpeta temporal) y revisarlo con la herramienta de lectura de imágenes: tarjetas superpuestas, flechas que cruzan tarjetas o se montan una sobre otra, contextos que se enciman, textos que no caben. Corregir el modelo y volver a dibujar hasta que pase. Si no hay forma de exportar, decirlo y pedir al arquitecto que revise el borrador en su editor.
5. **Presentar.** Un resumen de 3–5 líneas de lo que agregó el paso, la ruta `domain/drafts/event-storming.drawio` para abrirla en draw.io o en VS Code, y los puntos por confirmar. Las imágenes del proyecto no se generan todavía: se exportan al aprobar.
6. **Ajustes.** Los cambios que pide el arquitecto en la conversación se hacen en el modelo y se vuelve a dibujar. Si el arquitecto movió tarjetas a mano en el borrador, preguntar antes de volver a dibujar: dibujar de nuevo reemplaza la página de este paso.
7. **Cierre.** Cuando se cumple el criterio del paso, decirlo al orquestador para que pida la aprobación. Al aprobarse, el orquestador mueve el borrador a `domain/` y exporta la imagen.

## Pasos

Cada paso sigue el ciclo anterior. Lo que agrega cada uno:

### 1. Descubrimiento de eventos
- Todos los hechos del negocio que interesan, en pasado, sin orden.
- Incluir los de configuración (lo que hay que registrar antes de operar: usuarios, catálogos, parámetros) y los de operación (el recorrido del negocio).
- **Cambios que importan.** Además de crear, revisar qué se cambia, desactiva o revoca después. Un cambio es evento solo si tiene una regla o una consecuencia que el sistema debe respetar (algo deja de recibirse, un tercero se desvincula, se revoca una autorización, un usuario pierde acceso). Corregir un dato sin efecto no es evento: es mantenimiento del registro y se anota así en `event-storming.md`.
- **Antes de crear un evento nuevo, ver si uno existente ya lo cubre.** Un evento como "definido" o "configurado" ya incluye crear y cambiar; volver a definir un parámetro no es otro evento. La consecuencia del cambio va después como política.
- En el tablero los eventos van sueltos, sin flechas. La evidencia de cada uno se registra en `event-storming.md` y luego en el paso 6.
- En el modelo, cada evento lleva solo `id` y `name`; su línea y su columna se definen en el paso 2.
- Pregunta de cierre: ¿falta algún hecho del negocio, incluidos los cambios que importan? ¿Sobra alguno que en realidad es una consulta o una corrección sin efecto?

### 2. Línea de tiempo
- Ordenar los eventos de izquierda a derecha, en una línea por recorrido del negocio (por ejemplo, configuración, entrada y salida). Los eventos que se siguen uno a otro van en la misma línea aunque cambien de contexto.
- Las flechas unen un evento con el que le sigue en el recorrido. Necesitar un registro de otro contexto (un tercero, un catálogo) no es flecha.
- Los caminos alternos van debajo del evento del que se separan, con flecha punteada; no abren una línea nueva.
- Las líneas que nacen de un evento de otra línea empiezan una columna más a la derecha, para que la flecha baje como un tronco.

### 3. Comandos
- Sobre cada evento, la acción que lo origina, en presente.
- **Solo comandos que dejan un evento.** Buscar, listar o consultar no cambian nada en el negocio: no llevan tarjeta y salen en el paso 7 como vistas de consulta.
- La excepción es un cálculo que el negocio usa para decidir (un riesgo, un reporte): tiene comando, la consulta de quien lo pide.
- **Eventos que no ejecuta una persona.** Un evento no requiere usuario cuando lo provoca:
  - **otro evento:** el sistema crea, asigna o calcula algo como consecuencia, sin que nadie lo pida;
  - **el tiempo:** vence un plazo o llega una fecha ("al cierre del mes", "al día siguiente del vencimiento");
  - **un sistema externo:** la información llega de otro sistema sin que nadie la registre (en el paso 4 lleva la tarjeta del sistema externo, no la de usuario).

  En los tres casos el evento lleva su **comando propio**, con lo que hace el sistema ("Generar factura", "Reservar inventario"). No se repite el comando del evento que lo origina ni se inventa una acción de una persona ("Cerrar pedido"). Ese comando no tendrá usuario en el paso 4, y en el paso 5 lo dispara una política. Se lee: evento (o plazo, o sistema externo) → política → comando → evento.
- Si al poner comandos aparece una acción que cambia algo con consecuencia y no tiene evento (actualizar, desactivar, revocar), no se agrega aquí: se propone reabrir el paso 1, según "Cambios después de aprobar".

### 4. Usuarios y sistemas externos
- A la izquierda de cada comando, el rol que lo ejecuta.
- **Usuario es quien usa el sistema.** Quien firma un papel o recibe algo sin usar el sistema no es usuario; su acción la registra un usuario.
- **Los eventos automáticos no llevan usuario.** No se pone "Sistema" como rol: el propio sistema no es un actor del taller, y la tarjeta haría creer que alguien ejecuta la acción. El usuario va solo en el evento que la persona provoca; la consecuencia queda sin usuario y en el paso 5 recibe la política que explica qué hace el sistema. Antes de asignar un usuario, preguntar: ¿esta persona hace esto en el sistema, o pasa solo cuando ella hace otra cosa?
- Sistema externo: solo si hay intercambio de información con otro sistema. Si el intercambio es un archivo que alguien carga a mano, decirlo; si no hay intercambio, no se pone.

### 5. Políticas
- Sobre cada comando, la regla que lo valida o que reacciona a un evento.
- Hay dos clases de política, y conviene que se distingan al leerlas:
  - **De validación**, sobre un comando que ejecuta una persona: lo que se revisa antes de registrar ("Validar datos del cliente").
  - **De reacción**, sobre el comando de un evento automático: cuándo lo dispara el sistema y qué hace, escrita como "Al <evento, plazo o dato recibido que la dispara>, <qué hace el sistema>" ("Al confirmar el pedido, se genera la factura").
- Todo evento automático (sin usuario) tiene su política de reacción.
- Cada política tiene **origen** (insumo que la respalda, o `Propuesta del modelo`) y **estado**: Confirmada, Supuesto, Propuesta o Parametrizada.
- Una regla que depende de un valor que el negocio puede cambiar (días, umbrales, tolerancias) se modela como **parámetro** que configura un rol, no como una constante.

### 6. Datos
- Para cada evento, los datos que necesita para registrarse y su fuente (campo de un formato, entrevista, propuesta).
- Conservar lo que el negocio ya registra y agregar solo lo que hoy se pierde y hace falta para el propósito del sistema.
- **Datos personales mínimos:** pedir solo lo necesario. Si el insumo trae más, preguntar si de verdad hace falta antes de incluirlo.
- En el tablero, los datos van en una tarjeta verde sobre el comando de cada evento, solo en la página de este paso: desde el paso 7 no se dibujan, para no recargar el tablero. Al aprobar, también se genera `domain/data.md` con la tabla evento, datos y fuente; es el detalle de los datos para los pasos siguientes.

### 7. Agregados
- Sobre cada comando, la unidad con responsabilidad única que protege las invariantes de la operación.
- Cada agregado lista sus invariantes. Las que cambian la práctica actual del negocio se marcan como propuesta.
- Un cálculo o un reporte que se deriva de los registros (sin estado propio) es una **vista de consulta**, no un agregado (`aggregate_view: true`).

### 8. Contextos de negocio
- Agrupar los agregados en contextos delimitados. El paso 8 no lleva línea de tiempo: el tablero muestra un óvalo por contexto, con sus agregados consolidados y las relaciones entre contextos. La cantidad de contextos es la de módulos candidatos. Indicar el tipo de subdominio: central, de soporte o genérico.
- Señalar el **dominio central**: los contextos que corresponden al propósito principal del sistema.
- Separar en un contexto propio a los terceros (personas y organizaciones con las que el negocio se relaciona) y en uno genérico la identidad y el acceso.
- Si el sistema separa un núcleo operativo de una capa de soporte a la decisión, indicar a cuál pertenece cada contexto.
- **Relaciones entre contextos.** Proponer las relaciones entre contextos (un evento que dispara una política o un comando en otro contexto) y, con la confirmación del arquitecto, escribirlas en `relations`. No son relaciones el orden en que se configura el sistema ni que un evento necesite datos de otro contexto. Con ellas, la skill de estilo dibuja el paso 8.
- **Ajustes a mano de la ubicación.** Si el arquitecto acomoda los óvalos en draw.io y pide alinear o reorganizar, primero se guarda su ubicación con `layout` y luego se vuelve a dibujar: se respetan sus posiciones y se reacomodan las flechas y el contenido. No hace falta que lo especifique: mover los óvalos es la indicación.

## `event-storming.md`

```
# Event Storming — <dominio>
Fecha: <última actualización>
Insumos: <lista de archivos de inputs/>

| # | Paso | Estado | Notas |
|---|------|--------|-------|
| 1 | Eventos | Aprobado AAAA-MM-DD | |
| 2 | Línea de tiempo | En curso | |
| 3 | Comandos | Pendiente | |
| … | | | |

## Paso 1. Eventos            tabla: Grupo | Evento | Evidencia
## Paso 2. Línea de tiempo    líneas y caminos alternos, en 3–5 líneas
## Paso 3. Comandos           lista breve; el detalle está en el tablero
## Paso 4. Usuarios y sistemas externos
## Paso 5. Políticas          tabla: Evento | Política | Origen | Estado
## Paso 6. Datos              enlace a data.md
## Paso 7. Agregados          tabla: Agregado | Eventos | Invariantes
## Paso 8. Contextos          tabla: Contexto | Agregados | Subdominio | Parte del sistema
## Puntos por confirmar       lo marcado como hotspot, con su pregunta en questions.md
## Cambios posteriores a la aprobación   tabla: Fecha | Paso | Cambio | Origen
```

La tabla de estados es la que lee el orquestador. Estados válidos: Pendiente, En curso, Aprobado AAAA-MM-DD, Por revisar.

## Criterio de cierre de cada paso

| Paso | Se puede aprobar cuando |
|---|---|
| 1 | El arquitecto confirmó que no falta ningún hecho del negocio, incluidos los cambios con consecuencia; cada evento tiene evidencia o está marcado como propuesta. |
| 2 | Todo evento está en una línea; los caminos alternos tienen su flecha; el tablero no tiene avisos. |
| 3 | Todo evento tiene comando; los eventos automáticos tienen su comando propio; no hay comandos de consulta, salvo los cálculos que el negocio usa para decidir. |
| 4 | Todo comando que ejecuta una persona tiene usuario; los eventos automáticos no tienen usuario; los sistemas externos tienen un intercambio real. |
| 5 | Toda política tiene origen y estado; todo evento automático tiene la política que lo dispara; las reglas con valores configurables son parámetros. |
| 6 | Todo evento tiene sus datos y su fuente; los datos personales son los mínimos. |
| 7 | Todo agregado tiene invariantes; los cálculos y reportes son vistas de consulta. |
| 8 | Todo evento pertenece a un contexto; el dominio central está señalado; los contextos no se enciman; las relaciones entre contextos están confirmadas en `relations`. |

En todos: el tablero del borrador fue revisado visualmente después de su último cambio, y cada punto por confirmar tiene su pregunta en `questions.md`.

## Cambios después de aprobar

Cuando cambia un insumo o el negocio responde una pregunta:
1. Decir qué paso cambia y cuáles quedan afectados (un cambio de usuario afecta los pasos 4 a 8; uno de política, 5 a 8).
2. Con la aprobación del arquitecto, reabrir el primer paso afectado: vuelve a "En curso" con su borrador, y los posteriores pasan a "Por revisar".
3. Dibujar el paso reabierto sobre el tablero aprobado. El borrador conserva las páginas anteriores y deja fuera las posteriores, que se vuelven a dibujar y aprobar en orden.
4. Anotar una fila en "Cambios posteriores a la aprobación".

## Relación con el proceso de arquitectura

Si el proyecto también usa el plugin `add`, este modelo sirve de insumo para su proceso de diseño: cada contexto es candidato a módulo, y las diferencias (un contexto que se une a otro, un agregado que cambia de módulo) se registran allá con su razón. Este plugin no depende del de arquitectura.
