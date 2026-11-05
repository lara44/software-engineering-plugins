#!/usr/bin/env python3
"""Genera un diagrama de secuencia .drawio con el mismo estilo de los diagramas C4.
Uso: python3 seq_drawio.py spec.json salida.drawio

spec.json:
{
  "title": "UC-03 Confirmar pedido",
  "participants": [
    {"id": "u",   "name": "Vendedor", "kind": "person"},
    {"id": "web", "name": "Aplicacion web", "tag": "Container"},
    {"id": "dis", "name": "Pedidos", "tag": "Component"}
  ],
  "messages": [
    {"from": "u",   "to": "web", "label": "Confirma el pedido"},
    {"from": "web", "to": "dis", "label": "confirmarPedido(pedidoId)"},
    {"from": "dis", "to": "dis", "label": "Valida el programa"},
    {"from": "dis", "to": "web", "label": "Pedido confirmado", "reply": true}
  ]
}
"""
import html
import json
import sys
from xml.sax.saxutils import quoteattr

FONT = "Helvetica, Arial, sans-serif"
LINE = "#8C8C8C"
DASH = "#B3B3B3"
TXT = "#000000"
TAGC = "#6B6B6B"
EDGE = "#333333"

NAME_PX = 9.2      # negrita 13 px
MIN_W = 150
PAD_W = 36
GAP = 70           # espacio horizontal entre participantes
TOP = 70           # margen superior (deja sitio a la cabeza de las personas)
HEAD_H = 56
FIRST_MSG = 60     # distancia de la cabecera al primer mensaje
STEP = 48          # distancia entre mensajes
SELF_W = 40        # ancho del lazo de un mensaje a si mismo
MSG_PX = 6.3       # caracteres de la etiqueta, 10 px


def t(s):
    return html.escape(str(s), quote=False)


class B:
    def __init__(self):
        self.cells = []
        self.n = 0

    def nid(self, p):
        self.n += 1
        return f"{p}{self.n}"

    def v(self, value, style, x, y, w, h):
        self.cells.append(
            f'<mxCell id="{self.nid("v")}" value={quoteattr(value)} style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')

    def line(self, value, style, pts):
        (x1, y1), (x2, y2) = pts[0], pts[-1]
        mid = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in pts[1:-1])
        arr = f'<Array as="points">{mid}</Array>' if mid else ""
        self.cells.append(
            f'<mxCell id="{self.nid("e")}" value={quoteattr(value)} style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry"><mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/>{arr}</mxGeometry></mxCell>')


def build(spec):
    parts = spec["participants"]
    msgs = spec["messages"]
    ids = {p["id"] for p in parts}
    for m in msgs:
        for k in ("from", "to"):
            if m[k] not in ids:
                sys.exit(f"ERROR: el mensaje '{m.get('label', '')}' usa el participante desconocido '{m[k]}'")

    # anchos: el nombre en una linea, y espacio para la etiqueta mas larga entre vecinos
    widths = [140 if p.get("kind") == "person" else max(MIN_W, int(len(p["name"]) * NAME_PX) + PAD_W)
              for p in parts]
    xs, x = [], 40
    for i, w in enumerate(widths):
        xs.append(x)
        x += w + GAP
    centers = {p["id"]: xs[i] + widths[i] / 2 for i, p in enumerate(parts)}
    order = {p["id"]: i for i, p in enumerate(parts)}

    # si una etiqueta no cabe entre dos vidas, separar mas los participantes
    for m in msgs:
        a, b_ = order[m["from"]], order[m["to"]]
        if a == b_:
            continue
        lo, hi = min(a, b_), max(a, b_)
        need = len(f"{len(msgs)}. {m['label']}") * MSG_PX + 30
        have = centers[parts[hi]["id"]] - centers[parts[lo]["id"]]
        if have < need:
            extra = need - have
            for p in parts[hi:]:
                centers[p["id"]] += extra
            for i in range(hi, len(xs)):
                xs[i] += extra

    head_bottom = TOP + HEAD_H
    n_self = sum(1 for m in msgs if m["from"] == m["to"])
    bottom = head_bottom + FIRST_MSG + STEP * len(msgs) + 26 * n_self + 30
    b = B()

    for i, p in enumerate(parts):
        w = widths[i]
        x = xs[i]
        if p.get("kind") == "person":
            b.v(f'<b>{t(p["name"])}</b><br><font style="font-size:9px" color="{TAGC}">[Person]</font>',
                f"shape=mxgraph.c4.person2;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor={LINE};"
                f"strokeWidth=1;fontFamily={FONT};fontSize=10;fontColor={TXT};align=center;"
                f"verticalAlign=bottom;spacingBottom=6;spacingLeft=4;spacingRight=4;",
                x, TOP - 50, w, HEAD_H + 50)
        else:
            tag = p.get("tag", "Container")
            b.v(f'<b style="font-size:13px">{t(p["name"])}</b><br>'
                f'<font style="font-size:9px" color="{TAGC}">[{t(tag)}]</font>',
                f"rounded=1;arcSize=12;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor={LINE};"
                f"strokeWidth=1;fontFamily={FONT};fontSize=10;fontColor={TXT};align=center;verticalAlign=middle;",
                x, TOP, w, HEAD_H)
        cx = centers[p["id"]]
        b.line("", f"endArrow=none;html=1;dashed=1;dashPattern=6 6;strokeColor={DASH};strokeWidth=1;",
               [(cx, head_bottom), (cx, bottom)])

    y = head_bottom + FIRST_MSG - STEP
    for k, m in enumerate(msgs, 1):
        y += STEP
        if k > 1 and msgs[k - 2]["from"] == msgs[k - 2]["to"]:
            y += 26
        x1, x2 = centers[m["from"]], centers[m["to"]]
        label = f"{k}. {t(m['label'])}"
        reply = m.get("reply", False)
        style = (f"html=1;rounded=0;strokeColor={EDGE};strokeWidth=1;fontFamily={FONT};fontSize=10;"
                 f"fontColor={TXT};labelBackgroundColor=#FFFFFF;"
                 + ("dashed=1;endArrow=open;endFill=0;" if reply else "endArrow=block;endFill=1;endSize=6;"))
        if m["from"] == m["to"]:
            b.line("", style, [(x1, y), (x1 + SELF_W, y), (x1 + SELF_W, y + 22), (x1, y + 22)])
            b.v(label, f"text;html=1;align=left;verticalAlign=middle;fontFamily={FONT};fontSize=10;"
                       f"fontColor={TXT};", x1 + SELF_W + 6, y, len(label) * MSG_PX + 10, 22)
        else:
            b.line("", style, [(x1, y), (x2, y)])
            w = len(label) * MSG_PX + 10
            b.v(label, f"text;html=1;align=center;verticalAlign=bottom;fontFamily={FONT};fontSize=10;"
                       f"fontColor={TXT};", min(x1, x2) + abs(x2 - x1) / 2 - w / 2, y - 20, w, 18)

    pw = int(max(xs[i] + widths[i] for i in range(len(parts))) + 60)
    ph = int(bottom + 40)
    return ('<mxfile host="app.diagrams.net"><diagram name="' + html.escape(spec.get("title", "Secuencia"), quote=True)
            + f'" id="seq-1"><mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{pw}" pageHeight="{ph}" '
            'math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + "".join(b.cells) + "</root></mxGraphModel></diagram></mxfile>")


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(build(spec))
    print("OK ->", sys.argv[2])
