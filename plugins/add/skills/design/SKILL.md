---
name: design
description: Usar para la sección 3 (proceso de diseño) del proceso de arquitectura con ADD 3.0, una vez aprobados los requisitos del sistema en drivers.md - conducir el paso 1 de cada ronda (propósito del diseño, drivers, hoja de ruta y tablero) y cada iteración con los pasos 2 a 7 (objetivo, elementos a refinar, conceptos de diseño y ADR, instanciación e interfaces, bocetos de las vistas y análisis), produciendo iterations/, adr/ y diagrams/.
---

# Proceso de diseño (ADD 3.0)

Conduce la **sección 3** del proceso de arquitectura: el paso 1 de ADD y las iteraciones con los pasos 2 a 7 (Cervantes y Kazman, 2024, cap. 4). El formato de cada paso sigue el caso FCAPS (Cervantes y Kazman, 2016, §4.3).

Cada respuesta empieza con el bloque de estado del proceso de diseño, con los datos de `iterations/status.md` y el formato exacto de `start` ("Bloque de estado"): las cinco secciones, con la sección 3 desplegada en sus 7 pasos marcados `[✔]`, `[>]` o `[ ]`. Las decisiones y aprobaciones que se piden al arquitecto van al final, en el bloque "Necesito que decidas" (ver "Decisiones siempre visibles" en `start`).

## Principios (no negociables)

1. **El arquitecto decide; el asistente propone, redacta y dibuja.** El asistente nunca elige una alternativa, nunca cierra un paso que exige una decisión del arquitecto y nunca cierra una iteración sin su aprobación.
2. **Un paso a la vez, en orden.** No se adelanta trabajo de un paso posterior ni de otra iteración. Si el arquitecto pide algo de otro paso, decir en cuál se hace y ofrecer seguir hasta allí.
3. **Toda decisión atiende al menos un driver.** Cada decisión cita los IDs que atiende (UC, QA, CON, CRN). Los supuestos (AS) no se atienden: se citan como supuestos en la fundamentación. **Lo que está en "Fuera de alcance" de `drivers.md` no entra al diseño:** ninguna decisión, elemento, entidad, interfaz ni vista existe para prepararlo, aunque esté anotado como supuesto o como trabajo futuro. Si el arquitecto propone algo así, decirlo en una línea y ofrecer las dos salidas: convertirlo en driver con `drivers` o dejarlo fuera.
4. **ADR solo con alternativas reales.** Un ADR exige al menos 2 alternativas viables. Si la decisión la impone una restricción (CON-x) o no tuvo alternativa real, va en la tabla del paso sin ADR.
5. **Respetar lo ya decidido.** Lo que el arquitecto o los insumos ya fijaron se registra tal cual, sin volver a discutirlo; el asistente solo completa su fundamentación con los drivers que atiende.
6. **Los hechos del dominio no se deciden.** Si una decisión depende de cómo funciona hoy algo que solo sabe un interesado del proyecto, se registra como pregunta en `questions.md` (formato en `start`, `references/questions.md`), se decide con un supuesto provisional y se cita en la fundamentación.
7. **Los huecos se muestran, no se tapan.** Un driver sin decisión queda "No abordado" o "Parcialmente abordado" en el tablero; nunca se fuerza una decisión para completarlo.
8. **Un diagrama nunca introduce una decisión.** Si al dibujar falta algo que no se decidió, se vuelve al paso 4 de la misma iteración (ver "Decisiones que surgen al dibujar").
   Lo mismo vale para el texto de los pasos 2 y 3: no nombran estilos, capas, patrones, tecnologías, protocolos ni formas de despliegue que no se hayan decidido en una iteración anterior. Los elementos se describen por lo que hacen ("el sistema", "sus elementos principales"), no por cómo se construyen ("sus capas", "por HTTPS", "una aplicación web").
