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

    def e(self, id_, value, style, src, dst, parent, points=None, label_offset=None):
        pts = ""
        if points:
            pts = '<Array as="points">' + "".join(
                f'<mxPoint x="{px}" y="{py}"/>' for px, py in points
            ) + "</Array>"
        geom = 'relative="1" as="geometry"'
        offset_tag = ""
        if label_offset:
            along, perp = label_offset
            geom = f'relative="1" as="geometry" x="{along}" y="0"'
            offset_tag = f'<mxPoint x="{perp}" y="0" as="offset"/>'
        self.cells.append(
            f'<mxCell id="{id_}" value={attr(value)} style="{style}" edge="1" parent="{parent}" '
            f'source="{src}" target="{dst}"><mxGeometry {geom}>{offset_tag}{pts}</mxGeometry></mxCell>'
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
        f"jettySize=auto;orthogonalLoop=1;labelBackgroundColor=#FFFFFF;"
    )
    for k, name in (("exit", "exit"), ("entry", "entry")):
        if d.get(k):
            style += f"{name}X={d[k][0]};{name}Y={d[k][1]};{name}Dx=0;{name}Dy=0;"
            if k == "entry":
                style += "entryPerimeter=0;"
    b.e(f"edge{i}", label, style, d["from"], d["to"], d.get("parent", "1"), d.get("points"), d.get("label_offset"))


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
