# Formato de record.json

Referencia de `record`. Leer antes de escribir `document/source/record.json`.

Contenido:
- Reglas generales: rutas de imágenes, textos y claves que no aplican
- Ejemplo completo de `record.json`: portada, caso de negocio, requisitos, rondas (paso 1 e iteraciones con sus pasos 2 a 7), evolución y referencias
- De dónde sale cada clave (al final)

- Las rutas de imágenes son relativas al JSON. Desde `document/source/`: el contexto es `../../diagrams/images/c4-context.png`; las fotos de una iteración, `../../iterations/round-R/it-N/diagrams/images/<vista>.png`.
- Los textos aceptan un string o una lista de párrafos.
- Las claves que no apliquen se omiten.
- El contenido se copia de los archivos tal como quedaron al cierre; no se resume.

```json
{
  "portada": "record-cover.png",
  "control": [["1.0", "2026-11-02", "<autores>", "…"]],
  "introduccion": "Registro de diseño de <sistema> con ADD 3.0 (Cervantes y Kazman, 2024): 1 ronda y 2 iteraciones cerradas. El diseño vigente está en el documento de arquitectura v1.2.",

  "caso_negocio": {
    "contexto": ["<drivers.md §1.1>"],
    "objetivos": ["<objetivo>. Medida: <medida>."],
    "actores": ["<Actor>: <qué hace>."],
    "sistemas_externos": ["<Sistema>: <para qué>."],
    "diagrama": "../../diagrams/images/c4-context.png"
  },

  "requisitos": {
    "diagrama_casos_uso": "../../diagrams/images/use-cases.png",
    "casos_uso": [{"id": "UC-01", "nombre": "Registrar pedido", "descripcion": "…"}],
    "escenarios": [{"id": "QA-01", "atributo": "Desempeño", "escenario": "<frase completa del árbol>", "caso_uso": "UC-02"}],
    "restricciones": [["CON-1", "…"]],
    "preocupaciones": [["CRN-1", "…"]],
    "supuestos": [["AS-1", "…", "<impacto>", "<estado>"]]
  },

  "rondas": [{
    "numero": 1,
    "titulo": "Diseño inicial",
    "motivo": ["<solo desde la ronda 2: qué la abrió y qué drivers cambiaron>"],
    "paso1": {
      "categorias": [
        ["Propósito del diseño", ["Se trata de un sistema nuevo en un dominio conocido. El objetivo es …"]],
        ["Requisitos funcionales principales", ["De los casos de uso de la sección 2.1, se determinó que los principales son:", "UC-01: <razón>", "UC-03: <razón>"]],
        ["Escenarios de atributos de calidad", ["Los escenarios se describieron en la sección 2.2. Su prioridad es la siguiente:"]],
        ["Restricciones", ["…"]],
        ["Preocupaciones arquitectónicas", ["…"]]
      ],
      "prioridades": [["QA-01", "Alta", "Alta"]],
      "prioridades_en": "Escenarios de atributos de calidad",
      "prioridades_nota": "Se eligen como drivers QA-01 y …",
      "criterio": "<criterio de completamente abordado>",
      "hoja_ruta": [["1", "<objetivo>", "<drivers>"]]
    },
    "iteraciones": [{
      "numero": 1,
      "titulo": "<objetivo en pocas palabras>",
      "abierta": "AAAA-MM-DD",
      "cerrada": "AAAA-MM-DD",
      "paso2": {
        "texto": ["<objetivo y tipo>"],
        "drivers": [
          {"grupo": "Funcionalidad primaria", "items": ["UC-01: …"]},
          {"grupo": "Escenarios de calidad", "items": ["QA-01: …"]},
          {"grupo": "Restricciones", "items": ["CON-1: …"]},
          {"grupo": "Preocupaciones arquitectónicas", "items": ["CRN-1: …"]}
        ]
      },
      "paso3": {"texto": ["…"], "diagrama": "../../diagrams/images/c4-context.png"},
      "paso4": {
        "intro": "<frase sobre cómo se eligieron los conceptos>. La siguiente tabla resume las decisiones de diseño.",
        "decisiones": [
          {"decision": "<frase en imperativo, sin negritas>", "fundamentacion": "<prosa con los drivers entre paréntesis>. Ver ADR-00x.", "alternativas": [["<alternativa>", "<motivo>"]]},
          {"decision": "<decisión sin alternativas>", "fundamentacion": "<prosa>", "alternativas": "No se consideraron otras alternativas, ya que <razón>."}
        ]
      },
      "paso5": {
        "intro": "Las decisiones de instanciación tomadas en esta iteración se resumen en la siguiente tabla:",
        "decisiones": [["<decisión corta>", "<razón en prosa con los drivers entre paréntesis>"]],
        "texto": ["Los resultados de estas decisiones de instanciación se registran en el siguiente paso. <sistemas externos, en la iteración de estructura general>"],
        "preocupaciones_nuevas": "CRN-4: … (o \"Ninguna\")"
      },
      "paso6": {
        "secuencias": [{"imagen": "../../iterations/round-1/it-2/diagrams/images/seq-uc-01.png", "titulo": "Secuencia de UC-01"}],
        "interfaces": [{"elemento": "<elemento>", "metodos": [["<operación>", "<descripción>"]]}],
        "texto": ["Vistas que cambiaron: …"],
        "vistas": [{"imagen": "../../iterations/round-1/it-1/diagrams/images/c4-containers.png", "titulo": "Contenedores al cierre de la iteración 1"}],
        "responsabilidades": [["<elemento>", "<responsabilidad>"]],
        "relaciones": [["<A y B>", "<cómo se comunican>"]]
      },
      "paso7": {
        "texto": "<una o dos frases sobre lo que logró la iteración>",
        "tablero": [["", "QA-01", "", "<decisiones que lo movieron>"], ["", "", "UC-01", "…"]],
        "recorrido": "<ruta del recorrido o \"No aplica: el modelo no cambió\">",
        "revision": "<revisión del objetivo>"
      }
    }]
  }],

  "evolucion": {
    "texto": ["<una o dos frases>"],
    "rondas": [["1", "AAAA-MM-DD", "Diseño inicial"]],
    "adrs_reemplazados": [["ADR-003", "Reemplazado", "ADR-007", "AAAA-MM-DD"]]
  },

  "referencias": ["<si se citan otras fuentes además de CK16 y CK24>"]
}
```

De dónde sale cada clave:
- `caso_negocio` y `requisitos`: `drivers.md` §1 y §2. Los elementos retirados se incluyen con "(retirado AAAA-MM-DD)" al final del texto.
- `rondas[].paso1`: `step-1.md` de la ronda (tabla de categorías, tabla de prioridad, criterio, hoja de ruta; desde la ronda 2, su motivo).
- `rondas[].iteraciones`: cada `it-N.md` con `status: cerrada`, en orden; cada clave `pasoN` copia su sección. El tablero tiene cuatro columnas: el ID va en la columna de su estado y la cuarta lleva las decisiones.
- `evolucion`: los `step-1.md` de cada ronda y los ADR de `adr/` con estado "Reemplazado" o "Retirado". No lleva cambios a los requisitos: el avance lo muestra el tablero de cada iteración.
- `referencias`: si se omite, el generador pone CK16 y CK24.
