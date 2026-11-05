# Formato de document.json

Referencia de `document`. Leer antes de escribir `document/source/document.json`.

- Las rutas de imágenes son relativas al JSON. Las vistas vigentes se toman de `diagrams/images/`: desde `document/source/`, la ruta es `../../diagrams/images/<vista>.png`.
- Los textos aceptan un string o una lista de párrafos.
- Las claves opcionales que no apliquen se omiten (no se dejan vacías) y el script ajusta la numeración.

```json
{
  "portada": "cover.png",
  "control": [
    ["1.0", "2026-11-02", "<autores>", "Secciones 1 y 2 y paso 1 del proceso de diseño."],
    ["1.1", "2026-11-03", "<autores>", "Iteración 1: estructura general del sistema. ADR nuevos: ADR-001. Vistas: estilo, contenedores, despliegue."]
  ],
  "introduccion": [
    "<Qué sistema, para quién y qué cubre.>",
    "El diseño se elaboró con ADD 3.0 (Cervantes y Kazman, 2024) en 1 ronda y 1 iteración; el detalle está en el registro de diseño ADD v1.1."
  ],
  "contexto": {
    "situacion": ["<drivers.md §1.1>"],
    "objetivo": ["<drivers.md §1.2>"],
    "diagrama": "../../diagrams/images/c4-context.png"
  },
  "drivers": {
    "funcionalidades": ["UC-01 Registrar pedido: <descripción> (primario)"],
    "diagrama_casos_uso": "../../diagrams/images/use-cases.png",
    "restricciones": ["CON-1: <restricción>"],
    "supuestos": ["AS-1: <supuesto> Estado: <estado>."],
    "escenarios": [{
      "id": "QA-01", "nombre": "<nombre>", "atributo": "<atributo>", "refinamiento": "<refinamiento>",
      "negocio": "A", "dificultad": "A",
      "fuente": "…", "estimulo": "…", "ambiente": "…", "artefacto": "…", "respuesta": "…", "medida": "…",
      "caso_uso": "UC-02"
    }],
    "preocupaciones": ["CRN-1: Establecer una estructura general del sistema."]
  },
  "decisiones": {
    "estilo": {"nombre": "Monolito Modular", "texto": ["…"], "diagrama": "../../diagrams/images/architectural-style.png"},
    "patrones": [{"nombre": "Clean Architecture", "texto": "…"}],
    "base_datos": ["…"],
    "cloud": {"texto": "…", "servicios": [["Amazon ECS Fargate", "…"]]},
    "stack": [["Frontend", "…"], ["Backend", "…"]]
  },
  "vistas": {
    "contenedores": {"texto": "…", "diagrama": "../../diagrams/images/c4-containers.png"},
    "componentes": {"texto": "…", "diagrama": "../../diagrams/images/c4-components.png"},
    "informacion": {"texto": "…", "diagrama": "../../diagrams/images/data-model.png"},
    "despliegue": {"texto": "…", "diagrama": "../../diagrams/images/deployment-aws.png"},
    "desarrollo": {"texto": "…", "arbol": "solucion/\n├── …"}
  },
  "adrs": [{
    "id": "ADR-001", "titulo": "…", "contexto": "…",
    "alternativas": [
      {"titulo": "…", "descripcion": "…", "ventajas": ["…"], "desventajas": ["…"]},
      {"titulo": "…", "elegida": true, "descripcion": "…", "ventajas": ["…"], "desventajas": ["…"]}
    ],
    "decision": "…", "consecuencias": ["…"],
    "estado": "Aprobado", "fecha": "2026-11-03", "decidio": "…", "evidencia": "…"
  }],
  "tacticas": [["Fiabilidad", "Reintento", "QA-05", "ADR-004"]],
  "trazabilidad": [["QA-05", "Reintento en el registro de pedidos", "Módulo Pedidos", "Componentes"]],
  "validacion": {
    "escenarios": [{"id": "QA-01", "enfoque": "…", "sensibilidad": "…", "prueba": "…"}],
    "riesgos": [{"id": "R-01", "riesgo": "…", "impacto": "…", "mitigacion": "…", "estado": "…"}],
    "temas": ["…"]
  },
  "pendientes": {
    "drivers": [{"id": "QA-03 <nombre corto>", "estado": "Parcialmente abordado", "falta": "<justificación del tablero>"}]
  }
}
```

De dónde sale cada clave:
- `control`: filas anteriores de este mismo archivo, más la nueva (ver "Versión y control del documento" en SKILL.md).
- `drivers`: `drivers.md` §2, sin los elementos retirados; la marca "(primario)" sale del paso 1 vigente (`step-1.md`); `preocupaciones` incluye las nuevas de las iteraciones (columna de `kanban.md`).
- `decisiones`: decisiones vigentes de las iteraciones cerradas (pasos 4 y 5). Sin citar ADR.
- `vistas`: `diagrams/images/` y `development-view.md`. El texto de cada vista resume las responsabilidades de sus elementos (tablas del paso 6 de las iteraciones que la cambiaron).
- `adrs`: los archivos de `adr/` con `Estado: aprobado`, en orden de número; `fecha`, `decidio` y `evidencia` salen de su encabezado.
- `tacticas`: filas [atributo, táctica, escenarios, ADR o "—"] tomadas de las decisiones vigentes nombradas como táctica en las iteraciones cerradas; si no hay, se omite.
- `trazabilidad`: una fila por driver vigente (casos de uso, escenarios, restricciones y preocupaciones): [driver, decisiones, elementos, vistas], tomada de las tablas de los pasos 4 a 6 de las iteraciones cerradas; un driver sin decisión aparece con "—".
- `validacion`: `validation.md`, si está aprobado; si no, se omite.
- `pendientes`: filas de `kanban.md` de la última ronda que no están en "Completamente abordado" ni "Descartado"; si no hay, se omite.
