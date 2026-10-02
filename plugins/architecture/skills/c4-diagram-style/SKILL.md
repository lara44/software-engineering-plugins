---
name: "c4-diagram-style"
description: "Usar cuando se pida crear o actualizar un diagrama C4 (contexto, contenedores o componentes) para que siga su estilo visual: cajas blancas compactas (dimensionadas por contenido, sin estirarse al ancho del grupo) con icono de color, línea separadora, descripción, bordes punteados grises con espaciado generoso para límites/grupos (cada capa, incluyendo frontend y persistencia, envuelta en su propio grupo con aire suficiente) y entre módulos hermanos lo bastante ancho para las etiquetas de flechas horizontales que los conectan, flechas ortogonales ancladas a bordes específicos con separación entre etiquetas, tipografía Helvetica con reserva a Arial/sans-serif un punto más grande que el estándar de draw.io, dispuesto en capas horizontales de arriba hacia abajo (nunca todo en una sola fila). Sin colores de estado."
---

# Estilo C4 (draw.io)

Esta skill genera diagramas C4 (Contexto, Contenedores o Componentes) como archivos `.drawio` editables en draw.io/diagrams.net, replicando el estilo visual **y la disposición en capas** de un diagrama de referencia de un proyecto real, con espaciado generoso validado (ver nota de verificación empírica abajo).

## Cuándo usarla

Siempre que se pida crear, rehacer o extender un diagrama C4 — de un sistema nuevo, de un proyecto existente o de cualquier arquitectura que se describa. Si solo se pide "explicar" o "documentar" una arquitectura sin mencionar diagrama, no se activa.

## Nota importante sobre la fuente

El generador usa `fontFamily=Helvetica, Arial, sans-serif` (con reserva), nunca `Helvetica` a secas. Si se especifica una sola fuente y esa fuente no está instalada en la máquina donde el usuario abre el archivo, el motor de render puede sustituirla por una fuente mucho más ancha y el texto se desborda. No quites la reserva de fuentes del `FONT` del script.

## Sin colores de estado: todas las cajas llevan el mismo borde gris

Esta skill **no** marca automáticamente ningún componente como "fase posterior", "pendiente" ni con ningún otro color de estado. Todas las cajas usan siempre el mismo borde gris `#8C8C8C`. Si el usuario pide explícitamente resaltar algo con otro color, pregúntale qué color y qué significa antes de aplicarlo — nunca lo infieras.

## Espaciado generoso: nada apretado, en ningún nivel (esto es de `group`/`boundary`, no de las cajas individuales)

Esta regla existe porque las primeras versiones de la skill generaban diagramas visualmente correctos en estructura pero demasiado apretados: grupos pegados a sus cajas, título del `boundary` sin aire, y etiquetas de flechas montadas unas sobre otras cuando dos aristas convergen cerca. El espaciado generoso se aplica al **padding de `group`/`boundary` respecto a lo que envuelven y entre capas** — no agranda ni acolcha las cajas de contenedor/componente individuales, que mantienen su propio padding interno normal (ver "Reglas de estilo" más abajo). Usa estos valores como mínimos, no como sugerencia:

