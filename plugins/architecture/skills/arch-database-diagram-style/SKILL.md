---
name: "arch-database-diagram-style"
description: "Usar cuando se pida crear o actualizar un diagrama de modelo de datos conceptual/lógico (entidades, entidades débiles, enumeraciones, agrupaciones «Context», notas) como archivo .drawio editable, replicando su estilo visual: cajas UML con tira superior negra (estereotipo «Entity»/«WeakEntity»/«Enumeration» + nombre en blanco) y cuerpo blanco con atributos con \"+\" y claves subrayadas, agrupaciones grandes con pestaña negra «Context», notas amarillas tipo post-it, encabezado de texto con título/descripción/metadatos, y flechas de relación con notación de cardinalidad ER. No aplica a diagramas C4 (usar arch-c4-diagram-style) ni a diagramas de despliegue AWS (usar arch-aws-diagram-style)."
---

# Estilo de diagramas de modelo de datos (draw.io)

Esta skill genera diagramas de modelo de datos (conceptual o lógico) como archivos `.drawio` editables, replicando el estilo visual de un diagrama de referencia mostrado en una captura de pantalla (con entidades, entidades débiles, enumeraciones, agrupaciones «Context» y notas amarillas).

**IMPORTANTE — esto es distinto a las otras dos skills de diagramas:** para `arch-c4-diagram-style` y `arch-aws-diagram-style` sí tuvimos un `.drawio` real de referencia del que se extrajeron los estilos exactos carácter por carácter. Para ESTA skill, en cambio, **no había un archivo real al principio** — el estilo base se reconstruyó a partir de una sola captura de pantalla, usando formas NATIVAS de draw.io (rectángulos, texto, la forma `note`, flechas con marcadores ER estándar) en vez de stencils exóticos — por eso el riesgo de "forma no encontrada" es bajo. Ya se corrigieron dos bugs reales tras la primera corrida (ver abajo), pero **los símbolos exactos de cardinalidad de las flechas siguen sin confirmar** — trata eso como estimado hasta que el usuario lo confirme, y sigue afinándolo con cada corrida como se hizo con las otras dos skills (pedir el `.drawio` resultante cuando el usuario reporte una diferencia, comparar, corregir el script, verificar con un render antes de responder — nunca a ojo).

## Cuándo usarla

Siempre que el usuario pida crear, rehacer o extender un diagrama de modelo de datos (conceptual o lógico): entidades y sus atributos, entidades débiles (asociativas/de relación), enumeraciones, agrupaciones temáticas tipo "Context"/módulo, notas explicativas. No usar para diagramas C4 (usar `arch-c4-diagram-style`) ni para diagramas de despliegue/arquitectura AWS (usar `arch-aws-diagram-style`).

## Elementos visuales (base ESTIMADA a partir de la captura — dos bugs ya corregidos, ver "Bugs reales corregidos")

