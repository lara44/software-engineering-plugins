---
name: arch-decisions
description: Usar para la fase 2 del proceso de arquitectura, una vez aprobado drivers.md - registrar con el arquitecto las decisiones de diseño (estilo, módulos, patrones, base de datos, nube, stack y ADRs) ligadas a los drivers que atienden, produciendo decisiones.md según ADD.
---

# Decisiones de arquitectura

Fase 2 del asistente de arquitectura. Parte de `drivers.md` aprobado y produce `decisiones.md`, que alimenta las fases de vistas, validación y documento (secciones 3 y 5 del documento de arquitectura).

**Marco metodológico:** se diseña con ADD. Cada decisión elige un concepto de diseño (estilo, patrón, táctica, tecnología) y declara qué drivers atiende. La tabla de cobertura final es el tablero de drivers de ADD: muestra qué escenario o restricción quedó atendido, parcial o sin atender, y es el punto de partida de la validación con ATAM. Se usa la convención de IDs de ADD: UC-xx, QA-xx, CON-x, AS-x (de drivers.md) y ADR-00x.

## Principios (no negociables)

1. **El arquitecto decide; Claude propone y redacta.** Claude nunca elige una alternativa por su cuenta. Puede recomendar una, con su razón, pero la decisión la toma el arquitecto.
2. **Toda decisión atiende al menos un driver.** Cada decisión termina con una línea "Atiende:" con IDs de casos de uso, escenarios o restricciones (UC, QA, CON). Los supuestos (AS) no se "atienden": se citan en el contexto de la decisión o del ADR. Si el arquitecto toma una decisión que no atiende ningún driver, no se descarta: se registra, se señala en la cobertura como "Sin driver" y se propone reabrir drivers.md (ver "Reabrir los drivers").
3. **ADR solo con alternativas reales.** Un ADR exige al menos 2 alternativas viables. Si una decisión la impone una restricción (CON-x) o no tuvo alternativa real, va en su sección sin ADR.
4. **Respetar lo ya decidido.** Si el arquitecto o los insumos ya fijaron una decisión (estilo, base de datos, nube, stack), se registra tal cual, sin volver a discutirla. Claude solo completa su justificación con los drivers que atiende.
5. **Proponer en vez de preguntar en abierto**, de 2 a 3 preguntas por turno, igual que en la fase de drivers.
6. **Una elección entre alternativas por pregunta.** Si la pregunta define un ADR (elegir entre alternativas), va sola en su turno o claramente separada, para que el arquitecto la evalúe por sí misma. Solo se agrupan confirmaciones simples (por ejemplo, "¿confirmas el stack?"). Si el arquitecto responde "aprobado" a un grupo que incluye una elección de ADR, confirmar esa elección por separado antes de registrarla.
7. **No inventar.** Lo que Claude propone (módulos, alternativas descartadas, ventajas y desventajas, servicios sugeridos) se marca en línea con `[Propuesta]` mientras el archivo está en borrador.
8. **Los huecos se muestran, no se tapan.** Si un driver queda sin decisión que lo atienda, se marca "Parcial" o "Sin atender" en la cobertura y se pregunta; nunca se fuerza una decisión para cerrarlo.

## Paso 0: Revisar qué existe

1. Leer `drivers.md`. Si no existe o no está en `Estado: aprobado`, detenerse y decir que primero hay que cerrar la fase de drivers.
2. Si ya existe `decisiones.md`, retomarlo: revisarlo contra el formato y el criterio de cierre de esta skill y contra el `drivers.md` vigente (si los drivers cambiaron o se renumeraron, actualizar todas las referencias "Atiende:", los ADR y la cobertura). Mostrar en 3–4 líneas qué está completo y qué falta.
3. Revisar "Preguntas abiertas" de drivers.md: las marcadas `(para fase de decisiones)` son el punto de partida de esta fase.
4. Buscar decisiones previas en `insumos/` o en la carpeta del proyecto (borradores de decisiones, notas o historiales de otras conversaciones). Lo que el arquitecto ya decidió en esos documentos se trata como decisión tomada; si contradice algo dicho en esta sesión, mostrar la diferencia y preguntar cuál vale antes de registrar.
5. Preguntar primero qué decisiones ya están tomadas (estilo, base de datos, nube, stack, patrones) para no volver a discutirlas.

## Cómo proponer una decisión no tomada

Cuando el arquitecto no ha decidido algo, Claude no elige: sigue estos pasos.

1. **Identificar los drivers que más pesan en esa decisión:** primero los escenarios (A, A), luego las restricciones (CON), luego el resto.
2. **Proponer 2 o 3 candidatos viables** que respondan a esos drivers.
3. **Compararlos en una tabla corta** candidato × driver, con una marca (✔ / ✘ / parcial) y una frase por celda cuando haga falta.
4. **Recomendar uno, con su razón** en una o dos líneas.
5. **El arquitecto decide.** Su elección se registra como ADR, con las demás alternativas como descartadas.

