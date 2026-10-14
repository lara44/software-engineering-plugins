#!/usr/bin/env python3
"""Genera un .drawio (mxGraph XML) de diagramas de despliegue AWS con el
estilo (icono set mxgraph.aws4, jerarquia real de contenedores).

Uso: python3 aws_drawio.py spec.json salida.drawio
"""
import html
import json
import sys
from xml.sax.saxutils import quoteattr

EDGE_COLOR = "#666666"

GROUP_STYLES = {
    "cloud": (
        "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
        "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
        "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
        "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
        "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;"
        "strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;"
        "spacingLeft=30;fontColor=#232F3E;dashed=0;"
    ),
    "region": (
        "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
        "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
        "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
        "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
        "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;"
        "strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;"
        "spacingLeft=30;dashed=0;"
    ),
    "vpc": (
        "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
        "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
        "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=12;"
        "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
        "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;"
        "strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;"
        "spacingLeft=30;fontColor=#AAB7B8;dashed=0;"
    ),
    "public_subnet": (
        "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
        "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
        "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=10;"
        "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
        "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
        "grStroke=0;strokeColor=#7AA116;fillColor=#F2F6E8;verticalAlign=top;"
        "align=left;spacingLeft=30;fontColor=#248814;dashed=0;"
    ),
    "private_subnet": (
        "points=[[0,0],[0.25,0],[0.5,0],[0.75,0],[1,0],[1,0.25],[1,0.5],[1,0.75],"
        "[1,1],[0.75,1],[0.5,1],[0.25,1],[0,1],[0,0.75],[0,0.5],[0,0.25]];"
        "outlineConnect=0;gradientColor=none;html=1;whiteSpace=wrap;fontSize=10;"
        "fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;"
        "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;"
        "grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;"
        "align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;"
    ),
}

AZ_STYLE = (
    "container=1;collapsible=0;recursiveResize=0;pointerEvents=0;"
    "fillColor=none;strokeColor=#147EBA;verticalAlign=top;fontStyle=0;"
    "fontColor=#147EBA;whiteSpace=wrap;html=1;"
)
BOX_STYLE = (
    "container=1;collapsible=0;recursiveResize=0;pointerEvents=0;"
    "fillColor=none;strokeColor={stroke};verticalAlign=top;fontStyle=0;"
    "fontColor=#5A6C86;whiteSpace=wrap;html=1;"
)

ICONS = {
    "ecs": "#ED7100",
    "ecs_task": "#ED7100",
    "fargate": "#ED7100",
    "ecr": "#ED7100",
    "ecs_service": "#ED7100",
    "eks_cloud": "#ED7100",
    "ec2": "#ED7100",
    "lambda_function": "#ED7100",
    "internet_gateway": "#8C4FFF",
    "application_load_balancer": "#8C4FFF",
    "network_load_balancer": "#8C4FFF",
    "classic_load_balancer": "#8C4FFF",
    "nat_gateway": "#8C4FFF",
    "vpc": "#8C4FFF",
    "route_53": "#8C4FFF",
    "api_gateway": "#8C4FFF",
    "cloudfront": "#8C4FFF",
    "rds_mysql_instance": "#C925D1",
    "rds_postgresql_instance": "#C925D1",
    "dynamodb": "#C925D1",
    "cognito": "#DD344C",
    "certificate_manager": "#DD344C",
    "identity_access_management_iam_roles_anywhere": "#DD344C",
    "s3": "#7AA116",
    "codecommit": "#C925D1",
    "codepipeline": "#C925D1",
    "codedeploy": "#C925D1",
    "sqs": "#E7157B",
    "sns": "#E7157B",
    "cloudwatch": "#E7157B",
}

LABEL_POS = {
    "bottom": (None, "bottom", "top", "center"),
    "right": ("right", "middle", "middle", "left"),
    "left": ("left", "middle", "middle", "right"),
    "center": ("center", "bottom", "top", "center"),
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
        geom_open = 'relative="1" as="geometry"'
        offset_tag = ""
        if label_offset:
            along, perp = label_offset
            geom_open = f'relative="1" as="geometry" x="{along}" y="0"'
            offset_tag = f'<mxPoint x="{perp}" y="0" as="offset"/>'
        self.cells.append(
            f'<mxCell id="{id_}" value={attr(value)} style="{style}" edge="1" parent="{parent}" '
            f'source="{src}" target="{dst}"><mxGeometry {geom_open}>{offset_tag}{pts}</mxGeometry></mxCell>'
        )


def group_el(b, e):
    style = GROUP_STYLES[e["kind"]]
    b.v(e["id"], e.get("name", ""), style, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))


