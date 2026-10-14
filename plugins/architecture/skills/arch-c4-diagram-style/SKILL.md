---
name: "arch-c4-diagram-style"
description: "Usar cuando se pida crear o actualizar un diagrama C4 (contexto, contenedores o componentes) para que siga su estilo visual: cajas blancas compactas (dimensionadas por contenido, sin estirarse al ancho del grupo) con icono de color, línea separadora, descripción, bordes punteados grises con espaciado generoso para límites/grupos (cada capa, incluyendo frontend y persistencia, envuelta en su propio grupo con aire suficiente) y entre módulos hermanos lo bastante ancho para las etiquetas de flechas horizontales que los conectan, flechas ortogonales ancladas a bordes específicos con separación entre etiquetas, tipografía Helvetica con reserva a Arial/sans-serif un punto más grande que el estándar de draw.io, dispuesto en capas horizontales de arriba hacia abajo (nunca todo en una sola fila). Sin colores de estado."
---

# Estilo C4 (draw.io)

Genera diagramas C4 (Contexto, Contenedores o Componentes) como `.drawio` editables, con el estilo visual y la disposición en capas del diagrama de referencia del arquitecto. Los mínimos de espaciado de esta skill se validaron renderizando: no reducirlos para ahorrar espacio. Un diagrama alto o ancho es preferible a uno apretado o con texto desbordado.

Si solo piden explicar o documentar una arquitectura sin diagrama, esta skill no aplica.

## Generador

El generador está en `scripts/c4_drawio.py`, dentro de la carpeta de esta skill. Se ejecuta tal cual; no se lee, no se copia y no se reescribe:

```bash
python3 <carpeta-de-esta-skill>/scripts/c4_drawio.py spec.json salida.drawio
```

Ya trae todo el estilo: tipografía, colores, cajas, cilindros, personas, límites punteados y flechas. Calcula solo la altura del bloque título + etiqueta según la longitud del texto, para que la línea separadora nunca quede sobre un título largo. **No se modifica por proyecto:** un icono que no esté en la lista se pasa como `{"text": "XX", "color": "#RRGGBB"}` en el `spec.json`; si se va a repetir, se propone agregarlo a `ICONS` del plugin.

## Estilo (lo pone el script; no cambiar sin pedido explícito)

- **Tipografía:** `Helvetica, Arial, sans-serif`, siempre con reserva. Con una sola fuente, si no está instalada, draw.io la reemplaza por una más ancha y el texto se desborda. Nombre en negrita 13 px, etiqueta `[Tag]` 9 px en gris `#6B6B6B`, descripción 10 px en `#333333`.
- **Cajas:** fondo blanco, esquinas redondeadas, borde gris `#8C8C8C` de 1 px, icono cuadrado de 36x36 con color de marca, línea separadora entre título y descripción.
- **Sin colores de estado.** Todas las cajas llevan el mismo borde gris. No marcar nada como "pendiente" o "fase posterior" por iniciativa propia; si el arquitecto pide resaltar algo, preguntar qué color y qué significa.
- **Bases de datos y colas:** cilindro (las colas acostadas). Con nombres de tecnología largos, `w` ≈ 250–260 px (no más).
- **Personas:** óvalo y rectángulo redondeado, mismo borde gris.
- **Límites (`boundary`) y grupos (`group`):** sin relleno, borde punteado gris `#B3B3B3`, etiqueta en la esquina.
- **Flechas:** ortogonales, `#333333`, punta rellena, etiqueta con el protocolo entre corchetes y fondo blanco.

Iconos disponibles en el script: `net` (.NET), `vue`, `sql`, `postgres`, `blob`, `kafka`, `entra`, `policy`, `smtp`, `aws`. Los componentes internos (Endpoints, Application, Domain, Infrastructure) usan `"tag": "[Component]"` sin icono.

## Layout: capas de arriba hacia abajo

El diagrama siempre fluye de arriba hacia abajo por capas lógicas, con las cajas de cada capa una al lado de la otra. Nunca todo en una sola fila ni en cuadrícula libre. Si el arquitecto pide otra disposición, se sigue la suya.