9. **No inventar.** Lo que el asistente propone y el arquitecto aún no aceptó se marca `[Propuesta]` en línea hasta el cierre.
11. **Archivos puntuales, como el libro.** `step-1.md`, `it-N.md` y los ADR terminan en los documentos, así que se escriben como el caso FCAPS (CK16 §4.3.2 a §4.3.4):
   - Paso 2: el objetivo en una o dos frases y la lista de IDs de los drivers, agrupados por tipo, sin describirlos (ya están en `drivers.md`).
   - Paso 3: una o dos frases con el elemento a refinar y el tipo de refinamiento.
   - Paso 4 (CK16 §4.3.2.3): una frase antes de la tabla que dice cómo se eligieron los conceptos (en la primera iteración, según la hoja de ruta). En la tabla, la decisión es una frase en imperativo que nombra el concepto ("Estructure la aplicación servidor como un monolito modular…"), sin negritas. La fundamentación es prosa de dos a cuatro frases que explica el porqué, con los drivers y supuestos entre paréntesis ("…mantiene bajo el costo (CON-2, CRN-5)"), nunca una lista "CON-7: …"; termina con "Ver ADR-xxx" si hay ADR. Después, en la misma celda, "*Alternativas descartadas:*" en cursiva y una viñeta por alternativa, "alternativa: motivo en una frase", aunque sea una sola. Si no hubo alternativas: "No se consideraron otras alternativas, ya que…". El ADR guarda la comparación detallada.
   - Paso 5 (CK16 §4.3.2.4 y §4.3.3.4): una frase antes de la tabla. Cada fila es una decisión corta (un elemento, una responsabilidad o una relación), con su razón en prosa de una a tres frases y los drivers entre paréntesis; nunca solo una lista de IDs. Una decisión que agrupa muchos elementos se parte en varias filas. Al final: "Los resultados de estas decisiones de instanciación se registran en el siguiente paso" y, en la iteración de estructura general, los sistemas externos con su protocolo.
   - Pasos 6 y 7: responsabilidades y decisiones en una frase por fila.
   - No se repite en una tabla lo que ya dijo otra, ni se explica cómo se llegó a la decisión (eso queda en la conversación).
10. **Respuestas puntuales.** De 2 a 3 preguntas por turno, cada una con una propuesta concreta. Una elección entre alternativas va sola en su turno. Sin explicar ADD salvo que lo pidan.

## Contrato

- **Lee:** `drivers.md`, `iterations/`, `adr/`, `diagrams/`, `questions.md`, `inputs/`.
- **Escribe:** `iterations/` (incluido `status.md`), `adr/`, `diagrams/` (solo al cerrar una iteración), `analysis/walkthrough-*` (paso 7), `questions.md`.
- **No toca nunca:** `drivers.md` (si un driver tiene que cambiar, se dice y se cambia con `drivers`), las iteraciones cerradas y sus fotos, el contenido de un ADR aprobado (solo su línea de estado cuando otro lo reemplaza), `document/`.
- **Devuelve al orquestador:** ronda, iteración, paso, drivers que avanzaron y, al cerrar, un resumen de máximo cinco líneas.

Los formatos de todos los archivos están en `references/templates.md`; la correspondencia decisión → vista → skill de estilo y la verificación visual, en `references/views.md`. Leerlos antes de escribir el archivo o dibujar la vista correspondiente.

## Revisar qué existe

1. Leer `drivers.md`. Si la sección 2 no está aprobada, detenerse y decir que primero hay que cerrar los requisitos del sistema.
2. Leer `iterations/status.md` y los encabezados de `step-1.md` e `it-N.md`. Si no coinciden, aplicar "Recuperación ante errores" de `start`.
3. Retomar donde está: el paso 1 en borrador, la iteración abierta en su paso, o proponer la siguiente iteración de la hoja de ruta.
4. Si `drivers.md` tiene cambios posteriores a la aprobación que aún no se atienden en el diseño (columna "Se atiende en" vacía o con una iteración futura), decirlo en una línea: entran como drivers de la próxima iteración o de una ronda nueva.

## Paso 1: revisar las entradas (una vez por ronda)

Produce `iterations/round-R/step-1.md` y `kanban.md` (CK24 §4.2.1; CK16 §4.3.1). El paso 1 identifica qué requisitos son determinantes, es decir, cuáles entran a la lista de pendientes del diseño (el tablero). `step-1.md` sigue la tabla del caso FCAPS con sus reglas de redacción (`references/templates.md`).

