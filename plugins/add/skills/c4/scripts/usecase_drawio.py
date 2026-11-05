#!/usr/bin/env python3
"""Genera un diagrama de casos de uso UML (.drawio) con el estilo de los diagramas C4.
Uso: python3 usecase_drawio.py spec.json salida.drawio [vista-previa.svg]

spec.json:
{
  "system": "Sistema de Pedidos",
  "actors": [
    {"id": "ven", "name": "Vendedor", "side": "left"},
    {"id": "sup", "name": "Supervisor", "side": "left"},
    {"id": "pag", "name": "Pasarela de pagos", "side": "right"}
  ],
  "usecases": [
    {"id": "UC-01", "name": "Registrar pedido"},
    {"id": "UC-02", "name": "Consultar pedidos"},
    {"id": "UC-03", "name": "Confirmar pedido"}
  ],
  "links": [["ven", "UC-01"], ["ven", "UC-03"], ["sup", "UC-02"], ["pag", "UC-03"]],
  "groups": [{"id": "ped", "name": "Pedidos"}, {"id": "con", "name": "Consultas"}]
}
Cada caso de uso puede llevar "group": "<id>" para colorearlo por area funcional,
como la figura 4.1 del caso FCAPS; la leyenda se dibuja abajo a la derecha.

- Solo van los actores que interactuan con el sistema (personas o sistemas externos).
- Los casos de uso retirados no se incluyen.
- El tercer argumento, opcional, escribe una vista previa SVG con la misma geometria,
  para revisar la distribucion cuando no hay draw.io para exportar el PNG.
"""
import html
import json
import sys
from xml.sax.saxutils import quoteattr

FONT = "Helvetica, Arial, sans-serif"
LINE = "#8C8C8C"
EDGE = "#333333"
TXT = "#000000"

UC_H = 42          # alto de cada caso de uso
UC_GAP = 16        # separacion vertical entre casos de uso
UC_PX = 6.6        # ancho aproximado por caracter, 11 px
UC_PAD = 46
SYS_PAD_X = 40
SYS_PAD_TOP = 46   # deja sitio al nombre del sistema
SYS_PAD_BOT = 26
ACT_W = 30
ACT_H = 56
ACT_LABEL_W = 130
COL_GAP = 120      # distancia entre la columna de actores y el limite del sistema
ACT_MIN_DY = 112   # separacion vertical minima entre actores de una misma columna
MARGIN = 30
# rellenos y bordes pastel, en orden de los grupos (como la figura 4.1 de CK16)
PALETTE = [("#FFF2CC", "#D6B656"), ("#D5E8D4", "#82B366"), ("#DAE8FC", "#6C8EBF"),
           ("#E1D5E7", "#9673A6"), ("#F8CECC", "#B85450"), ("#FFE6CC", "#D79B00")]
LEG_ROW = 18
LEG_W = 170


def colors(spec):
    groups = spec.get("groups", [])
    pal = {g["id"]: PALETTE[i % len(PALETTE)] for i, g in enumerate(groups)}
    for u in spec["usecases"]:
        if u.get("group") and u["group"] not in pal:
            sys.exit(f"ERROR: el caso de uso {u['id']} usa el grupo desconocido '{u['group']}'")
    return groups, pal


def t(s):
    return html.escape(str(s), quote=False)


def layout(spec):
    actors, ucs, links = spec["actors"], spec["usecases"], spec["links"]
    a_ids = {a["id"] for a in actors}
    u_ids = {u["id"] for u in ucs}
    for a, u in links:
        if a not in a_ids:
            sys.exit(f"ERROR: el enlace usa el actor desconocido '{a}'")
        if u not in u_ids:
            sys.exit(f"ERROR: el enlace usa el caso de uso desconocido '{u}'")

    uc_w = max(200, int(max(len(f'{u["id"]}: {u["name"]}') for u in ucs) * UC_PX) + UC_PAD)
    left = [a for a in actors if a.get("side", "left") == "left"]
    right = [a for a in actors if a.get("side") == "right"]

    sys_x = MARGIN + (ACT_LABEL_W + COL_GAP if left else 0)
    sys_y = MARGIN
    uc_x = sys_x + SYS_PAD_X
    geo_uc, y = {}, sys_y + SYS_PAD_TOP
    for u in ucs:
        geo_uc[u["id"]] = (uc_x, y, uc_w, UC_H)
        y += UC_H + UC_GAP
    sys_w = uc_w + 2 * SYS_PAD_X
    sys_h = y - UC_GAP - sys_y + SYS_PAD_BOT

    def place(col, x_label):
        # cada actor a la altura media de sus casos de uso, sin solaparse
        want = []
        for a in col:
            ys = [geo_uc[u][1] + UC_H / 2 for aa, u in links if aa == a["id"]]
            want.append(sum(ys) / len(ys) if ys else sys_y + sys_h / 2)
        order = sorted(range(len(col)), key=lambda i: want[i])
        out, last = {}, None
        for i in order:
            cy = want[i] if last is None else max(want[i], last + ACT_MIN_DY)
            out[col[i]["id"]] = (x_label + (ACT_LABEL_W - ACT_W) / 2, cy - ACT_H / 2 - 8, ACT_W, ACT_H)
            last = cy
        return out

    geo_act = {}
    geo_act.update(place(left, MARGIN))
    geo_act.update(place(right, sys_x + sys_w + COL_GAP))
    bottom = max([sys_y + sys_h] + [g[1] + g[3] + 30 for g in geo_act.values()])
    width = sys_x + sys_w + (COL_GAP + ACT_LABEL_W if right else 0) + MARGIN
    legend = None
    if spec.get("groups"):
        lh = LEG_ROW * (len(spec["groups"]) + 1) + 8
        lw = max(LEG_W, int(max(len(g["name"]) for g in spec["groups"]) * 5.8) + 40)
        legend = (width - MARGIN - lw, bottom + 10, lw, lh)
        bottom = bottom + 10 + lh
    return geo_uc, geo_act, (sys_x, sys_y, sys_w, sys_h), int(width), int(bottom + MARGIN), legend


