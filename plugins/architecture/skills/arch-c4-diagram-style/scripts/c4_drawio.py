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
    "postgres": ("PG", "#336791"),
    "aws": ("AWS", "#232F3E"),
}

# Anchos de caracter promedio (px) para ESTIMAR cuantas lineas ocupara un
# texto -- recalibrados para los tamanos de fuente actuales (nombre 13px
# negrita, tag 9px normal). Deliberadamente generosos (sobreestiman) para
# evitar que el texto se monte sobre la linea separadora o la descripcion.
NAME_PX_PER_CHAR = 9.2   # negrita, 13px
TAG_PX_PER_CHAR = 6.1    # normal, 9px
DESC_PX_PER_CHAR = 6.0   # normal, 10px


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

    def e(self, id_, value, style, src, dst, points=None, label_offset=None):
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
            f'<mxCell id="{id_}" value={attr(value)} style="{style}" edge="1" parent="1" '
            f'source="{src}" target="{dst}"><mxGeometry {geom}>{offset_tag}{pts}</mxGeometry></mxCell>'
        )


def boundary(b, e):
    label = f'<b>{t(e["name"])}</b><br>{tag("[" + e.get("type", "Software System") + "]")}'
    style = (f"rounded=0;html=1;whiteSpace=wrap;fillColor=none;dashed=1;dashPattern=8 8;"
             f"strokeColor={C['dash']};strokeWidth=1;align=left;verticalAlign=top;"
             f"spacingLeft=18;spacingTop=16;fontFamily={FONT};fontSize=14;fontColor={C['txt']};")
    if e.get("label_bottom"):
        style = style.replace("verticalAlign=top;", "verticalAlign=bottom;").replace(
            "spacingTop=16;", "spacingBottom=12;")
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
    main_idx = len(b.cells)
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
    # Alto minimo para que la descripcion no se salga de la caja ni caiga
    # sobre el arco inferior de un cilindro: si no alcanza, la caja crece y
    # se avisa por consola para reacomodar el grupo que la envuelve.
    desc_w = w - left_pad - right_pad
    desc_h = est_lines(desc, desc_w, DESC_PX_PER_CHAR) * 13 if desc else 0
    bottom = 28 if kind in ("database", "queue") else 8
    min_h = desc_y + desc_h + bottom
    if h < min_h:
        print(f"AVISO: {pid} crecio de {h} a {min_h} de alto para que quepa su descripcion; "
              f"revisa el group que lo envuelve.", file=sys.stderr)
        h = min_h
        b.cells[main_idx] = b.cells[main_idx].replace(f'height="{e.get("h", 130)}"', f'height="{h}"')
    b.v(pid + "_desc", t(desc),
        f"text;html=1;whiteSpace=wrap;align=left;verticalAlign=top;fillColor=none;strokeColor=none;"
        f"fontFamily={FONT};fontSize=10;fontColor={C['desc']};spacing=0;",
        left_pad, desc_y, desc_w, max(h - desc_y - bottom, 20), parent=pid)


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
    b.e(f"edge{i}", label, style, d["from"], d["to"], d.get("points"), d.get("label_offset"))


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