Reglas adicionales:
- **Decisiones organizacionales no se deducen.** El proveedor de nube, la tecnología que domina el equipo o un convenio de la organización se preguntan. Si son impuestos, se registran como restricción (reabriendo drivers.md); no se justifican con drivers técnicos inventados.
- **Costo.** Si una decisión afecta una restricción de costo, incluir una estimación del costo de operación de cada candidato. Si no se verificó con una fuente (por ejemplo, la calculadora de precios del proveedor), marcarla como "estimación no verificada" y dejarla como riesgo para la validación.

## Reabrir los drivers

Si en esta fase aparece un driver nuevo o hay que cambiar uno (por ejemplo, una decisión sin driver), esta skill **no edita drivers.md directamente**:
1. Explicar en una línea qué cambia en drivers.md y por qué.
2. Cargar la skill `arch-drivers` y hacer el cambio con ella, aplicando su formato y su criterio de cierre (por ejemplo, el máximo de atributos del árbol de utilidad).
3. drivers.md vuelve a `Estado: borrador` hasta que el arquitecto lo apruebe de nuevo; al aprobar se actualiza la fecha.
4. Volver a esta fase y actualizar todas las referencias de decisiones.md a la numeración vigente.

## Cambios posteriores a la aprobación

Cuando decisiones.md ya está aprobado y una fase posterior (vistas, validación, documento) necesita cambiarlo:

1. **Explicar el cambio** en una línea: qué cambia, en qué fase surgió y qué drivers atiende.
2. **Proponer el tipo de cambio**; el arquitecto lo clasifica:
   - **Complementa:** detalla o agrega algo sin contradecir lo decidido (por ejemplo, un servicio de red que el despliegue exige, un ajuste del control de acceso, una táctica que mitiga un riesgo).
   - **Reemplaza:** cambia o revierte una decisión (otro estilo, otra base de datos, otra alternativa en un ADR) o crea un ADR nuevo.
3. **Si complementa:** se edita la sección correspondiente, con su "Atiende:", y se agrega una fila en la tabla "Cambios posteriores a la aprobación". El arquitecto aprueba el cambio de forma explícita. El archivo sigue en `Estado: aprobado`.
4. **Si reemplaza, o si hay duda:** decisiones.md vuelve a `Estado: borrador`, el cambio se hace con esta skill y su criterio de cierre, y el arquitecto lo aprueba de nuevo. Un ADR aprobado no se reescribe: se agrega uno nuevo que lo reemplaza, y el anterior queda marcado "Reemplazado por ADR-00x".
5. En los dos casos, avisar qué vistas o qué partes de la validación quedan por revisar.

## Entrevista: orden de bloques

Cada ronda: 1–2 líneas de lo entendido y 2–3 preguntas con propuesta concreta.

1. **Estilo arquitectónico.** El estilo de despliegue y organización de alto nivel (monolito modular, microservicios, etc.) con su justificación frente a los drivers.
2. **Módulos o servicios.** Claude los propone agrupando los casos de uso por contexto del dominio; cada módulo lista los UC que contiene. Todo UC de drivers.md debe quedar en algún módulo. Identificar el núcleo del dominio y señalarlo.
3. **Patrones.** Uno por subsección, nunca agrupados (por ejemplo, Clean Architecture y DDD son dos patrones). Cada uno dice cómo se usa en este sistema y qué atiende. Incluye el mecanismo de comunicación entre módulos.
4. **Base de datos.** Motor, organización (por ejemplo, esquemas o multi-tenant) y reglas de datos relevantes (por ejemplo, tablas de solo inserción).
5. **Servicios cloud.** Proveedor y servicio → para qué. Si no hay nube, la sección se omite. Lo no definido queda como pendiente, no se inventa.
6. **Stack tecnológico.** Tabla Categoría / Herramientas con lo que indique el arquitecto.
7. **ADRs.** Para cada decisión con alternativas reales: Claude propone las alternativas con ventajas y desventajas frente a los drivers; el arquitecto elige. Si la decisión ya estaba tomada, la alternativa elegida es la del arquitecto y las demás se documentan como descartadas.
8. **Cobertura de drivers.** Claude arma la tabla y presenta los huecos: escenarios o restricciones sin decisión, parciales, o decisiones sin driver. Para cada hueco propone una táctica o decisión, o lo deja como pendiente.
   - **Restricciones normativas (leyes, regulaciones):** revisar obligación por obligación, no solo el tema. Por ejemplo, una ley de protección de datos personales no queda atendida solo con seguridad (cifrado, acceso por rol): también exige autorización del titular, finalidad del tratamiento y atención de consultas y reclamos. Si alguna obligación no tiene decisión, la restricción queda "Parcial".

Prioridad de atención: los escenarios (A, A) del árbol de utilidad deben quedar atendidos antes de cerrar.

## Escritura incremental

Actualizar `decisiones.md` al cerrar cada bloque. Mantener `Estado: borrador` hasta la aprobación.

## Formato de decisiones.md