def build(spec):
    geo_uc, geo_act, (sx, sy, sw, sh), pw, ph, legend = layout(spec)
    groups, pal = colors(spec)
    cells, ids = [], {}
    cells.append(
        f'<mxCell id="sys" value={quoteattr("<b>" + t(spec["system"]) + "</b>")} '
        f'style="rounded=0;html=1;whiteSpace=wrap;fillColor=#FFFFFF;strokeColor={LINE};strokeWidth=1;'
        f'fontFamily={FONT};fontSize=12;fontColor={TXT};align=left;verticalAlign=top;spacingLeft=10;spacingTop=6;" '
        f'vertex="1" parent="1"><mxGeometry x="{sx}" y="{sy}" width="{sw}" height="{sh}" as="geometry"/></mxCell>')
    for u in spec["usecases"]:
        x, y, w, h = geo_uc[u["id"]]
        cid = "uc_" + u["id"].replace("-", "_")
        ids[u["id"]] = cid
        fill, stroke = pal.get(u.get("group"), ("#FFFFFF", LINE))
        cells.append(
            f'<mxCell id="{cid}" value={quoteattr(t(u["id"]) + ": " + t(u["name"]))} '
            f'style="ellipse;html=1;whiteSpace=wrap;fillColor={fill};strokeColor={stroke};strokeWidth=1;'
            f'fontFamily={FONT};fontSize=11;fontColor={TXT};" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    for a in spec["actors"]:
        x, y, w, h = geo_act[a["id"]]
        cid = "act_" + a["id"]
        ids[a["id"]] = cid
        cells.append(
            f'<mxCell id="{cid}" value={quoteattr(t(a["name"]))} '
            f'style="shape=umlActor;html=1;whiteSpace=wrap;verticalLabelPosition=bottom;verticalAlign=top;'
            f'fillColor=#FFFFFF;strokeColor={EDGE};strokeWidth=1;fontFamily={FONT};fontSize=11;fontColor={TXT};" '
            f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
    side = {a["id"]: a.get("side", "left") for a in spec["actors"]}
    for n, (a, u) in enumerate(spec["links"], 1):
        # la linea sale del costado del actor y llega al extremo de la elipse que lo mira:
        # asi nunca roza las elipses vecinas
        ends = ("exitX=1;exitY=0.5;entryX=0;entryY=0.5;" if side[a] == "left"
                else "exitX=0;exitY=0.5;entryX=1;entryY=0.5;")
        cells.append(
            f'<mxCell id="l{n}" style="endArrow=none;html=1;rounded=0;strokeColor={EDGE};strokeWidth=1;'
            f'{ends}exitPerimeter=0;entryPerimeter=0;" '
            f'edge="1" parent="1" source="{ids[a]}" target="{ids[u]}">'
            f'<mxGeometry relative="1" as="geometry"/></mxCell>')
    if legend:
        lx, ly, lw, lh = legend
        cells.append(
            f'<mxCell id="leg" value="" style="rounded=0;html=1;fillColor=#FFFFFF;strokeColor={LINE};strokeWidth=1;" '
            f'vertex="1" parent="1"><mxGeometry x="{lx}" y="{ly}" width="{lw}" height="{lh}" as="geometry"/></mxCell>')
        cells.append(
            f'<mxCell id="legt" value="&lt;b&gt;Áreas&lt;/b&gt;" style="text;html=1;fontFamily={FONT};fontSize=10;'
            f'fontColor={TXT};align=left;verticalAlign=middle;spacingLeft=6;" vertex="1" parent="1">'
            f'<mxGeometry x="{lx}" y="{ly + 2}" width="{lw}" height="{LEG_ROW}" as="geometry"/></mxCell>')
        for i, g in enumerate(groups, 1):
            fill, stroke = pal[g["id"]]
            cells.append(
                f'<mxCell id="leg{i}" value={quoteattr(t(g["name"]))} style="rounded=0;html=1;fillColor={fill};'
                f'strokeColor={stroke};strokeWidth=1;fontFamily={FONT};fontSize=10;fontColor={TXT};align=left;'
                f'spacingLeft=6;" vertex="1" parent="1"><mxGeometry x="{lx + 6}" y="{ly + 2 + LEG_ROW * i}" '
                f'width="{lw - 12}" height="{LEG_ROW - 2}" as="geometry"/></mxCell>')
    name = html.escape("Casos de uso", quote=True)
    return (f'<mxfile host="app.diagrams.net"><diagram name="{name}" id="uc-1"><mxGraphModel dx="1400" dy="900" '
            f'grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
            f'pageWidth="{pw}" pageHeight="{ph}" math="0" shadow="0"><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
            + "".join(cells) + "</root></mxGraphModel></diagram></mxfile>")


def preview(spec):
    geo_uc, geo_act, (sx, sy, sw, sh), pw, ph, legend = layout(spec)
    groups, pal = colors(spec)
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{pw}" height="{ph}" font-family="Helvetica, Arial, sans-serif">',
         f'<rect width="{pw}" height="{ph}" fill="#fff"/>',
         f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" fill="#fff" stroke="{LINE}"/>',
         f'<text x="{sx + 10}" y="{sy + 20}" font-size="12" font-weight="bold">{t(spec["system"])}</text>']
    for a, u in spec["links"]:
        ax, ay, aw, ah = geo_act[a]
        ux, uy, uw, uh = geo_uc[u]
        left = ax < ux
        x1 = ax + aw if left else ax
        x2 = ux if left else ux + uw
        s.append(f'<line x1="{x1}" y1="{ay + ah / 2}" x2="{x2}" y2="{uy + uh / 2}" stroke="{EDGE}"/>')
    for u in spec["usecases"]:
        x, y, w, h = geo_uc[u["id"]]
        fill, stroke = pal.get(u.get("group"), ("#FFFFFF", LINE))
        s.append(f'<ellipse cx="{x + w / 2}" cy="{y + h / 2}" rx="{w / 2}" ry="{h / 2}" fill="{fill}" stroke="{stroke}"/>')
        s.append(f'<text x="{x + w / 2}" y="{y + h / 2 + 4}" font-size="11" text-anchor="middle">'
                 f'{t(u["id"])}: {t(u["name"])}</text>')
    for a in spec["actors"]:
        x, y, w, h = geo_act[a["id"]]
        cx = x + w / 2
        s.append(f'<circle cx="{cx}" cy="{y + 8}" r="8" fill="#fff" stroke="{EDGE}"/>'
                 f'<line x1="{cx}" y1="{y + 16}" x2="{cx}" y2="{y + 38}" stroke="{EDGE}"/>'
                 f'<line x1="{x}" y1="{y + 24}" x2="{x + w}" y2="{y + 24}" stroke="{EDGE}"/>'
                 f'<line x1="{cx}" y1="{y + 38}" x2="{x}" y2="{y + h}" stroke="{EDGE}"/>'
                 f'<line x1="{cx}" y1="{y + 38}" x2="{x + w}" y2="{y + h}" stroke="{EDGE}"/>'
                 f'<text x="{cx}" y="{y + h + 16}" font-size="11" text-anchor="middle">{t(a["name"])}</text>')
    if legend:
        lx, ly, lw, lh = legend
        s.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" fill="#fff" stroke="{LINE}"/>'
                 f'<text x="{lx + 6}" y="{ly + 15}" font-size="10" font-weight="bold">Áreas</text>')
        for i, g in enumerate(groups, 1):
            fill, stroke = pal[g["id"]]
            yy = ly + 2 + LEG_ROW * i
            s.append(f'<rect x="{lx + 6}" y="{yy}" width="{lw - 12}" height="{LEG_ROW - 2}" fill="{fill}" stroke="{stroke}"/>'
                     f'<text x="{lx + 12}" y="{yy + 12}" font-size="10">{t(g["name"])}</text>')
    s.append("</svg>")
    return "".join(s)


if __name__ == "__main__":
    with open(sys.argv[1], encoding="utf-8") as f:
        spec = json.load(f)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        f.write(build(spec))
    if len(sys.argv) > 3:
        with open(sys.argv[3], "w", encoding="utf-8") as f:
            f.write(preview(spec))
    print("OK ->", sys.argv[2])