- **Padding de cada `group` respecto a las cajas que envuelve**: al menos 30px a cada lado (izquierda/derecha), al menos 50-55px arriba (deja espacio a la etiqueta de 2 líneas `Nombre` + `[Group]` sin tocar la esquina de la primera caja), y al menos 25-30px abajo.
- **Padding del `boundary` respecto al primer `group` que envuelve**: al menos 45-50px arriba (para que el título `Nombre del sistema` + `[Software System]` tenga aire antes de que empiece el primer grupo), y al menos 20-30px a los lados y abajo.
- **Espacio vertical entre el último actor y el `boundary`**: al menos 120-130px (no los 70-90px que bastan entre capas internas) — ahí vive la etiqueta de la flecha actor→sistema (a veces de 2 líneas: acción + protocolo) y necesita su propio aire antes de tocar el borde del sistema.
- **Espacio vertical entre capas/groups sucesivos**: al menos 80-90px (no 70px) — ahí va la etiqueta de la flecha que conecta esa capa con la siguiente.
- **Espacio horizontal entre `group`/módulos hermanos que van lado a lado**: si NO hay ninguna flecha horizontal con etiqueta entre ellos, ≥40-60px de separación basta. Pero si hay una flecha horizontal etiquetada conectando cajas de ambos módulos (p. ej. una dependencia entre módulos, un contrato compartido), el hueco entre los bordes de las cajas que se conectan debe ser lo bastante ancho para el texto completo de la etiqueta — estima el ancho como `caracteres_de_la_linea_mas_larga_del_texto × 6.5px + 30-40px de margen` (con la etiqueta partida en 2 líneas cortas vs. una sola larga) y usa ESE valor como separación mínima entre los `group`, no el 40-60px genérico. Como referencia validada con render real: una etiqueta de dos líneas tipo `NombreInterfaz` + `[descripción del contrato]` (~25-35 caracteres por línea) necesita ≥180-220px de separación entre las cajas que conecta — los 40-60px genéricos NO alcanzan y el texto se desborda sobre las cajas vecinas de ambos lados.
- **Cuando dos o más flechas convergen sobre la misma caja destino** (p. ej. dos actores que le hablan al mismo frontend): nunca ancles ambas en `entry: [0.5, 0]` (se apilarían una sobre otra). Repártelas a lo ancho del borde de destino según la posición relativa de cada origen: si hay 2, usa `entry: [0.25, 0]` para la de la izquierda y `entry: [0.75, 0]` para la de la derecha; si hay 3+, repártelas proporcionalmente (`0.2, 0.5, 0.8`, etc.). Esto separa automáticamente las dos líneas y sus etiquetas.
- Estos mínimos ya están validados renderizando con el motor real de mxGraph (no son una suposición) — no los reduzcas para "ahorrar espacio"; si el diagrama queda muy alto o muy ancho, es preferible eso a que se vea apretado o con texto desbordado.

## No estires las cajas de contenedor al ancho completo del grupo

Cuando un `group`/`boundary` contiene una sola caja (o pocas), **no la hagas ocupar todo el ancho interior del grupo de borde a borde** — eso la hace ver desproporcionadamente ancha y vacía, con poco texto disperso en mucho espacio horizontal. Deja un margen visible a los lados: al menos 60-90px de aire total (30-45px por lado) entre el borde del `group` y el borde de la caja, más si el grupo es muy ancho. Dimensiona la caja según su contenido (nombre + descripción), no según el ancho disponible del grupo. Como referencia, un contenedor típico de una sola caja centrada en un grupo de ~600px de ancho usa un ancho de caja de ~380-450px, no los 600px completos.

## Regla de oro del layout: capas verticales, no una fila horizontal

El diagrama de referencia SIEMPRE fluye de arriba hacia abajo por capas lógicas (actores → frontend → agregador → servicios de dominio → almacenamiento/colas → workers/procesadores en segundo plano), y dentro de cada capa las cajas se acomodan una al lado de la otra. **Nunca** pongas todos los contenedores en una sola fila horizontal ni los distribuyas en una cuadrícula libre. Los sistemas externos son la única excepción y van a un costado, fuera del boundary, alineados verticalmente con la capa con la que más interactúan. Esto aplica igual a diagramas de Componentes: cada capa de la arquitectura (endpoints/API → application/CQRS → domain → infrastructure) es una franja horizontal propia. Cuando un diagrama de Componentes tiene dos módulos lado a lado (p. ej. "Módulo Gestión" y "Módulo Indicadores", cada uno con su propia franja Endpoints/Application/Domain/Infrastructure), y hay una flecha horizontal etiquetada entre ellos (p. ej. una dependencia entre capas Application), aplica la regla de separación horizontal de la sección "Espaciado generoso" — no el gap genérico de 40-60px.

### Algoritmo de layout (seguir siempre, no improvisar coordenadas)

1. **Clasifica cada elemento en una capa**, de arriba hacia abajo:
   - Capa 0: Actores/personas.
   - Capa 1: Frontend / Web App / punto de entrada del usuario (o, en Componentes, Endpoints/Controllers).
   - Capa 2: Servicio agregador o BFF (si existe).
   - Capa 3: Servicios de dominio / microservicios de negocio (o, en Componentes, Application/CQRS y Domain).
   - Capa 4: Almacenamiento/persistencia (o, en Componentes, Infrastructure/repositorios).
   - Capa 5: Workers, jobs o procesadores en segundo plano.
   - Sistemas externos: se ubican a la derecha del boundary, `y` alineado a la capa con la que hablan.

