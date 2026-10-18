---
name: "arch-database-diagram-style"
description: "Usar para crear o actualizar un diagrama de modelo de datos (esquemas, «Context», entidades, enumeraciones y relaciones con cardinalidad) como archivo .drawio editable, con el estilo de referencia del arquitecto. No aplica a diagramas C4 ni a despliegue AWS."
---

# Estilo de diagramas de modelo de datos (draw.io)

Genera diagramas de modelo de datos (conceptual o lógico) como `.drawio` editables, con el estilo del diagrama de referencia del arquitecto: esquemas, agrupaciones «Context», entidades, entidades débiles, enumeraciones, notas amarillas y relaciones con cardinalidad.

El estilo se reconstruyó a partir de una captura de pantalla (no de un `.drawio` real como en C4 y AWS), usando formas nativas de draw.io, así que el riesgo de "forma no encontrada" es bajo. **Lo único sin confirmar son los símbolos de cardinalidad:** se usan los marcadores ER estándar de draw.io como mejor aproximación. Si el arquitecto reporta una diferencia, pedirle el `.drawio` real, comparar y proponer el cambio al script del plugin.

Para diagramas C4 usar `arch-c4-diagram-style`; para despliegue AWS, `arch-aws-diagram-style`.

## Generador

El generador está en `scripts/db_drawio.py`, dentro de la carpeta de esta skill. Se ejecuta tal cual; no se lee, no se copia y no se reescribe:

```bash
python3 <carpeta-de-esta-skill>/scripts/db_drawio.py spec.json salida.drawio
```

Ya trae los estilos y dos correcciones verificadas con el arquitecto: el nombre de cada entidad lleva el color blanco fijado en su propio texto (si no, draw.io lo muestra gris), y el ancho de la pestaña «Context» se calcula sobre el texto completo `«Context» Nombre` (si no, se recorta). Las etiquetas de las relaciones llevan fondo blanco para que la línea no las tache. **No se modifica por proyecto:** lo que falte se propone como cambio al script del plugin.

## Elementos

- **Encabezado** (`header`): texto suelto arriba a la izquierda, sin borde: título en negrita, subtítulo entre corchetes en cursiva gris (p. ej. "[Conceptual Model Diagram]"), "Descripción: …" y una línea de metadatos ("Vista: … | Modelo: … | Versión: … | Fecha: …").
- **Esquema** (`schema`): caja exterior con el mismo estilo que un Context (fondo blanco, borde gris continuo, pestaña negra con texto blanco), pero con `«Schema» nombre (nota)` en la pestaña; por ejemplo `«Schema» banco_<id> (uno por banco)`. Representa un esquema físico de la base. Es contenedor: los Context van adentro.
- **Agrupación «Context»** (`context`): rectángulo blanco de borde gris fino que agrupa entidades de un mismo tema, con una pestaña negra en la esquina superior izquierda que dice `«Context» Nombre`. Es contenedor: sus hijos usan coordenadas relativas.
- **Entidad / entidad débil** (`entity`, con `weak: true` para la débil): caja de dos partes. Arriba, tira negra con `«Entity»` o `«WeakEntity»` y el nombre en blanco y negrita. Abajo, un atributo por línea con `+ Nombre: Tipo`; las claves (primaria, o la compuesta de una entidad débil) van subrayadas.
- **Enumeración** (`enum`): misma caja con `«Enumeration»`; cuerpo con `+ NOMBRE = "Valor"`.
- **Nota** (`note`): post-it amarillo con esquina doblada y texto negro a la izquierda, para aclaraciones (convenciones, valores de ejemplo, campos calculados). Va cerca de la entidad a la que aplica, sin flecha.
- **Relación** (`edges`): línea ortogonal gris con una etiqueta corta del rol ("clasifica", "se fracciona en") y marcadores de cardinalidad en cada extremo.

## Reglas

1. **Esquema y Context son dos dimensiones distintas, y se dibujan las dos:**
   - **Esquema** = dónde viven los datos (decisión física: base de datos, multitenant). Sale de la sección de base de datos de `decisions.md`.
   - **«Context»** = a qué módulo o bounded context pertenece cada tabla (decisión lógica). Sale de los módulos de `decisions.md`.

   Si `decisions.md` define esquemas (por ejemplo, uno compartido `seguridad` y uno por banco), cada esquema es una caja `schema` exterior y los Context de sus módulos van adentro, con `parent` = el id del esquema. Las relaciones que cruzan esquemas se conservan (por ejemplo, `Banco` → "tiene su esquema" → el esquema del banco). Nunca reemplazar los esquemas por los Context ni al revés. Si no hay esquemas definidos, los Context van directo en la página.