- **Encabezado de texto** (fuera de cualquier caja, arriba a la izquierda de la página): título en negrita grande, subtítulo entre corchetes en cursiva gris debajo (p. ej. "[Conceptual Model Diagram]"), luego un párrafo "Descripción: ...", y una línea de metadatos ("Vista: ... | Modelo: ... | Versión: ... | Fecha: ..."). Sin bordes ni relleno, solo texto.
- **Agrupación «Context»**: un rectángulo grande de fondo blanco y borde gris fino que envuelve varias entidades relacionadas temáticamente, con una pestaña negra pegada a su borde superior izquierdo (ligeramente montada sobre el borde) que dice "«Context» NombreDelContexto" en blanco y negrita, con el ANCHO calculado a partir del texto completo de la pestaña (ver bug corregido abajo). Es un `container=1` para que las entidades dentro tengan coordenadas relativas a él.
- **Entidad / Entidad débil**: caja UML de dos partes — tira superior negra con el estereotipo `«Entity»` o `«WeakEntity»` en una línea y el nombre en blanco y negrita debajo (color fijado EXPLÍCITO en el texto, ver bug corregido abajo), y un cuerpo blanco debajo listando los atributos, uno por línea, cada uno con "+ " al inicio y `Nombre: Tipo`; los atributos que son clave (primaria o de la relación en una entidad débil) van SUBRAYADOS.
- **Enumeración**: misma caja de dos partes, tira superior con `«Enumeration»` + nombre, cuerpo listando `+ NOMBRE = "Valor"` o `+ NOMBRE = Número`.
- **Nota**: rectángulo amarillo con la esquina superior derecha doblada (forma `note` de draw.io), borde amarillo/ocre, texto negro alineado a la izquierda — se usa para aclaraciones sueltas (convenciones de nombres, ejemplos de valores, advertencias sobre campos calculados, etc.), normalmente flotando cerca de la entidad a la que aplica, sin conectarla con una flecha.
- **Flechas de relación**: líneas ortogonales grises finas entre entidades, con una etiqueta corta en el punto medio describiendo el rol de la relación (p. ej. "Zonas Proyecto", "Subproyectos", "clasifica"), y marcadores de cardinalidad en cada extremo (notación tipo Entidad-Relación: uno, cero-o-uno, muchos, cero-o-muchos, etc.). **Los símbolos exactos que usa el usuario (algo como "+"/"o"/"×" en su captura) NO están confirmados** — el generador usa los marcadores ER estándar de draw.io (`ERone`, `ERmandOne`, `ERzeroToOne`, `ERmany`, `ERoneToMany`, `ERzeroToMany`) como mejor aproximación; pedir al usuario que confirme o corrija cuando lo revise.

## Bugs reales corregidos (verificados contra el `.drawio` real que el usuario generó con esta skill)

El usuario aplicó la primera versión de esta skill y reportó dos defectos visuales reales, ya corregidos en el script de abajo:

1. **El nombre de la entidad/enumeración no salía en blanco** (se veía gris apagado sobre el fondo negro, difícil de leer), aunque el estilo de la celda ya tenía `fontColor=#FFFFFF`. La causa: el nombre iba dentro de un `<b>` anidado sin color propio, y en el draw.io real ese `<b>` no heredaba el `fontColor` del estilo de la celda (a diferencia de lo que se veía en el render de prueba con mxgraph puro, donde sí heredaba — otra diferencia entre el arnés de verificación y el draw.io real, como ya había pasado con los iconos badge de AWS). **Solución verificada**: fijar `color:#FFFFFF` EXPLÍCITO en el propio `<span>`/`<b>` del texto (estereotipo y nombre), no solo confiar en el `fontColor` del estilo de la celda contenedora.
2. **La pestaña «Context» quedaba más angosta que su propio texto** y draw.io la recortaba (`whiteSpace=nowrap` evita el salto de línea pero NO ensancha la caja sola). La causa: la fórmula de ancho solo contaba los caracteres del NOMBRE del contexto (`len(name)`) e ignoraba el prefijo fijo `"«Context» "` (10 caracteres) que también forma parte del mismo texto sin salto de línea. **Solución verificada**: calcular el ancho a partir de la LONGITUD TOTAL de la etiqueta completa (`"«Context» " + nombre`), con una estimación generosa de `8.5px` por carácter (fuente negrita ~12px) más `44px` de margen — mejor una pestaña un poco más ancha de lo necesario que una recortada.

Si el usuario vuelve a reportar cualquiera de estos dos síntomas (nombre gris en vez de blanco, o pestaña «Context» con texto cortado), revisar primero si el script embebido de abajo sigue teniendo estas dos correcciones — no reintroducir la versión vieja por error al copiar.

## Flujo de trabajo