2. **Calcula la franja vertical de cada capa** apilando de arriba hacia abajo, respetando los mínimos de la sección "Espaciado generoso" (≥80-90px entre groups sucesivos, ≥120-130px entre actores y boundary). Ejemplo validado (coincide con el archivo de prueba que generó el render correcto): actores y≈110 (h=50), boundary y≈290, primer group (frontend) y≈340 (h=230, con su caja interior en y≈395,h=145,w≈420 centrada dejando margen a los lados), siguiente group (backend) y≈660 (90px de separación con el anterior), group de persistencia y≈950 (con la base de datos en w≈250-260 centrada).

3. **Dentro de cada capa, reparte las cajas horizontalmente**, centradas como grupo, con separación de 30-40px entre cajas hermanas, y sin estirarlas al ancho completo del grupo (ver sección anterior).

4. **TODA capa va envuelta en su propio `group` punteado con etiqueta, sin excepción** — frontend, cada capa de backend, y persistencia/almacenamiento incluidos. Usa los paddings mínimos de la sección de espaciado (30px lados, 50-55px arriba, 25-30px abajo). Cuando dos módulos van lado a lado, déjales ≥40-60px entre sus bordes — o el ancho de la etiqueta si hay una flecha horizontal etiquetada entre ellos (ver "Espaciado generoso").

5. **El `boundary` del sistema** envuelve todos los `group` de capas de contenedores, con el padding mínimo de la sección de espaciado (≥45-50px arriba, ≥20-30px lados/abajo).

6. **Sistemas externos**: columna a la derecha, `x` después del borde derecho del boundary + ~60-80px, `y` alineado a la capa con la que hablan. No necesitan `group` propio.

7. **Verifica antes de generar el XML**: confirma que las bandas no se solapan, que cada capa tiene su `group`, que se cumplen los mínimos de espaciado (sobre todo actor→boundary y group→group), que ninguna caja de contenedor está estirada al ancho completo de su group, y que ninguna flecha horizontal con etiqueta larga tiene menos separación entre sus cajas que el ancho estimado de su texto.

Si el usuario pide explícitamente otra disposición, sigue esa instrucción — el comportamiento por defecto es SIEMPRE el apilado vertical por capas con espaciado generoso.

## Regla de oro de las flechas: siempre anclar `exit`/`entry`, y separar etiquetas convergentes

El generador conecta centro-a-centro si no se dan puntos de anclaje. **Siempre** especifica `exit`/`entry` (fracciones `[x,y]`, `[0,0]`=esquina superior izquierda, `[1,1]`=esquina inferior derecha):

- **Flujo vertical entre capas** (alineadas en la misma columna): `exit: [0.5, 1]` → `entry: [0.5, 0]`.
- **Flujo horizontal / entre módulos lado a lado**: `exit: [1, 0.5]` → `entry: [0, 0.5]` (o al revés) — y asegúrate de que el hueco entre las dos cajas sea lo bastante ancho para la etiqueta (ver "Espaciado generoso").
- **Actor hacia el sistema**: `exit: [0.5, 1]` → `entry: [0.5, 0]` — PERO si hay 2+ actores/orígenes apuntando a la misma caja, reparte los `entry` a lo ancho (`0.25`/`0.75` para 2, `0.2`/`0.5`/`0.8` para 3) en vez de que todos usen `0.5` — ver "Espaciado generoso" arriba.
- **Hacia/desde un sistema externo**: el lado que da hacia el boundary, normalmente `exit: [1, 0.5]`/`entry: [0, 0.5]`.
- Si la línea tendría que atravesar cajas de por medio, añade un desvío con `points`.
- Evita que una arista quede montada sobre el borde punteado de un `group`/`boundary`: que su cruce caiga en el espacio libre entre grupos.

## Flujo de trabajo

1. **Reunir el contenido primero**: actores, sistema (boundary), groups de cada capa, cada contenedor/componente, y relaciones (origen, destino, etiqueta, protocolo, lados a conectar).
2. **Clasifica en capas, define el group de cada una, y calcula coordenadas** con los mínimos de espaciado — nunca coordenadas apretadas ni una sola fila; dimensiona cada caja por su contenido, no por el ancho del group; si hay flechas horizontales etiquetadas entre módulos, calcula el gap entre ellos según el ancho de esas etiquetas antes de fijar las coordenadas.
3. **Para cada arista, decide `exit`/`entry`**, repartiendo entradas convergentes.
4. **Construir el JSON** con esas coordenadas, groups y anclajes.
5. **Escribir el JSON** a un archivo y **ejecutar el script embebido** (`c4_drawio.py`) con `python3 c4_drawio.py spec.json salida.drawio`.
6. **Validar el XML**: IDs de aristas existentes, capas sin solape, CADA capa con su `group`, espaciados cumpliendo los mínimos, `exit`/`entry` explícitos, entradas convergentes repartidas, ninguna caja estirada al ancho completo de su group, y ninguna etiqueta de flecha horizontal más ancha que el hueco entre sus cajas.
7. **Entregar el `.drawio`** al usuario.