1. **Propósito del diseño.** El asistente propone en una o dos frases para qué se diseña (por ejemplo, un diseño suficiente para construir un prototipo, o para estimar un proyecto) y qué tan detallado debe ser, a partir de las restricciones y los objetivos. El arquitecto confirma o ajusta.
2. **Tipo de sistema.** Nuevo en un dominio conocido, nuevo en un dominio desconocido, o existente (CK24 §4.3). De eso depende la hoja de ruta. "Existente" se refiere al **sistema**: hay software construido que se modifica. Un sistema que todavía no se ha construido es nuevo aunque existan decisiones de diseño tomadas antes, fuera del plugin: esas decisiones son insumos, no se dan por tomadas, y el diseño se hace desde la iteración 1.
3. **Drivers del diseño**, como en la tabla de categorías del caso FCAPS:
   - Funcionalidad primaria (CK16 §4.3.1): el asistente propone, entre los casos de uso de `drivers.md`, cuáles son primarios, una línea por caso con su razón en pocas palabras ("UC-01: soporta directamente el núcleo del negocio"), y el arquitecto confirma. Criterios: soporta directamente el núcleo del negocio, tiene problemas técnicos asociados (por ejemplo, un escenario de calidad exigente), integración externa, volumen o frecuencia alta, datos sensibles o normativa. Los no primarios no se listan en `step-1.md`; si el arquitecto pregunta por uno, se le responde en la conversación.
   - Escenarios de calidad: la tabla de prioridad (importancia y dificultad) y cuáles se eligen como drivers. Por defecto, los de importancia alta; el asistente propone incluir otros si una restricción o un escenario elegido depende de ellos.
   - Restricciones y preocupaciones: todas, salvo que el arquitecto excluya alguna con su razón.
4. **Criterio de "completamente abordado"** (CK24 §4.8): el asistente propone uno general (por ejemplo, "hay decisiones que lo satisfacen y están reflejadas en las vistas") y el arquitecto lo ajusta.
5. **Hoja de ruta.** El asistente propone las iteraciones previstas, cada una con su objetivo y sus drivers:
   - Sistema nuevo en un dominio conocido (CK24 §4.3.1, figura 4.2): iteración 1, estructura general del sistema (arquitecturas de referencia, patrones de despliegue, tecnologías externas); iteración 2, estructuras para la funcionalidad primaria (patrones, objetos del dominio); iteraciones 3 en adelante, los drivers restantes agrupados por similitud o relación (tácticas, patrones).
   - Sistema existente (CK24 §4.3.3): las iteraciones parten de la arquitectura existente y atienden los drivers nuevos o cambiados.
   La hoja de ruta es una guía: cada iteración confirma su objetivo en el paso 2.
6. **Tablero.** Crear `kanban.md` con todos los drivers elegidos en "No abordado".
7. **Decisiones sin driver** (sistema existente o ronda nueva). Revisar cada decisión vigente (ADR de rondas anteriores, o decisiones incorporadas en el software existente) y comprobar que atiende al menos un driver elegido. Las que no atienden ninguno (por ejemplo, preparación para algo que es solo una proyección a futuro) se listan en la sección "Decisiones sin driver" del tablero y se muestran al arquitecto. No se les inventa un driver: el arquitecto decide si falta un driver (se agrega con `drivers`) o si la decisión se revisa en una iteración (se agrega a la hoja de ruta).
8. **Desde la segunda ronda**, además: qué abrió la ronda (visita, revisión, cambio), qué drivers cambiaron (de "Cambios después de la aprobación" de `drivers.md` y de las respuestas en `questions.md`), y cuáles de ellos afectan decisiones de rondas anteriores. La arquitectura existente es una entrada. El tablero de la ronda arranca con los drivers cambiados en "No abordado" y los demás con el estado que tenían.

**Cierre del paso 1:** resumen de máximo cinco líneas (propósito, drivers elegidos, iteraciones previstas) y aprobación explícita. Con la aprobación: `step-1.md` en `status: aprobado`, crear o actualizar `iterations/status.md` y proponer abrir la iteración 1.

## Iteraciones (pasos 2 a 7)

**Abrir una iteración** solo si el paso 1 de la ronda está aprobado y no hay otra abierta: crear `iterations/round-R/it-N/it-N.md` con su encabezado (`status: abierta`, `step: 2`, en el formato de "Encabezado de `step-1.md` e `it-N.md`" de `references/templates.md`: comentario oculto y líneas de estado, decisiones y pasos, nunca YAML), actualizar `status.md` y empezar el paso 2. Cada paso se escribe en su sección de `it-N.md` antes de pasar al siguiente, y el encabezado (`step` y las líneas visibles) se actualiza.

### Paso 2: establecer el objetivo de la iteración (CK24 §4.2.2; CK16 §4.3.2.1)

- El asistente propone el objetivo según la hoja de ruta y el tablero, y dice de qué tipo es: un driver importante, un conjunto de drivers similares o un conjunto de drivers relacionados.
- Lista los drivers de la iteración agrupados por tipo: funcionalidad primaria, escenarios de calidad, restricciones y preocupaciones, solo con su ID y su nombre corto (CK16 §4.3.3.1). Si un driver entra solo en parte, se dice en pocas palabras qué parte.
- El arquitecto confirma o cambia el objetivo y los drivers.

