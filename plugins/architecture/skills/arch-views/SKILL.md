---
name: arch-views
description: Usar para la fase 3 del proceso de arquitectura, una vez aprobados drivers.md y decisiones.md - construir con el arquitecto las vistas (contexto, estilo, contenedores, componentes, modelo de datos, despliegue y desarrollo) como diagramas .drawio verificados visualmente, recorrer un caso real por el modelo de datos y registrar las decisiones que surjan, produciendo diagramas/ y vistas.md.
---

# Vistas de arquitectura

Fase 3 del asistente de arquitectura. Parte de `drivers.md` y `decisiones.md` aprobados y produce la carpeta `diagramas/` con su índice `vistas.md`. Las vistas alimentan la validación (fase 4) y las secciones 1.3, 3.1 y 4 del documento de arquitectura.

**Marco metodológico:** en ADD, las vistas son el paso en que se instancian los elementos de arquitectura y se asignan responsabilidades. Por eso aquí aparecen huecos y decisiones que no se vieron en la fase 2. Esta skill los hace visibles y los devuelve a `decisiones.md`; nunca los resuelve en silencio dentro de un diagrama.

## Principios (no negociables)

1. **El arquitecto decide; Claude dibuja, verifica y propone.** Un diagrama nunca introduce una decisión que no esté en `decisiones.md` (un servicio nuevo, una entidad que cambia una regla, un proyecto compartido, una red). Si hace falta, se aplica "Decisiones que surgen en las vistas".
2. **Todas las vistas del documento se hacen en esta fase.** Ninguna pieza de diseño se crea por primera vez en la fase 5. La lista de vistas sale de la estructura del documento de arquitectura (ver "Vistas de la fase").
3. **Ver el diagrama antes de mostrarlo.** Siempre que se pueda, cada `.drawio` se convierte a PNG y Claude lo revisa con la herramienta de lectura de imágenes antes de presentarlo. Si no se puede, se muestra marcado "sin verificación visual" (ver "Verificación visual").
4. **Una vista por turno, aprobada por separado.** Cada vista se presenta con su imagen y un resumen de 3–5 líneas; el arquitecto la aprueba o pide ajustes antes de pasar a la siguiente.
5. **Solo cuenta como aprobación un "apruebo" explícito** (o equivalente claro: "aprobado", "de acuerdo con la vista"). Respuestas como "continuar" o "sigamos" no aprueban: se pregunta de nuevo en una línea. No se infiere aprobación del silencio ("como no comentaste nada, entiendo que…").
6. **Nombres idénticos entre vistas.** Un módulo, contenedor o entidad se llama igual en todos los diagramas, en `decisiones.md` y en el documento.
7. **Cargar solo la skill de estilo de la vista actual.** Las skills de estilo son extensas; no se cargan todas al inicio.
8. **`diagramas/` es solo para las vistas:** los `.drawio` con su PNG, `borradores/`, `vistas.md` y `vista-desarrollo.md` (la única vista en texto). Recorridos, flujos explicados y demás material de análisis van en `analisis/`.
9. **Los borradores viven en el proyecto, nunca en una carpeta temporal.** Cada vista en revisión se guarda en `diagramas/borradores/<archivo>.drawio`, con su PNG al lado (`<archivo>.png`), para que el arquitecto la abra en su editor antes de aprobarla. Al presentarla se da la ruta relativa de los dos archivos y, en Mac, se abre el PNG con `open`. La imagen pegada en el chat no basta: en la terminal no se ve. Con el "apruebo", el `.drawio` pasa a `diagramas/` (reemplazando la versión anterior, que queda en git) y se borra el borrador.

## Paso 0: Revisar qué existe

1. Leer `drivers.md` y `decisiones.md`. Si alguno no existe o no está en `Estado: aprobado`, detenerse y decir qué fase hay que cerrar primero.
2. **Verificar herramientas antes de dibujar.** Python 3 es necesario (genera los `.drawio`). Para convertir a PNG, revisar qué hay disponible según el orden de "Verificación visual" y decirlo en una línea. Si no hay ninguna opción, ofrecer la de Playwright en una carpeta temporal; si el arquitecto no la quiere, seguir sin verificación visual. Nunca instalar sin permiso, y nunca bloquear la fase por una herramienta.
3. Si ya existe `diagramas/vistas.md`, retomarlo: revisar cada vista contra esta skill y contra los archivos aprobados vigentes (si `decisiones.md` cambió después de aprobar una vista, esa vista vuelve a "por revisar"). Mostrar en 3–4 líneas qué está aprobado y qué falta.
4. Si hay diagramas sueltos en `diagramas/` sin índice, crear `vistas.md` y tratarlos como borradores por verificar.
5. Revisar `insumos/` en busca de datos reales (formatos, planillas, registros) para el recorrido del modelo de datos.