## Reglas de estilo (no cambiar sin que el usuario lo pida)

- Tipografía: `Helvetica, Arial, sans-serif` (nunca una sola fuente), un punto más grande que el estándar de draw.io: nombre en negrita 13px, etiqueta `[Tag]` 9px, descripción 10px (ver script).
- Cajas de contenedor: fondo blanco, esquinas redondeadas (arcSize 10), borde gris `#8C8C8C` de 1px SIEMPRE (nunca colores automáticos); ancho por defecto 185 cuando no se calcula explícitamente por contenido, alto 115-130 (componentes: 60-90 de alto). Dimensiona por contenido, no por el ancho del group que la envuelve (ver "No estires las cajas..." arriba) — un contenedor único dentro de un group de ~600px normalmente usa ~380-450px de ancho, no el ancho completo.
- Ícono cuadrado de 36x36 con color de marca (`.NET` morado `#512BD4`, Vue verde `#42B883`, Azure SQL azul `#0078D4`, Blob Storage teal `#3A96B0`, Kafka negro `#231F20`, Entra ID azul `#0078D4`); si no hay ícono conocido, usa texto corto y color neutro, o pregunta. Componentes internos (Endpoints, Application, Domain, Infrastructure) usan `"tag": "[Component]"` sin `icon`.
- Bajo el nombre en negrita, etiqueta pequeña gris `#6B6B6B` (`[Container: Tech]`, `[External System]`, `[Person]`, `[Group]`, `[Component]`), tamaño 9px. El bloque título+etiqueta se dimensiona dinámicamente según cuántas líneas ocupará cada texto (ver script) — no fuerces una altura fija en el JSON que contradiga eso.
- Línea separadora horizontal gris clara entre el título y la descripción (su posición se calcula después del bloque de título, nunca a una altura fija).
- Descripción en gris oscuro `#333333`, tamaño 10px, alineada a la izquierda.
- Bases de datos y colas/tópicos: cilindro (`shape=cylinder3`, colas con `direction=south`). Dales un ancho de ~250-260px cuando el nombre de la tecnología sea largo (p. ej. "SQL Server / PostgreSQL") para que el título/etiqueta quepan en 1-2 líneas sin apretarse ni verse de más ancho de lo necesario (validado con render real: 260px es suficiente, no hace falta ir a 300px); el margen vertical/horizontal del cilindro (`top`≈30-34px, padding lateral 14px) evita que el ícono/título toquen la curva elíptica.
- Personas: óvalo (cabeza) + rectángulo redondeado debajo, mismo borde gris.
- Límites de sistema (`boundary`) y grupos lógicos (TODA capa): rectángulo sin relleno, borde punteado gris `#B3B3B3` (`dashPattern=8 8`), etiqueta en la esquina, con el padding generoso de la sección de espaciado (aplica solo a groups/boundary, no a las cajas individuales).
- Flechas: ortogonales, negras/gris oscuro `#333333`, punta rellena, ancladas siempre a `exit`/`entry` explícito con entradas convergentes repartidas, etiqueta + protocolo entre corchetes, fondo blanco detrás del texto. Cuando una flecha horizontal conecta dos módulos lado a lado, el hueco entre las cajas debe ser ≥ al ancho estimado de la etiqueta (ver "Espaciado generoso").
- Sistemas externos: mismo estilo de caja, etiqueta `[External System]`.

## Esquema del JSON de especificación

```json
{
  "title": "Nombre del diagrama",
  "page": [ancho, alto],
  "elements": [
    {"id": "unico", "kind": "person|boundary|group|container|external|database|queue",
     "name": "...", "tech": ".NET, Docker", "icon": "net|vue|sql|blob|kafka|entra|policy|smtp",
     "tag": "[Component]", "desc": "...", "x":0, "y":0, "w":185, "h":125}
  ],
  "edges": [
    {"from": "id_origen", "to": "id_destino", "label": "...", "protocol": "HTTPS / JSON", "dashed": false,
     "exit": [0.5, 1], "entry": [0.25, 0], "points": [[x1,y1], [x2,y2]]}
  ]
}
```