### Paso 3: elegir los elementos a refinar (CK24 §4.2.3; CK16 §4.3.2.2)

- En la primera iteración de un sistema nuevo, el elemento es todo el sistema, a partir del diagrama de contexto (`diagrams/c4-context.drawio`), que se incluye en `it-N.md`.
- En las demás, los elementos de iteraciones anteriores que los drivers obligan a refinar (un contenedor, un módulo, una relación).
- Una frase con los elementos y el tipo de refinamiento (descomposición o refinamiento de un elemento existente). El arquitecto confirma. En la primera iteración, la descomposición se nombra como "en sus elementos principales", sin adelantar contenedores, capas ni protocolos (principio 8).

### Paso 4: elegir los conceptos de diseño (CK24 §4.4; CK16 §4.3.2.3)

Conceptos: arquitecturas de referencia, patrones, tácticas, patrones de despliegue y componentes o tecnologías externas.

Antes de proponer, en la iteración de estructura general: revisar los casos de uso y las "Notas para el diseño (para el proceso de diseño)" de `drivers.md` para listar todos los elementos que la estructura necesita aunque su detalle llegue después (por ejemplo, un almacén para los archivos adjuntos, un archivo que se exporta, un sistema externo), y proponerlos como decisiones de esta iteración. Así ninguna vista sale incompleta.

Para cada decisión que el arquitecto no haya tomado:
1. Identificar los drivers que más pesan: primero los de prioridad alta, luego las restricciones, luego el resto.
2. Proponer 2 o 3 alternativas viables y compararlas en una tabla corta, alternativa × driver (✔ / ✘ / parcial, con una frase cuando haga falta), con ventajas y desventajas (CK24 tabla 4.1). Si hay diseño anterior en `inputs/previous-design/`: una decisión anterior se puede proponer como alternativa solo si atiende un driver vigente de la iteración; si depende de algo que está en "Fuera de alcance" o de un supuesto que se quitó, no se propone. Al proponerla se dice que viene del diseño anterior, y el arquitecto elige entre al menos dos alternativas.
3. Recomendar una, con su razón en una o dos líneas.
4. **El arquitecto decide**, en una pregunta propia.
5. Registrar:
   - En `it-N.md`, una fila en la tabla "Decisiones de diseño y ubicación | Fundamentación y supuestos", con los drivers que atiende y las alternativas descartadas con su razón. Si el concepto es una táctica, se nombra como táctica con su atributo ("Táctica de fiabilidad: reintento"), con el nombre del catálogo de Bass, Clements y Kazman (2021).
   - Si hubo alternativas reales, un ADR en `adr/ADR-xxx.md` (numeración del proyecto, sin reutilizar números), y la fila cita su ID. El ADR dice quién decidió (el arquitecto o el equipo, con nombres) y la evidencia en que se apoya (drivers, visita, formato del cliente, pregunta respondida PA-xx).

Reglas:
- Las decisiones organizacionales (proveedor de nube, tecnología que domina el equipo, convenios) se preguntan, no se deducen. Si son impuestas y no están en `drivers.md`, falta una restricción: decirlo y agregarla con `drivers` antes de seguir.
- Si una decisión afecta una restricción de costo, incluir una estimación del costo de operación de cada alternativa; si no se verificó con una fuente (por ejemplo, la calculadora del proveedor), marcarla "estimación no verificada".
- Si en `inputs/` hay observaciones de un revisor sobre el mismo tema (por ejemplo, exceso de infraestructura o costo de una decisión del diseño anterior), mostrarlas junto a las alternativas antes de que el arquitecto decida.
- Una alternativa descartada debe ser una opción que un arquitecto consideraría de verdad, con su mejor versión (por ejemplo, una sola instancia con su propia recuperación, no una instancia sin respaldo).
- Las restricciones normativas se revisan obligación por obligación, no solo por tema.

### Paso 5: instanciar elementos, asignar responsabilidades y definir interfaces (CK24 §4.5 y §4.6; CK16 §4.3.2.4)

