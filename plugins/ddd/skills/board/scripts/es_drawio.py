#!/usr/bin/env python3
"""Tablero de Event Storming en un solo .drawio, con una página por paso.

Uso:
  python3 es_drawio.py build  modelo.json --paso N [--base aprobado.drawio] --out borrador.drawio
  python3 es_drawio.py export tablero.drawio --paso N --out step-N.png
  python3 es_drawio.py data   modelo.json --out data.md
  python3 es_drawio.py layout tablero.drawio modelo.json

build   Genera (o regenera) la página del paso N a partir del modelo. Cada página
        lleva el panel de terminología y proceso, y el tablero de su paso. Si se da
        --base, conserva tal cual las páginas de los pasos anteriores (incluidos los
        ajustes hechos a mano en draw.io) y quita las de pasos posteriores. Un
        tablero del formato anterior (una capa por paso) se convierte a páginas.
export  Exporta a PNG solo el tablero del paso N, con draw.io Desktop.
layout  Guarda en el modelo ('context_layout') la ubicación de los contextos acomodados a mano en
        la página del paso 8, para respetarla al volver a dibujar.
data    Escribe la tabla de datos por evento (paso 6) en Markdown.

Solo usa la biblioteca estándar de Python.
"""
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import quoteattr

# ---------------------------------------------------------------- estilo
FONT = "Inter, Helvetica, Arial, sans-serif"
COL = {"evento": "#FFAA5B", "comando": "#8ED3F5", "usuario": "#FFE15A", "politica": "#BDA6F2",
       "externo": "#F592C8", "datos": "#7ED69B", "agregado": "#FFF4A8", "texto": "#1E1E1E",
       "hot": "#D92D20", "linea": "#8A8A8A", "vista": "#B59A00", "panel": "#DCE6F8",
       "fondo": "#E9E9E9", "barra": "#000000"}
# Geometría del tablero de referencia (px)
P = 170                     # paso entre columnas
EW, EH = 84, 62             # evento
CH, PH, GH, DH = 52, 50, 36, 46   # comando, política, agregado, datos (mínimo)
AW, AH = 62, 30             # usuario
G = 5                       # entre tarjetas apiladas
LEFT_W = 400                # panel de terminología y proceso
BOARD_X = LEFT_W + 60       # inicio del tablero

PASOS = {
    1: ("Descubrimiento de eventos", "Se escriben todos los hechos del negocio, en pasado y sin orden."),
    2: ("Línea de tiempo", "Los eventos se ordenan de izquierda a derecha, en una línea por recorrido."),
    3: ("Localización de comandos", "Sobre cada evento, la acción que lo origina, en presente."),
    4: ("Usuarios y sistemas externos", "Quién ejecuta cada comando y con qué sistemas se intercambia información."),
    5: ("Políticas", "Las reglas que validan un comando o reaccionan a un evento."),
    6: ("Datos", "La información que necesita cada evento para registrarse."),
    7: ("Agregados", "La unidad con responsabilidad única que protege las invariantes."),
    8: ("Contextos de negocio", "Las fronteras que agrupan los agregados; y cuál es el dominio central."),
}
TERMINOS = [
    ("evento", "Evento", "Un hecho del negocio que ya ocurrió, escrito en pasado."),
    ("comando", "Comando", "Una acción o decisión que alguien solicita, en presente."),
    ("usuario", "Usuario", "El rol que ejecuta el comando."),
    ("externo", "Sistema externo", "Un sistema fuera del dominio que envía o recibe información."),
    ("politica", "Política", "Una regla que valida un comando o reacciona a un evento."),
    ("datos", "Datos", "La información que requiere el evento para registrarse."),
    ("agregado", "Agregado", "La unidad con responsabilidad única que agrupa comandos y eventos."),
]


def fail(msg):
    sys.exit("ERROR: " + msg)


# ---------------------------------------------------------------- modelo
def load(path, paso=8):
    with open(path, encoding="utf-8") as f:
        m = json.load(f)
    ev = m.get("events") or fail("el modelo no tiene 'events'")
    ids = {}
    for e in ev:
        for k in (("id", "name") if paso == 1 else ("id", "name", "lane", "col")):
            if k not in e:
                fail(f"evento sin '{k}': {e}")
        if e["id"] in ids:
            fail(f"id repetido: {e['id']}")
        ids[e["id"]] = e
    if paso == 1:            # en el paso 1 los eventos todavía no tienen lugar en el tablero
        return m, ids
    for e in ev:
        b = e.get("below")
        if b and (b not in ids or ids[b]["col"] != e["col"] or ids[b]["lane"] != e["lane"]):
            fail(f"'below' de '{e['id']}' debe apuntar a un evento de la misma línea y columna")

    def slot(e, seen=()):
        if not e.get("below"):
            return 0
        if e["id"] in seen:
            fail("ciclo en 'below'")
        return slot(ids[e["below"]], seen + (e["id"],)) + 1
    taken = {}
    for e in ev:
        e["slot"] = slot(e)
        k = (e["lane"], e["slot"], e["col"])
        if k in taken:
            fail(f"'{e['id']}' y '{taken[k]}' ocupan el mismo lugar")
        taken[k] = e["id"]
    ctx = {c["id"] for c in m.get("contexts", [])}
    for e in ev:
        if e.get("context") and e["context"] not in ctx:
            fail(f"contexto no definido: {e['context']}")
    for fl in m.get("flows", []):
        if fl.get("from") not in ids or fl.get("to") not in ids:
            fail(f"flujo con evento inexistente: {fl}")
    return m, ids


def data_text(e):
    d = e.get("data")
    if not d:
        return None
    return d if isinstance(d, str) else ", ".join(d)