1. **Clasificar cada elemento en una capa:**
   - 0: actores;
   - 1: frontend o punto de entrada (en Componentes: Endpoints/Controllers);
   - 2: agregador o BFF, si existe;
   - 3: servicios de dominio (en Componentes: Application/CQRS y Domain);
   - 4: persistencia (en Componentes: Infrastructure/repositorios);
   - 5: workers o procesos en segundo plano.

   Los sistemas externos van en una columna a la derecha del `boundary` (≈60–80 px después de su borde), alineados con la capa con la que hablan, sin `group` propio.
2. **Cada capa va en su propio `group`** punteado con etiqueta, sin excepción (frontend y persistencia incluidos). El `boundary` del sistema envuelve todos los `group`.
3. **Apilar las capas** con los mínimos de espaciado de abajo. Ejemplo validado con render: actores en y≈110 (h=50), `boundary` en y≈290, `group` de frontend en y≈340 (h=230, caja interior en y≈395, h=145, w≈420 centrada), `group` de backend en y≈660, `group` de persistencia en y≈950 (base de datos w≈250–260 centrada).
4. **Dentro de cada capa,** repartir las cajas centradas como grupo, con 30–40 px entre hermanas.
5. **En Componentes,** cada capa de la arquitectura (Endpoints → Application → Domain → Infrastructure) es una franja propia. Si hay dos módulos lado a lado con flechas entre ellos, aplicar la separación por etiqueta (ver abajo).

## Espaciado mínimo

Aplica al aire de `group` y `boundary`, no al relleno interno de las cajas:

| Dónde | Mínimo |
|---|---|
| `group` → sus cajas | 30 px a los lados, 50–55 px arriba (para la etiqueta de 2 líneas `Nombre` + `[Group]`), 25–30 px abajo |
| `boundary` → primer `group` | 45–50 px arriba (título + `[Software System]`), 20–30 px a los lados y abajo |
| Último actor → `boundary` | 120–130 px (ahí va la etiqueta de la flecha actor → sistema, a veces de 2 líneas) |
| Entre `group` sucesivos | 80–90 px (ahí va la etiqueta de la flecha entre capas) |
| Entre `group` lado a lado sin flecha etiquetada | 40–60 px |
| Entre cajas unidas por una flecha horizontal etiquetada | ancho de la etiqueta: `caracteres de la línea más larga × 6.5 px + 30–40 px`. Referencia validada: una etiqueta de 2 líneas de 25–35 caracteres necesita 180–220 px; con 40–60 px el texto se monta sobre las cajas |

**Las cajas no se estiran al ancho del `group`.** Se dimensionan por contenido (nombre + descripción) y dejan al menos 30–45 px de aire por lado. Por qué: una caja estirada se ve vacía y desproporcionada. Referencia: una caja única en un `group` de ~600 px mide ~380–450 px. Tamaño típico de caja: 185 x 115–130 (componentes: alto 60–90).

## Flechas

**Siempre `exit`/`entry` explícitos** (`[x, y]`, con `[0,0]` arriba a la izquierda y `[1,1]` abajo a la derecha). Sin ellos, el script conecta centro con centro.
- Vertical entre capas: `exit: [0.5, 1]` → `entry: [0.5, 0]`.
- Horizontal entre módulos lado a lado: `exit: [1, 0.5]` → `entry: [0, 0.5]`, con el hueco calculado por el ancho de la etiqueta.
- Hacia o desde un sistema externo: por el lado que mira al `boundary`.
- **Flechas que convergen en una misma caja:** repartir los `entry` a lo ancho del borde según la posición de cada origen (2 → `0.25` y `0.75`; 3 → `0.2`, `0.5`, `0.8`). Nunca dos flechas con el mismo `entry`.
- Si la línea atravesaría una caja, desviarla con `points`. Que los cruces de bordes punteados caigan en el espacio libre entre grupos, no a lo largo de un borde.
- `label_offset: [a, o]` mueve el texto de una flecha sin mover la línea (`a` de -1 a 1, 0 = punto medio; `o` = desplazamiento perpendicular en px).

## Diagramas de Contexto