## Vistas de la fase

| # | Vista | Archivo | Skill de estilo | Sección del documento |
|---|-------|---------|-----------------|-----------------------|
| 1 | Contexto (C4 nivel 1) | `c4-contexto.drawio` | `arch-c4-diagram-style` | 1.3 |
| 2 | Estilo arquitectónico | `estilo-arquitectonico.drawio` | `arch-c4-diagram-style` | 3.1 |
| 3 | Contenedores (C4 nivel 2) | `c4-contenedores.drawio` | `arch-c4-diagram-style` | 4.1.1 |
| 4 | Componentes (C4 nivel 3) | `c4-componentes.drawio` | `arch-c4-diagram-style` | 4.1.2 |
| 5 | Modelo de datos + recorrido | `modelo-datos.drawio`, `analisis/recorrido-<caso>.md` | `arch-database-diagram-style` | 4.2 |
| 6 | Despliegue | `despliegue-<nube>.drawio` | `arch-aws-diagram-style` (si es AWS) | 4.3 |
| 7 | Desarrollo (paquetes) | `vista-desarrollo.md` | — | 4.4 |

Contenido mínimo de cada vista:

1. **Contexto:** el sistema como una sola caja, los actores y los sistemas externos de `drivers.md`, con lo que intercambian.
2. **Estilo:** el punto de entrada arriba; el proceso o los servicios con sus módulos (los de `decisiones.md`, señalando núcleo y soporte) y el mecanismo de comunicación entre ellos; los componentes aparte (por ejemplo, el análisis); la persistencia abajo.
3. **Contenedores:** cada unidad desplegable y cada almacén, con tecnología y protocolo en las flechas. Debe coincidir con el estilo y con el stack.
4. **Componentes:** los módulos del núcleo del dominio (no todos), con sus capas y el contrato entre ellos. Se pregunta al arquitecto cuáles módulos mostrar.
5. **Modelo de datos:** entidades, enumeraciones y agrupaciones por esquema o contexto, según `decisiones.md` (base de datos y multitenant). Cada caso de uso primario debe poder ejecutarse con las entidades del modelo. Incluye el recorrido (ver abajo).
6. **Despliegue:** red, zonas, servicios gestionados y salidas a internet según los servicios cloud de `decisiones.md`. Lo que el diagrama exija y no esté decidido (NAT, zonas, región) es una decisión que surge.
7. **Desarrollo:** árbol de carpetas de la solución, por módulo y por capa, coherente con los patrones (Clean Architecture, contratos entre módulos). Se presenta en texto monoespaciado. Los proyectos compartidos (por ejemplo, un kernel común) son decisiones que surgen si no están en `decisiones.md`.

Si una vista no aplica (por ejemplo, no hay nube), se omite y se anota en `vistas.md` con la razón.

## Recorrido del modelo de datos

El modelo de datos no se aprueba solo con el diagrama. Se recorre con un caso real del dominio:

1. **Elegir el caso** con el arquitecto, preferiblemente de `insumos/` (un registro, una planilla, un formato real). Debe tocar los casos de uso primarios y las excepciones del dominio (por ejemplo, productos sin fecha, a granel, que se fraccionan o se descartan).
2. **Seguirlo paso a paso**: en cada paso, qué entidades se crean o cambian, qué movimientos se registran y qué cálculos resultan, con cifras.
3. **Marcar los huecos**: lo que el modelo no permite representar o que se pierde en el camino. Cada hueco se presenta con una propuesta de ajuste.
4. **Guardar** el recorrido en `analisis/recorrido-<caso>.md` (tabla paso → entidades y movimientos → resultado → hueco). Si al arquitecto le cuesta seguir el flujo, ofrecer una versión visual en HTML (`analisis/recorrido-<caso>.html`).

Las reglas del dominio que el recorrido no puede resolver sin un interesado (el que corresponda en este proyecto) van a `preguntas.md`, con el supuesto provisional con que se dibuja mientras tanto. No se presentan como hechos ni se le pide al arquitecto que las decida.

## Verificación visual

La herramienta para convertir a PNG es opcional. Usar la primera disponible:

1. **draw.io Desktop**, si está instalado: `drawio -x -f png <archivo>.drawio`.
2. **Playwright con Chromium**, en una carpeta temporal de la sesión, cargando el `.drawio` en el visor de draw.io (requiere internet). No instala nada en el sistema del arquitecto.
3. **Sin verificación visual:** si ninguna es posible o el arquitecto no quiere instalar, se entrega el `.drawio` marcado "sin verificación visual" y el arquitecto lo revisa en su editor (por ejemplo, la extensión de draw.io para VS Code) y dice qué corregir. En `vistas.md` la vista lleva esa nota.

Antes de mostrar cada diagrama:

1. Generar el `.drawio` con la skill de estilo y convertirlo a PNG.
2. Abrir el PNG con la herramienta de lectura de imágenes y revisar:
   - ningún texto se sale de su caja ni se superpone con otro;
   - las flechas no cruzan cajas ni se confunden sus etiquetas;
   - el diagrama se lee al ancho de una página.
3. Comprobar la coherencia: todos los elementos existen en `decisiones.md` con el mismo nombre, y no falta ningún módulo, contenedor o servicio decidido.
4. Corregir y volver a convertir hasta que pase. Solo entonces mostrar la imagen al arquitecto.

Si no se pudo convertir a PNG, igual se hace la comprobación de coherencia (paso 3) sobre el `.drawio`, y se dice que falta la revisión visual. Nunca presentar un diagrama como verificado sin haberlo visto.

## Decisiones que surgen en las vistas

Cuando un diagrama necesita algo que `decisiones.md` no decide:

1. **Detenerse** y decir en una línea qué falta y en qué vista apareció.
2. **Proponer** con el método de la fase 2: 2–3 candidatos, tabla corta frente a los drivers, recomendación. Las decisiones organizacionales o de costo se preguntan.
3. **El arquitecto decide**, en una pregunta propia.
4. **Registrar** con la skill `arch-decisions`, que aplica su regla de "Cambios posteriores a la aprobación": Claude propone si el cambio complementa o reemplaza una decisión, y el arquitecto lo clasifica. Si complementa, se registra como cambio y `decisiones.md` sigue aprobado; si reemplaza o hay duda, la fase 2 se reabre.
5. Si el cambio afecta una vista ya aprobada, esa vista vuelve a "por revisar".

Si lo que surge es un driver nuevo, se aplica "Reabrir los drivers" de `arch-decisions`.

## Formato de vistas.md

```markdown
# Vistas de arquitectura — <Sistema>
Estado: borrador | aprobado · Fecha: AAAA-MM-DD

Parte de: drivers.md (aprobado) · decisiones.md (aprobado)

| # | Vista | Archivo | Estado | Notas |
|---|-------|---------|--------|-------|
| 1 | Contexto | c4-contexto.drawio | Aprobada AAAA-MM-DD | |
| 5 | Modelo de datos | modelo-datos.drawio, analisis/recorrido-<caso>.md | Por revisar | Cambió el control de acceso |
| 6 | Despliegue | — | No aplica | Sin nube |

## Decisiones surgidas en esta fase
- <Decisión> — vista <n>; registrada en decisiones.md (<fecha>).

## Preguntas abiertas
PA-xx, PA-yy (en `preguntas.md`) — afectan: <vista o entidad>.
```

## Criterio de cierre

Antes de pedir aprobación de la fase, verificar:
- [ ] Todas las vistas de la tabla están aprobadas o marcadas "No aplica" con su razón.
- [ ] Cada diagrama fue revisado visualmente después de su último cambio, por Claude (PNG) o por el arquitecto si quedó "sin verificación visual".
- [ ] Los nombres coinciden entre vistas y con `decisiones.md`.
- [ ] El modelo de datos se recorrió con un caso real y sus huecos quedaron resueltos o registrados en `preguntas.md`.
- [ ] Cada decisión surgida está registrada en `decisiones.md` con su fila de cambio aprobada.
- [ ] Ninguna vista quedó "por revisar" por un cambio posterior a su aprobación.

Si algo falla, decirlo en una línea y preguntar si se resuelve ahora o queda pendiente.

## Cierre

1. Mostrar un resumen de 5–8 líneas: vistas aprobadas, decisiones surgidas, huecos del recorrido y preguntas abiertas que afectan las vistas.
2. Pedir aprobación explícita de la fase.
3. Con la aprobación, cambiar `vistas.md` a `Estado: aprobado` y poner la fecha.
4. Indicar que la siguiente fase es la validación. Los huecos del recorrido y las preguntas abiertas son riesgos candidatos.