Notas:
- `kind: boundary` dibuja el rectángulo grande del sistema completo (`type` opcional, por defecto "Software System").
- `kind: group` dibuja el rectángulo punteado de UNA capa o módulo — TODA capa de contenedores lleva uno, sin excepción, con el padding generoso indicado arriba.
- `tag` sobreescribe la etiqueta por defecto bajo el nombre.
- Los `container`/`external`/`database`/`queue` deben ir dentro del rango x/y del `boundary`/`group` que los contiene visualmente (el anidamiento es solo geométrico), sin estirarse a su ancho completo.
- `exit`/`entry` son obligatorios salvo conexión vertical ya perfectamente alineada; reparte los `entry` cuando convergen varias flechas en la misma caja; `points` es opcional para desviar aristas.
- Si dos módulos lado a lado tienen una flecha horizontal etiquetada entre ellos, separa esos módulos (y las cajas que se conectan) según el ancho estimado de esa etiqueta, no según el gap genérico de 40-60px.
- No existe un campo de color de estado; todas las cajas usan el borde gris estándar salvo pedido explícito del usuario.
- Si un ícono no está en `ICONS`, pasa `"icon": {"text": "XX", "color": "#RRGGBB"}`.
- Añade nuevos íconos de marca al diccionario `ICONS` cuando aparezcan tecnologías recurrentes.

## Script generador

Guarda esto como `c4_drawio.py` antes de usarlo (no lo reescribas desde cero, es determinístico). El bloque título+etiqueta de cada caja se dimensiona dinámicamente según la longitud estimada del nombre y la etiqueta — esto es lo que evita que la línea separadora quede montada sobre un título largo (como en cilindros de base de datos con nombres de tecnología largos):

