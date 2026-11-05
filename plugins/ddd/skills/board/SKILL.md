---
name: "board"
description: "Usar para dibujar o actualizar el tablero de un taller de Event Storming como un solo .drawio editable (una página por paso, cada una con el panel de terminología y proceso: eventos, línea de tiempo, comandos, usuarios y sistemas externos, políticas, datos, agregados y contextos), con el estilo de notas adhesivas de referencia, y para exportar a PNG la imagen de un paso aprobado. No conduce el taller: eso lo hacen start y storming."
---

# Estilo del tablero de Event Storming (draw.io)

Dibuja el taller completo en **un solo `.drawio`**, como en un tablero de pared:

- **Cada paso es una página** del archivo («Paso 3 · Localización de comandos»), que en draw.io se abre con las pestañas de abajo. Así cada paso se ve solo y completo, sin una tira larga de pasos.
- **A la izquierda** de cada página, el panel del taller: la barra con el nombre, la **terminología** (cada tipo de tarjeta con su color y qué representa) y el **proceso** (los ocho pasos, con el de esa página resaltado).
- **A la derecha**, el título del paso («PASO 3: Localización de comandos») y su tablero.

Los pasos 2 a 7 son el flujo (la línea de tiempo). **El paso 8 no tiene línea de tiempo:** es la vista de contextos delimitados, un óvalo por contexto con sus agregados consolidados (ver «Paso 8: contextos delimitados»).

La imagen de un paso (`domain/images/step-N.png`) se exporta **solo al aprobarlo**, y contiene solo el tablero de ese paso, sin el panel ni el título.

## Generador

El generador está en `scripts/es_drawio.py`, dentro de la carpeta de esta skill. Se ejecuta tal cual; no se lee, no se copia y no se reescribe. Solo usa la biblioteca estándar de Python.

```bash
# dibujar el paso N en el borrador, conservando las páginas aprobadas
python3 <carpeta-de-esta-skill>/scripts/es_drawio.py build domain/drafts/event-storming.json --paso N \
    --base domain/event-storming.drawio --out domain/drafts/event-storming.drawio

# paso 1 (todavía no hay tablero aprobado): sin --base
python3 <carpeta-de-esta-skill>/scripts/es_drawio.py build domain/drafts/event-storming.json --paso 1 \
    --out domain/drafts/event-storming.drawio

# al aprobar: exportar la imagen del paso N (requiere draw.io Desktop)
python3 <carpeta-de-esta-skill>/scripts/es_drawio.py export domain/event-storming.drawio --paso N \
    --out domain/images/step-N.png

# paso 8: si el arquitecto acomodó los óvalos a mano, guardar su ubicación en el modelo antes de volver a dibujar
python3 <carpeta-de-esta-skill>/scripts/es_drawio.py layout domain/drafts/event-storming.drawio domain/drafts/event-storming.json

# al aprobar el paso 6: tabla de datos por evento
python3 <carpeta-de-esta-skill>/scripts/es_drawio.py data domain/event-storming.json --out domain/data.md
```

Cómo trabaja `build`:
- **Con `--base`**, copia del tablero aprobado las páginas de los pasos anteriores **tal como están**, incluidos los ajustes que el arquitecto haya hecho a mano en draw.io, y solo dibuja de nuevo la página del paso N. Las páginas de pasos posteriores se dejan fuera del borrador: se vuelven a dibujar y aprobar en orden.
- **Sin `--base`**, crea el tablero con la página del paso N.
- Un tablero del formato anterior (una sola página con una capa por paso) se convierte solo: cada capa pasa a su propia página, con sus ajustes a mano.

Cómo trabaja `export`: toma del `.drawio` solo el tablero de la página del paso N, la exporta con draw.io Desktop (`drawio -x -f png -s 2`) y la recorta al contenido. Si draw.io Desktop no está, deja en una carpeta temporal un `.drawio` con solo ese paso y dice cómo exportarlo desde el editor (Archivo › Exportar como › PNG, escala 200 %). Para revisar un borrador, exportar a una carpeta temporal fuera del proyecto, nunca a `domain/images/`.

**No se ajustan coordenadas a mano para corregir el dibujo del paso en curso:** se corrige el modelo (línea, columna, `below` o `flows`) y se vuelve a dibujar. El script avisa con `AVISO` cuando dos flechas se cruzan, dos contextos se superponen o una flecha va hacia atrás; con un aviso, el paso no se presenta hasta corregir el modelo.