2. **Agrupar por Context.** Cada módulo es un `context`; lo que le pertenece lleva `parent` = el id de ese context.
3. **Entidades dimensionadas por contenido,** nunca con tamaños redondos arbitrarios:
   - alto = tira del encabezado (`start_size`, 34) + 18–20 px por atributo + margen;
   - ancho = lo que necesita el atributo `Nombre: Tipo` más largo (≈ 8–9 px por carácter), con un mínimo de 160–200 px.
4. **Context y esquema dimensionados por contenido:** borde del hijo más lejano + 30–40 px (el esquema, además, deja ~40 px arriba para su pestaña y la del primer Context). El ancho de las pestañas lo calcula el script.
5. **Toda relación lleva etiqueta de rol y cardinalidad** en los dos extremos.
6. **Flechas que comparten entidad** salen o entran por puntos distintos (`exit`/`entry`), y la etiqueta se mueve con `label_offset` si cae sobre otro texto. Usar `points` solo si el render muestra un cruce.

## Formato del spec.json

```json
{
  "title": "Nombre del diagrama",
  "page": [1400, 900],
  "elements": [
    {"id": "hdr", "kind": "header", "x": 20, "y": 10, "w": 700, "h": 90,
     "title": "Diagrama de Modelo de Datos Conceptual de X",
     "subtitle": "Conceptual Model Diagram",
     "description": "Descripción corta del diagrama.",
     "meta": "Vista: Información | Modelo: Datos Conceptual | Versión: 1.0 | Fecha: 2026-09-20"},
    {"id": "sch1", "kind": "schema", "name": "banco_<id>", "note": "uno por banco", "x": 20, "y": 120, "w": 680, "h": 480, "parent": "1"},
    {"id": "ctx1", "kind": "context", "name": "NombreDelContexto", "x": 20, "y": 40, "w": 620, "h": 420, "parent": "sch1"},
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
     "values": [{"name": "ACTIVO", "value": "0"}, {"name": "INACTIVO", "value": "1"}]},
    {"id": "nota1", "kind": "note", "x": 340, "y": 180, "w": 220, "h": 100, "parent": "ctx1",
     "text": "Texto de la nota aclaratoria."}
  ],
  "edges": [
    {"from": "entidad1", "to": "entidad_debil1", "parent": "1", "label": "Zonas Proyecto",
     "start": "mandatory_one", "end": "zero_or_many", "exit": [1, 0.3], "entry": [0, 0.5]}
  ]
}
```

- `parent`: id del contenedor que lo envuelve (`context` o `schema`), o `"1"`. Las coordenadas son relativas al padre (absolutas solo con `"1"`).
- `schema.note`: texto opcional entre paréntesis en la pestaña ("compartido", "uno por banco").
- `start`/`end`: `one | mandatory_one | zero_or_one | many | one_or_many | zero_or_many | none` (marcadores `ERone`, `ERmandOne`, `ERzeroToOne`, `ERmany`, `ERoneToMany`, `ERzeroToMany`).
- En flechas, opcionales: `exit`/`entry` (`[x, y]` de 0 a 1), `points` (absolutos) y `label_offset` (`[a, o]`: `a` de -1 a 1 con 0 = punto medio; `o` = desplazamiento perpendicular en px).

## Flujo de trabajo

1. Reunir el contenido: esquemas (si los hay), módulos, entidades fuertes y débiles con sus atributos y claves, enumeraciones con sus valores, relaciones (rol y cardinalidad) y notas.
2. Armar la jerarquía esquema → Context → entidades y dimensionar todo por contenido, de adentro hacia afuera.
3. Escribir el `spec.json` y generar con `scripts/db_drawio.py`.
4. Renderizar a PNG y mirarlo (draw.io Desktop: `drawio -x -f png -o salida.png salida.drawio`; en Mac, si `drawio` no está en el PATH, `/Applications/draw.io.app/Contents/MacOS/draw.io`). Corregir y repetir hasta que no haya texto cortado, etiquetas encimadas ni flechas que atraviesen cajas. Si no se puede renderizar, decirlo y entregar como "sin verificación visual".
5. Entregar el `.drawio`, recordando que los símbolos de cardinalidad son una aproximación. Si el diagrama cambia el modelo (una clave, una entidad o una enumeración nueva), decirlo aparte: es una decisión del arquitecto, no de estilo.

## Verificación antes de entregar

- [ ] Todo `parent` y toda flecha apuntan a IDs que existen (parsear con `xml.etree.ElementTree`).
- [ ] Si `decisions.md` define esquemas, cada uno es una caja `schema` con sus Context adentro, y las relaciones entre esquemas siguen dibujadas.
- [ ] Entidades, enumeraciones, contexts y esquemas dimensionados por contenido.
- [ ] Entidades débiles con `«WeakEntity»` y su clave compuesta subrayada.
- [ ] Toda relación con etiqueta de rol y cardinalidad en los dos extremos.
- [ ] En el render: nombres de entidad en blanco, pestañas «Context» sin texto cortado, ningún atributo recortado, ninguna etiqueta encimada.
