# Vistas y verificación visual

Referencia de `design`. Leer en el paso 5 (secuencias) y en el paso 6 (vistas).

## Qué vista cambia según la decisión

| Si la decisión cambia… | Vista | Archivo | Skill de estilo |
|------------------------|-------|---------|-----------------|
| El estilo o la organización de alto nivel (monolito, servicios, módulos y su comunicación) | Estilo arquitectónico | `architectural-style.drawio` | `c4` |
| Aplicaciones, bases de datos, almacenes o servicios y cómo se comunican | Contenedores (C4 nivel 2) | `c4-containers.drawio` | `c4` |
| Los módulos del núcleo, sus capas o los contratos entre ellos | Componentes (C4 nivel 3) | `c4-components.drawio` | `c4` |
| Entidades, relaciones o reglas de datos | Modelo de datos | `data-model.drawio` | `data` |
| Infraestructura en la nube (red, zonas, servicios gestionados) | Despliegue | `deployment-<cloud>.drawio` | `aws` (si es AWS) |
| La organización del código (soluciones, proyectos, capas) | Desarrollo | `development-view.md` (texto monoespaciado) | — |
| La interacción de elementos en un caso de uso (paso 5) | Secuencia | `seq-<uc>.drawio` | `c4` (generador de secuencias) |

El contexto (`c4-context.drawio`) lo hace `drivers` en la sección 1; aquí solo se lee.

Contenido mínimo:
- **Estilo:** muestra cómo está organizada por dentro la aplicación que se eligió (por ejemplo, un monolito modular): su límite, el punto de entrada arriba, los módulos (señalando núcleo y soporte) con su comunicación y su regla de dependencia. La persistencia (bases de datos, almacenes de archivos) va abajo y **fuera** del límite de la aplicación, porque son contenedores aparte. El título dice qué representa ("Estilo arquitectónico: monolito modular").
- **Contenedores:** cada unidad desplegable y cada almacén, con tecnología y protocolo en las flechas; coherente con el estilo.
- **Componentes:** los módulos del núcleo del dominio, con sus capas y contratos. Se pregunta cuáles módulos mostrar.
- **Modelo de datos:** entidades, enumeraciones y agrupaciones por esquema o contexto. Cada caso de uso primario debe poder ejecutarse con el modelo.
- **Despliegue:** red, zonas, servicios gestionados y salidas a internet. Lo que el diagrama exija y no esté decidido es una decisión que surge.
- **Desarrollo:** árbol de carpetas de la solución por módulo y por capa, coherente con los patrones.

Nombres idénticos: un módulo, contenedor o entidad se llama igual en todas las vistas, en las tablas de las iteraciones y en los ADR.

Cargar solo la skill de estilo de la vista que se está dibujando.

## Diagramas de secuencia

Se generan con el generador de secuencias de `c4` (`scripts/seq_drawio.py`, ver su sección "Diagramas de secuencia"), con el mismo estilo de las vistas C4. Uno por caso de uso primario de la iteración, solo con el flujo principal, con los participantes nombrados igual que en las vistas. Archivo: `seq-<uc>.drawio` en la carpeta de la iteración.

## Verificación visual

Herramienta para convertir a PNG, la primera disponible:
1. **draw.io Desktop:** `drawio -x -f png -o <images>/<archivo>.png <archivo>.drawio`.
2. **Playwright con Chromium**, en una carpeta temporal de la sesión, cargando el `.drawio` en el visor de draw.io. No instala nada en el sistema del arquitecto.
3. **Sin verificación visual:** se entrega el `.drawio` marcado "sin verificación visual" y el arquitecto lo revisa en su editor.

Verificar las herramientas una vez por sesión, antes del primer dibujo, y decirlo en una línea. Nunca instalar sin permiso y nunca bloquear el paso por una herramienta.

Antes de mostrar cada diagrama:
1. Generar el `.drawio` con la skill de estilo en `iterations/round-R/it-N/diagrams/` y su PNG en `iterations/round-R/it-N/diagrams/images/`.
2. Abrir el PNG con la herramienta de lectura de imágenes y revisar: ningún texto se sale de su caja ni se superpone; las flechas no cruzan cajas ni se confunden sus etiquetas; se lee al ancho de una página.
3. Comprobar la coherencia: todo elemento existe en las decisiones de esta iteración o de anteriores con el mismo nombre, no falta ninguno decidido, y ninguno (contenedor, módulo, entidad, esquema, red) sirve solo a algo que está en "Fuera de alcance".
4. Corregir y volver a convertir hasta que pase. Solo entonces mostrarlo, con la ruta del `.drawio` para que el arquitecto lo abra en su editor.

Nunca presentar un diagrama como verificado sin haberlo visto.