def data_h(text):
    # alto de la tarjeta de datos según el largo del texto (10,5 px, ~14 caracteres por línea)
    lines = max(1, -(-len(text) // 14))
    return max(DH, int(lines * 13 + 12))



def bezier(p0, c1, c2, p3, n=10):
    """Puntos interiores de una curva de Bézier cúbica (sin los extremos)."""
    out = []
    for k in range(1, n):
        t = k / n
        u = 1 - t
        out.append((u ** 3 * p0[0] + 3 * u * u * t * c1[0] + 3 * u * t * t * c2[0] + t ** 3 * p3[0],
                    u ** 3 * p0[1] + 3 * u * u * t * c1[1] + 3 * u * t * t * c2[1] + t ** 3 * p3[1]))
    return out

# ---------------------------------------------------------------- disposición de un paso
class Step:
    """Tarjetas, flechas y contextos de un paso, en coordenadas locales (0,0)."""

    def __init__(self, m, ids, S):
        self.m, self.ids, self.S = m, ids, S
        self.notes, self.edges, self.regions, self.warn = [], [], [], []
        self.w = self.h = 0
        (self.scatter if S == 1 else self.board)()

    def note(self, kind, x, y, w, h, text, ev=None, hot=False, view=False, key=None):
        n = dict(kind=kind, x=x, y=y, w=w, h=h, text=text, hot=hot, view=view, ev=ev, key=key)
        self.notes.append(n)
        return n

    def stack(self, e):
        S, out = self.S, []
        if e.get("aggregate") and (S == 7 or (S >= 8 and e["id"] in self.first_agg)):
            out.append(("agregado", GH, e["aggregate"], bool(e.get("aggregate_view"))))
        if S >= 5 and e.get("policy"):
            out.append(("politica", PH, e["policy"], False))
        if S == 6 and data_text(e):        # los datos solo se ven en su paso; luego quedan en data.md
            t = data_text(e)
            out.append(("datos", data_h(t), t, False))
        if S >= 3 and e.get("command"):
            out.append(("comando", CH, e["command"], False))
        return out

    def above(self, e):
        return sum(h + G for _, h, _, _ in self.stack(e))

    def scatter(self):
        rnd = random.Random(7)
        ev = list(self.m["events"])
        rnd.shuffle(ev)
        ew, eh, cols, cw, rh = 96, 70, 6, 150, 100
        for i, e in enumerate(ev):
            r, c = divmod(i, cols)
            x = c * cw + (cw - ew) / 2 + rnd.uniform(-18, 18) + (24 if r % 2 else 0)
            y = r * rh + rnd.uniform(-10, 10)
            self.note("evento", round(x), round(y) + 10, ew, eh, e["name"], ev=e["id"],
                      hot=bool(e.get("hotspot")), key=e["id"])
        self.w = cols * cw + 40
        self.h = (-(-len(ev) // cols)) * rh + 10

    def context_groups(self):
        """Grupos de eventos que comparten recuadro: mismo contexto, misma línea y columnas seguidas."""
        EV, out = self.m["events"], []
        for c in self.m.get("contexts", []):
            groups = []
            for e in [e for e in EV if e.get("context") == c["id"]]:
                hit = [g for g in groups if any(o["lane"] == e["lane"] and abs(o["col"] - e["col"]) <= 1 for o in g)]
                groups = [g for g in groups if g not in hit] + [[e] + [o for g in hit for o in g]]
            out += [(c, g) for g in groups]
        return out

    def board(self):
        S, EV = self.S, self.m["events"]
        # paso 8: en cada recuadro de contexto, la tarjeta de un agregado va solo en el primer evento
        # que le pertenece (en el orden de lectura); si el contexto se repite en otro recuadro, ese
        # recuadro muestra también sus agregados, para que cada uno se lea solo
        self.first_agg = {e["id"] for e in EV if not e.get("context")}
        if S >= 8:
            for _, g in self.context_groups():
                seen = set()
                for o in sorted(g, key=lambda o: (o["slot"], o["col"])):
                    if o.get("aggregate") and o["aggregate"] not in seen:
                        seen.add(o["aggregate"])
                        self.first_agg.add(o["id"])
        X0 = AW + 10
        ncols = max(e["col"] for e in EV) + 1
        pc = P + (20 if S >= 8 else 0)            # en el paso 8 el recuadro incluye al usuario: más aire entre columnas
        X = [X0 + i * pc for i in range(ncols)]
        evY, bottom = self.pack(EV), 0
        for e in EV:
            e["_x"], e["_y"] = X[e["col"]], evY[(e["lane"], e["slot"])]
            bottom = max(bottom, e["_y"] + EH + (14 if S >= 4 and e.get("external") else 0))
            e["_m"] = e["_y"] + EH / 2
            e["_boxes"] = [(e["_x"], e["_y"], EW, EH)]
            self.note("evento", e["_x"], e["_y"], EW, EH, e["name"], ev=e["id"],
                      hot=bool(e.get("hotspot")), key=e["id"])
            if S >= 4 and e.get("external"):
                self.note("externo", e["_x"] + 44, e["_y"] + EH - 12, 64, 28, e["external"], ev=e["id"])
                e["_boxes"].append((e["_x"] + 44, e["_y"] + EH - 12, 64, 28))
            y = e["_y"]
            for kind, h, text, view in reversed(self.stack(e)):
                y -= h + G
                self.note(kind, e["_x"], y, EW, h, text, ev=e["id"], view=view)
                e["_boxes"].append((e["_x"], y, EW, h))
                if kind == "comando" and S >= 4 and e.get("actor"):
                    self.note("usuario", e["_x"] - AW - 4, y + h - AH, AW, AH, e["actor"], ev=e["id"])
                    e["_boxes"].append((e["_x"] - AW - 4, y + h - AH, AW, AH))   # el contexto encierra también al usuario
        self.w = X[-1] + EW + 60
        self.h = bottom + 10
        self.arrows()
        if S >= 8:
            self.contexts()
        if self.h > 1.6 * self.w:
            self.warn.append("el tablero es mucho más alto que ancho: revisa si un recorrido quedó partido en varias "
                             "líneas, si hay flechas de dependencia (no de secuencia) o caminos alternos en líneas propias")

    def pack(self, EV):
        """Altura de cada fila (línea, nivel), aprovechando el espacio libre de cada columna.

        Una fila no ocupa todo el ancho del tablero: solo sus columnas (y, si es la línea principal,
        las columnas entre su primer y su último evento). Cada fila sube hasta donde se lo permiten
        esas columnas y el camino de las flechas que le llegan: la que baja por la columna del evento
        de origen y entra por la izquierda. Las líneas principales conservan su orden de arriba abajo.
        """
        S, ids = self.S, self.ids
        top = 30 if S >= 8 else 0
        gap_lane = 34 + (24 if S >= 8 else 0)
        colbot = {}                                # columna -> (borde inferior ocupado, línea)
        evY, placed, prev_main = {}, set(), None
        rows = sorted({(e["lane"], e["slot"]) for e in EV})
        flows = self.m.get("flows", [])
        # en el paso 8, cada evento ocupa el ancho de todo su contexto (el recuadro llega hasta su
        # último nivel): así ninguna fila se mete dentro del recuadro de otro contexto
        span = {e["id"]: {e["col"]} for e in EV}
        if S >= 8:
            for e in EV:
                if e.get("context"):
                    grp, todo = {e["id"]}, [e]
                    while todo:
                        o = todo.pop()
                        for q in EV:
                            if (q["id"] not in grp and q.get("context") == e["context"] and q["lane"] == o["lane"]
                                    and abs(q["col"] - o["col"]) <= 1):
                                grp.add(q["id"]); todo.append(q)
                    span[e["id"]] = {ids[g]["col"] for g in grp}
        for ln, s in rows:
            row = [e for e in EV if e["lane"] == ln and e["slot"] == s]
            cols = {e["col"] for e in row}
            if s == 0:
                cols |= set(range(min(cols), max(cols) + 1))
            paths = set()                          # columnas que cruza una flecha que llega a la fila
            for fl in flows:
                a, b = ids[fl["from"]], ids[fl["to"]]
                if a["id"] in placed and b in row and b["col"] > a["col"]:
                    paths |= set(range(a["col"], b["col"]))
            y = top + max(self.above(e) for e in row)
            for c in cols | paths:
                if c in colbot:
                    cb, cl = colbot[c]
                    gap = 26 if cl == ln else gap_lane
                    need = max(self.above(e) for e in row if e["col"] == c) if c in {e["col"] for e in row} else 0
                    y = max(y, cb + gap + need)
            if s == 0 and prev_main is not None:
                y = max(y, prev_main)   # una línea principal no sube por encima de la anterior (puede quedar a su altura, más a la derecha)
            evY[(ln, s)] = y
            if s == 0:
                prev_main = y
            ext = 14 if S >= 4 and any(e.get("external") for e in row) else 0
            for c in cols | paths | {c for e in row for c in span[e["id"]]}:
                colbot[c] = (max(colbot.get(c, (0,))[0], y + EH + ext), ln)
            placed |= {e["id"] for e in row}
        return evY

    def edge(self, a, b, exit_, entry, pts, dashed):
        self.edges.append(dict(src=a["id"], tgt=b["id"], exit=exit_, entry=entry, pts=pts, dashed=dashed))

    def free_below(self, a, b):
        """True si la línea que baja por el centro de `a` hasta la altura de `b` no toca ninguna tarjeta."""
        x = a["_x"] + EW / 2
        y1, y2 = a["_y"] + EH, b["_y"] + EH / 2
        for n in self.notes:
            if n["ev"] in (a["id"], b["id"]):
                continue
            if n["x"] - 4 < x < n["x"] + n["w"] + 4 and n["y"] < y2 and n["y"] + n["h"] > y1:
                return False
        return True

    def arrows(self):
        """Flechas con las curvas del tablero de referencia.

        Primero se decide la forma de cada flecha y por qué lado sale y entra; luego, si varias
        flechas comparten el lado de una tarjeta, se reparten a lo alto del lado para que no se
        monten una sobre otra. Las curvas (Bézier) se pasan a draw.io como puntos sobre la curva,
        que draw.io suaviza con curved=1.
        """
        EV, ids = self.m["events"], self.ids
        specs = []                                  # (a, b, forma, lado_salida, lado_entrada, punteada)
        for ln in sorted({e["lane"] for e in EV}):
            main = sorted([e for e in EV if e["lane"] == ln and e["slot"] == 0], key=lambda e: e["col"])
            for a, b in zip(main, main[1:]):
                specs.append((a, b, "recta", "R", "L", False))
        self.loops = set()
        for fl in self.m.get("flows", []):
            a, b, dash = ids[fl["from"]], ids[fl["to"]], bool(fl.get("dashed"))
            down_free = b["_y"] > a["_y"] and self.free_below(a, b)
            if b["lane"] != a["lane"] and b["col"] > a["col"] and down_free:
                specs.append((a, b, "tronco", "B", "L", dash))
            elif b["col"] == a["col"]:
                specs.append((a, b, "bucle", "R", "R", dash))
                self.loops.add(a["id"])
            elif b["col"] == a["col"] + 1 and down_free:
                specs.append((a, b, "baja", "B", "L", dash))         # sale por debajo y entra con curva
            elif b["col"] > a["col"]:
                specs.append((a, b, "s" if b["col"] == a["col"] + 1 and b["lane"] == a["lane"] else "larga",
                              "R", "L", dash))
            else:
                self.warn.append(f"la flecha {a['id']} -> {b['id']} va hacia atrás; revisa las columnas")
                specs.append((a, b, "atras", "L", "R", dash))
        # Reparto de puntos de salida y de entrada cuando varias flechas comparten un lado de una
        # tarjeta, ordenadas por de dónde vienen para que no se crucen:
        #  - al entrar: arriba las que bajan desde arriba, con la más cercana más arriba; en medio
        #    las que llegan a la misma altura; abajo las que suben, con la más cercana más abajo;
        #  - al salir: arriba las que van hacia arriba; abajo las que bajan, con la que va más lejos
        #    más arriba. El tronco comparte su salida a propósito (es una sola línea que se ramifica).
        def approach_x(a, kind):
            return a["_x"] + EW / 2 if kind in ("tronco", "baja") else a["_x"] + EW + (16 if kind == "s" else 0)

        frac, groups = {}, {}
        for k, (a, b, kind, so, si, _) in enumerate(specs):
            if kind not in ("tronco", "baja", "bucle"):
                dy = b["_y"] - a["_y"]
                key = ((0, -b["_x"]) if dy < 0 else (1, 0) if dy == 0 else (2, -b["_x"]))
                groups.setdefault((a["id"], so, "out"), []).append((k, key))
            dy = b["_y"] - a["_y"]
            ax = approach_x(a, kind)
            key = ((0, -ax) if dy > 0 else (1, 0) if dy == 0 else (2, ax))
            groups.setdefault((b["id"], si, "in"), []).append((k, key))
        for (nid, side, d), lst in groups.items():
            lst.sort(key=lambda t: t[1])
            # la flecha que va a la misma altura conserva el centro del lado (sale y entra derecha);
            # las demás se reparten por encima y por debajo de ella
            level = [k for k, key in lst if key[0] == 1]
            above = [k for k, key in lst if key[0] == 0]
            below = [k for k, key in lst if key[0] == 2]
            if level:
                frac[(level[0], d)] = 0.5
                rest = level[1:]
                above, below = above + rest[:len(rest) // 2], rest[len(rest) // 2:] + below
                for pos, k in enumerate(above):
                    frac[(k, d)] = 0.2 + 0.22 * pos / max(1, len(above) - 1) if len(above) > 1 else 0.3
                for pos, k in enumerate(below):
                    frac[(k, d)] = 0.58 + 0.22 * pos / max(1, len(below) - 1) if len(below) > 1 else 0.7
            else:
                n = len(lst)
                for pos, (k, _) in enumerate(lst):
                    frac[(k, d)] = 0.5 if n == 1 else 0.25 + 0.5 * pos / (n - 1)
        for k, (a, b, kind, so, si, dash) in enumerate(specs):
            fo, fi = frac.get((k, "out"), 0.5), frac.get((k, "in"), 0.5)
            xa, xb = a["_x"], b["_x"]
            ma, mb = a["_y"] + EH * fo, b["_y"] + EH * fi
            r = xa + EW
            side = {"L": 0, "R": 1}
            exit_ = (.5, 1) if so == "B" else (side[so], fo)
            entry = (side[si], fi)
            if kind == "recta":
                pts = [] if abs(ma - mb) < 1 else bezier((r, ma), (r + 40, ma), (xb - 40, mb), (xb, mb))
            elif kind == "tronco":                       # baja recto y entra con una curva amplia
                tx, top = xa + EW / 2, a["_y"] + EH
                L = max(24, min(90, xb - tx - 24, mb - top - 12))
                pts = ([(tx, mb - L)] + bezier((tx, mb - L), (tx, mb - L * .45), (tx + L * .45, mb), (tx + L, mb))
                       + [(tx + L, mb)])
            elif kind == "baja":                         # sale por debajo y entra a la siguiente columna
                tx, top = xa + EW / 2, a["_y"] + EH
                L = max(24, min(70, xb - tx - 20, mb - top - 10))
                pts = ([(tx, mb - L)] + bezier((tx, mb - L), (tx, mb - L * .45), (tx + L * .45, mb), (tx + L, mb))
                       + [(tx + L, mb)])
            elif kind == "bucle":                        # C por la derecha; varias desde un evento comparten el tronco
                R = 14
                if mb - ma > 2 * R + 4:
                    pts = (bezier((r, ma), (r + R * .55, ma), (r + R, ma + R * .45), (r + R, ma + R), 6)
                           + [(r + R, ma + R), (r + R, mb - R)]
                           + bezier((r + R, mb - R), (r + R, mb - R * .45), (r + R * .55, mb), (r, mb), 6))
                else:
                    pts = bezier((r, ma), (r + 22, ma), (r + 22, mb), (r, mb), 14)
            elif kind == "s":                            # S suave hacia la columna siguiente
                gx = r + 16
                pts = bezier((r, ma), (gx + 4, ma), (gx, ma + (mb - ma) * .25), (gx, (ma + mb) / 2), 8)
                pts += [(gx, (ma + mb) / 2)]
                pts += bezier((gx, (ma + mb) / 2), (gx, ma + (mb - ma) * .75), (gx + 4, mb), (xb, mb), 10)
            elif kind == "larga":
                pts = bezier((r, ma), (r + 70, ma), (xb - 70, mb), (xb, mb), 16)
            else:
                pts = bezier((xa, ma), (xa - 70, ma), (xb + EW + 70, mb), (xb + EW, mb), 16)
            self.edge(a, b, exit_, entry, pts, dash)
            self.edges[-1]["poly"] = self._poly(a, b, exit_, entry, pts)
        self._crossings()

    @staticmethod
    def _anchor(e, c):
        return (e["_x"] + EW * c[0], e["_y"] + EH * c[1])

    def _poly(self, a, b, exit_, entry, pts):
        return [self._anchor(a, exit_)] + list(pts) + [self._anchor(b, entry)]

    def _crossings(self):
        def cross(p1, p2, p3, p4):
            def o(a, b, c):
                return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
            d1, d2, d3, d4 = o(p3, p4, p1), o(p3, p4, p2), o(p1, p2, p3), o(p1, p2, p4)
            return (d1 * d2 < 0) and (d3 * d4 < 0)
        E = self.edges
        for i in range(len(E)):
            for j in range(i + 1, len(E)):
                a, b = E[i], E[j]
                if {a["src"], a["tgt"]} & {b["src"], b["tgt"]} and a["src"] == b["src"] and a["exit"] == b["exit"]:
                    continue                                   # ramas del mismo tronco
                pa, pb = a["poly"], b["poly"]
                if any(cross(pa[x], pa[x + 1], pb[y], pb[y + 1])
                       for x in range(len(pa) - 1) for y in range(len(pb) - 1)):
                    self.warn.append(f"las flechas {a['src']} -> {a['tgt']} y {b['src']} -> {b['tgt']} se cruzan: "
                                     "acerca los eventos o cambia su columna o su línea")

    def contexts(self):
        drawn = []
        bycontext = {}
        for c, g in self.context_groups():
            bycontext.setdefault(c["id"], (c, []))[1].append(g)
        for c, groups in bycontext.values():
            groups.sort(key=lambda g: (min(o["_y"] for o in g), min(o["col"] for o in g)))
            for i in range(len(groups)):
                for j in range(i + 1, len(groups)):
                    a_ids, b_ids = {o["id"] for o in groups[i]}, {o["id"] for o in groups[j]}
                    for fl in self.m.get("flows", []):
                        if {fl["from"], fl["to"]} & a_ids and {fl["from"], fl["to"]} & b_ids:
                            x, y = self.ids[fl["from"]], self.ids[fl["to"]]
                            if abs(x["col"] - y["col"]) <= 1:
                                self.warn.append(
                                    f"el contexto '{c['id']}' quedó partido en recuadros pegados ({x['id']} -> {y['id']}): "
                                    f"si {y['id']} es un camino alterno de {x['id']}, va debajo de él con 'below'; "
                                    "si sigue en el recorrido, va en la misma línea")
            for gi, g in enumerate(groups):
                bb = [r for o in g for r in o["_boxes"]]
                x1, y1 = min(r[0] for r in bb) - 8, min(r[1] for r in bb) - 26
                x2, y2 = max(r[0] + r[2] for r in bb) + 8, max(r[1] + r[3] for r in bb) + 10
                if any(o["id"] in self.loops for o in g):
                    x2 = max(x2, max(o["_x"] for o in g if o["id"] in self.loops) + EW + 22)
                lab = c["name"]                      # cada recuadro dice a qué contexto pertenece
                if len(lab) * 7.2 > x2 - x1 - 16:
                    y1 -= 15
                self.regions.append(dict(x=x1, y=y1, w=x2 - x1, h=y2 - y1, label=lab, core=bool(c.get("core"))))
                for (oid, a1, b1, a2, b2) in drawn:
                    if oid != c["id"] and not (x1 >= a2 or a1 >= x2 or y1 >= b2 or b1 >= y2):
                        self.warn.append(f"los contextos '{c['id']}' y '{oid}' se superponen: ajusta columnas o líneas")
                drawn.append((c["id"], x1, y1, x2, y2))
        if self.regions:
            self.w = max(self.w, max(r["x"] + r["w"] for r in self.regions) + 20)
            self.h = max(self.h, max(r["y"] + r["h"] for r in self.regions) + 10)
            top = min(r["y"] for r in self.regions)
            if top < 0:
                self.shift(-top)

    def shift(self, dy):
        for n in self.notes:
            n["y"] += dy
        for r in self.regions:
            r["y"] += dy
        for ed in self.edges:
            ed["pts"] = [(x, y + dy) for x, y in ed["pts"]]
        self.h += dy


# ---------------------------------------------------------------- paso 8: contextos agrupados
class Grouped:
    """Vista de cierre del taller: sin línea de tiempo, un óvalo por contexto con sus agregados
    consolidados. Cada agregado reúne sus filas política → comando (con su rol) → evento, y las
    flechas unen un evento con la política (o el comando) que dispara en otro contexto.

    Cada flecha es una sola curva suave (Bézier: sale, se dobla una vez y entra), sin puntos de
    paso. Para que eso funcione, lo que se elige es la ubicación: se prueban varias disposiciones
    de los contextos y del orden de las filas, y gana la que deja todas las curvas sin pisar
    tarjetas, sin cruzarse y lo más cortas posible."""

    PW, CW, EW, EH, CH, AW, AH = 84, 84, 84, 58, 58, 58, 22   # política, comando, evento y agregado del mismo tamaño
    GI, GE, ROW, COLG, AGGH = 10, 4, 18, 26, 58
    AGGT = 54                                    # el agregado se monta sobre la unión del primer comando y su evento
    PAD, GAP = 10, 16

    def __init__(self, m, ids):
        import itertools
        self.m, self.ids, self.warn = m, ids, []
        self.order_ev = sorted(m["events"], key=lambda e: (e["lane"], e["slot"], e["col"]))
        self.relations()
        self.analyze()
        # dos pasadas: la ubicación se busca con un orden de filas, se elige el mejor orden, y se vuelve a
        # buscar la ubicación con ese orden (el orden decide por qué lado puede entrar o salir cada flecha)
        inners = [(t, s_, sw) for t in ("first", "last") for s_ in ("first", "last") for sw in (None, False, True)]
        best, best_inner = None, inners[0]
        for rnd in range(2):
            self._beam = None
            self.build(best_inner)
            for inner in inners:
                st = self.build(inner)
                if best is None or st["score"] < best["score"]:
                    best, best_inner = st, inner
        self.notes, self.ovals, self.edges = best["notes"], best["ovals"], best["edges"]
        self.w, self.h = best["w"], best["h"]
        self.warn += best["warn"]

    # -- relaciones entre contextos
    def relations(self):
        ids = self.ids
        m_rel = self.m.get("relations")
        if m_rel:
            out = []
            for r in m_rel:
                if r.get("from") not in ids or r.get("to") not in ids:
                    fail(f"relación con evento inexistente: {r}")
                out.append((r["from"], r["to"]))
        else:
            out = [(f["from"], f["to"]) for f in self.m.get("flows", [])]
            for ln in {e["lane"] for e in self.m["events"]}:
                main = sorted([e for e in self.m["events"] if e["lane"] == ln and e["slot"] == 0], key=lambda e: e["col"])
                out += [(a["id"], b["id"]) for a, b in zip(main, main[1:])]
            if any(ids[a].get("context") != ids[b].get("context") for a, b in out):
                self.warn.append("las relaciones entre contextos salen del flujo: proponerlas al arquitecto y, con su "
                                 "confirmación, escribirlas en 'relations' (solo las que de verdad disparan algo en otro contexto)")
        seen, self.rel = set(), []
        for a, b in out:
            if (ids[a].get("context") and ids[b].get("context") and ids[a]["context"] != ids[b]["context"]
                    and (a, b) not in seen):
                seen.add((a, b))
                self.rel.append((a, b))

    # -- contexto central y niveles (izquierda: le envían; derecha: reciben)
    def analyze(self):
        self.C = {c["id"]: c for c in self.m.get("contexts", [])}
        self.first = []
        for e in self.order_ev:
            if e.get("context") in self.C and e["context"] not in self.first:
                self.first.append(e["context"])
        ctx = lambda ev: self.ids[ev]["context"]
        deg, linked = {}, set()
        for a, b in self.rel:
            linked |= {ctx(a), ctx(b)}
            deg[ctx(a)] = deg.get(ctx(a), 0) + 1
            deg[ctx(b)] = deg.get(ctx(b), 0) + 1
        nev = {c: sum(1 for e in self.m["events"] if e.get("context") == c) for c in self.first}
        self.level, self.center, self.bidir = {}, None, []
        if linked:
            center = max(linked, key=lambda c: (deg[c], bool(self.C[c].get("core")), nev[c], -self.first.index(c)))
            self.center = center
            self.level[center] = 0
            frontier = [center]
            while frontier:
                nxt = []
                for c in frontier:
                    for a, b in self.rel:
                        if ctx(a) == c and ctx(b) not in self.level:
                            self.level[ctx(b)] = self.level[c] + 1 if self.level[c] >= 0 else self.level[c]
                            nxt.append(ctx(b))
                        elif ctx(b) == c and ctx(a) not in self.level:
                            self.level[ctx(a)] = self.level[c] - 1 if self.level[c] <= 0 else self.level[c]
                            nxt.append(ctx(a))
                frontier = nxt
            for c in linked - set(self.level):
                self.level[c] = max(self.level.values()) + 1
            # los que se relacionan con el central en los dos sentidos pueden ir a su lado, debajo o arriba
            to_c = {ctx(a) for a, b in self.rel if ctx(b) == center}
            from_c = {ctx(b) for a, b in self.rel if ctx(a) == center}
            self.bidir = sorted(to_c & from_c, key=self.first.index)[:3]
        self.linked = linked
        # momento del proceso de cada contexto: la primera columna de sus eventos que participan en
        # relaciones (o de todos sus eventos, si no tiene relaciones). Ordena la fila principal.
        inrel = {x for r_ in self.rel for x in r_}
        self.pkey = {}
        for c in self.first:
            evs = [e for e in self.m["events"] if e.get("context") == c]
            ev_r = [e for e in evs if e["id"] in inrel] or evs
            self.pkey[c] = (min(e["col"] for e in ev_r), self.first.index(c))

    # -- contenido de un contexto (coordenadas locales)
    def content(self, cid, inner):
        P = self
        evs = [e for e in self.order_ev if e.get("context") == cid]
        targets = {b for a, b in self.rel if self.ids[b].get("context") == cid}
        late = {b for a, b in self.rel if self.ids[b].get("context") == cid
                and self.pkey.get(self.ids[a]["context"], (0,)) > self.pkey.get(cid, (0,))}
        sources = {a for a, b in self.rel if self.ids[a].get("context") == cid} - targets
        t_pos, s_pos, swap = inner
        aggs = {}
        for e in evs:
            aggs.setdefault(e.get("aggregate") or "", []).append(e)
        for a in aggs:                           # las filas que reciben o envían flechas, al principio o al final
            lst = aggs[a]
            tg = [e for e in lst if e["id"] in targets and e["id"] not in late]
            lt = [e for e in lst if e["id"] in late]
            sr = [e for e in lst if e["id"] in sources]
            ot = [e for e in lst if e["id"] not in targets and e["id"] not in sources]
            # las que reciben desde la derecha: una al final (entra por abajo) y otra al principio
            # (entra por arriba), alternando, para que cada una tenga un lado libre
            if swap is None:                     # sin repartir: van con las demás que reciben flechas
                tg, lt = tg + lt, []
            lt_tail, lt_head = (lt[1::2], lt[0::2]) if swap else (lt[0::2], lt[1::2])
            head = lt_head + (tg if t_pos == "first" else []) + (sr if s_pos == "first" else [])
            tail = (sr if s_pos == "last" else []) + (tg if t_pos == "last" else []) + lt_tail
            aggs[a] = head + ot + tail
        rowh = P.EH + P.ROW
        colw = P.PW + P.GI + P.CW + P.GE + P.EW
        items = list(aggs.items())
        ncol = max(1, round(len(items) ** 0.5 + 0.2)) if len(items) > 2 else len(items)
        cols = [[] for _ in range(ncol)]
        hts = [0] * ncol
        recv = {self.ids[b].get("aggregate") for _, b in self.rel if self.ids[b].get("context") == cid}
        emit = {self.ids[a].get("aggregate") for a, _ in self.rel if self.ids[a].get("context") == cid}

        def put(i, a, lst):
            cols[i].append((a, lst))
            hts[i] += P.AGGT + len(lst) * rowh + 14
        rest = []
        for a, lst in items:                     # el que recibe flechas, a la izquierda; el que las envía, a la derecha
            if a in recv and a not in emit:
                put(0, a, lst)
            elif a in emit and a not in recv and ncol > 1:
                put(ncol - 1, a, lst)
            else:
                rest.append((a, lst))
        for a, lst in rest:
            put(hts.index(min(hts)), a, lst)
        cols = [c for c in cols if c]
        hts = [h for h in hts if h]
        boxes = []
        x = 0
        for col in cols:
            y = 0
            for a, lst in col:
                cx = x + P.PW + P.GI
                agg_box = None
                if a:                            # el agregado encima, centrado en la unión del comando y el evento
                    view = any(e.get("aggregate_view") for e in lst)
                    mid = cx + P.CW + P.GE / 2
                    agg_box = ("agregado", mid - P.CW / 2, y, P.CW, P.AGGH, a, None, view)
                y += P.AGGT
                for e in lst:
                    if e.get("policy"):
                        boxes.append(("politica", x, y, P.PW, P.EH, e["policy"], e["id"], False))
                    boxes.append(("comando", cx, y, P.CW, P.CH, e.get("command", ""), e["id"], False))
                    if e.get("actor"):
                        boxes.append(("usuario", cx - 10, y + P.CH - 8, P.AW, P.AH, e["actor"], e["id"], False))
                    boxes.append(("evento", cx + P.CW + P.GE, y, P.EW, P.EH, e["name"], e["id"], bool(e.get("hotspot"))))
                    if e.get("external"):
                        boxes.append(("externo", cx + P.CW + P.GE + 36, y + P.EH - 10, 56, 22, e["external"], e["id"], False))
                    y += rowh
                if agg_box:
                    boxes.append(agg_box)        # se dibuja después: queda encima del comando y el evento
                y += 14
            x += colw + P.COLG
        return boxes, x - P.COLG, max(hts) - 14

    @staticmethod
    def min_ellipse(pts):
        mx = max(abs(x) for x, _ in pts) + 1
        best = None
        a = mx
        while a < mx * 2.2:
            b = 0
            for x, y in pts:
                b = max(b, abs(y) / (1 - (x / a) ** 2) ** 0.5)
            if best is None or a * b < best[0]:
                best = (a * b, a, b)
            a += 3
        return best[1], best[2]

    def shape(self, cid, inner):
        boxes, w, h = self.content(cid, inner)
        lab = self.C[cid]["name"]
        lw = min(w, len(lab) * 12 + 16)
        cx0, cy0 = w / 2, (h - 30) / 2
        pts = []
        for (_, x, y, bw, bh, *_r) in boxes:
            for px, py in ((x - self.PAD, y - self.PAD), (x + bw + self.PAD, y - self.PAD),
                           (x - self.PAD, y + bh + self.PAD), (x + bw + self.PAD, y + bh + self.PAD)):
                pts.append((px - cx0, py - cy0))
        for px in (w / 2 - lw / 2 - 6, w / 2 + lw / 2 + 6):
            pts.append((px - cx0, -44 - cy0))
        a, b = self.min_ellipse(pts)
        return dict(boxes=boxes, w=w, h=h, a=a, b=b, ox=cx0, oy=cy0, name=lab)

    # -- una disposición completa: ubicación de los óvalos, tarjetas y curvas, con su puntaje
    def build(self, inner, beam=3):
        """Una disposición: el contexto central en el medio y cada contexto relacionado pegado a uno
        con el que se relaciona, en la dirección (de ocho posibles) que deja las flechas más cortas,
        sin cruces y sin pisar tarjetas. Se busca por haz: se ubica un contexto a la vez y se guardan
        las mejores disposiciones parciales. Los contextos sin relaciones van arriba o abajo."""
        import math
        first = self.first
        order_all = list(first)
        shapes = {c: self.shape(c, inner) for c in order_all}
        G2 = self.GAP / 2

        def overlap(c1, s1, c2, s2):
            for (pa, sa, pb, sb) in ((c1, s1, c2, s2), (c2, s2, c1, s1)):
                for k in range(72):
                    t = 2 * math.pi * k / 72
                    x = pa[0] + (sa["a"] + G2) * math.cos(t)
                    y = pa[1] + (sa["b"] + G2) * math.sin(t)
                    if ((x - pb[0]) / (sb["a"] + G2)) ** 2 + ((y - pb[1]) / (sb["b"] + G2)) ** 2 < 1:
                        return True
            return False

        def free(placed, c, s_):
            return not any(overlap(c, s_, p, shapes[q]) for q, p in placed.items())

        def materialize(placed):
            notes, ovals, wh = [], [], {}
            for cid, (cx, cy) in placed.items():
                s = shapes[cid]
                ox, oy = cx - s["ox"], cy - s["oy"]
                tw = len(s["name"]) * 12 + 90
                d = s["b"] * max(0.0, 1 - (tw / (2 * s["a"])) ** 2) ** 0.5
                ly = min(oy - 30, cy - d + 14)
                ovals.append(dict(x=cx - s["a"], y=cy - s["b"], w=2 * s["a"], h=2 * s["b"], name=s["name"],
                                  lx=ox, ly=ly, lw=s["w"], cx=cx, cy=cy, a=s["a"], b=s["b"], top=oy, low=oy - 30))
                for kind, x, y, bw, bh, text, ev, flag in s["boxes"]:
                    n = dict(kind=kind, x=ox + x, y=oy + y, w=bw, h=bh, text=text, ev=ev,
                             hot=flag if kind == "evento" else False, view=flag if kind == "agregado" else False, key=None)
                    if kind in ("politica", "comando", "evento"):
                        n["key"] = f"{kind}:{ev}"
                        wh[n["key"]] = n
                    notes.append(n)
            return notes, ovals, wh

        def evaluate(placed):
            notes, ovals, wh = materialize(placed)
            rels = [(a, b) for a, b in self.rel if self.ids[a]["context"] in placed and self.ids[b]["context"] in placed]
            edges, sc, warn = self.curves(notes, ovals, wh, rels)
            xs = [p[0] - shapes[q]["a"] for q, p in placed.items()] + [p[0] + shapes[q]["a"] for q, p in placed.items()]
            ys = [p[1] - shapes[q]["b"] for q, p in placed.items()] + [p[1] + shapes[q]["b"] for q, p in placed.items()]
            W, H = max(xs) - min(xs), max(ys) - min(ys)
            return sc + (W * H) / 4000 + 0.15 * abs(W - 1.4 * H), (notes, ovals, wh, edges, warn)

        ctx = lambda ev: self.ids[ev]["context"]
        nbrs = {}
        for a, b in self.rel:
            nbrs.setdefault(ctx(a), set()).add(ctx(b))
            nbrs.setdefault(ctx(b), set()).add(ctx(a))
        pins = {c: tuple(p) for c, p in (self.m.get("context_layout") or {}).items() if c in shapes}
        states = [(dict(pins), 0)]
        if getattr(self, "_beam", None) is not None:
            states = self._beam                  # la ubicación no depende del orden de las filas: se reutiliza
        elif self.center and not all(c in pins for c in self.linked):
            start = dict(pins) if pins else {self.center: (0.0, 0.0)}
            if self.center not in start:
                start[self.center] = (0.0, 0.0)
                while not all(free({q: p for q, p in start.items() if q != self.center}, start[self.center], shapes[self.center]) for _ in [0]):
                    start[self.center] = (start[self.center][0] + 40, start[self.center][1])
            states = [(start, 0)]
            seq, seen = [], set(start)
            frontier = list(start)
            while frontier:                      # en anchura desde el central; a igualdad, en el orden del proceso
                nxt = []
                for c in frontier:
                    for n in sorted(nbrs.get(c, ()), key=lambda q: self.pkey[q]):
                        if n not in seen:
                            seen.add(n)
                            seq.append(n)
                            nxt.append(n)
                frontier = nxt
            DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
            for c in seq:
                s_ = shapes[c]
                cand = []
                for placed, _ in states:
                    for anchor in [q for q in nbrs[c] if q in placed]:
                        ax, ay = placed[anchor]
                        sa = shapes[anchor]
                        for dx, dy in DIRS:
                            n_ = math.hypot(dx, dy)
                            ux, uy = dx / n_, dy / n_
                            t = 0.0
                            while True:          # se aleja del ancla en esa dirección hasta no tocar a nadie
                                p = (ax + ux * t, ay + uy * t)
                                if free(placed, p, s_):
                                    break
                                t += 8
                            np_ = dict(placed)
                            np_[c] = p
                            sc, _ = evaluate(np_)
                            cand.append((sc, np_))
                cand.sort(key=lambda z: z[0])
                states, keys = [], set()
                for sc, st in cand:
                    k = tuple(sorted((q, round(v[0] / 20), round(v[1] / 20)) for q, v in st.items()))
                    if k not in keys:
                        keys.add(k)
                        states.append((st, sc))
                    if len(states) == beam:
                        break
        self._beam = states
        best = None
        for placed, _ in states:
            placed = dict(placed)
            # los contextos sin relaciones: arriba o abajo, de izquierda a derecha, lo más cerca posible
            loose = [c for c in first if c not in placed]
            pos0 = min((first.index(c) for c in self.linked), default=len(first))
            tops = [c for c in loose if first.index(c) < pos0]
            bots = [c for c in loose if first.index(c) >= pos0]
            area = sum(4 * s_["a"] * s_["b"] for s_ in shapes.values())
            for grp, sgn in ((tops, -1), (bots, 1)):
                if not grp:
                    continue
                if placed:
                    lo_x = min(p[0] - shapes[q]["a"] for q, p in placed.items())
                    hi_x = max(p[0] + shapes[q]["a"] for q, p in placed.items())
                else:
                    lo_x = hi_x = 0
                maxw = max(hi_x - lo_x, 1.4 * area ** 0.5, max(2 * shapes[c]["a"] for c in grp))
                x = lo_x
                for cid in grp:
                    s_ = shapes[cid]
                    if x > lo_x and x + 2 * s_["a"] - lo_x > maxw:
                        x = lo_x
                    cx = x + s_["a"]
                    if placed:
                        ext = [p[1] + sgn * shapes[q]["b"] for q, p in placed.items()]
                        cy = (min(ext) if sgn < 0 else max(ext)) + sgn * (s_["b"] + self.GAP)
                        while free(placed, (cx, cy - sgn * 6), s_):
                            cy -= sgn * 6
                        while cx - 6 > lo_x + s_["a"] and free(placed, (cx - 6, cy), s_):
                            cx -= 6
                    else:
                        cy = 0
                    placed[cid] = (cx, cy)
                    x = cx + s_["a"]
            mnx = min(p[0] - shapes[q]["a"] for q, p in placed.items())
            mny = min(p[1] - shapes[q]["b"] for q, p in placed.items())
            placed = {q: (p[0] - mnx, p[1] - mny) for q, p in placed.items()}
            sc, (notes, ovals, wh, edges, warn) = evaluate(placed)
            ql = list(placed)
            for i_ in range(len(ql)):            # contextos fijados a mano que ahora se enciman (cambió su contenido)
                for j_ in range(i_ + 1, len(ql)):
                    if (ql[i_] in pins or ql[j_] in pins) and overlap(placed[ql[i_]], shapes[ql[i_]], placed[ql[j_]], shapes[ql[j_]]):
                        warn = warn + [f"los contextos '{shapes[ql[i_]]['name']}' y '{shapes[ql[j_]]['name']}' se enciman: "
                                       "corre uno de los dos en draw.io y vuelve a guardar la ubicación con 'layout'"]
                        sc += 3000
            tw_ = self.place_titles(ovals, notes, edges)
            sc += 1500 * len(tw_)
            if best is None or sc < best["score"]:
                W = max(o["x"] + o["w"] for o in ovals) + 10
                H = max(o["y"] + o["h"] for o in ovals) + 10
                best = dict(notes=notes, ovals=ovals, edges=edges, w=W, h=H, score=sc, warn=warn + tw_)
        return best

    # -- una curva por relación
    def curves(self, notes, ovals, wh, rels=None):
        import math
        rects = [(n["x"] - 5, n["y"] - 5, n["x"] + n["w"] + 5, n["y"] + n["h"] + 5, n.get("key")) for n in notes]
        # por arriba, el evento sale cerca de su esquina derecha: así no cruza el agregado montado
        # sobre la unión del comando y el evento
        OUT = {"R": ((1, .5), (1, 0)), "T": ((.8, 0), (0, -1)), "B": ((.5, 1), (0, 1))}
        IN = {"L": ((0, .5), (-1, 0)), "T": ((.5, 0), (0, -1)), "B": ((.5, 1), (0, 1)), "R": ((1, .5), (1, 0))}

        def hits(path, skip):
            n_ = 0
            bx1, bx2 = min(p[0] for p in path), max(p[0] for p in path)
            by1, by2 = min(p[1] for p in path), max(p[1] for p in path)
            near = [r_ for r_ in rects if not (r_[2] < bx1 or r_[0] > bx2 or r_[3] < by1 or r_[1] > by2)]
            for (x1, y1), (x2, y2) in zip(path, path[1:]):
                for rx1, ry1, rx2, ry2, key in near:
                    if key in skip and key is not None:
                        continue
                    if max(x1, x2) < rx1 or min(x1, x2) > rx2 or max(y1, y2) < ry1 or min(y1, y2) > ry2:
                        continue
                    for s_ in range(5):
                        t = s_ / 4
                        x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
                        if rx1 < x < rx2 and ry1 < y < ry2:
                            n_ += 1
                            break
            return n_
        edges, total, warn = [], 0, []
        drawn = []
        for a, b in sorted(self.rel if rels is None else rels, key=lambda r: math.dist(
                (wh[f"evento:{r[0]}"]["x"], wh[f"evento:{r[0]}"]["y"]),
                ((wh.get(f"politica:{r[1]}") or wh[f"comando:{r[1]}"])["x"], (wh.get(f"politica:{r[1]}") or wh[f"comando:{r[1]}"])["y"]))):
            src = wh[f"evento:{a}"]
            tgt = wh.get(f"politica:{b}") or wh[f"comando:{b}"]
            skip = {src["key"], tgt["key"]}
            best = None
            for fo, do in OUT.values():
                for fi, di in IN.values():
                    P0 = (src["x"] + src["w"] * fo[0], src["y"] + src["h"] * fo[1])
                    P3 = (tgt["x"] + tgt["w"] * fi[0], tgt["y"] + tgt["h"] * fi[1])
                    dist = math.dist(P0, P3)
                    for k1 in (0.35, 0.65, 1.0):
                      for k2 in (0.35, 0.65, 1.0):
                        d1 = max(45, min(480, dist * k1))
                        d2 = max(45, min(480, dist * k2))
                        C1 = (P0[0] + do[0] * d1, P0[1] + do[1] * d1)
                        C2 = (P3[0] + di[0] * d2, P3[1] + di[1] * d2)
                        path = [P0] + bezier(P0, C1, C2, P3, 40) + [P3]
                        L = sum(math.dist(p, q) for p, q in zip(path, path[1:]))
                        if best is not None and L >= best[0]:
                            continue             # ya hay una curva mejor: no hace falta revisar choques
                        sc = 2500 * hits(path[1:-1], skip) + 900 * sum(1 for d_ in drawn if self._cross(path, d_)) + L
                        if best is None or sc < best[0]:
                            best = (sc, path, fo, fi)
            if best[0] >= 2500:
                warn.append(f"la flecha {a} -> {b} pasa sobre tarjetas")
            total += best[0]
            drawn.append(best[1])
            edges.append(dict(src=src, tgt=tgt, pts=best[1][1:-1], exit=best[2], entry=best[3]))
        return edges, total, warn

    def place_titles(self, ovals, notes, edges):
        """El nombre de cada contexto, lo más arriba posible dentro de su óvalo, sin tocar flechas ni tarjetas.
        Si una flecha pasa por donde iría, se corre a un lado o un poco más abajo."""
        out = []
        pts = [p for e in edges for p in e["pts"]]
        boxes = [(n["x"] - 4, n["y"] - 4, n["x"] + n["w"] + 4, n["y"] + n["h"] + 4) for n in notes]
        for o in ovals:
            tw = len(o["name"]) * 12 + 16
            th = 30
            cxl = o["lx"] + o["lw"] / 2

            def ok(x, y):
                for qx, qy in ((x, y), (x + tw, y), (x, y + th), (x + tw, y + th)):
                    if ((qx - o["cx"]) / o["a"]) ** 2 + ((qy - o["cy"]) / o["b"]) ** 2 > 0.93:
                        return False
                if any(not (x + tw < b[0] or x > b[2] or y + th < b[1] or y > b[3]) for b in boxes):
                    return False
                return not any(x - 6 < px < x + tw + 6 and y - 6 < py < y + th + 6 for px, py in pts)
            best = None
            for dy in range(0, 400, 6):
                y = o["ly"] - 6 + dy
                if y + th > o["top"] + 2:
                    break
                for dx in sorted(range(-int(o["lw"] / 2), int(o["lw"] / 2) + 1, 8), key=abs):
                    x = cxl - tw / 2 + dx
                    if ok(x, y):
                        sc = dy + 0.7 * abs(dx)
                        if best is None or sc < best[0]:
                            best = (sc, x, y)
                        break
                if best and best[0] <= dy:
                    break
            if best:
                o["tx"], o["ty"], o["tw"] = best[1], best[2], tw
            else:
                o["tx"], o["ty"], o["tw"] = cxl - tw / 2, o["ly"] - 6, tw
                out.append(f"el nombre del contexto '{o['name']}' queda bajo una flecha")
        return out

    @staticmethod
    def _cross(p, q):
        def o(a, b, c):
            return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        for i in range(len(p) - 1):
            for j in range(len(q) - 1):
                a1, a2, b1, b2 = p[i], p[i + 1], q[j], q[j + 1]
                if max(a1[0], a2[0]) < min(b1[0], b2[0]) or max(b1[0], b2[0]) < min(a1[0], a2[0]):
                    continue
                if o(b1, b2, a1) * o(b1, b2, a2) < 0 and o(a1, a2, b1) * o(a1, a2, b2) < 0:
                    return True
        return False


def grouped_cells(g, x0, y0):
    c = Cells("g")
    L = "paso-8"
    hdr = (f"text;html=1;fillColor=none;strokeColor=none;align=left;verticalAlign=middle;fontFamily={FONT};fontStyle=1;fontSize=13;"
           f"fontColor={COL['texto']};")
    c.vertex(L, f"PASO 8: {PASOS[8][0]}", hdr, x0, y0, 420, 24, cid="p8-hdr")
    oy = y0 + 40
    for o in g.ovals:
        c.vertex(L, "", f"ellipse;shape=ellipse;perimeter=ellipsePerimeter;whiteSpace=wrap;html=1;fillColor=none;"
                        f"strokeColor=#6B6B6B;strokeWidth=1.8;dashed=1;dashPattern=8 6;", x0 + o["x"], oy + o["y"], o["w"], o["h"])
        c.vertex(L, o["name"], f"text;html=1;fillColor=none;strokeColor=none;align=center;verticalAlign=middle;fontFamily={FONT};"
                               f"fontStyle=1;fontSize=19;fontColor=#1E1E1E;", x0 + o["tx"], oy + o["ty"], o["tw"], 30)
    ids = {}
    for n in g.notes:
        st = note_style(n)
        cid = c.vertex(L, n["text"], st, x0 + n["x"], oy + n["y"], n["w"], n["h"])
        if n["key"]:
            ids[n["key"]] = cid
    for e in g.edges:
        st = (f"edgeStyle=none;curved=1;html=1;endArrow=block;endFill=1;endSize=6;strokeColor={COL['linea']};strokeWidth=1.8;"
              f"exitX={e['exit'][0]};exitY={e['exit'][1]};entryX={e['entry'][0]};entryY={e['entry'][1]};"
              "exitDx=0;exitDy=0;entryDx=0;entryDy=0;")
        c.edge(L, st, ids[e["src"]["key"]], ids[e["tgt"]["key"]], [(x0 + x, oy + y) for x, y in e["pts"][1::3]])
    return c.out


def grouped_page_xml(m, g):
    name = f"Paso 8 · {PASOS[8][0]}"
    layer = f'<mxCell id="paso-8" value={esc(name)} parent="0"/>'
    return (f'<diagram id="paso-8" name={esc(name)}>{GRAPH}'
            '<mxCell id="1" value="Leyenda" parent="0"/>' + "".join(legend_cells(m, 8)) + layer
            + "".join(grouped_cells(g, BOARD_X, 0)) + "</root></mxGraphModel></diagram>")


# ---------------------------------------------------------------- draw.io
def esc(s):
    return quoteattr(s)


def note_style(n):
    fill = COL[n["kind"]]
    size = {"evento": 12, "usuario": 9.5, "externo": 10.5, "politica": 10.5, "datos": 10.5}.get(n["kind"], 11)
    s = (f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};shadow=1;fontFamily={FONT};"
         f"fontColor={COL['texto']};fontSize={size};spacing=3;")
    if n["hot"]:
        s += f"strokeColor={COL['hot']};strokeWidth=2;dashed=1;dashPattern=5 3;"
    elif n["view"]:
        s += f"strokeColor={COL['vista']};strokeWidth=1.3;dashed=1;dashPattern=5 3;"
    else:
        s += "strokeColor=none;"
    return s


class Cells:
    def __init__(self, prefix):
        self.prefix, self.k, self.out = prefix, 0, []

    def nid(self):
        self.k += 1
        return f"{self.prefix}-{self.k}"

    def vertex(self, layer, value, style, x, y, w, h, cid=None):
        cid = cid or self.nid()
        self.out.append(f'<mxCell id="{cid}" value={esc(value)} style={esc(style)} vertex="1" parent="{layer}">'
                        f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')
        return cid

    def edge(self, layer, style, src=None, tgt=None, pts=(), sp=None, tp=None, cid=None):
        attrs = (f' source="{src}"' if src else "") + (f' target="{tgt}"' if tgt else "")
        geo = '<mxGeometry relative="1" as="geometry">'
        if sp:
            geo += f'<mxPoint x="{sp[0]:.1f}" y="{sp[1]:.1f}" as="sourcePoint"/>'
        if tp:
            geo += f'<mxPoint x="{tp[0]:.1f}" y="{tp[1]:.1f}" as="targetPoint"/>'
        if pts:
            geo += "<Array as=\"points\">" + "".join(f'<mxPoint x="{x:.1f}" y="{y:.1f}"/>' for x, y in pts) + "</Array>"
        geo += "</mxGeometry>"
        self.out.append(f'<mxCell id="{cid or self.nid()}" style={esc(style)} edge="1" parent="{layer}"{attrs}>{geo}</mxCell>')


def legend_cells(m, S=None):
    c = Cells("leyenda")
    L = "1"
    txt = f"text;html=1;fillColor=none;strokeColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontFamily={FONT};fontColor={COL['texto']};"
    title = m.get("title") or "Event Storming"
    c.vertex(L, f"EVENT STORMING · {title}", f"rounded=0;fillColor={COL['barra']};strokeColor=none;fontColor=#FFFFFF;"
             f"fontStyle=1;fontSize=12;fontFamily={FONT};html=1;whiteSpace=wrap;", 0, 0, LEFT_W, 30)
    y = 44
    c.vertex(L, "TERMINOLOGÍA", txt + "fontStyle=1;fontSize=11;", 8, y, 200, 20)
    y += 24
    th = len(TERMINOS) * 46 + 52 + 46
    c.vertex(L, "", f"rounded=0;fillColor={COL['panel']};strokeColor=none;", 0, y, LEFT_W, th)
    yy = y + 10
    for kind, name, desc in TERMINOS:
        c.vertex(L, name, f"rounded=0;whiteSpace=wrap;html=1;fillColor={COL[kind]};strokeColor=none;shadow=1;"
                 f"fontFamily={FONT};fontSize=9.5;fontColor={COL['texto']};", 14, yy, 64, 38)
        c.vertex(L, desc, txt + "fontSize=10.5;", 90, yy, LEFT_W - 104, 38)
        yy += 46
    c.vertex(L, "Por confirmar", f"rounded=0;whiteSpace=wrap;html=1;fillColor={COL['evento']};strokeColor={COL['hot']};"
             f"strokeWidth=2;dashed=1;dashPattern=5 3;fontFamily={FONT};fontSize=9.5;", 14, yy, 64, 38)
    c.vertex(L, "Regla o hecho que falta confirmar con el negocio.", txt + "fontSize=10.5;", 90, yy, LEFT_W - 104, 38)
    yy += 46
    box = f"rounded=1;absoluteArcSize=1;arcSize=14;whiteSpace=wrap;html=1;fillColor=none;strokeColor=#6B6B6B;strokeWidth=1.6;fontFamily={FONT};fontSize=9.5;fontStyle=1;"
    c.vertex(L, "Contexto", box, 14, yy, 64, 38)
    c.vertex(L, "Contexto de negocio: agrupa los agregados de un mismo propósito.", txt + "fontSize=10.5;", 90, yy, LEFT_W - 104, 38)

    y = y + th + 16
    c.vertex(L, "PROCESO", txt + "fontStyle=1;fontSize=11;", 8, y, 200, 20)
    y += 24
    ph = len(PASOS) * 52 + 14
    c.vertex(L, "", f"rounded=0;fillColor={COL['panel']};strokeColor=none;", 0, y, LEFT_W, ph)
    yy = y + 10
    for n, (name, desc) in PASOS.items():
        if n == S:                      # el paso de esta página, resaltado
            c.vertex(L, "", f"rounded=0;fillColor={COL['evento']};opacity=35;strokeColor=none;", 6, yy - 4, LEFT_W - 12, 52)
        c.vertex(L, f"<b>Paso {n}: {name}</b><br>{desc}", txt + "fontSize=10.5;verticalAlign=top;", 14, yy, LEFT_W - 28, 46)
        yy += 52
    return c.out


def step_cells(step, S, x0, y0):
    """Celdas del tablero del paso S, trasladadas a (x0, y0)."""
    c = Cells(f"p{S}")
    L = f"paso-{S}"
    name = PASOS[S][0]
    hdr = (f"text;html=1;fillColor=none;strokeColor=none;align=left;verticalAlign=middle;fontFamily={FONT};fontStyle=1;fontSize=13;"
           f"fontColor={COL['texto']};")
    c.vertex(L, f"PASO {S}: {name}", hdr, x0, y0, 420, 24, cid=f"p{S}-hdr")
    oy = y0 + 34
    for r in step.regions:
        sw, sc = "1.6", "#6B6B6B"                # todos los contextos con la misma línea
        c.vertex(L, r["label"], f"rounded=1;absoluteArcSize=1;arcSize=40;whiteSpace=wrap;html=1;fillColor=none;strokeColor={sc};"
                 f"strokeWidth={sw};verticalAlign=top;fontFamily={FONT};fontStyle=1;fontSize=12.5;"
                 f"fontColor=#2B2B2B;spacingTop=2;", x0 + r["x"], oy + r["y"], r["w"], r["h"])
    ids = {}
    for n in step.notes:
        cid = c.vertex(L, n["text"], note_style(n), x0 + n["x"], oy + n["y"], n["w"], n["h"])
        if n["key"]:
            ids[n["key"]] = cid
    for e in step.edges:
        st = (f"edgeStyle=none;curved=1;html=1;endArrow=block;endFill=1;endSize=5;strokeColor={COL['linea']};"
              f"strokeWidth=1.6;exitX={e['exit'][0]};exitY={e['exit'][1]};exitDx=0;exitDy=0;"
              f"entryX={e['entry'][0]};entryY={e['entry'][1]};entryDx=0;entryDy=0;"
              + ("dashed=1;dashPattern=6 4;" if e["dashed"] else ""))
        c.edge(L, st, ids.get(e["src"]), ids.get(e["tgt"]), [(x0 + x, oy + y) for x, y in e["pts"]])
    return c.out, oy + step.h


GRAPH = ('<mxGraphModel grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
         'page="0" pageScale="1" math="0" shadow="0"><root><mxCell id="0"/>')


def page_open(S, m):
    """Inicio de la página del paso S, con el panel de terminología y proceso."""
    return (f'<diagram id="paso-{S}" name={esc(f"Paso {S} · {PASOS[S][0]}")}>{GRAPH}'
            '<mxCell id="1" value="Leyenda" parent="0"/>' + "".join(legend_cells(m, S)))


def page_xml(m, step, S):
    layer = f'<mxCell id="paso-{S}" value={esc(f"Paso {S} · {PASOS[S][0]}")} parent="0"/>'
    return (page_open(S, m) + layer + "".join(step_cells(step, S, BOARD_X, 0)[0])
            + "</root></mxGraphModel></diagram>")


def shift_y(cell, dy):
    g = cell.find("mxGeometry")
    if g is None:
        return
    if g.get("y") is not None:
        g.set("y", str(float(g.get("y")) + dy))
    for pt in g.iter("mxPoint"):
        pt.set("y", str(float(pt.get("y", 0)) + dy))


def cell_top(cell):
    g = cell.find("mxGeometry")
    if g is None:
        return None
    ys = [float(pt.get("y", 0)) for pt in g.iter("mxPoint")]
    if g.get("y") is not None:
        ys.append(float(g.get("y")))
    return min(ys) if ys else None


def read_pages(path, m):
    """Páginas de un tablero, por número de paso.

    Acepta también el formato anterior (una sola página con una capa por paso): cada capa pasa a su
    propia página, con el panel de terminología, conservando los ajustes hechos a mano.
    """
    top = ET.parse(path).getroot()
    if top.tag != "mxfile":
        fail(f"{path} no es un .drawio de este generador")
    diagrams = top.findall("diagram")
    pages = {}
    for d in diagrams:
        did = d.get("id") or ""
        if did.startswith("paso-") and did[5:].isdigit():
            pages[int(did[5:])] = d
        elif did == "contextos":                # formato anterior: la página de contextos agrupados
            pages[8.5] = d
    if pages or len(diagrams) != 1:
        return pages
    root = diagrams[0].find(".//root")
    if root is None:
        fail(f"{path} no es un .drawio de este generador")
    cells = root.findall("mxCell")
    for lid in [c.get("id") for c in cells if c.get("parent") == "0" and (c.get("id") or "").startswith("paso-")]:
        k = int(lid[5:])
        mine = [c for c in cells if (c.get("id") == lid or c.get("parent") == lid) and c.get("id") != f"p{k}-sep"]
        tops = [t for t in (cell_top(c) for c in mine) if t is not None]
        for c in mine:
            shift_y(c, -min(tops) if tops else 0)
        d = ET.fromstring(page_open(k, m) + "</root></mxGraphModel></diagram>")
        r = d.find(".//root")
        for c in mine:
            r.append(c)
        pages[k] = d
    return pages


def wrap_file(body, title):
    return (f'<mxfile host="es_drawio"><diagram id="event-storming" name={esc(title)}>{GRAPH}'
            f'{body}</root></mxGraphModel></diagram></mxfile>')


def cmd_build(args):
    model = args[0]
    S = int(opt(args, "--paso"))
    out = opt(args, "--out")
    base = opt(args, "--base", None)
    if S not in PASOS:
        fail("el paso va de 1 a 8")
    m, ids = load(model, S)
    step = Step(m, ids, min(S, 7)) if S == 8 else Step(m, ids, S)
    pages = {}
    if base and os.path.exists(base):
        # las páginas de los pasos anteriores se conservan tal como quedaron (con sus ajustes a mano);
        # la del paso S se regenera y las de pasos posteriores se quitan
        pages = {k: ET.tostring(d, encoding="unicode") for k, d in read_pages(base, m).items() if k < S}
    elif S != 1 and base:
        print(f"AVISO: no existe {base}; el tablero empieza en el paso {S}")
    if S == 8:
        # el paso 8 son los contextos delimitados sin línea de tiempo (el flujo ya quedó en los pasos 2 a 7)
        if not any(e.get("context") for e in m["events"]):
            fail("en el paso 8 cada evento necesita su 'context'")
        g = Grouped(m, ids)
        pages[8] = grouped_page_xml(m, g)
        warn = list(g.warn)
    else:
        pages[S] = page_xml(m, step, S)
        warn = list(step.warn)
    with open(out, "w", encoding="utf-8") as f:
        f.write('<mxfile host="es_drawio">' + "".join(pages[k] for k in sorted(pages)) + "</mxfile>")
    print(f"OK  {out}  (página del paso {S}: {PASOS[S][0]})")
    for w in warn:
        print(f"AVISO paso {S}: {w}")


def find_drawio():
    for c in ("drawio", "draw.io"):
        p = shutil.which(c)
        if p:
            return p
    for p in ("/Applications/draw.io.app/Contents/MacOS/draw.io",
              os.path.expanduser("~/Applications/draw.io.app/Contents/MacOS/draw.io"),
              "C:/Program Files/draw.io/draw.io.exe"):
        if os.path.exists(p):
            return p
    return None


def cmd_export(args):
    src = args[0]
    S = int(opt(args, "--paso"))
    out = opt(args, "--out")
    pages = read_pages(src, {"title": ""})
    key, layer, hdr = S, f"paso-{S}", f"p{S}-hdr"
    if key not in pages:
        fail(f"{src} no tiene la página del paso {S}")
    # solo el tablero: sin el panel de terminología ni el título
    keep = [c for c in pages[key].find(".//root").findall("mxCell")
            if (c.get("id") == layer or c.get("parent") == layer) and c.get("id") not in (hdr, f"p{S}-sep")]
    body = "".join(ET.tostring(c, encoding="unicode") for c in keep)
    tmp = os.path.join(tempfile.mkdtemp(prefix="es-"), f"step-{S}.drawio")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(wrap_file(body, f"Paso {S}"))
    exe = find_drawio()
    if not exe:
        print(f"AVISO: no se encontró draw.io Desktop. Queda el archivo de un solo paso en {tmp}: "
              "ábrelo y expórtalo a PNG (Archivo > Exportar como > PNG, escala 200 %).")
        sys.exit(2)
    subprocess.run([exe, "-x", "-f", "png", "-s", "2", "-b", "16", "-o", out, tmp], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"OK  {out}")


def cmd_layout(args):
    """Guarda en el modelo la ubicación de los contextos que el arquitecto acomodó a mano en la
    página del paso 8, para que al volver a dibujar se respete."""
    src, model = args[0], args[1]
    pages = read_pages(src, {"title": ""})
    page = pages.get(8.5) if 8.5 in pages else pages.get(8)
    if page is None:
        fail(f"{src} no tiene la página del paso 8")
    with open(model, encoding="utf-8") as f:
        m = json.load(f)
    byname = {c["name"]: c["id"] for c in m.get("contexts", [])}
    ovals, titles = [], []
    for c in page.iter("mxCell"):
        st, g = c.get("style") or "", c.find("mxGeometry")
        if g is None:
            continue
        x, y = float(g.get("x", 0)), float(g.get("y", 0))
        w, h = float(g.get("width", 0)), float(g.get("height", 0))
        if "ellipse" in st:
            ovals.append((x + w / 2, y + h / 2, w / 2, h / 2))
        elif "fontSize=19" in st and c.get("value") in byname:
            titles.append((c.get("value"), x + w / 2, y + h / 2))
    lay = {}
    for name, tx, ty in titles:
        inside = [o for o in ovals if ((tx - o[0]) / o[2]) ** 2 + ((ty - o[1]) / o[3]) ** 2 <= 1]
        if inside:
            o = min(inside, key=lambda o: o[2] * o[3])
            lay[byname[name]] = [round(o[0] - BOARD_X, 1), round(o[1] - 40, 1)]
    if not lay:
        fail("no encontré óvalos de contexto con su nombre en la página del paso 8")
    m["context_layout"] = lay
    with open(model, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"OK  {model}  (ubicación de {len(lay)} contextos guardada en 'context_layout')")
    for c in m.get("contexts", []):
        if c["id"] not in lay:
            print(f"AVISO: no encontré el óvalo de '{c['name']}': se ubicará solo")


def cmd_data(args):
    m, _ = load(args[0])
    out = opt(args, "--out")
    rows = [e for e in m["events"] if data_text(e)]
    lines = ["| Evento | Datos | Fuente |", "|---|---|---|"]
    lines += [f"| {e['name']} | {data_text(e)} | {e.get('source', '')} |" for e in rows]
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"OK  {out}")


def opt(args, name, default=...):
    if name in args:
        return args[args.index(name) + 1]
    if default is ...:
        fail(f"falta {name}")
    return default


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("build", "export", "data", "layout"):
        sys.exit(__doc__)
    {"build": cmd_build, "export": cmd_export, "data": cmd_data, "layout": cmd_layout}[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