```python
#!/usr/bin/env python3
"""Genera un .drawio (mxGraph XML) con el estilo C4 del usuario.
Uso: python3 c4_drawio.py spec.json salida.drawio
"""
import html
import json
import math
import sys
from xml.sax.saxutils import quoteattr

# IMPORTANTE: reserva a Arial/sans-serif -- si se deja solo "Helvetica" y esa
# fuente no esta instalada en la maquina donde se abre el archivo, el motor
# de render puede sustituirla por una fuente mucho mas ancha y el texto se
# desborda sobre la linea separadora y la descripcion.
FONT = "Helvetica, Arial, sans-serif"
C = {
    "line": "#8C8C8C",
    "dash": "#B3B3B3",
    "group_txt": "#B3B3B3",
    "txt": "#000000",
    "desc": "#333333",
    "tag": "#6B6B6B",
    "edge": "#333333",
}
ICONS = {
    "net": (".NET", "#512BD4"),
    "vue": ("Vue", "#42B883"),
    "sql": ("SQL", "#0078D4"),
    "blob": ("Blob", "#3A96B0"),
    "kafka": ("Kafka", "#231F20"),
    "entra": ("Entra", "#0078D4"),
    "policy": ("Pol", "#3AA7E0"),
    "smtp": ("SMTP", "#7A7A7A"),
}

# Anchos de caracter promedio (px) para ESTIMAR cuantas lineas ocupara un
# texto -- recalibrados para los tamanos de fuente actuales (nombre 13px
# negrita, tag 9px normal). Deliberadamente generosos (sobreestiman) para
# evitar que el texto se monte sobre la linea separadora o la descripcion.
NAME_PX_PER_CHAR = 9.2   # negrita, 13px
TAG_PX_PER_CHAR = 6.1    # normal, 9px


def t(s):
    return html.escape(str(s), quote=False)


def attr(s):
    return quoteattr(s)


def tag(s):
    return f'<font style="font-size:9px" color="{C["tag"]}">{t(s)}</font>'


def est_lines(text, avail_w, px_per_char):
    if not text:
        return 0
    chars_per_line = max(1, int(avail_w / px_per_char))
    return max(1, math.ceil(len(text) / chars_per_line))


class Builder:
    def __init__(self):
        self.cells = []

    def v(self, id_, value, style, x, y, w, h, parent="1"):
        self.cells.append(
            f'<mxCell id="{id_}" value={attr(value)} style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    def e(self, id_, value, style, src, dst, points=None):
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(
                f'<mxPoint x="{px}" y="{py}"/>' for px, py in points
            ) + "</Array>"
        self.cells.append(
            f'<mxCell id="{id_}" value={attr(value)} style="{style}" edge="1" parent="1" '
            f'source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>'
        )


def boundary(b, e):
    label = f'<b>{t(e["name"])}</b><br>{tag("[" + e.get("type", "Software System") + "]")}'
    style = (f"rounded=0;html=1;whiteSpace=wrap;fillColor=none;dashed=1;dashPattern=8 8;"
             f"strokeColor={C['dash']};strokeWidth=1;align=left;verticalAlign=top;"
             f"spacingLeft=18;spacingTop=16;fontFamily={FONT};fontSize=14;fontColor={C['txt']};")
    b.v(e["id"], label, style, e["x"], e["y"], e["w"], e["h"])


def group(b, e):
    if e.get("name"):
        label = f'{t(e["name"])}<br>{tag("[Group]")}'
    else:
        label = ""
    style = (f"rounded=0;html=1;whiteSpace=wrap;fillColor=none;dashed=1;dashPattern=8 8;"
             f"strokeColor={C['dash']};strokeWidth=1;align=right;verticalAlign=top;"
             f"spacingRight=12;spacingTop=10;fontFamily={FONT};fontSize=12;fontColor={C['group_txt']};")
    b.v(e["id"], label, style, e["x"], e["y"], e["w"], e["h"])


def person(b, e):
    w, h = e.get("w", 120), e.get("h", 40)
    x, y = e["x"], e["y"]
    stroke = C["line"]
    b.v(e["id"] + "_head", "",
        f"ellipse;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=1;",
        x + w // 2 - 20, y - 50, 40, 40)
    label = f'<b>{t(e["name"])}</b><br>{tag("[Person]")}'
    b.v(e["id"], label,
        f"rounded=1;arcSize=12;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor={stroke};"
        f"strokeWidth=1;fontFamily={FONT};fontSize=10;fontColor={C['txt']};align=center;verticalAlign=middle;",
        x, y, w, h)


def card(b, e):
    kind = e.get("kind", "container")
    stroke = C["line"]
    w, h = e.get("w", 185), e.get("h", 130)
    x, y = e["x"], e["y"]
    top, right_pad, left_pad = 0, 8, 8
    if kind == "database":
        shape, top, left_pad, right_pad = "shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=18;", 34, 14, 14
    elif kind == "queue":
        shape, top, left_pad, right_pad = "shape=cylinder3;direction=south;boundedLbl=1;backgroundOutline=1;size=18;", 30, 14, 30
    else:
        shape = "rounded=1;arcSize=10;"
    pid = e["id"]
    b.v(pid, "", f"{shape}html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor={stroke};strokeWidth=1;",
        x, y, w, h)

    icon = e.get("icon")
    if isinstance(icon, str):
        icon = ICONS.get(icon)
    elif isinstance(icon, dict):
        icon = (icon["text"], icon["color"])
    title_x = left_pad
    if icon:
        b.v(pid + "_icon", t(icon[0]),
            f"rounded=1;arcSize=12;html=1;whiteSpace=wrap;fillColor={icon[1]};strokeColor=none;"
            f"fontColor=#FFFFFF;fontStyle=1;fontSize=10;fontFamily={FONT};align=center;verticalAlign=middle;",
            left_pad, top + 8, 36, 36, parent=pid)
        title_x = left_pad + 42

    if e.get("tag"):
        tg = e["tag"]
    elif kind == "external":
        tg = "[External System]"
    elif e.get("tech"):
        tg = f"[Container: {e['tech']}]"
    else:
        tg = ""

    name = e["name"]
    label = f'<b>{t(name)}</b>' + (f"<br>{tag(tg)}" if tg else "")
    title_w = w - title_x - right_pad

    # Reserva dinamica de alto para el bloque titulo+tag segun cuantas lineas
    # se estima que ocuparan (evita que la linea separadora quede montada
    # sobre un titulo/tag que se envuelve a 2+ lineas -- este era el bug que
    # hacia ver mal los cilindros de base de datos con nombres largos).
    name_lines = est_lines(name, title_w, NAME_PX_PER_CHAR)
    tag_lines = est_lines(tg, title_w, TAG_PX_PER_CHAR)
    title_block_h = name_lines * 19 + (6 if tag_lines else 0) + tag_lines * 13 + 10
    title_block_h = max(title_block_h, 36)

    b.v(pid + "_title", label,
        f"text;html=1;whiteSpace=wrap;align=center;verticalAlign=top;fillColor=none;strokeColor=none;"
        f"fontFamily={FONT};fontSize=13;fontColor={C['txt']};",
        title_x, top + 6, title_w, title_block_h, parent=pid)

    sep_y = top + 6 + title_block_h + 6
    b.v(pid + "_sep", "",
        f"line;strokeWidth=1;fillColor=none;strokeColor={C['dash']};align=left;verticalAlign=middle;"
        f"points=[];rotatable=0;",
        left_pad, sep_y, w - left_pad - right_pad, 8, parent=pid)

    desc_y = sep_y + 12
    desc = e.get("desc", "")
    b.v(pid + "_desc", t(desc),
        f"text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fillColor=none;strokeColor=none;"
        f"fontFamily={FONT};fontSize=10;fontColor={C['desc']};spacing=0;",
        left_pad, desc_y, w - left_pad - right_pad, max(h - desc_y - 8, 20), parent=pid)


def edge(b, i, d):
    label = t(d.get("label", ""))
    if d.get("protocol"):
        label += f"<br>[{t(d['protocol'])}]"
    style = (f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;endSize=6;"
             f"strokeColor={C['edge']};strokeWidth=1;fontFamily={FONT};fontSize=9;fontColor={C['txt']};"
             f"labelBackgroundColor=#FFFFFF;")
    if d.get("dashed"):
        style += "dashed=1;"
    for k, name in (("exit", "exit"), ("entry", "entry")):
        if d.get(k):
            style += f"{name}X={d[k][0]};{name}Y={d[k][1]};{name}Dx=0;{name}Dy=0;"
    b.e(f"edge{i}", label, style, d["from"], d["to"], d.get("points"))


def build(spec):
    b = Builder()
    els = spec["elements"]
    for e in els:
        if e["kind"] == "boundary":
            boundary(b, e)
        elif e["kind"] == "group":
            group(b, e)
    for e in els:
        if e["kind"] == "person":
            person(b, e)
        elif e["kind"] in ("container", "external", "database", "queue"):
            card(b, e)
    for i, d in enumerate(spec.get("edges", []), 1):
        edge(b, i, d)
    pw, ph = spec.get("page", [1100, 1600])
    return (
        '<mxfile host="app.diagrams.net"><diagram name="' + html.escape(spec.get("title", "C4"), quote=True) +
        '" id="c4-1"><mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" '
        f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw}" pageHeight="{ph}" '
        'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
        + "".join(b.cells) + "</root></mxGraphModel></diagram></mxfile>"
    )


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(build(spec))
    print("OK ->", sys.argv[2])
```