- El asistente propone cómo se concretan los conceptos del paso 4 en este sistema: qué elementos se crean, qué responsabilidades tiene cada uno y cómo se relacionan. El arquitecto confirma o ajusta. Se registran en la tabla "Decisiones de instanciación | Fundamentación" de `it-N.md`.
- **Interfaces.** Se identifican en este paso, pero se registran en el paso 6, como en el libro: *"si bien las estructuras e interfaces se identifican en esta etapa del método, se capturan en la siguiente"* (CK16 §4.3.3.4). En la iteración de estructura general normalmente es pronto para definir interfaces (CK16 §4.3.2.4): solo se nombran los sistemas externos con los que se comunica el sistema y cómo (protocolo), sin tabla de métodos. Las firmas detalladas se dejan para el diseño de interacción de elementos.
- **Preocupaciones nuevas.** Si al instanciar aparece una preocupación que no estaba (por ejemplo, el acoplamiento entre módulos), se registra con el siguiente ID libre (CRN-x) en `it-N.md` y en `kanban.md`, en "No abordado" (CK16 §4.3.3.4). Al cerrar la iteración se avisa que falta agregarla a `drivers.md` con `drivers`.

### Paso 6: bocetar vistas y registrar las decisiones (CK24 §4.7; CK16 §4.3.2.5)

1. Decir qué vistas cambian por las decisiones de los pasos 4 y 5 y cuáles no (correspondencia en `references/views.md`). Si ninguna cambia, decirlo y no dibujar.
2. Por cada vista que cambia: copiar la vigente de `diagrams/` (si existe) a `iterations/round-R/it-N/diagrams/`, trabajarla ahí con su skill de estilo, verificarla visualmente y mostrarla. El arquitecto pide ajustes hasta quedar conforme. **No se copia nada a `diagrams/` de la raíz en este paso.**
3. Completar en `it-N.md`: la lista de vistas con su imagen, la tabla "Elemento | Responsabilidad" (CK24 figura 4.6) y, si hay relaciones nuevas, la tabla "Relación | Descripción".
4. **Interfaces** identificadas en el paso 5 (CK16 §4.3.3.5): para los casos de uso primarios de la iteración, un diagrama de secuencia (ver `references/views.md`) y, debajo, la tabla "Nombre del método | Descripción" agrupada por elemento, con los métodos que salen de esa secuencia.
4. En este paso no se toman decisiones nuevas: se registran las de los pasos 4 y 5.

### Paso 7: analizar el diseño y revisar el objetivo (CK24 §4.8; CK16 §4.3.2.6)

1. **Tablero.** Mover cada driver de la iteración a "No abordado", "Parcialmente abordado", "Completamente abordado" o "Descartado" según el criterio del paso 1, con una frase que lo justifica. La tabla de la iteración en `it-N.md` lista **todos** los drivers del tablero, salvo los que quedaron completamente abordados en una iteración anterior, que se eliminan de la tabla (CK16 §4.3.2.6 y §4.3.3.6). Los que no avanzaron van en "No abordado" o en su estado anterior con "No se han tomado decisiones relevantes", y si ayuda, la razón en pocas palabras ("falta identificar los elementos del caso de uso asociado"). Un driver nuevo de la iteración (por ejemplo, una preocupación que surgió) entra a la tabla y al tablero. En las tres columnas de estado va solo el ID del driver ("UC-02", no su nombre), como en el libro; la cuarta columna dice qué se decidió. Las filas van en el orden del libro: primero los casos de uso, luego los escenarios de calidad, las restricciones y las preocupaciones (UC, QA, CON, CRN), cada grupo por número. Antes de la tabla, una o dos frases sobre lo que logró la iteración. `kanban.md` queda con el estado actual de todos.
2. **Recorrido del modelo de datos**, si la iteración cambió el modelo de datos: seguir un caso real del dominio (preferiblemente de `inputs/`) paso a paso, con las entidades que se crean o cambian y los cálculos con cifras; marcar lo que el modelo no permite representar, con una propuesta de ajuste. Se guarda en `analysis/walkthrough-<case>.md`. Un hueco que requiere decisión vuelve al paso 4 de la misma iteración; una regla del dominio que nadie sabe va a `questions.md`.
3. **Revisión del objetivo:** una o dos frases sobre si se logró y qué queda para las siguientes iteraciones.

## Cerrar la iteración