## Estilo (lo pone el script; no cambiar sin pedido explícito)

- **Tarjetas:** notas adhesivas rectas con sombra. Evento `#FFAA5B`, comando `#8ED3F5`, usuario `#FFE15A`, sistema externo `#F592C8`, política `#BDA6F2`, datos `#7ED69B`, agregado `#FFF4A8`.
- **Por confirmar:** el evento con `hotspot` lleva borde rojo punteado `#D92D20`. Solo se marca lo que depende de una regla no confirmada con el negocio.
- **Vistas de consulta:** el agregado con `aggregate_view` (un cálculo o un reporte que no guarda estado propio) lleva borde punteado ocre.
- **Flechas grises y curvas** (aristas `curved=1` con sus puntos calculados; no se cambian a ortogonales):
  - entre eventos seguidos de una misma línea, rectas;
  - de un evento a otras líneas, un **tronco** recto que baja y entra a cada evento con una curva;
  - hacia un evento de la misma columna, un **bucle en C** por la derecha;
  - hacia la columna siguiente de la misma línea, una **S** suave;
  - continuas para el flujo principal, punteadas (`dashed`) para los caminos alternos.
  - Cada flecha queda conectada a sus tarjetas: si el arquitecto mueve una tarjeta en draw.io, la flecha la sigue.
  - **Sin cruces:** cuando varias flechas llegan o salen por el mismo lado de una tarjeta, el script las reparte a lo alto según de dónde vienen: arriba las que bajan, con la más cercana más arriba; abajo las que suben. Así una flecha que viene de cerca no cruza a una que viene de lejos.
- **Tipografía:** Inter, con reserva Helvetica y Arial. Eventos 12 px (sin negrita: las tarjetas se distinguen por el color); comandos y agregados 11 px; políticas, datos y sistemas externos 10,5 px; usuarios 9,5 px.

## Disposición (cómo la calcula el script)

**Regla principal: se respeta el orden del proceso.** La columna es el momento en que ocurre el evento y la línea es el recorrido al que pertenece. El script nunca los cambia; solo aprovecha el espacio libre sin alterar ese orden. Las reglas de abajo sirven para que el tablero quede limpio, y ninguna justifica cambiar el orden: si una mejora de espacio exige mover un evento de momento o de recorrido, o quitar una flecha que muestra qué sigue a qué, no se hace.

- **Paso 1:** las tarjetas se mezclan en una cuadrícula irregular, sin flechas: así queda la pared al terminar la lluvia de eventos. Solo necesita `id` y `name` de cada evento.
- **Pasos 2 a 7:** cada **línea** (`lane`) es una fila de eventos y las líneas se ordenan de arriba hacia abajo. La columna (`col`) fija la posición horizontal, igual en todas las líneas.
- **Espacio aprovechado:** una línea no ocupa todo el ancho del tablero, solo sus columnas. Cada fila sube hasta justo debajo de lo que ya hay en esas columnas y en el camino de las flechas que le llegan (la que baja por la columna del evento de origen y entra por la izquierda). Así, una línea que sale de un evento queda pegada a él aunque otra columna tenga una pila larga de caminos alternos. Las líneas principales conservan su orden: ninguna sube por encima de la anterior. En el paso 8, una fila tampoco se mete dentro del recuadro de otro contexto.
- **El script no cambia columnas ni líneas.** La columna es el momento del recorrido y la línea es el recorrido: los decide el modelo. El script solo aprovecha el espacio vertical sin alterar ese orden.
- Los eventos de la fila principal de una línea se unen solos, de izquierda a derecha. Las demás flechas se declaran en `flows`, y su forma (tronco, C o S) sale de la posición de los dos eventos.
- Un **camino alterno** va debajo del evento del que se separa, en la misma columna (`below`). Si un evento tiene varios caminos alternos, se encadenan con `below` uno debajo del otro, y sus flechas bajan por un solo tronco a la derecha que se ramifica a cada uno.
- Sobre cada evento se apilan, de abajo hacia arriba, el comando, los datos, la política y el agregado. El usuario va a la izquierda del comando y el sistema externo en la esquina inferior derecha del evento.
- **Los datos solo se dibujan en la página del paso 6.** Desde el paso 7 las tarjetas verdes no se dibujan, para que el tablero de agregados y contextos se vea en alto nivel. Los datos siguen en el modelo, en `data.md` y en la imagen del paso 6.