```markdown
# Decisiones de arquitectura — <Sistema>
Estado: borrador | aprobado · Fecha: AAAA-MM-DD

Parte de: drivers.md (aprobado)

## Estilo arquitectónico: <Nombre del estilo>
<Párrafo: qué es en este sistema y por qué, frente a los drivers.>

Módulos:
- <Módulo>: <responsabilidad> (UC-xx, UC-yy).

Atiende: <IDs>.

## Patrones

### <Patrón 1>
<Cómo se usa en este sistema, en 2–3 líneas.> Ver ADR-00x (si aplica).
Atiende: <IDs>.

## Base de datos
<Motor, organización y reglas de datos.>
Atiende: <IDs>.

## Servicios cloud
Proveedor: <proveedor>.
- <Servicio>: <para qué>.
- <Lo no definido>: pendiente, <con qué criterio se decidirá>.

Atiende: <IDs>.

## Stack tecnológico
| Categoría | Herramientas |
|-----------|--------------|
| Frontend | |
| Backend | |

## ADRs

### ADR-001 — <Título de la decisión>
- **Contexto:** <qué drivers fuerzan esta decisión, citando sus IDs>.
- **Alternativa 1: <Título>**
  - Descripción:
  - Ventajas:
  - Desventajas:
- **Alternativa 2: <Título>** *(elegida)*
  - Descripción:
  - Ventajas:
  - Desventajas:
- **Decisión:** <qué se decidió>.
- **Consecuencias:** <implicaciones, incluidas las que dejan algo pendiente>.

Candidatas a ADR pendientes: <lista>.

## Cobertura de drivers
| Driver | Atendido por | Táctica | Estado |
|--------|--------------|---------|--------|
| QA-01 <nombre corto> | <decisiones, ADR> | <táctica> | Atendido / Parcial: <qué falta> / Sin atender |
| CON-1 <nombre corto> | | | |
| Sin driver: <decisión> | <decisión> | | Falta el driver en drivers.md |

## Cambios posteriores a la aprobación
| Fecha | Cambio | Tipo | Origen | Atiende |
|-------|--------|------|--------|---------|
| AAAA-MM-DD | <qué cambió y en qué sección> | Complementa | <fase o vista donde surgió> | <IDs> |
```

Reglas del formato:
- Secciones en el orden del documento de arquitectura: estilo (3.1), patrones (3.2), base de datos (3.3), servicios cloud (3.4), stack (3.5) y ADRs (5). La cobertura no va al documento; la usa la fase de validación.
- El título del estilo usa dos puntos: "Estilo arquitectónico: Monolito Modular".
- Un patrón por subsección, nunca agrupados.
- Toda decisión termina con "Atiende:" y solo cita IDs de UC, QA o CON que existen en drivers.md. Los supuestos (AS) no van en "Atiende:".
- ADRs con mínimo 2 alternativas, cada una con descripción, ventajas y desventajas; la elegida marcada *(elegida)*. Campos en este orden: Contexto, Alternativas, Decisión, Consecuencias.
- La cobertura lista todos los QA y todas las CON de drivers.md, más las decisiones sin driver.
- Solo `[Propuesta]` como marca, en línea, mientras el archivo está en borrador.
- La tabla "Cambios posteriores a la aprobación" solo aparece cuando hay cambios; no va al documento, pero se usa para el control de versiones del documento.

## Criterio de cierre

Antes de pedir aprobación, verificar:
- [ ] drivers.md está aprobado y todas las referencias corresponden a su numeración vigente.
- [ ] Estilo, módulos, patrones, base de datos, nube (si aplica) y stack definidos.
- [ ] Todo caso de uso de drivers.md está asignado a un módulo.
- [ ] Cada decisión tiene su línea "Atiende:".
- [ ] Cada ADR tiene al menos 2 alternativas reales y la elegida fue decidida por el arquitecto en una pregunta propia.
- [ ] Las decisiones que afectan el costo tienen estimación (verificada o marcada como no verificada).
- [ ] Las restricciones normativas se revisaron obligación por obligación.
- [ ] Si se reabrió drivers.md, se hizo con su skill y quedó aprobado de nuevo.
- [ ] La cobertura incluye todos los QA y todas las CON.
- [ ] Los escenarios (A, A) están atendidos.
- [ ] Los huecos restantes (parciales, sin atender, sin driver) fueron mostrados al arquitecto y aceptados como pendientes.
- [ ] Todos los elementos `[Propuesta]` fueron mostrados al arquitecto.

Si algo falla, decirlo en una línea y preguntar si se resuelve ahora o queda pendiente.

## Cierre

1. Mostrar un resumen de 5–8 líneas: estilo, módulos, patrones principales, ADRs y estado de la cobertura (cuántos drivers atendidos, parciales y sin atender).
2. Pedir aprobación explícita.
3. Con la aprobación: quitar las marcas `[Propuesta]` de lo aceptado, sacar lo no aceptado, cambiar a `Estado: aprobado` y poner la fecha.
4. Si quedaron decisiones sin driver, recordar que hay que reabrir drivers.md para agregarlos.
5. Indicar que la siguiente fase es la de vistas (skill `arch-views`), que parte de drivers.md y decisiones.md. Los huecos de la cobertura son riesgos candidatos para la fase de validación.