1. **Reunir el contenido primero**: qué entidades (fuertes y débiles), qué atributos tiene cada una y cuáles son clave, qué enumeraciones existen y qué valores tienen, en qué agrupaciones «Context» se organizan, qué relaciones hay entre ellas (con su cardinalidad y etiqueta de rol), y qué notas aclaratorias hacen falta.
2. **Agrupar por Context**: cada agrupación temática es un elemento `context` (container), y cada entidad/enumeración/nota que le pertenece visualmente lleva `parent` = el id de ese context, con coordenadas relativas a él.
3. **Calcular el tamaño de cada entidad por CONTENIDO**: alto = altura de la tira del encabezado (`start_size`, típicamente 34) + ~18-20px por línea de atributo + margen; ancho = suficiente para que quepa el atributo más largo sin que el texto se corte (aprox. 8-9px por carácter del atributo `Nombre: Tipo` más largo, con un mínimo de ~160-200px). Igual que en `arch-c4-diagram-style` y `arch-aws-diagram-style`: nunca estirar una caja a un tamaño redondo arbitrario, dimensionarla por lo que realmente contiene.
4. **Calcular el tamaño de cada `context` por CONTENIDO**, igual que los contenedores AWS: ancho/alto = extremo del hijo más lejano (entidad, enumeración o nota) + margen (~30-40px), nunca al revés. El ancho de la PESTAÑA del context es independiente de esto — se calcula del largo de su propio texto (ver "Bugs reales corregidos").
5. **Construir el JSON** con esa jerarquía, dando `label` (rol de la relación), `start`/`end` (cardinalidad) a cada `edge`.
6. **Escribir el JSON** a un archivo y **ejecutar el script embebido** (`db_drawio.py`) con `python3 db_drawio.py spec.json salida.drawio`.
7. **Validar el XML** con `xml.etree.ElementTree`: que todo `parent` referenciado exista, que las aristas referencien IDs existentes.
8. **Renderizar y revisar visualmente antes de entregar** cuando sea posible (igual que con las otras dos skills: mxgraph + Playwright) — pero recordar que el arnés de prueba puede NO reproducir todos los defectos reales (como el bug del color del nombre, que en el render de prueba sí se veía bien): cuando el usuario reporte algo que el render no mostró, pedir el `.drawio` real y confiar en él por encima del render de prueba.
9. **Entregar el `.drawio`** al usuario, dejando claro en la respuesta que los símbolos de cardinalidad de las flechas son una estimación pendiente de confirmar.

## Esquema del JSON de especificación

```json
{
  "title": "Nombre del diagrama",
  "page": [ancho, alto],
  "elements": [
    {"id": "hdr", "kind": "header", "x": 20, "y": 10, "w": 700, "h": 90,
     "title": "Diagrama de Modelo de Datos Conceptual de X",
     "subtitle": "Conceptual Model Diagram",
     "description": "Descripción corta del diagrama.",
     "meta": "Vista: Información | Modelo: Datos Conceptual | Versión: 1.0 | Fecha: 2026-09-20"},

    {"id": "ctx1", "kind": "context", "name": "NombreDelContexto", "x": 20, "y": 130, "w": 620, "h": 420, "parent": "1"},

    {"id": "entidad1", "kind": "entity", "name": "Proyecto", "x": 60, "y": 40, "w": 200, "h": 140, "parent": "ctx1",
     "attrs": [
       {"name": "IDProyecto", "type": "String", "key": true},
       {"name": "Nombre", "type": "String"},
       {"name": "Estado", "type": "EstadoProyecto"}
     ]},

    {"id": "entidad_debil1", "kind": "entity", "weak": true, "name": "ProyectoZonaRegion", "x": 340, "y": 40, "w": 220, "h": 90, "parent": "ctx1",
     "attrs": [
       {"name": "IDProjectId", "type": "String", "key": true},
       {"name": "IDZonaRegion", "type": "String", "key": true}
     ]},

    {"id": "enum1", "kind": "enum", "name": "EstadoProyecto", "x": 60, "y": 230, "w": 200, "h": 100, "parent": "ctx1",
     "values": [
       {"name": "ACTIVO", "value": "0"},
       {"name": "INACTIVO", "value": "1"}
     ]},

    {"id": "nota1", "kind": "note", "x": 340, "y": 180, "w": 220, "h": 100, "parent": "ctx1",
     "text": "Texto de la nota aclaratoria."}
  ],
  "edges": [
    {"from": "entidad1", "to": "entidad_debil1", "parent": "1", "label": "Zonas Proyecto", "start": "mandatory_one", "end": "zero_or_many"}
  ]
}
```