Reglas para que el tablero quede limpio (verificadas con render):
1. **Una línea de tiempo por recorrido del negocio** (por ejemplo, configuración, entrada y salida). Los eventos que se siguen uno a otro van en la misma línea, aunque pertenezcan a contextos distintos: la línea es el recorrido, no el contexto. Partir un recorrido en varias líneas crea una escalera que alarga el tablero.
2. **Una flecha une un evento con el que le sigue en el recorrido.** Que un evento necesite un registro de otro contexto (un tercero, un producto del catálogo, un usuario) no es una flecha: esa dependencia la explican los datos y los agregados. Las flechas de dependencia cruzan el tablero, bloquean columnas enteras y empujan todo hacia abajo.
3. **Los caminos alternos no abren una línea nueva:** van con `below` debajo del evento del que se separan (corregir, cancelar, desactivar, revocar, dar de baja).
4. **Desplazar una columna** las líneas que nacen de un evento de otra línea (por ejemplo, empezar en `col: 1` las líneas que salen del registro del usuario en `col: 0`). Así la columna del evento de origen queda libre para el tronco; si no está libre, la flecha sale como una curva larga.
5. **Caminos alternos en la columna siguiente:** una flecha punteada entre un evento y el camino alterno de la columna siguiente sale como una S limpia; a dos o más columnas, sale como una curva larga.
6. **Contextos contiguos:** los eventos de un mismo contexto van en columnas seguidas de la misma línea. Si dos contextos se encimarían, mover el evento que sobra de columna o de línea.
7. **Pocas flechas punteadas:** solo para caminos alternos reales. Si un tablero tiene más de cinco, revisar si falta una línea de tiempo.
8. **Cada evento cerca de los eventos de los que viene.** Si un evento recibe flechas de varios, ubicarlo en la columna siguiente al más cercano y en la línea de ese recorrido. Un tronco que salta varias columnas pasa por debajo de las intermedias y suele cruzarse con otras flechas.
9. **Con un aviso de cruce, reorganizar, no aceptar.** Mover de columna o de línea el evento que provoca el cruce (casi siempre, el destino de la flecha más larga) y volver a dibujar hasta que no haya avisos.

## Paso 8: contextos delimitados

El flujo ya quedó en los pasos 2 a 7. Para cerrar el taller se **quita la línea de tiempo**, se **delimita cada contexto una sola vez** y se **consolidan los agregados**. Eso es la página del paso 8, que el script genera del mismo modelo:

- **Un óvalo punteado por contexto** (todos con el mismo trazo), sin repetir: su cantidad es la de módulos candidatos. La política, el comando, el evento y el agregado tienen el mismo tamaño, con un poco de aire entre filas. El óvalo es el más pequeño que encierra su contenido, con el nombre del contexto lo más arriba posible dentro del óvalo.
- **Una tarjeta por agregado**, encima del primer comando y su evento, centrada en la unión de los dos y montada sobre su borde superior (como el rol va montado en la esquina del comando). Debajo, sus filas **política → comando → evento**; el comando y el evento van pegados, sin flecha entre ellos, y el rol va montado en la esquina del comando. El sistema externo va en la esquina del evento.
- **Las flechas entre contextos** salen de un evento y llegan a la política (o al comando, si no tiene) que dispara en el otro contexto: evento → política → comando. **Cada flecha es una sola curva suave** (sale, se dobla una vez y entra), sin puntos de paso ni quiebres. Puede salir por la derecha, arriba o abajo del evento y entrar por la izquierda, arriba o abajo de la política; se usa el par de lados que da la curva más corta y limpia.
- **Lo que se elige es la ubicación, no el camino de la flecha.** El script prueba varias disposiciones y se queda con la de mejor puntaje: una curva que pisa una tarjeta pesa mucho, un cruce entre curvas pesa bastante, y luego cuentan el largo total y que el dibujo quede compacto. Lo que se prueba:
  - **Contexto central en el medio y los demás donde las flechas queden más directas.** El central es el que tiene más relaciones (a igualdad, el del dominio central y luego el que tiene más eventos). Cada contexto relacionado se ubica pegado a uno con el que se relaciona, probando ocho direcciones (a los lados, arriba, abajo y en diagonal), y se queda la combinación con las curvas más cortas, sin cruces ni tarjetas pisadas. Así, si dos contextos envían flechas al central, pueden quedar los dos del mismo lado, uno encima del otro, con conexiones directas. La búsqueda va un contexto a la vez, guardando las mejores disposiciones parciales (búsqueda por haz).
  - **Flechas que vuelven hacia atrás** pueden entrar a su política por arriba o por abajo: las filas que las reciben se prueban al principio o al final de su columna.
  - **Orden de las filas dentro de cada agregado:** las filas que reciben flechas y las que las envían se prueban al principio o al final de su columna, para que tengan un lado libre por donde entrar o salir.
  - Dentro de un contexto, el agregado que recibe flechas va a la izquierda y el que las envía a la derecha.
  - Los contextos sin relaciones van arriba o abajo, según aparecen en el tablero, lo más cerca posible sin encimarse.