## Verificación antes de entregar

- Parsear el `.drawio` con `xml.etree.ElementTree` y confirmar que todas las aristas referencian IDs existentes.
- Revisar las cajas de nivel superior (boundary/groups) y confirmar que envuelven visualmente a sus hijos con el padding mínimo de la sección "Espaciado generoso" (no solo que las contengan, sino que haya aire), y que ninguna caja de contenedor está estirada al ancho completo de su group.
- **Comprobar el apilado por capas**: cada capa con `y` creciente, sin solape, y con ≥ 80-90px de separación entre groups y ≥120-130px entre actores y boundary.
- **Confirmar que cada capa de contenedores tiene su `group`** (frontend y persistencia incluidos).
- **Revisar cada arista**: `exit`/`entry` explícitos, sin atravesar cajas intermedias, con las entradas convergentes repartidas (nunca dos flechas con `entry` idéntico sobre la misma caja), y para cada flecha horizontal etiquetada entre módulos, que el hueco entre las cajas sea ≥ al ancho estimado del texto de la etiqueta (≥180-220px para etiquetas típicas de 2 líneas de 25-35 caracteres).
- Confirmar que `FONT` sigue siendo `"Helvetica, Arial, sans-serif"`.
- Confirmar que ningún elemento lleva un color de borde distinto al gris estándar salvo pedido explícito del usuario en ese mismo turno.
- Para bases de datos/colas con nombres de tecnología largos, confirmar que el ancho (`w`) es de ~250-260px (no más) para que el bloque título (dimensionado dinámicamente por el script) quepa en 1-2 líneas sin verse apretado ni desproporcionadamente ancho.