Notas:
- `kind`: `header` (bloque de texto libre) | `context` (agrupación grande con pestaña «Context», container) | `entity` (caja Entity/WeakEntity según `weak`) | `enum` (caja Enumeration) | `note` (post-it amarillo).
- `parent`: id del `context` que lo envuelve visualmente, o `"1"` si no está dentro de ninguno. Coordenadas `x`/`y` relativas al `parent` (salvo `parent: "1"`, que son absolutas de página).
- `entity.attrs[].key`: `true` subraya el atributo (clave primaria o clave de relación en una entidad débil).
- `edge.start`/`edge.end`: uno de `one | mandatory_one | zero_or_one | many | one_or_many | zero_or_many | none` — mapean a los marcadores ER de draw.io (`ERone`, `ERmandOne`, `ERzeroToOne`, `ERmany`, `ERoneToMany`, `ERzeroToMany`). Ver la advertencia de "Elementos visuales" sobre esto — es una estimación.
- `edge.label`: el rol/nombre de la relación, se muestra centrado sobre la línea.

## Script generador

Guarda esto como `db_drawio.py` (no lo reescribas desde cero, es determinístico):

```python
#!/usr/bin/env python3
"""Genera un .drawio (mxGraph XML) de diagramas de modelo de datos conceptual
con el estilo (clases UML tipo Entity/WeakEntity/Enumeration, frames
"Context", notas amarillas, relaciones ER). Base ESTIMADA a partir de una
captura de pantalla -- no de un .drawio real -- pedir al usuario un archivo real
para afinar simbolos exactos de las flechas de relacion si algo no calza.

Uso: python3 db_drawio.py spec.json salida.drawio
"""
import html
import json
import sys
from xml.sax.saxutils import quoteattr

EDGE_COLOR = "#666666"

HEADER_STYLE = (
    "text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;"
    "rounded=0;fontColor=#000000;fillColor=none;strokeColor=none;"
)

CONTEXT_BODY_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#999999;"
    "verticalAlign=top;align=left;spacingTop=14;spacingLeft=10;container=1;"
    "collapsible=0;recursiveResize=0;"
)
CONTEXT_TAB_STYLE = (
    "rounded=0;whiteSpace=nowrap;html=1;fillColor=#000000;strokeColor=#000000;"
    "fontColor=#FFFFFF;fontStyle=1;align=left;spacingLeft=6;fontSize=12;"
)

# Clase UML de 2 niveles, construida a mano con 3 celdas (evita depender de
# claves de estilo "swimlane"/"swimlaneFillColor" que no siempre se respetan
# igual fuera del editor real de draw.io):
#   1) CLASS_CONTAINER_STYLE: el rectangulo contenedor completo (container=1,
#      fondo blanco, borde negro) -- todo lo demas es hijo suyo con
#      coordenadas relativas.
#   2) CLASS_HEADER_STYLE: tira superior fija (fondo negro, texto blanco
#      centrado) del alto "start_size", con el estereotipo + nombre.
#   3) CLASS_BODY_STYLE: bloque de texto debajo del header con la lista de
#      atributos, uno por linea, con "+" al inicio y subrayado en las claves.
CLASS_CONTAINER_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;"
    "verticalAlign=top;container=1;collapsible=0;recursiveResize=0;"
)
CLASS_HEADER_STYLE = (
    "rounded=0;whiteSpace=wrap;html=1;fillColor=#000000;strokeColor=#000000;"
    "fontColor=#FFFFFF;fontStyle=1;align=center;verticalAlign=middle;fontSize=12;"
)
CLASS_BODY_STYLE = (
    "text;align=left;verticalAlign=top;spacingLeft=6;spacingTop=4;fontSize=11;"
    "strokeColor=none;fillColor=none;fontColor=#000000;html=1;whiteSpace=wrap;"
)

NOTE_STYLE = (
    "shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;"
    "fillColor=#FFF9B2;strokeColor=#D6B656;fontColor=#000000;align=left;"
    "verticalAlign=top;spacingLeft=6;spacingTop=6;fontSize=11;size=16;"
)

# Simbolos de extremo ER -- ESTIMADOS (no verificados contra un .drawio real
# del usuario). El original usa un notacion con "+"/"o"/"x" en los extremos que
# probablemente viene de otra herramienta (Sparx EA); estos son los
# equivalentes mas cercanos disponibles en draw.io. Pedir al usuario su archivo
# real si necesita que calcen exacto.
CARDINALITY = {
    "one": "ERone",
    "mandatory_one": "ERmandOne",
    "zero_or_one": "ERzeroToOne",
    "many": "ERmany",
    "one_or_many": "ERoneToMany",
    "zero_or_many": "ERzeroToMany",
    "none": "none",
}


def t(s):
    return html.escape(str(s), quote=False)


def attr(s):
    return quoteattr(s)


class Builder:
    def __init__(self):
        self.cells = []

    def v(self, id_, value, style, x, y, w, h, parent):
        self.cells.append(
            f'<mxCell id="{id_}" value={attr(value)} style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )

    def e(self, id_, value, style, src, dst, parent, points=None):
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(
                f'<mxPoint x="{px}" y="{py}"/>' for px, py in points
            ) + "</Array>"
        self.cells.append(
            f'<mxCell id="{id_}" value={attr(value)} style="{style}" edge="1" parent="{parent}" '
            f'source="{src}" target="{dst}"><mxGeometry relative="1" as="geometry">{pts}</mxGeometry></mxCell>'
        )


def header_el(b, e):
    lines = []
    if e.get("title"):
        lines.append(f'<b style="font-size:16px">{t(e["title"])}</b>')
    if e.get("subtitle"):
        lines.append(f'<i style="color:#666666">[{t(e["subtitle"])}]</i>')
    if e.get("description"):
        lines.append(f'<div style="margin-top:6px">Descripción: {t(e["description"])}</div>')
    if e.get("meta"):
        lines.append(f'<div style="margin-top:6px;color:#333333">{t(e["meta"])}</div>')
    value = "<br>".join(lines)
    b.v(e["id"], value, HEADER_STYLE, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))


def context_el(b, e):
    body_id = e["id"]
    b.v(body_id, "", CONTEXT_BODY_STYLE, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))
    tab_label = f'«Context» {t(e.get("name", ""))}'
    # Ancho estimado a partir del texto COMPLETO de la pestana (estereotipo +
    # nombre), no solo del nombre -- ese fue el bug real: la formula anterior
    # solo contaba len(name) e ignoraba "«Context» " (10 caracteres), asi que
    # la pestana quedaba mas angosta que el texto y draw.io lo recortaba
    # (whiteSpace=nowrap no ensancha la caja, solo evita el salto de linea).
    # 8.5px/caracter es una sobreestimacion deliberada para fuente negrita
    # ~12px -- mejor una pestana un poco mas ancha que una recortada.
    tab_w = int(8.5 * len(tab_label)) + 44
    b.v(f"{body_id}_tab", tab_label, CONTEXT_TAB_STYLE, e["x"] + 8, e["y"] - 13, tab_w, 24, e.get("parent", "1"))


def _class_shell(b, e, stereotype, name):
    start_size = e.get("start_size", 34)
    # 1) contenedor
    b.v(e["id"], "", CLASS_CONTAINER_STYLE, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))
    # 2) header (hijo, coordenadas relativas al contenedor)
    # color:#FFFFFF puesto EXPLICITO en cada tag de texto (no solo en el
    # fontColor del estilo de la celda) -- bug real observado: en draw.io
    # real, el nombre dentro del <b> salia gris en vez de blanco pese a
    # fontColor=#FFFFFF en el style, por no heredar el color en ese contexto.
    # Fijarlo inline evita depender de esa herencia.
    header_value = (
        f'<span style="color:#FFFFFF">«{t(stereotype)}»</span><br>'
        f'<b style="font-size:13px;color:#FFFFFF">{t(name)}</b>'
    )
    b.v(f'{e["id"]}_hdr', header_value, CLASS_HEADER_STYLE, 0, 0, e["w"], start_size, e["id"])
    return start_size


def entity_el(b, e):
    stereotype = "WeakEntity" if e.get("weak") else "Entity"
    start_size = _class_shell(b, e, stereotype, e.get("name", ""))
    rows = []
    for a in e.get("attrs", []):
        text = f'{a["name"]}: {a.get("type", "")}' if a.get("type") else a["name"]
        text = f'<span style="text-decoration:underline">{t(text)}</span>' if a.get("key") else t(text)
        rows.append(f'+ {text}')
    body_value = "<br>".join(rows)
    body_h = e["h"] - start_size
    b.v(f'{e["id"]}_attrs', body_value, CLASS_BODY_STYLE, 0, start_size, e["w"], body_h, e["id"])


def enum_el(b, e):
    start_size = _class_shell(b, e, "Enumeration", e.get("name", ""))
    rows = []
    for v in e.get("values", []):
        rows.append(f'+ {t(v["name"])} = {t(v["value"])}')
    body_value = "<br>".join(rows)
    body_h = e["h"] - start_size
    b.v(f'{e["id"]}_attrs', body_value, CLASS_BODY_STYLE, 0, start_size, e["w"], body_h, e["id"])


def note_el(b, e):
    b.v(e["id"], t(e.get("text", "")), NOTE_STYLE, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))


def edge_el(b, i, d):
    label = t(d.get("label", ""))
    start_arrow = CARDINALITY.get(d.get("start", "none"), "none")
    end_arrow = CARDINALITY.get(d.get("end", "none"), "none")
    style = (
        f"edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;strokeColor={EDGE_COLOR};"
        f"fontColor=#000000;startArrow={start_arrow};startFill=1;endArrow={end_arrow};endFill=1;"
        f"jettySize=auto;orthogonalLoop=1;"
    )
    for k, name in (("exit", "exit"), ("entry", "entry")):
        if d.get(k):
            style += f"{name}X={d[k][0]};{name}Y={d[k][1]};{name}Dx=0;{name}Dy=0;"
            if k == "entry":
                style += "entryPerimeter=0;"
    b.e(f"edge{i}", label, style, d["from"], d["to"], d.get("parent", "1"), d.get("points"))


KIND_DISPATCH = {
    "header": header_el, "context": context_el,
    "entity": entity_el, "enum": enum_el, "note": note_el,
}


def build(spec):
    b = Builder()
    els = spec["elements"]
    order = ["header", "context", "entity", "enum", "note"]
    by_kind = {}
    for e in els:
        by_kind.setdefault(e["kind"], []).append(e)
    for k in order:
        for e in by_kind.get(k, []):
            KIND_DISPATCH[k](b, e)
    for i, d in enumerate(spec.get("edges", []), 1):
        edge_el(b, i, d)
    pw, ph = spec.get("page", [1600, 1200])
    return (
        '<mxfile host="app.diagrams.net"><diagram name="' + html.escape(spec.get("title", "Modelo de Datos"), quote=True) +
        '" id="db-1"><mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
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

- Parsear el `.drawio` con `xml.etree.ElementTree`: confirmar que todo `parent` referenciado existe como `id` de otro elemento (o es `"1"`), y que las aristas referencian IDs existentes.
- Confirmar que cada entidad/enumeración está dimensionada por contenido (alto = tira de encabezado + ~18-20px por atributo + margen), no con un tamaño redondo arbitrario.
- Confirmar que cada `context` está dimensionado por el extremo del hijo más lejano + margen, igual que los contenedores de `arch-aws-diagram-style`.
- **Confirmar que la pestaña «Context» usa el ancho calculado sobre el texto COMPLETO (estereotipo + nombre), no solo el nombre** — si el usuario reporta texto cortado en la pestaña, es este bug (ver "Bugs reales corregidos").
- **Confirmar que el nombre de cada entidad/enumeración lleva `color:#FFFFFF` inline en su propio tag** (no solo `fontColor` en el estilo de la celda) — si el usuario reporta el nombre en gris en vez de blanco, es este bug (ver "Bugs reales corregidos").
- Confirmar que las entidades débiles usan el estereotipo `«WeakEntity»` (no `«Entity»`) y que sus atributos clave (generalmente los que forman la clave compuesta) están subrayados.
- **Recordar en la respuesta al usuario que los símbolos de cardinalidad de las flechas son una estimación** y pedirle que los confirme o corrija.
- Si es posible, renderizar el resultado (mxgraph + Playwright) antes de entregar, sabiendo que el arnés de prueba puede no reproducir todos los defectos reales de draw.io (como el bug del color heredado) — el archivo real que abre el usuario manda por encima del render de prueba.