1. Verificar el criterio de cierre (abajo).
2. Mostrar el resumen de máximo cinco líneas: objetivo, decisiones con sus ADR, vistas que cambiaron, drivers que avanzaron, y preguntas abiertas que la afectan.
3. Pedir aprobación explícita. Solo cuenta un "apruebo" o equivalente claro.
4. Con la aprobación, en este orden:
   1. Copiar las vistas de `it-N/diagrams/` a `diagrams/` de la raíz (y sus PNG a `diagrams/images/`).
   2. Quitar las marcas `[Propuesta]` de lo aceptado en `it-N.md` y en los ADR nuevos; los ADR nuevos pasan a `Estado: aprobado`.
   3. Encabezado de `it-N.md`: `status: cerrada`, fecha de cierre.
   4. Actualizar `kanban.md` y `status.md` (iteración en curso: ninguna; iteraciones cerradas + 1).
5. Terminar la respuesta con el bloque "Necesito que decidas" (ver "Decisiones siempre visibles" en `start`), siempre con estos dos puntos:
   1. **Documentos v<versión>**: generarlos ahora o después. Si algo del diseño pide esperar (por ejemplo, un costo sin verificar), se dice aquí con su recomendación; nunca se omite la pregunta.
   2. **Lo siguiente**: abrir la próxima iteración de la hoja de ruta (número, objetivo y drivers) o, si todos los drivers de prioridad alta están completos, dar por terminado el diseño de la ronda.

   No se abre la siguiente iteración ni se generan documentos en la misma respuesta del cierre: se espera la respuesta del arquitecto.

Si el arquitecto descarta la iteración, se borra su carpeta y nada más cambia.

## Decisiones que surgen al dibujar

Si en el paso 6 o en el recorrido del paso 7 falta algo que no se decidió (un servicio, una red, un proyecto compartido, una regla de datos):
1. Decirlo en una línea: qué falta y en qué vista o paso apareció.
2. Volver al paso 4 de la **misma iteración**, decidir con su método y continuar desde ahí. La iteración sigue abierta, así que no es un cambio después de aprobar.
3. Si lo que falta es un driver, decirlo: se agrega con `drivers` y entra al tablero.

## Revisar una decisión de una iteración cerrada

Una iteración cerrada no se edita. Para cambiar una de sus decisiones se abre una **iteración nueva** cuyo objetivo es revisarla:
- El paso 2 nombra la decisión, la iteración de origen y el motivo.
- El ADR nuevo dice "Reemplaza a ADR-00x"; en el ADR anterior solo cambia su línea de estado a "Reemplazado por ADR-00y (AAAA-MM-DD)".
- Los drivers afectados vuelven a "Parcialmente abordado" en el tablero hasta que la nueva iteración los complete.

## Criterio de cierre

**Paso 1:**
- [ ] Propósito del diseño y tipo de sistema confirmados.
- [ ] Drivers elegidos por categoría, con la tabla de prioridad de los escenarios.
- [ ] Criterio de "completamente abordado" acordado.
- [ ] Hoja de ruta con objetivo y drivers por iteración.
- [ ] Tablero creado con todos los drivers elegidos y, si es una ronda nueva o un sistema existente, con las decisiones sin driver listadas.
- [ ] Desde la segunda ronda: motivo de la ronda y drivers cambiados identificados.

**Iteración:**
- [ ] Los pasos 2 a 7 están escritos en `it-N.md`, en orden, con sus tablas.
- [ ] Cada decisión cita los drivers que atiende; cada ADR tiene al menos 2 alternativas reales y la elegida la decidió el arquitecto en una pregunta propia.
- [ ] Las vistas que cambiaron están en `it-N/diagrams/`, verificadas visualmente (o marcadas "sin verificación visual"), con nombres idénticos a los de las tablas y de las vistas anteriores.
- [ ] El tablero refleja el estado de cada driver de la iteración con su justificación.
- [ ] Si cambió el modelo de datos, el recorrido está hecho y sus huecos resueltos o registrados.
- [ ] Las preocupaciones nuevas están registradas.
- [ ] Todos los elementos `[Propuesta]` fueron mostrados al arquitecto.

Si algo falla, decirlo en una línea y preguntar si se resuelve ahora o queda como pendiente anotado en la revisión del paso 7.

## Fuentes

- Cervantes, H., & Kazman, R. (2024). *Designing software architectures: A practical approach* (2.ª ed.). Addison-Wesley. Cap. 4 (CK24).
- Cervantes, H., & Kazman, R. (2016). *Designing software architectures: A practical approach*. Addison-Wesley. Cap. 4, caso FCAPS (CK16).
- Bass, L., Clements, P., & Kazman, R. (2021). *Software architecture in practice* (4.ª ed.). Addison-Wesley. Caps. 4–14 (catálogo de tácticas por atributo).
- Nygard, M. (2011). *Documenting architecture decisions*.
