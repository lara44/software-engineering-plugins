---
name: architecture-decisions
description: Usar para la fase 2 del proceso de arquitectura, una vez aprobado drivers.md - registrar con el arquitecto las decisiones de diseño (estilo, módulos, patrones, base de datos, nube, stack y ADRs) ligadas a los drivers que atienden, produciendo decisiones.md según ADD.
---

# Decisiones de arquitectura

Fase 2 del asistente de arquitectura. Parte de `drivers.md` aprobado y produce `decisiones.md`, que alimenta las fases de vistas, validación y documento (secciones 3 y 5 del documento de arquitectura).

**Marco metodológico:** se diseña con ADD. Cada decisión elige un concepto de diseño (estilo, patrón, táctica, tecnología) y declara qué drivers atiende. La tabla de cobertura final es el tablero de drivers de ADD: muestra qué escenario o restricción quedó atendido, parcial o sin atender, y es el punto de partida de la validación con ATAM. Se usa la convención de IDs de ADD: UC-xx, QA-xx, CON-x, AS-x (de drivers.md) y ADR-00x.

## Principios (no negociables)

1. **El arquitecto decide; Claude propone y redacta.** Claude nunca elige una alternativa por su cuenta. Puede recomendar una, con su razón, pero la decisión la toma el arquitecto.
2. **Toda decisión atiende al menos un driver.** Cada decisión termina con una línea "Atiende:" con IDs de drivers.md. Si el arquitecto toma una decisión que no atiende ningún driver, no se descarta: se registra y se señala en la cobertura como "Sin driver", y se propone reabrir drivers.md para agregar el driver que la justifica.
3. **ADR solo con alternativas reales.** Un ADR exige al menos 2 alternativas viables. Si una decisión la impone una restricción (CON-x) o no tuvo alternativa real, va en su sección sin ADR.
4. **Respetar lo ya decidido.** Si el arquitecto o los insumos ya fijaron una decisión (estilo, base de datos, nube, stack), se registra tal cual, sin volver a discutirla. Claude solo completa su justificación con los drivers que atiende.
5. **Proponer en vez de preguntar en abierto**, de 2 a 3 preguntas por turno, igual que en la fase de drivers.
6. **No inventar.** Lo que Claude propone (módulos, alternativas descartadas, ventajas y desventajas, servicios sugeridos) se marca en línea con `[Propuesta]` mientras el archivo está en borrador.
7. **Los huecos se muestran, no se tapan.** Si un driver queda sin decisión que lo atienda, se marca "Parcial" o "Sin atender" en la cobertura y se pregunta; nunca se fuerza una decisión para cerrarlo.

## Paso 0: Revisar qué existe

1. Leer `drivers.md`. Si no existe o no está en `Estado: aprobado`, detenerse y decir que primero hay que cerrar la fase de drivers.
2. Si ya existe `decisiones.md`, retomarlo: revisarlo contra el formato y el criterio de cierre de esta skill y contra el `drivers.md` vigente (si los drivers cambiaron o se renumeraron, actualizar todas las referencias "Atiende:", los ADR y la cobertura). Mostrar en 3–4 líneas qué está completo y qué falta.
3. Revisar "Preguntas abiertas" de drivers.md: las marcadas `(para fase de decisiones)` son el punto de partida de esta fase.
4. Preguntar primero qué decisiones ya están tomadas (estilo, base de datos, nube, stack, patrones) para no volver a discutirlas.

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
```

Reglas del formato:
- Secciones en el orden del documento de arquitectura: estilo (3.1), patrones (3.2), base de datos (3.3), servicios cloud (3.4), stack (3.5) y ADRs (5). La cobertura no va al documento; la usa la fase de validación.
- El título del estilo usa dos puntos: "Estilo arquitectónico: Monolito Modular".
- Un patrón por subsección, nunca agrupados.
- Toda decisión termina con "Atiende:" y solo cita IDs que existen en drivers.md.
- ADRs con mínimo 2 alternativas, cada una con descripción, ventajas y desventajas; la elegida marcada *(elegida)*. Campos en este orden: Contexto, Alternativas, Decisión, Consecuencias.
- La cobertura lista todos los QA y todas las CON de drivers.md, más las decisiones sin driver.
- Solo `[Propuesta]` como marca, en línea, mientras el archivo está en borrador.

## Criterio de cierre

Antes de pedir aprobación, verificar:
- [ ] drivers.md está aprobado y todas las referencias corresponden a su numeración vigente.
- [ ] Estilo, módulos, patrones, base de datos, nube (si aplica) y stack definidos.
- [ ] Todo caso de uso de drivers.md está asignado a un módulo.
- [ ] Cada decisión tiene su línea "Atiende:".
- [ ] Cada ADR tiene al menos 2 alternativas reales y la elegida fue decidida por el arquitecto.
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
5. Indicar que la siguiente fase es la de vistas, que parte de drivers.md y decisiones.md. Los huecos de la cobertura son riesgos candidatos para la fase de validación.