- Si con la mejor disposición una curva todavía pasa sobre tarjetas, el script avisa: casi siempre sobran relaciones (no confirmadas) o falta una relación que ordene los contextos.
- El nombre de cada contexto va en letra grande (19 px), lo más arriba posible dentro de su óvalo. Se ubica después de las flechas: si una pasa por donde iría, se corre a un lado o un poco más abajo.
- **La ubicación que fija el arquitecto manda.** Si el arquitecto mueve los óvalos en draw.io, antes de volver a dibujar se guarda su ubicación con `layout` (queda en `context_layout` del modelo). Desde ahí, el script respeta esas posiciones y solo reacomoda el contenido de cada óvalo, las flechas y los nombres. Si un contexto sin ubicación fijada aparece después, se ubica solo junto a los demás. Si dos óvalos fijados se enciman (porque cambió su contenido), el script avisa para correr uno en draw.io.
- **Las relaciones las confirma el arquitecto.** Van en `relations` del modelo: solo las que de verdad disparan algo en otro contexto (no el orden en que se configura el sistema). Sin `relations`, el script las saca del flujo y avisa que hay que confirmarlas.

## Modelo (`domain/event-storming.json`)

```json
{
  "title": "<nombre del dominio>",
  "contexts": [
    {"id": "<id-contexto>", "name": "<Nombre del contexto>", "core": true}
  ],
  "events": [
    {
      "id": "<id-evento>",
      "name": "<Evento en pasado>",
      "lane": 0, "col": 0,
      "command": "<Comando en presente>",
      "actor": "<Rol que lo ejecuta>",
      "policy": "<Regla que lo valida>",
      "external": "<Sistema externo, si hay>",
      "aggregate": "<Agregado>",
      "aggregate_view": false,
      "hotspot": false,
      "context": "<id-contexto>",
      "data": ["<dato>", "<dato>"],
      "source": "<De dónde sale>"
    },
    {"id": "<id-alterno>", "name": "<Evento alterno>", "lane": 0, "col": 0, "below": "<id-evento>"}
  ],
  "flows": [
    {"from": "<id-evento>", "to": "<id-otro-evento>", "dashed": true}
  ],
  "relations": [
    {"from": "<id-evento de un contexto>", "to": "<id-evento que dispara en otro contexto>"}
  ]
}
```

- Obligatorios por evento: `id` y `name` desde el paso 1; `lane` y `col` desde el paso 2. Todo lo demás es opcional y aparece desde su paso.
- `name` del evento en pasado; `command` en presente.
- `below` pone el evento debajo de otro de la misma línea y columna (camino alterno). Se pueden encadenar.
- `data` se dibuja en el paso 6 como tarjeta verde; `data` y `source` alimentan también `data.md`.
- `relations` (paso 8): las relaciones entre contextos confirmadas por el arquitecto.
- `context_layout` (paso 8): la ubicación de cada contexto que el arquitecto fijó a mano (la escribe `layout`; no se edita a mano).

## Errores que el script rechaza

- Un evento sin `id` o `name` (o, desde el paso 2, sin `lane` o `col`), o un `id` repetido.
- Dos eventos en el mismo lugar (misma línea, fila y columna).
- `below` hacia un evento de otra columna o línea, o en ciclo.
- Un `context` o un evento de `flows` que no existe.

## Requisitos

- Python 3, para dibujar.
- draw.io Desktop, para exportar las imágenes al aprobar. Sin él, la imagen se exporta desde el editor (draw.io o la extensión de VS Code).
- Recomendado: la fuente Inter instalada; sin ella, draw.io usa Helvetica o Arial.