def az_el(b, e):
    label = f'<font style="font-size: 10px;">{t(e.get("name", ""))}</font>' if e.get("name") else ""
    b.v(e["id"], label, AZ_STYLE, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))


def box_el(b, e):
    stroke = e.get("stroke", "#FF8000")
    style = BOX_STYLE.format(stroke=stroke)
    b.v(e["id"], "", style, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))


BADGE_ICONS = {"ecs", "fargate", "ecr", "codecommit", "codepipeline", "codedeploy"}
BADGE_POINTS = (
    "points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],"
    "[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],"
    "[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];"
)


def icon_el(b, e):
    icon = e["icon"]
    fill = e.get("fill") or ICONS.get(icon, "#232F3E")
    font_color = e.get("font_color", "#232F3E")
    font_size = e.get("font_size", 11)
    pos = e.get("label_pos", "bottom")
    lp, vlp, va, al = LABEL_POS[pos]
    if icon in BADGE_ICONS:
        style = (
            f"sketch=0;{BADGE_POINTS}outlineConnect=0;fontColor={font_color};"
            f"fillColor={fill};strokeColor=#ffffff;dashed=0;"
            f"verticalLabelPosition={vlp};verticalAlign={va};align={al};html=1;"
            f"fontSize={font_size};fontStyle=0;aspect=fixed;"
            f"shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{icon};"
        )
    else:
        style = (
            f"sketch=0;outlineConnect=0;fontColor={font_color};gradientColor=none;"
            f"fillColor={fill};strokeColor=none;dashed=0;verticalLabelPosition={vlp};"
            f"verticalAlign={va};align={al};html=1;fontSize={font_size};fontStyle=0;"
            f"aspect=fixed;pointerEvents=1;shape=mxgraph.aws4.{icon};"
        )
    if lp:
        style += f"labelPosition={lp};"
    b.v(e["id"], e.get("label", ""), style, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))


def actor_el(b, e):
    style = (
        "verticalLabelPosition=bottom;sketch=0;html=1;fillColor=#A153A0;"
        "strokeColor=#ffffff;verticalAlign=top;align=center;"
        "points=[[0,0.5,0],[0.125,0.25,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],"
        "[0.875,0.25,0],[1,0.5,0],[0.875,0.75,0],[0.75,1,0],[0.5,1,0],"
        "[0.125,0.75,0]];pointerEvents=1;shape=mxgraph.cisco_safe.compositeIcon;"
        "bgIcon=ellipse;resIcon=mxgraph.cisco_safe.design.users;fontSize=10;"
    )
    b.v(e["id"], e.get("label", ""), style, e["x"], e["y"], e.get("w", 45), e.get("h", 45), e.get("parent", "1"))


NOTE_STYLE = (
    "shape=note;whiteSpace=wrap;html=1;backgroundOutline=1;darkOpacity=0.05;"
    "fillColor=#FFF9B2;strokeColor=#D6B656;fontColor=#000000;align=left;"
    "verticalAlign=top;spacingLeft=6;spacingTop=6;fontSize=11;size=16;"
)


def note_el(b, e):
    b.v(e["id"], e.get("text", ""), NOTE_STYLE, e["x"], e["y"], e["w"], e["h"], e.get("parent", "1"))


def edge_el(b, i, d):
    label = d.get("label", "")
    style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={EDGE_COLOR};labelBackgroundColor=#ffffff;"
    for k, name in (("exit", "exit"), ("entry", "entry")):
        if d.get(k):
            style += f"{name}X={d[k][0]};{name}Y={d[k][1]};{name}Dx=0;{name}Dy=0;"
            if k == "entry":
                style += "entryPerimeter=0;"
    b.e(f"edge{i}", label, style, d["from"], d["to"], d.get("parent", "1"), d.get("points"), d.get("label_offset"))


KIND_DISPATCH = {
    "cloud": group_el, "region": group_el, "vpc": group_el,
    "public_subnet": group_el, "private_subnet": group_el,
    "az": az_el, "box": box_el, "icon": icon_el, "actor": actor_el, "note": note_el,
}


def build(spec):
    b = Builder()
    els = spec["elements"]
    order = ["cloud", "region", "vpc", "az", "public_subnet", "private_subnet", "box", "icon", "actor", "note"]
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
        '<mxfile host="app.diagrams.net"><diagram name="' + html.escape(spec.get("title", "AWS"), quote=True) +
        '" id="aws-1"><mxGraphModel dx="1400" dy="900" grid="0" gridSize="10" guides="1" tooltips="1" '
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