Reglas verificadas con render, tras corregir una caja de sistema estirada a 720x220 y una flecha que atravesaba el título del límite:
- **La caja del sistema mide igual que los sistemas externos** (referencia: `280x115`) y nunca se estira para alcanzar a los actores: las flechas se adaptan a la caja, no la caja a las flechas. Descripción breve (~110–120 caracteres, 3 líneas); el detalle va en el diagrama de contenedores.
- **Actores:** con 4 actores (140 px de ancho, centros cada 160 px, fila centrada sobre la caja):
  - Los dos centrales bajan rectos, con `entryX = (centro_actor − x_caja) / ancho_caja` (referencia: `0.214` y `0.786`).
  - Los dos de los extremos bajan hasta una franja ~30 px por encima del límite de la organización, giran hacia adentro con `points` y entran por arriba, por fuera de los centrales (referencia: `0.089` y `0.911`). Así ninguna flecha cruza a otra.
- **Etiquetas de los actores a la misma altura:** `label_offset` ≈ `[-0.45, 0]` en las flechas rectas y ≈ `[-0.7, 0]` en las que hacen codo, alineadas en el tramo vertical superior.
- **Etiqueta del límite de la organización abajo a la izquierda** (`"label_bottom": true` en el `boundary`) cuando los actores entran desde arriba; si queda arriba, la flecha del primer actor la atraviesa. Padding del límite: ~30 px arriba y a los lados, ~55 px abajo.
- **Sistemas externos con flechas horizontales rectas:** salir en `exit: [1, 0.25]` y `[1, 0.75]` y calcular el `entryY` del destino para que coincida con esa altura exacta (con `0.5` por defecto se forma un codo). Hueco caja–externos ≥ 180 px.

## Formato del spec.json

```json
{
  "title": "Nombre del diagrama",
  "page": [1100, 1600],
  "elements": [
    {"id": "unico", "kind": "person|boundary|group|container|external|database|queue",
     "name": "...", "tech": ".NET, Docker", "icon": "net", "tag": "[Component]",
     "desc": "...", "x": 0, "y": 0, "w": 185, "h": 125}
  ],
  "edges": [
    {"from": "id_origen", "to": "id_destino", "label": "...", "protocol": "HTTPS / JSON", "dashed": false,
     "exit": [0.5, 1], "entry": [0.25, 0], "points": [[x1, y1], [x2, y2]], "label_offset": [-0.45, 0]}
  ]
}
```

- `boundary`: el rectángulo del sistema (`type` opcional, "Software System" por defecto; `label_bottom: true` para la etiqueta abajo).
- `group`: el rectángulo de una capa o módulo.
- `tag`: reemplaza la etiqueta por defecto bajo el nombre.
- El anidamiento es solo geométrico: cada caja va dentro del rango x/y de su `group`, con todas las coordenadas absolutas.
- `icon`: nombre de la lista o `{"text": "XX", "color": "#RRGGBB"}`.

## Flujo de trabajo

1. Reunir el contenido: actores, sistema, capas, cada contenedor o componente y cada relación (origen, destino, etiqueta, protocolo).
2. Clasificar en capas, definir el `group` de cada una y calcular coordenadas con los mínimos de espaciado; si hay flechas horizontales etiquetadas, calcular primero esos huecos.
3. Decidir `exit`/`entry` de cada flecha, repartiendo las convergentes.
4. Escribir el `spec.json` y generar con `scripts/c4_drawio.py`.
5. Renderizar a PNG y mirarlo (draw.io Desktop: `drawio -x -f png -o salida.png salida.drawio`; en Mac, si `drawio` no está en el PATH, `/Applications/draw.io.app/Contents/MacOS/draw.io`). Corregir y repetir hasta que no haya texto desbordado, etiquetas encimadas ni flechas que atraviesen cajas. Si no se puede renderizar, decirlo y entregar como "sin verificación visual".
6. Entregar el `.drawio`.

## Verificación antes de entregar

- [ ] Toda flecha apunta a IDs que existen (parsear con `xml.etree.ElementTree`).
- [ ] Capas apiladas de arriba hacia abajo, sin solape, cada una con su `group`, y el `boundary` envolviéndolas.
- [ ] Mínimos de espaciado cumplidos, sobre todo actor → `boundary` (120–130 px), entre `group` (80–90 px) y los huecos de flechas horizontales etiquetadas.
- [ ] Ninguna caja estirada al ancho de su `group`; cilindros de nombre largo en ~250–260 px.
- [ ] Todas las flechas con `exit`/`entry` explícitos, convergentes repartidas, sin atravesar cajas.
- [ ] En el render: ningún texto desbordado ni sobre la línea separadora, ninguna etiqueta encimada.
- [ ] Ningún color distinto al gris estándar, salvo pedido explícito.
