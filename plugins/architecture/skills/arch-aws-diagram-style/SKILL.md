---
name: "arch-aws-diagram-style"
description: "Usar cuando se pida crear o actualizar un diagrama de despliegue/arquitectura AWS (AWS Cloud > Region > VPC > Availability Zone > subredes > ECS/Fargate, bases de datos, IGW, load balancers, actores) como archivo .drawio editable, replicando el estilo visual exacto de su diagrama de referencia: contenedores anidados con los iconos y colores oficiales de la librería mxgraph.aws4 (AWS Cloud negro, Region teal, VPC morado, subredes públicas verdes y privadas teal con icono de candado, cajas ECS/Fargate naranjas sin relleno), iconos de recursos AWS4 (Internet Gateway, ALB, RDS/MySQL, NAT Gateway, etc.) y actores con la librería mxgraph.cisco_safe (círculos morados de personas), flechas ortogonales grises. No aplica a diagramas C4 (usar la skill arch-c4-diagram-style para esos)."
---

# Estilo de diagramas de despliegue AWS (draw.io)

Esta skill genera diagramas de despliegue/arquitectura AWS como archivos `.drawio` editables, replicando el estilo visual del diagrama de referencia (arquitectura de microservicios ECS/Fargate detrás de un ALB, con RDS MySQL en subred privada). Todos los estilos, colores e identificadores de iconos de este documento fueron extraídos DIRECTAMENTE del `.drawio` real (Extras > Editar diagrama), no adivinados — esto importa porque un `resIcon` mal escrito se ve en draw.io como una caja gris con signo de interrogación ("forma no encontrada").

## Cuándo usarla

Siempre que el usuario pida crear, rehacer o extender un diagrama de despliegue/infraestructura AWS — arquitectura de un sistema en AWS, un diagrama de red/VPC, un diagrama de CI/CD con servicios AWS, etc. Si pide un diagrama C4 (Contexto/Contenedores/Componentes), usar la skill `arch-c4-diagram-style` en su lugar, no esta.

## Regla de oro: nunca inventar un `resIcon` que no esté confirmado

La librería `mxgraph.aws4` tiene más de 1000 iconos, y un nombre incorrecto no da error visible al generar el XML — simplemente se ve como una caja gris "forma no encontrada" cuando el usuario abre el archivo. Antes de usar un icono que NO esté en la tabla "Iconos verificados" de abajo:

1. Si el usuario puede compartir un `.drawio`/fragmento XML que ya use ese icono (Extras > Editar diagrama en draw.io, o el botón de copiar en VS Code), pídeselo y usa el `resIcon=`/`shape=` exacto de ahí.
2. Si no, usa tu mejor estimación del nombre en inglés del servicio en minúsculas con guiones bajos (p. ej. `dynamodb`, `lambda_function`, `s3`) — el patrón observado es: nombre del servicio en inglés, todo minúscula, espacios reemplazados por `_`. Marca en tu respuesta al usuario cuáles iconos son "estimados" para que los revise al abrir el archivo, y ofrece corregirlos si alguno sale mal.
3. Nunca digas que un icono "debería funcionar" sin dejar claro si viene de la tabla verificada o es una estimación.

## REGLA CRÍTICA: solo un grupo pequeño de iconos usa el "badge" cuadrado — el resto es icono plano sin fondo

Esto causó un bug real ya corregido: generar TODOS los iconos con el wrapper `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<nombre>` hace que TODOS salgan como un cuadrado sólido de color (un "badge"), pero eso NO es lo que hace el diagrama real de referencia. Verificado carácter por carácter contra su `.drawio`:

- **Variante "badge"** (cuadrado sólido de color + borde blanco festoneado) — SOLO para: `ecs`, `fargate` (y por el mismo patrón documentado ya antes: `ecr`, `codecommit`, `codepipeline`, `codedeploy`). Usa `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.<nombre>;` CON el `points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[0,1,0],[0.25,1,0],[0.5,1,0],[0.75,1,0],[1,1,0],[0,0.25,0],[0,0.5,0],[0,0.75,0],[1,0.25,0],[1,0.5,0],[1,0.75,0]];` de esquinas festoneadas y `strokeColor=#ffffff` (nunca `none` en esta variante).
- **Variante nativa (por defecto para todo lo demás)** — icono de color plano SIN fondo cuadrado, sobre fondo transparente. Usa `shape=mxgraph.aws4.<nombre>;` DIRECTO (sin `resourceIcon`, sin `resIcon=`) y `strokeColor=none`. Verificado así para: `internet_gateway`, `application_load_balancer`, `rds_mysql_instance`, `identity_access_management_iam_roles_anywhere`, `ecs_task`. Este es el comportamiento por defecto para cualquier icono nuevo/estimado — NO envolverlo en `resourceIcon` a menos que el usuario confirme que ese icono específico usa la variante badge.

Si el usuario reporta que "los íconos no tienen el mismo fondo que en el archivo que te pasé" o que se ven como cuadrados sólidos cuando no deberían, es este bug: revisar si el icono en cuestión está incorrectamente en la lista badge.

## Iconos y contenedores verificados (extraídos del .drawio real de referencia)

Estos estilos son exactos, cópialos tal cual (están también embebidos en el script generador más abajo):

**Contenedores (`shape=mxgraph.aws4.group`, todos con `container=1` para anidar hijos con coordenadas RELATIVAS a su propio origen):**
| Nivel | `grIcon` | strokeColor | fillColor | fontColor |
|---|---|---|---|---|
| AWS Cloud | `group_aws_cloud_alt` | `#232F3E` | none | `#232F3E` |
| Region | `group_region` | `#00A4A6` | none | (por defecto) |
| VPC | `group_vpc2` | `#8C4FFF` | none | `#AAB7B8` |
| Subred pública | `group_security_group` (con `grStroke=0`) | `#7AA116` | `#F2F6E8` | `#248814` |
| Subred privada | `group_security_group` (con `grStroke=0`) | `#00A4A6` | `#E6F6F7` | `#147EBA` |

**IMPORTANTE — ningún contenedor se estira más allá de su contenido, EXCEPTO las subredes hermanas dentro de una misma AZ (ver regla de tamaño estándar de subredes más abajo):** AWS Cloud, Region, VPC, Availability Zone deben calcularse de AFUERA HACIA ADENTRO según lo que realmente contienen, no con anchos/altos redondos arbitrarios. Regla práctica: el ancho de cada contenedor = (x del hijo más a la derecha + su ancho) + margen (~20-30px, ver nota de márgenes en "Tamaño estándar de subredes"), y así sucesivamente hacia afuera (subred → AZ → VPC → Region → Cloud). Si después reduces el ancho de una caja ECS/Fargate (ver nota abajo), tienes que RECALCULAR EN CASCADA el ancho de la subred, la AZ, la VPC, la Region y la Cloud que la envuelven — no basta con angostar la caja interna y dejar los contenedores externos con su ancho viejo, porque eso es exactamente lo que deja la subred (y todo lo que la envuelve) con aire de sobra a la derecha. Esto aplica también cuando se AGREGA una subred nueva como hermana de las existentes: el ancho de la AZ, VPC, Region y Cloud debe recalcularse para sumar la subred nueva más sus márgenes.

**IMPORTANTE — un icono cerca del BORDE SUPERIOR de un contenedor con su propio título compite por el mismo espacio vertical que ese título (bug real corregido, ver "Bugs reales corregidos" abajo):** cuando un icono (p. ej. Amazon Cognito) va directamente dentro de un contenedor con `grIcon` (Region, VPC, etc.), ese contenedor ya reserva su propia franja superior para el título ("Region (p.ej. us-east-1)", etc.). Si el icono queda a menos de ~30-35px del borde superior del contenedor, su propia etiqueta (sobre todo si usa `label_pos: bottom`, que dibuja el texto DEBAJO del icono en dos líneas) puede terminar visualmente encima/pegada al texto del título del contenedor. Antes de colocar un icono cerca del borde superior de un contenedor con título: (a) dejar al menos 30-35px de aire entre el borde superior del contenedor y el icono, y (b) si el espacio vertical sigue ajustado, usar `label_pos: right` o `left` en vez de `bottom` — el texto queda al costado del icono, en la misma fila, en vez de ocupar una segunda franja vertical hacia abajo.

**Cajas planas sin icono de grupo (no son `shape=mxgraph.aws4.group`, son rectángulos simples con `container=1` para anidar):**
- Availability Zone: `strokeColor=#147EBA;fontColor=#147EBA;fillColor=none`, etiqueta envuelta en `<font style="font-size: 10px;">`.
- Caja ECS y caja Fargate (contorno sin relleno alrededor de las tareas): `strokeColor=#FF8000;fillColor=none`, sin etiqueta propia — el nombre "ECS"/"Fargate" va en un icono pequeño con etiqueta a la derecha, no en el borde de la caja. Su ancho/alto debe calcularse por CONTENIDO (icono ~22-30px + el texto más largo de las tareas que contiene + margen a la derecha y abajo — ver "Tamaño estándar de subredes" para los márgenes verificados más recientes), nunca estirarse para llenar el ancho completo de la subred que las envuelve — exactamente el mismo principio que en `arch-c4-diagram-style`, donde los componentes nunca se estiran al ancho de su grupo. Y recuerda propagar ese angostamiento hacia afuera (ver nota de arriba).

**Iconos de recurso, confirmados — nota la columna "Variante" (badge = cuadrado sólido con borde blanco; nativa = icono plano sin fondo, shape directo):**
| Icono | `resIcon`/`shape` | fillColor | Variante | Notas de posición de etiqueta |
|---|---|---|---|---|
| ECS (pequeño, dentro de su caja) | `ecs` | `#ED7100` | badge | etiqueta a la derecha, `fontColor=#808080`, `fontSize=10` |
| Fargate (pequeño, dentro de su caja) | `fargate` | `#ED7100` | badge | etiqueta a la derecha, `fontColor=#808080`, `fontSize=10` |
| Tarea/contenedor ECS | `ecs_task` | `#ED7100` | nativa | etiqueta a la derecha, `fontColor=#232F3E`, `fontSize=10` |
| ECR | `ecr` | `#ED7100` | badge | etiqueta abajo |
| Internet Gateway | `internet_gateway` | `#8C4FFF` | nativa | etiqueta a la izquierda (abajo si una flecha entra por su izquierda, p. ej. desde CloudFront — ver "Alineación del camino de entrada") |
| Application Load Balancer | `application_load_balancer` | `#8C4FFF` | nativa | etiqueta abajo, centrada |
| NAT Gateway | `nat_gateway` | `#8C4FFF` | nativa (estimado — no confirmado aún contra un archivo real de referencia) | etiqueta a la izquierda o derecha, según el lado por el que entre/salga su(s) flecha(s) — ver "Flechas" |
| RDS MySQL | `rds_mysql_instance` | `#C925D1` | nativa | etiqueta abajo |
| IAM | `identity_access_management_iam_roles_anywhere` | `#DD344C` | nativa | etiqueta abajo |
| Cognito User Pool | `cognito` | `#DD344C` | nativa | etiqueta a la derecha (ver nota de espacio vertical arriba — evitar `bottom` si va cerca del título de su contenedor) |
| CodeCommit | `codecommit` | `#C925D1` | badge | etiqueta abajo |
| CodePipeline | `codepipeline` | `#C925D1` | badge | etiqueta abajo |
| CodeDeploy | `codedeploy` | `#C925D1` | badge | etiqueta abajo |

**Actores/personas — OJO: no son AWS4.** Usan la librería `mxgraph.cisco_safe` (incluida por defecto en draw.io): `shape=mxgraph.cisco_safe.compositeIcon;bgIcon=ellipse;resIcon=mxgraph.cisco_safe.design.users;fillColor=#A153A0;strokeColor=#ffffff`. No intentes usar un `resIcon=mxgraph.aws4.user` para actores — no es el patrón que usa el usuario.

## Iconos estimados (no verificados aún — confirmar con el usuario o su archivo si aparecen mal)

Siguen el patrón `nombre_en_ingles_con_guiones_bajos`, el color por categoría oficial de AWS, y la **variante nativa por defecto** (shape directo, sin fondo cuadrado — ver regla crítica arriba), pero no vienen de un archivo real de referencia: `ec2`, `lambda_function`, `eks_cloud`, `ecs_service` (naranja `#ED7100`, Cómputo/Contenedores); `network_load_balancer`, `classic_load_balancer`, `nat_gateway`, `vpc`, `route_53`, `api_gateway`, `cloudfront` (morado `#8C4FFF`, Redes y entrega de contenido); `rds_postgresql_instance`, `dynamodb` (magenta `#C925D1`, Bases de datos); `s3` (verde `#7AA116`, Almacenamiento); `sqs`, `sns`, `cloudwatch` (rosa `#E7157B`, Integración/Management). Si el usuario reporta que alguno se ve mal (caja gris, o con fondo cuadrado cuando no debería), pídele el fragmento XML de ese icono y actualiza esta tabla.

## Jerarquía de anidamiento (seguir siempre esta estructura, no aplanar)

A diferencia del skill de C4 (que usa coordenadas absolutas para todo), aquí los contenedores son verdaderos padres de mxGraph: cada elemento hijo lleva `parent` apuntando al `id` del contenedor que lo envuelve visualmente, y sus coordenadas `x`/`y` son RELATIVAS al origen de ESE padre (no de la página). Esto es lo que hace el usuario al armar sus diagramas a mano en draw.io, y es la forma correcta de anidar en AWS4.

Jerarquía típica (de afuera hacia adentro):

1. **Actores** (Customers, Employee, etc.): fuera del `AWS Cloud`, a la izquierda, `parent` = raíz (`"1"`).
   - Si hay frontend web, **CloudFront** va dentro del `AWS Cloud` pero fuera de la Region (`parent` = id de la Cloud), en la franja izquierda, alineado con el IGW y el ALB (ver "Alineación del camino de entrada").
2. **AWS Cloud** (`parent="1"`).
3. **Region** (`parent=` id de AWS Cloud).
4. **VPC** (`parent=` id de Region).
5. Dentro de la VPC, directamente: **Internet Gateway** (icono suelto, sin subred propia) y las **Availability Zone** (una por cada zona).
6. Dentro de cada **Availability Zone**, TRES subredes hermanas lado a lado en horizontal, TODAS DEL MISMO TAMAÑO (ver "Tamaño estándar de subredes" más abajo): **subred pública** (la más a la izquierda, cerca del punto de entrada), **subred privada de aplicación** ("app", a su derecha) y **subred privada de datos** ("datos", a la derecha de la de aplicación).
7. Dentro de la **subred pública**: normalmente el **Load Balancer (ALB)** y, si el backend necesita salida a Internet (para descargar paquetes, imágenes, actualizaciones), un **NAT Gateway** — ambos son la única capa de PASO/ENTRADA-SALIDA, no de cómputo. Cuando ambos coexisten, apílalos verticalmente (uno arriba del otro) en vez de ponerlos lado a lado, para dejar la subred con más aire y mejor legibilidad (ver "Flechas", nota sobre iconos apilados verticalmente, y bug #15).
8. Dentro de la **subred privada de aplicación**: la **caja ECS** (naranja, sin relleno, dimensionada por contenido — ver nota arriba) conteniendo el icono ECS + etiqueta, y dentro de ella la **caja Fargate** (también dimensionada por contenido) conteniendo el icono Fargate + etiqueta y los iconos de **tarea/contenedor** (`ecs_task`) uno debajo del otro. Esta es normalmente la subred con más contenido, y por eso su tamaño define el tamaño estándar de las tres.
9. Dentro de la **subred privada de datos**: el/los icono(s) de base de datos (p. ej. RDS MySQL), centrado(s) dentro del espacio estándar de la subred — NUNCA en la misma subred que la caja ECS/Fargate/tarea (ver "Backend y base de datos en subredes privadas separadas").

Si el usuario pide un servicio o capa que no aparece en esta jerarquía (p. ej. una cola SQS, un bucket S3, un pipeline de CI/CD, un Cognito User Pool para autenticación), colócalo en el nivel que corresponda lógicamente (dentro de la VPC, dentro de la Region pero fuera de la VPC para servicios como Cognito/CodePipeline/CodeCommit que suelen dibujarse a un lado, etc.) siguiendo el mismo patrón de anidamiento real con `parent` — y si queda cerca del borde superior de su contenedor, ver la nota de espacio vertical de arriba.

**Nota — un archivo editado a mano en draw.io puede mostrar un `parent` que ya no coincide con el contenedor visual, sin que el render se vea mal (observado en un archivo real de referencia).** Cuando el usuario ajusta posiciones usando el panel "Arrange" (campos numéricos de X/Y absolutos) en vez de arrastrar el elemento dentro de su contenedor, draw.io puede dejar el `parent` original mientras las coordenadas absolutas siguen cayendo visualmente dentro de otro contenedor (p. ej. una Availability Zone con `parent` = Region en vez de VPC, o un ALB con `parent` = la AZ en vez de la subred pública, mientras ambos se ven perfectamente anidados en el render). Esto es un artefacto de edición manual, no una intención de diseño. Al extraer un archivo del usuario como referencia para esta skill: (a) toma las MEDIDAS (tamaños, márgenes, posiciones relativas) tal cual, pero (b) al construir el `spec.json` de un diagrama NUEVO, usa siempre el `parent` verdadero según el anidamiento visual (VPC → AZ → subred → contenido), no el que pueda traer un archivo editado a mano — la jerarquía real de `parent` es la que garantiza que mover el contenedor externo (p. ej. la VPC completa) mueva todo su contenido junto, cosa que un `parent` desincronizado no garantiza de forma confiable.

## Subredes lado a lado dentro de la AZ (regla verificada con el usuario, no una alternativa)

Dentro de una misma Availability Zone, TODAS las subredes van **una junto a la otra en horizontal**, no apiladas verticalmente — con dos subredes (pública/privada) o con tres (pública/privada-app/privada-datos, ver "Backend y base de datos en subredes privadas separadas"):

- **Subred pública siempre a la izquierda** (más cerca del flujo de entrada: actor → Internet Gateway → subred pública), y las subredes privadas a su derecha, en el orden en que las atraviesa el tráfico (primero la de aplicación, luego la de datos), todas como hijas directas del mismo `az` (mismo `parent`). La `x` de cada subred = `x` de la subred anterior + su `w` + margen (ver "Tamaño estándar de subredes" para el margen actual recomendado).
- El flujo de la conexión principal queda así estrictamente de izquierda a derecha: actor(es) → Internet Gateway → subred pública (ALB) → subred privada de aplicación (ECS/Fargate/tarea) → subred privada de datos (base de datos) — nunca zigzagueando hacia abajo para llegar a alguna de las privadas.
- **Por qué (razón dada por el usuario, aplícala como principio general, no solo para este diagrama):** este patrón horizontal es el que generaliza limpio cuando el diagrama tiene MÁS DE UNA Availability Zone. Cada AZ se convierte en su propia "fila" autocontenida con sus subredes lado a lado, y si hace falta agregar una segunda AZ, esa fila completa se apila DEBAJO de la primera — la organización general del diagrama no se complica.
- Esto aplica por defecto a CUALQUIER diagrama de despliegue nuevo con una o más AZs — no es una preferencia puntual de un solo diagrama, es el layout estándar de esta skill de aquí en adelante.
- Ejemplo de coordenadas verificado, con el tamaño y margen estándar MÁS RECIENTE (dentro de una AZ, las tres subredes con `parent` = id de la AZ, TODAS de `w=260,h=200` — ver "Tamaño estándar de subredes"): subred pública en `x=13,y=40`; subred privada de aplicación en `x=292,y=40` (arranca después del borde derecho de la pública [13+260=273] + margen ~19); subred privada de datos en `x=571,y=40` (arranca después del borde derecho de la de aplicación [292+260=552] + margen ~19). Ver el ejemplo completo en "Esquema del JSON de especificación" abajo.

## Tamaño estándar de subredes — todas las subredes de una AZ miden lo mismo (regla verificada con el usuario, bug real corregido)

**Todas las subredes dentro de una misma Availability Zone deben tener EXACTAMENTE el mismo ancho y alto — nunca una más ancha o más alta que otra**, aunque su contenido sea muy distinto (una caja ECS/Fargate completa vs. un solo icono de ALB o de BD). Esto es distinto a la regla general de "ningún contenedor se estira más allá de su contenido" (que sigue aplicando a AWS Cloud/Region/VPC/AZ y a las cajas ECS/Fargate) — las SUBREDES HERMANAS dentro de una AZ son la excepción: se estandarizan al tamaño de la más exigente, no al de su propio contenido individual.

- **Cómo elegir la medida estándar:** calcula el tamaño mínimo que necesitaría, por su propio contenido, la subred MAS EXIGENTE (normalmente la subred privada de aplicación, que aloja la caja ECS/Fargate/tarea completa — ver "Jerarquía de anidamiento"). Ese es el tamaño estándar (`w`,`h`) que se aplica a TODAS las subredes de la AZ, incluidas las que tienen mucho menos contenido (pública con solo el ALB, datos con solo la BD). No inventes un tamaño mayor "por si acaso" — debe ser el mínimo que alcanza para la subred más exigente, ni un píxel más. Cuando el usuario pida reducir aún más el tamaño, revisa primero si los márgenes internos de la caja ECS/Fargate (entre el icono/tarea y el borde de su caja, y entre la caja y el borde de la subred) tienen aire de sobra — normalmente sí lo tienen y se pueden apretar antes de tocar cualquier otra cosa.
- **Tamaño y márgenes estándar ACTUALES (última referencia verificada, ajustada a mano por el usuario y confirmada por render limpio — usar estos valores como punto de partida por defecto en cualquier diagrama nuevo):**
  - Subred (cualquiera de las tres): `w=260, h=200` (bajó de `320x230` → `280x200` → **`260x200`**, la más reciente).
  - Margen horizontal ENTRE subredes hermanas: **~19px** (bajó del rango genérico 30-40px usado en iteraciones anteriores).
  - Margen interno de la caja ECS (entre el borde izquierdo de la subred y el borde izquierdo de `ecs_box`): **~15px** (bajó de ~25px).
  - Margen superior dentro de la subred antes del contenido (para dejar aire al título): sigue en ~34-40px.
  - Margen inferior dentro de la AZ, debajo de las subredes: se puede apretar a ~15px (antes ~30-40px).
  - Estos números son el nuevo punto de partida "por defecto", no un mínimo absoluto — si un diagrama nuevo tiene contenido más grande (más tareas ECS apiladas, iconos adicionales, o un NAT Gateway además del ALB en la pública), la subred correspondiente puede necesitar más espacio, y ese tamaño mayor se propaga a las tres por igual como siempre.
- **Cómo ubicar el contenido dentro de una subred con espacio de sobra:** en las subredes con menos contenido que el estándar (p. ej. la pública con el ALB, o la de datos con la BD), centra el icono horizontal y verticalmente dentro del área disponible (dejando el margen superior de ~35-40px para el título de la subred, igual que en cualquier otro contenedor con título) — no lo dejes pegado a una esquina ni en la posición que tenía cuando la subred era más pequeña. Cuando la subred pública aloja DOS iconos (ALB + NAT Gateway), apílalos verticalmente centrados como par, no los pongas lado a lado (ver "Flechas", nota sobre iconos apilados, y bug #15).
- **Por qué (razón dada por el usuario, aplícala como principio general, no solo para este diagrama):** subredes de tamaños distintos dentro de la misma fila se ven inconsistentes y sugieren visualmente una jerarquía o importancia que no existe — las tres subredes son igual de "importantes" arquitectónicamente (pública de entrada, privada de aplicación, privada de datos), así que deben verse como bloques iguales y predecibles, sin importar cuánto contenido tenga cada una.
- **Caso real corregido (historial completo de ajustes):** un diagrama tenía la subred pública en `130x150`, la privada de aplicación en `320x230` y la privada de datos en `150x230` — cada una dimensionada solo por su propio contenido, con anchos y altos distintos entre sí. El usuario lo señaló explícitamente ("las subnets deben tener las mismas dimensiones, no puede ser una más ancha, otra menos... debe ser lo más pequeño posible, claramente dándole el espacio suficiente para colocar componentes dentro"). Fix inicial: `320x230` (el tamaño que ya necesitaba la subred de aplicación) aplicado a las TRES, centrando ALB y BD en el espacio disponible de las otras dos. Luego el usuario pidió reducir más ("creo que se puede disminuir un poco el tamaño aún de las subnets") — se apretaron los márgenes internos de las cajas ECS/Fargate y el resultado quedó en `280x200`. Luego el usuario tomó ese archivo y lo ajustó él mismo a mano en draw.io (dimensiones, flechas, posiciones) y lo devolvió como la referencia de estilo/medidas definitiva ("este tipo de estilo y medidas es la que me gustaría") — ese archivo, verificado con un render limpio, es la referencia ACTUAL: subredes en `260x200`, margen entre subredes ~19px, margen interno de `ecs_box` ~15px. Más tarde, al agregar un NAT Gateway a la subred pública, el usuario pidió apilarlo arriba del ALB en vez de ponerlo al lado, para dejar más aire y legibilidad (ver bug #15).
- Aplica esta regla por defecto en cualquier diagrama nuevo con dos o más subredes hermanas dentro de una AZ, no solo cuando el usuario lo pida.

## Backend siempre en subred privada — la subred pública es solo de paso (regla arquitectónica, no visual; bug real corregido)

**Un backend (ECS/Fargate/tarea, o cualquier servicio de cómputo que procese lógica de negocio) NUNCA va en la subred pública — siempre en una privada.** Esto no es una preferencia de estilo: una subred pública tiene ruta directa a/desde el Internet Gateway, así que cualquier cosa ahí es potencialmente alcanzable desde internet. El patrón correcto es:

- **Subred pública = capa de PASO/ENTRADA-SALIDA únicamente.** Normalmente contiene el **Load Balancer (ALB)**, que es el único componente diseñado para recibir tráfico público y reenviarlo hacia adentro, y opcionalmente un **NAT Gateway** si el backend necesita salida a Internet (descargar paquetes, actualizaciones, llamar APIs externas) sin exponerse él mismo directamente. Ninguno de los dos aloja lógica de aplicación ni datos.
- El flujo de red correcto es: actor externo → Internet Gateway → ALB (subred pública) → backend en ECS/Fargate (subred privada de aplicación) → base de datos (subred privada de datos, ver regla siguiente). Para el sentido inverso (egreso), el flujo es: backend (subred privada de aplicación) → NAT Gateway (subred pública) → Internet Gateway → Internet. El ALB y el NAT Gateway son los únicos puentes entre la capa pública y las privadas.
- Si el usuario pide agregar un nuevo servicio de cómputo (otro microservicio, una función Lambda que procese lógica de negocio, etc.), va en una subred privada de aplicación por defecto, salvo que sea explícitamente un recurso de borde/entrada como un segundo load balancer o un NAT Gateway.
- **Caso real corregido:** un diagrama inicial (hecho por el usuario a mano) tenía la caja ECS/Fargate completa dentro de la subred pública, dejando el backend expuesto directamente al segmento con ruta a internet. El usuario lo detectó explícitamente ("Porque colocaste el backend en una subnet publica? eso esta mal. Un backend siempre debe ir en una subnet private y debes colocar una subnet public por donde pase.") y se corrigió moviendo TODO el subárbol ECS/Fargate/tarea a una subred privada, dejando la subred pública con solo el ALB (más tarde también el NAT Gateway, ver bug #15).

## Backend y base de datos en subredes privadas SEPARADAS — capas app y datos (regla arquitectónica, bug real corregido)

**El backend (ECS/Fargate/tarea) y la base de datos NUNCA comparten la misma subred, aunque ambas sean privadas.** Van cada uno en su propia subred privada, como hermanas dentro de la misma AZ (ver "Subredes lado a lado dentro de la AZ" y "Tamaño estándar de subredes"):

- **Subred privada de APLICACIÓN**: aloja la caja ECS/Fargate/tarea (el backend). No tiene ruta directa al Internet Gateway, pero sí puede llegar a la subred de datos y a la subred pública (para su egreso vía NAT Gateway) dentro de la misma VPC.
- **Subred privada de DATOS**: aloja la(s) base(s) de datos (p. ej. RDS MySQL) y cualquier otro recurso de persistencia. Es la capa más aislada — solo el backend en la subred de aplicación debe poder alcanzarla.
- **Por qué (segmentación en profundidad, no solo "todo detrás del ALB"):** aunque el backend ya está protegido de internet por estar en una subred privada, separarlo de la base de datos en su PROPIA subred permite aplicar reglas de red (NACLs/security groups) distintas y más estrictas a la capa de datos — por ejemplo, que solo acepte tráfico desde la subred de aplicación y en el puerto de la base de datos, nada más.
- El flujo de red de 3 capas queda: actor → IGW → ALB (subred pública) → backend (subred privada de aplicación) → base de datos (subred privada de datos).
- **Caso real corregido:** un diagrama (ya corregido una vez para sacar el backend de la subred pública) dejó el backend y la base de datos juntos dentro de UNA sola subred privada. El usuario lo señaló explícitamente ("no puede quedar la base de datos y el backend desde la misma subnet, deben ser dos subnet privadas diferentes para back y base de datos") y preguntó qué propósito cumplía entonces la subred pública si el backend ya estaba en la privada — la respuesta es que la subred pública sigue siendo necesaria como el ÚNICO punto con ruta al Internet Gateway (el ALB debe ser alcanzable desde internet; el backend y la BD, no). Fix: se dividió la subred privada en dos hermanas — "Subred privada (app)" con la caja ECS/Fargate/tarea, y "Subred privada (datos)" con la base de datos — y se recalcularon en cascada los anchos de AZ/VPC/Region/Cloud para acomodar la subred nueva, además de re-enrutar la flecha `task → db` hacia la nueva posición de la BD.
- Aplica esta separación por defecto en cualquier diagrama nuevo con backend + base de datos, no solo cuando el usuario lo pida — son siempre subredes privadas DISTINTAS, una por capa (aplicación, datos), además de nunca ser la pública.

## Frontend web (SPA) nunca en una subred: se sirve desde S3 detrás de CloudFront (regla arquitectónica, bug real corregido)

**Un frontend web estático (SPA compilada: React, Vue, Angular, etc.) NUNCA va como tarea ECS/Fargate en la subred privada de aplicación, ni en ninguna otra subred.** Es contenido estático que descarga el navegador del usuario, no un servicio de backend.

- La SPA va en un bucket **Amazon S3 privado** (sin acceso público) servido por **Amazon CloudFront** con OAC (Origin Access Control). CloudFront es el único que puede leer el bucket.
- El bucket de la SPA va dentro de la Region pero FUERA de la VPC, en la fila de servicios regionales (ver "Servicios regionales fuera de la VPC"), con `label_pos: right` y una etiqueta tipo `"Amazon S3<br>(Web App SPA)"`.
- En la caja Fargate quedan SOLO los servicios de backend (APIs, workers, servicios de análisis). Al quitar la tarea del frontend, recalcula el alto de `fargate_box`, `ecs_box` y el tamaño estándar de subredes, y propágalo en cascada.
- **Caso real corregido:** un diagrama puso la "Web App (SPA)" como tarea `ecs_task` dentro de Fargate en la subred privada de aplicación. El usuario lo señaló ("Ojo, la web (SPA) nunca puede ir en una red privada, podemos colocarlo en s3"). Fix: la SPA pasó a un bucket S3 en la fila regional, servida por CloudFront con OAC, y Fargate quedó solo con la API y el servicio predictivo.

## Punto único de entrada: los clientes solo hablan con CloudFront (regla arquitectónica, bug real corregido)

**Cuando el diagrama tiene CloudFront, NINGÚN actor externo conecta directamente con el Internet Gateway ni con el ALB.** CloudFront es el único punto de entrada y reparte el tráfico por ruta entre sus orígenes:

- `/*` → bucket S3 de la SPA (origen privado con OAC).
- `/api/*` → ALB (a través del Internet Gateway).
- Flujo completo: actor → CloudFront → Internet Gateway → ALB (subred pública) → backend (subred privada de aplicación) → base de datos (subred privada de datos). La etiqueta de la flecha ALB → backend indica solo la ruta de API (p. ej. `"HTTPS<br>/api"`).
- El ALB debe aceptar tráfico solo de CloudFront (security group restringido a la *managed prefix list* de CloudFront, o un encabezado secreto que solo CloudFront envía). No hace falta dibujarlo, pero menciónalo en la respuesta al usuario como táctica de seguridad. Si se pide WAF, va asociado a CloudFront.
- Excepción: el login con Cognito Hosted UI usa su propio dominio, así que la flecha directa actor → Cognito (`"Login (OIDC)"`) se mantiene. Menciónalo por si en el diseño del usuario el login pasa por la misma SPA.
- Vocabulario: el usuario puede llamar "API gateway" al Internet Gateway. Si el diagrama no tiene Amazon API Gateway, aclara la diferencia en la respuesta.
- **Caso real corregido:** tras mover la SPA a S3 + CloudFront, los actores seguían conectados directamente al Internet Gateway. El usuario lo señaló ("¿por qué los clientes pasan directamente al api gateway? ¿no debería pasar primero por CloudFront y luego llegar al api gateway?"). Fix: se quitaron las flechas actor → IGW; los actores van solo a CloudFront, y CloudFront tiene dos flechas: `/*` hacia el bucket de la SPA y `/api/*` hacia el IGW.

## Alineación del camino de entrada en un mismo eje horizontal (regla de layout verificada con el usuario, bug real corregido)

**Los elementos del camino de entrada (actores, CloudFront si existe, Internet Gateway y ALB) van centrados en el MISMO eje horizontal:** centro Y de CloudFront = centro Y del IGW = centro Y del ALB. Los actores se reparten simétricamente arriba y abajo de ese eje (p. ej. ±120px), de modo que CloudFront quede centrado verticalmente entre ellos.

- **CloudFront es un servicio global de borde:** va dentro de `AWS Cloud` pero FUERA de la Region (`parent` = id de la Cloud), en una franja a la izquierda de la Region. Deja ≈150-170px entre el borde izquierdo de la Cloud y el de la Region para que quepan el icono y su etiqueta. NUNCA en la fila de servicios regionales de arriba, junto a Cognito/S3/SNS.
- Calcula la Y de CloudFront a partir de la Y absoluta del IGW con el script de coordenadas absolutas (ver "Flechas"). No la fijes a ojo ni antes de conocer la posición final del IGW.
- **Entradas de los actores a CloudFront:** el actor de arriba entra por ARRIBA y el de abajo por ABAJO, nunca los dos por el mismo lado. Actor de arriba: `exit=[1,0.5]`, `points=[[x_cf + 0.3*w_cf, y_centro_actor]]`, `entry=[0.3,0]`. Actor de abajo: igual, con `entry=[0.3,1]`. CloudFront usa `label_pos: left`, porque arriba y abajo los ocupan los actores y la derecha las salidas.
- **CloudFront → IGW:** flecha recta, `exit=[1,0.5]` → `entry=[0,0.5]`. Como entra por la izquierda del IGW, en este caso el IGW usa `label_pos: bottom` en vez del `left` de la tabla por defecto (regla de etiqueta lateral, ver "Flechas"). IGW → ALB también recta, a la misma altura.
- **CloudFront → bucket de la SPA:** sale por ARRIBA, del lado opuesto a la entrada del actor (`exit=[0.8,0]`), sube por la franja de la Cloud hasta la altura del centro del bucket y entra por su izquierda (`entry=[0,0.5]`). Deja ≥120px entre la franja de CloudFront y el bucket para que quepa la etiqueta (`"/* (SPA)<br>origen OAC"`).
- **ALB y NAT apilados en la subred pública:** el ALB va en la fila del eje de entrada y el NAT se alinea con la salida de egreso de la caja ECS (`ecs_box` `exit=[0,0.85]` → NAT `entry=[1,0.5]`, recta). Si eso deja el ALB arriba y el NAT abajo (al revés del ejemplo del bug #15), está bien: la alineación manda sobre el orden, siempre que sigan apilados en la misma columna y ninguna flecha cruce al vecino.
- **Caso real corregido:** CloudFront quedó en la fila superior de servicios regionales, lejos de los clientes y del IGW. El usuario lo señaló ("¿Por qué CloudFront queda tan arriba? ¿Por qué no queda centrado a los clientes y al internet gateway?"). Fix: CloudFront pasó a la franja de la Cloud a la izquierda de la Region, alineado con el IGW y el ALB y centrado entre los dos actores; el IGW cambió su etiqueta a `bottom`.

## Servicios regionales fuera de la VPC (Cognito, S3, SNS, etc.): fila superior de la Region

- Van en una fila horizontal en la parte superior de la Region, todos con `label_pos: right`. Usa una `y` relativa ≈70 para dejar libre la franja entre el título de la Region y los iconos: ahí pasa el corredor horizontal del login actor → Cognito (`y ≈ y_region + 30`, entrando por ARRIBA de Cognito con `entry=[0.5,0]`).
- Deja ≈75px entre el borde inferior de la fila y el borde superior de la VPC. Ahí giran las flechas que suben desde la caja ECS. Cada flecha gira a una altura distinta (p. ej. +42 y +58 bajo la fila), y la que tiene su icono justo encima sube recta sin girar.
- Las flechas salen del borde superior de `ecs_box` en fracciones que queden a la DERECHA del título de la subred de aplicación y del título centrado de la AZ (p. ej. `0.72`, `0.85`, `0.97`), nunca atravesando esos textos. Coloca el icono que va recto (p. ej. el bucket de datos) con su centro X exactamente sobre su punto de salida.
- La etiqueta de la flecha recta se lleva con `label_offset` (≈`[0.7, 0]`) al tramo alto, por encima de donde giran las otras flechas, para que no tape las líneas vecinas.

## Flechas

Todas las conexiones usan: `edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#666666;labelBackgroundColor=#ffffff;` (gris, ortogonal, **con fondo blanco en la etiqueta — ver bug real #10**). Especifica `exit`/`entry` cuando el enrutado por defecto no sea claro (p. ej. cuando la línea debería salir por un lado específico para no atravesar otras cajas), y usa `points` para forzar un desvío cuando la conexión cruza varios niveles de anidamiento.

**Nota sobre cuándo SÍ hace falta un `points` explícito (afinado tras revisar el archivo final ajustado a mano por el usuario):** con el layout más compacto (subredes 260x200, márgenes ~19px), varias conexiones que antes necesitaban un waypoint manual (p. ej. actor→Cognito, tarea→Cognito) renderizaron limpias en el archivo final del usuario usando SOLO `exit`/`entry` (lado + fracción), sin `points`. Esto no cambia la regla de fondo — sigue siendo obligatorio fijar `exit`/`entry` explícitos siempre que dos flechas compartan origen/destino o crucen cerca de una etiqueta lateral — pero significa que `points` es una herramienta para cuando el render (¡siempre verificado renderizando, nunca asumido!) muestre un cruce o rodeo, no un paso obligatorio en cada flecha que cruza niveles de anidamiento. Regla práctica: define primero `exit`/`entry`, renderiza, y solo agrega `points` si el resultado muestra un problema real.

**Cuando dos iconos van APILADOS VERTICALMENTE dentro de la misma subred/caja (p. ej. un NAT Gateway arriba de un ALB, para dejar la fila más abierta y legible — pedido real del usuario: "Porque no colocas el nat gateway encima del alb, para que tenga más espacio, quede más abierto mejor legible. Es tener cuidado con esos detalles, no coloques cosas encima de otras"), la flecha que conecta uno de ellos con un elemento de OTRA subred casi nunca debe entrar/salir por el lado que da hacia el otro icono apilado (arriba/abajo), porque cualquier ruta que pase por esa columna en la altura del icono vecino lo atraviesa visualmente — hay que rodear por un lado lateral (izquierda/derecha) que quede fuera de la columna que ocupan ambos iconos, o entrar/salir por el lado opuesto al vecino (arriba del de arriba, abajo del de abajo) si hay espacio.** Además, cuando la conexión tiene que cruzar el hueco ENTRE dos subredes hermanas y ya existe otra flecha (p. ej. la de JWKS/Cognito) que usa ese mismo hueco como corredor vertical en un rango de alturas amplio, cruza el hueco a una altura que quede CLARAMENTE fuera del rango vertical que ocupa esa otra flecha (por debajo de su punto de salida más bajo, o por encima de su punto de entrada más alto) — no basta con offsetear unos pocos píxeles dentro del mismo rango; primero identifica dónde sale y dónde entra la flecha ya existente. Caso real: al agregar un NAT Gateway apilado arriba del ALB en la subred pública, la flecha de egreso del backend (`ecs_box → nat`) debía cruzar desde la subred de aplicación hasta la subred pública; cruzar el hueco a la altura del icono (~y=310 abs) coincidía con el rango vertical de la flecha `task→cognito` (JWKS), que usa ese mismo hueco como corredor entre y≈145 y 396. Fix: se hizo cruzar el hueco por DEBAJO de ese rango (y≈432, en el margen inferior de la AZ), y luego se subió por una columna lateral libre a la derecha de la columna NAT/ALB (nunca directamente debajo de ambos) para entrar al NAT Gateway por el lado derecho, evitando atravesar el ALB. Ver bug #15.

**La etiqueta de una flecha con una ruta en forma de "escalón" con varios tramos (vertical-horizontal-vertical) puede aterrizar, con el `label_offset` por defecto, encima de un icono aunque la LÍNEA en sí ya lo esquive — revisa siempre con un render.** Recuerda que la convención de `label_offset: [a, o]` usa `a` en el rango -1..1 con **0 = punto medio de la ruta completa (no 0 = inicio)**; para moverla hacia el tramo más vacío de una ruta en escalón, prueba valores negativos (hacia el origen) o positivos (hacia el destino) e itera con renders, en vez de asumir cuál tramo corresponde a qué fracción — el mapeo entre fracción y tramo no es obvio a simple vista cuando la ruta tiene varios segmentos de longitudes distintas.

**Toda etiqueta de flecha lleva fondo blanco opaco (`labelBackgroundColor=#ffffff`), sin excepción — bug real corregido, se veía "tachada".** Por defecto, draw.io dibuja el texto de una etiqueta de flecha SIN fondo, así que si la línea pasa exactamente por debajo del texto (lo normal, ya que el punto medio de la ruta suele coincidir con donde se ancla la etiqueta), la línea atraviesa visualmente las letras y el texto se ve tachado (le pasó a "OIDC", "SQL" y "1. Login (redirect OIDC)" en un diagrama real). Esto es independiente de si la ruta en sí está bien enrutada — puede pasar incluso en una flecha perfectamente recta. Fix: agregar `labelBackgroundColor=#ffffff;` al estilo base de TODAS las flechas (ya está en el script generador de abajo) — no requiere ningún campo nuevo en el JSON, es automático para cada edge.

**Evitar que las flechas se crucen con la etiqueta de un icono, sea en el lado de SALIDA (origen) o de ENTRADA (destino):** si un icono tiene `label_pos: "left"` o `"right"`, su etiqueta ocupa una banda horizontal completa junto a ese lado del icono, del mismo alto que el icono. Cualquier flecha que ENTRE o SALGA por ESE MISMO lado (aunque uses `entryY`/`exitY` distintos para separarlas entre sí) va a cruzar esa banda — separar solo el `entryY`/`exitY` NO basta, hay que cambiar el LADO.

- **Caso de ENTRADA lateral** (verificado, funciona con un solo waypoint): si el icono tiene `label_pos: "left"` y las flechas ENTRAN desde ese lado, entra por ARRIBA o por ABAJO (`entryX=0.5,entryY=0` o `entryY=1`, nunca `entryX=0`), con un waypoint en `(centro_x_del_icono, y_de_salida_del_origen)` para que la línea suba/baje DENTRO de la columna del propio icono antes de entrar. Ejemplo real (Internet Gateway, dos actores entrando): actor de arriba → `exit=[1,0.5]`, `points=[[cx, y_actor]]`, `entry=[0.5,0]`; actor de abajo → `exit=[1,0.5]`, `points=[[cx, y_actor]]`, `entry=[0.5,1]`. `cx` es la X absoluta del centro del icono destino.
- **Caso de SALIDA lateral cuando el icono de origen está SOLO (sin otros iconos apilados encima/debajo dentro de la misma caja)**: si sale hacia el lado de su propia etiqueta, cambia el lado de salida a arriba/abajo (`exitX=0.5,exitY=0` o `exitY=1`) con un waypoint que suba/baje hasta la altura del destino, alineado con el centro X del origen, y de ahí cruce recto — igual que el caso de entrada pero en espejo.
- **Caso de SALIDA lateral cuando el icono de origen está DENTRO de una caja con OTROS iconos apilados arriba o abajo (como `ecs_task` dentro de la caja Fargate, que a su vez está dentro de la caja ECS, con los iconos ECS y Fargate apilados arriba de la tarea) — CUIDADO, esto NO se resuelve solo cambiando a "arriba": el resultado real seguía cruzando visualmente las filas de ECS y Fargate, porque CUALQUIER altura entre esas filas apiladas todavía pasa por algún icono o etiqueta — "arriba" no es automáticamente una zona libre cuando hay más contenido apilado en esa dirección. La solución verificada es salir por el lado OPUESTO a donde está apilado el resto del contenido (en este caso, por ABAJO, ya que ECS y Fargate están arriba de la tarea) y llevar la línea, con un waypoint, al MARGEN VACIO que queda dentro de la caja contenedora más externa (la caja ECS), entre el borde inferior del último icono/etiqueta y el borde inferior de esa caja. Calcula esa franja como: borde inferior absoluto del último icono apilado hasta el borde inferior absoluto de la caja contenedora externa; el waypoint va a la mitad de ese rango. Ejemplo real verificado (tarea `ecs_task` saliendo hacia una BD en OTRA subred, a su derecha, con las tres subredes ya del mismo tamaño estándar): tarea centro absoluto x=996, borde inferior de la tarea en y=422; caja ECS (la contenedora externa) termina en y=450 — margen libre entre 422 y 450, se usó y=436; BD (destino, ya en la subred de datos) centro absoluto x=1440.5. Estilo: `exit=[0.5,1]` (sale por abajo de la tarea), `points=[[996,436],[1440.5,436]]` (baja al margen libre de la caja ECS, cruza horizontal — atravesando el hueco vacío entre ambas subredes — hasta la columna X de la BD), `entry=[0.5,1]` (entra por abajo de la BD) — resultado: una línea corta en forma de escalón que no atraviesa ningún icono ni etiqueta.
- Regla práctica general para este último caso: cuando el icono de origen/destino está apilado junto a otros dentro de una misma caja, el waypoint de desvío NUNCA debe ser "el lado opuesto a la etiqueta" sin más — debe caer en un hueco realmente libre de contenido. Si el destino ahora vive en OTRA subred (p. ej. tras separar app y datos), el segmento horizontal que cruza el hueco ENTRE subredes es zona libre por definición.
- **Caso de ENTRADA desde AFUERA de un contenedor grande hacia un icono anidado adentro (bug real corregido — flecha "da mucha vuelta"):** cuando un actor/elemento FUERA del `AWS Cloud` conecta con un icono anidado varios niveles adentro (p. ej. Usuario → Cognito, con Cognito dentro de Region dentro de AWS Cloud), NUNCA dejes que el router por defecto (sin waypoints) resuelva el cruce de esos niveles SIN VERIFICAR PRIMERO CON UN RENDER. En vez de asumir, identifica el margen VERTICAL libre más cercano entre los elementos que ya existen fuera del contenedor grande y úsalo como corredor si el render muestra un rodeo; en un layout ya compacto puede que el router directo baste (ver nota sobre `points` opcional al inicio de esta sección) — renderiza y decide según el resultado, no según la regla sola. Ejemplo real verificado donde SÍ hizo falta el corredor: Usuario (fuera del Cloud, abajo-izquierda) → Cognito (dentro de Region, dentro de AWS Cloud): corredor usado = franja libre entre las cajas de Google/Microsoft Entra ID (terminan en `x=190`) y el borde izquierdo del AWS Cloud (`x=260`), es decir una columna vertical en `x≈210`. Estilo: `exit=[0.5,0]`, `points=[[210, y_actor],[210, y_cognito_entry]]`, `entry=[0,0.1]` — resultado: un recorrido corto en escalón en vez de un rodeo por encima de todo el diagrama. Nota: si Cognito se reposiciona más adelante (p. ej. para alinearse con otro corredor, o si el layout se vuelve más compacto), este mismo tramo puede dejar de hacer falta — vuelve a verificar con un render antes de mantenerlo o quitarlo.
- **La etiqueta (texto) de una flecha NO sigue automáticamente su ruta libre de cruces — hay que revisarla por separado (bug real corregido):** draw.io coloca el TEXTO de la etiqueta por defecto en el punto medio geométrico de TODA la ruta — un punto que puede caer perfectamente sobre la etiqueta de OTRO elemento aunque la línea en sí ya los esquive limpiamente. Antes de entregar, revisa DÓNDE cae el punto medio de cada ruta con texto contra las etiquetas de los demás elementos; si cae encima de algo, usa `label_offset: [a, o]` en el edge del JSON — `a` es la posición a lo largo de la ruta (-1 a 1, 0 = punto medio) y `o` es un desplazamiento perpendicular en píxeles — y llévala a un tramo del corredor que esté realmente vacío.
- La regla general de "si dos flechas comparten destino, dales `entry` distintos" sigue aplicando, pero cuando el icono tiene etiqueta lateral, la separación tiene que ser de LADO (arriba vs. abajo), no solo de punto dentro del mismo lado.
- **Dos flechas que entran a un icono destino por el MISMO lado casi en el mismo punto (p. ej. ambas por la izquierda, una en `entryY=0` y otra en `entryY=0.1`) se ven como si se encimaran o "no conectaran bien" — bug real corregido.** Una separación de menos de ~20-25px entre dos puntos de entrada/salida no es suficiente para distinguirlas visualmente, sobre todo si además convergen desde direcciones parecidas (dos flechas que vienen ambas de la izquierda-arriba, por ejemplo). Cuando esto pase, la solución preferida es moverlas a LADOS distintos del icono (una por arriba, otra por la izquierda), no solo separar más la fracción `entryY` dentro del mismo lado — igual que la regla de arriba para iconos con etiqueta lateral, pero aplicada aquí a cualquier caso de dos o más flechas convergiendo cerca. Caso real: en un diagrama, la flecha "1. Login" (actor → Cognito) entraba en `entry=[0,0.1]` y la flecha "OIDC" de Google entraba en `entry=[0,0]` — casi el mismo punto, en la esquina superior izquierda de Cognito. Fix: la flecha de Google se movió a entrar por ARRIBA (`entry=[0.7,0]`) en vez de por la izquierda, dejando "1. Login" sola en el lado izquierdo (con su propio `entryY` reubicado a `0.25` para más aire). Esta separación por lado se mantuvo intacta en la versión final ajustada a mano por el usuario (Google sigue entrando por arriba, Login y el otro IdP por la izquierda a alturas distintas) — confírmalo así en cualquier diagrama nuevo con más de un IdP.
- **Dos flechas que salen o entran por el MISMO lado de un mismo icono a alturas parecidas (aunque técnicamente distintas) recorren un tramo paralelo muy junto y se ven como una "línea doble" — bug real corregido.** Esto pasa incluso cuando cada flecha individualmente está bien enrutada: si ambas tocan, por ejemplo, el lado izquierdo de un icono con solo 5-6px de diferencia en la entrada/salida, sus tramos horizontales corren prácticamente pegados antes de separarse, y se leen como una sola línea gruesa o corrida. Fix: separar los puntos de contacto del mismo lado por al menos ~15-20% de la altura del propio icono (usar fracciones como `0.15` y `0.85` en vez de `0.3` y `0.5`, por ejemplo) para que los dos tramos sean visualmente distinguibles antes de converger. Caso real: en la tarea `ecs_task` (28px de alto), la flecha ALB→task entraba en `entryY=0.3` y la flecha task→Cognito (JWKS) salía en `exitY=0.5` — solo 5.6px de diferencia — y ambas corrían paralelas y pegadas por el interior de la caja ECS antes de separarse. Fix: `entryY=0.15` para ALB→task y `exitY=0.85` para task→Cognito, separándolas casi al máximo del alto del icono. Esta separación se mantuvo en la versión final del usuario.
- Deja al menos 60-80px de separación horizontal entre un icono con etiqueta lateral y el elemento de origen/destino de sus flechas, para que el texto tenga espacio propio.
- **Dirección de la flecha entre el backend y un IdP (Cognito u otro) para validación de JWT — principio conceptual, no solo visual (bug real corregido):** el IdP (Cognito) NUNCA llama al backend para "validar" nada — el backend valida el JWT LOCALMENTE (firma + issuer + audience) usando las llaves públicas (JWKS) que el IdP expone en un endpoint público, y solo necesita pedirlas una vez (las cachea). Por eso la flecha correspondiente siempre va del BACKEND hacia el IdP (`source` = backend/tarea, `target` = Cognito/IdP), nunca al revés, y su etiqueta debe describir la obtención del JWKS (p. ej. `"Obtiene JWKS<br>(cacheado)"`), no una "validación" que el IdP hace sobre el backend. Aplica esto por defecto en cualquier diagrama con Cognito/IdP + validación de JWT en el backend.
- **Cuando una flecha entra a un icono destino siguiendo un corredor recto (vertical u horizontal) ya usado para esquivar otros elementos, alinea el icono con ese corredor — no dejes un "codo" final pegado a la entrada (bug real corregido, se ve "torcido").** Si el último tramo de la ruta llega por un corredor en una coordenada fija pero el punto de entrada del icono destino está en una coordenada distinta, el router agrega un jog final de lado. La solución NO es agregar más waypoints para disimular el jog — es mover el ICONO DESTINO para que su centro (o el borde relevante) coincida exactamente con la coordenada del corredor.
- **Cuando se mueve, divide o reescala un contenedor grande (p. ej. sacar el backend de la subred pública, partir una subred privada en app+datos, o estandarizar el tamaño de todas las subredes), TODAS las flechas que tocan algo dentro de ese subárbol necesitan revisión, no solo las que cambian de contenedor padre.** Un cambio de coordenadas o de jerarquía de esta magnitud desplaza las columnas/filas que otras flechas usaban como corredores libres, así que hay que re-verificar: (a) que ningún corredor recién movido ahora cruza un icono/etiqueta que antes evitaba, y (b) que el punto medio de cada ruta con etiqueta sigue sin caer encima de otro texto — ver los bugs reales corregidos de subredes en "Bugs reales corregidos".
- **NUNCA recalcules a mano, "de memoria", las coordenadas absolutas de `exit`/`entry`/`points` después de reescalar o mover contenedores — un desfase de solo 3-4px entre el waypoint y el punto de entrada real genera un jog/torcedura visible justo en ese punto (bug real corregido).** El error típico: se reduce el tamaño de un icono o se le cambia su `y` relativo dentro de su caja padre (p. ej. `task.y` de 44 a 40), pero el waypoint de una flecha que lo referencia se deja con el valor viejo (calculado para la posición anterior) — la flecha sigue "conectando" funcionalmente (el `source`/`target` no cambia), pero el waypoint intermedio ya no coincide con la altura/columna real de entrada, y el router agrega un jog extra justo ahí para compensar, que se ve como un doblez o cruce raro pegado al borde de un contenedor. Fix / prevención: después de fijar TODAS las coordenadas finales del `spec.json` (incluida cualquier última reducción de tamaño), computa las coordenadas absolutas de cada elemento con un script corto (sumando `x`/`y` relativos subiendo por la cadena de `parent` hasta `"1"`) ANTES de escribir a mano los `points`/`exit`/`entry` de las flechas — nunca de memoria ni por aritmética mental. Ejemplo de script de apoyo (pégalo tal cual cuando necesites verificar):\n  ```python\n  import json\n  spec = json.load(open("spec.json"))\n  els = {e["id"]: e for e in spec["elements"]}\n  def abs_origin(id_):\n      e = els[id_]\n      if e.get("parent", "1") == "1":\n          return (e["x"], e["y"])\n      px, py = abs_origin(e["parent"])\n      return (px + e["x"], py + e["y"])\n  for id_ in els:\n      ox, oy = abs_origin(id_)\n      e = els[id_]\n      print(id_, ox, oy, "right=", ox+e.get("w",0), "bottom=", oy+e.get("h",0))\n  ```\n  Usa esa salida — no cálculos manuales — para fijar cada `points`/`entryY`/`exitY` que dependa de una posición absoluta.

## Bugs reales corregidos (revisar que el script de abajo los siga teniendo)

1. **Doble escape de `<br>` en etiquetas de FLECHAS (no de iconos) — aparecía literalmente el texto `<br>` en vez de un salto de línea.** Causa raíz: `edge_el()` pasaba la etiqueta por `t()` (que hace `html.escape`, convirtiendo `<br>` en `&lt;br&gt;`) ANTES de pasarla a `quoteattr()` — `quoteattr` vuelve a escapar el `&` de `&lt;` a `&amp;`, dejando `&amp;lt;br&amp;gt;` en el XML final, que draw.io muestra como el texto literal `<br>`. Fix verificado: en `edge_el()`, usar la etiqueta CRUDA (`d.get("label", "")`) igual que `icon_el()`, sin pasarla por `t()`.
2. **Icono cerca del título de su contenedor (Cognito dentro de Region) con etiqueta `bottom` competía visualmente con el texto del título del contenedor.** Fix: usar `label_pos: right` (o `left`) para iconos que van cerca del borde superior de un contenedor con título, y dejar 30-35px de aire respecto a ese borde.
3. **Flecha de un actor externo hacia un icono anidado varios niveles adentro daba un rodeo enorme por encima de todo el contenedor externo.** Fix: enrutar por el margen/corredor libre más cercano entre elementos existentes, no dejar que el router por defecto decida sin verificar con un render.
4. **Etiqueta de una flecha (aunque la línea ya esquivara los iconos) caía encima del texto de otro elemento porque el punto medio de la ruta coincidía con esa fila.** Fix: revisar el punto medio de cada ruta con texto contra las etiquetas de los demás elementos, y usar `label_offset` para desplazarla si hace falta.
5. **Flecha de validación de JWT dibujada en la dirección conceptual equivocada (Cognito → backend, "Valida JWT").** Fix: invertir `source`/`target` para que la flecha vaya del backend hacia Cognito, y renombrar la etiqueta a algo como `"Obtiene JWKS<br>(cacheado)"`. Aplica esto por defecto en cualquier diagrama con Cognito/IdP + validación de JWT en el backend.
6. **Flecha entrando "torcida" a un icono (jog final pegado a la entrada) aunque conectara bien funcionalmente.** Fix: mover el icono destino para que su centro (o el borde de entrada relevante) coincida con la coordenada del corredor. Nunca "disimular" esto con más waypoints; el icono es lo que se mueve.
7. **Backend (caja ECS/Fargate/tarea) colocado en la subred PÚBLICA en vez de una privada — error arquitectónico real, no solo visual, detectado explícitamente por el usuario.** Fix: mover TODO el subárbol ECS/Fargate/tarea a una subred privada, dejando la subred pública con únicamente el ALB como capa de paso — ver "Backend siempre en subred privada" arriba. Aplica esta regla por defecto en cualquier diagrama nuevo.
8. **Backend y base de datos colocados juntos en la MISMA subred privada — deben ser subredes privadas separadas (app y datos), error arquitectónico real detectado explícitamente por el usuario.** Fix: se dividió la subred privada en dos hermanas dentro de la misma AZ — una de aplicación (backend) y otra de datos (BD) — recalculando en cascada los anchos de AZ/VPC/Region/Cloud y re-enrutando la flecha `task → db` — ver "Backend y base de datos en subredes privadas separadas" arriba. Aplica esta separación por defecto en cualquier diagrama nuevo con backend + base de datos.
9. **Subredes hermanas dentro de la misma AZ con tamaños distintos entre sí (cada una dimensionada solo por su propio contenido) — error de consistencia visual real, detectado explícitamente por el usuario.** Un diagrama tenía la subred pública en `130x150`, la privada de aplicación en `320x230` y la privada de datos en `150x230`. El usuario pidió que todas midieran igual, con el tamaño más pequeño posible que alcanzara para la subred más exigente. Fix: se estandarizó `320x230` (el tamaño de la subred de aplicación) para las tres, centrando ALB y BD en su espacio disponible, y recalculando en cascada AZ/VPC/Region/Cloud/página — ver "Tamaño estándar de subredes" arriba. Aplica esta regla por defecto en cualquier diagrama nuevo con dos o más subredes hermanas.
10. **Etiquetas de flecha sin fondo blanco — la línea las atravesaba y se veían "tachadas" (p. ej. "OIDC", "SQL", "1. Login (redirect OIDC)").** El usuario lo señaló como parte de "seguimos con el mismo problema[s], flechas torcidas, desalineadas, no conectan correctamente". Fix: se agregó `labelBackgroundColor=#ffffff;` al estilo base de TODAS las flechas en el script generador — ver "Flechas" arriba. Esto es automático para cualquier edge nuevo, no requiere ningún campo en el JSON.
11. **Dos flechas convergiendo casi en el mismo punto/lado de un icono destino (Google→Cognito y Login→Cognito, ambas entrando por la izquierda con solo ~5px de diferencia) — se veían encimadas, como si "no conectaran correctamente".** Fix: se movió una de las dos a entrar por un LADO distinto del icono (Google entra por ARRIBA en vez de por la izquierda), en vez de solo separar más la fracción dentro del mismo lado — ver "Flechas" arriba, caso de flechas convergentes.
12. **Dos flechas tocando el MISMO lado de un mismo icono a alturas muy parecidas (ALB→task entrando en `entryY=0.3` y task→Cognito saliendo en `exitY=0.5`, solo 5.6px de diferencia) — sus tramos corrían pegados y se veían como una "línea doble".** Fix: se separaron a `entryY=0.15` y `exitY=0.85` (casi los extremos del icono) — ver "Flechas" arriba.
13. **Waypoint de una flecha (ALB→task) calculado a mano y dejado con el valor viejo después de reducir el tamaño estándar de las subredes — el punto ya no coincidía exactamente con la nueva altura de entrada del icono, y el router agregaba un jog visible justo en el borde de la caja ECS.** Fix: recomputar SIEMPRE las coordenadas absolutas con un script (nunca a mano) inmediatamente después de fijar el tamaño final de cualquier elemento, antes de escribir los `points`/`entry`/`exit` — ver "Flechas" arriba, nota sobre reescalado.
14. **El usuario tomó el archivo entregado con los fixes #10-13 y lo ajustó él mismo a mano en draw.io (dimensiones, flechas, posiciones), devolviéndolo como la referencia de estilo/medidas definitiva ("este tipo de estilo y medidas es la que me gustaría").** Verificado con un render limpio (dos recortes de cerca sin superposiciones, líneas torcidas ni etiquetas encimadas). Cambios extraídos de ese archivo y adoptados como nuevo default: subredes de `280x200` bajaron a `260x200`; margen entre subredes hermanas de ~30px bajó a ~19px; margen interno de `ecs_box` de ~25px bajó a ~15px; algunas flechas que antes llevaban un `points` explícito (p. ej. actor→Cognito, tarea→Cognito) quedaron sin waypoints manuales y renderizan limpias en este layout más compacto (ver nota sobre `points` opcional en "Flechas"). También se observó que el archivo editado a mano dejó el `parent` de algunos elementos (la AZ, el ALB) desincronizado de su contenedor visual real, sin afectar el render — ver la nota sobre este artefacto de edición manual en "Jerarquía de anidamiento": al construir un `spec.json` nuevo, usa siempre el `parent` real, no el que traiga un archivo editado a mano.
15. **Al agregar un NAT Gateway para la salida a Internet del backend, el usuario pidió explícitamente apilarlo ARRIBA del ALB en vez de ponerlo al lado ("Porque no colocas el nat gateway encima del alb, para que tenga más espacio, quede más abierto mejor legible. Es tener cuidado con esos detalles, no coloques cosas encima de otras") — la primera versión los puso lado a lado dentro de la subred pública, cosa que el usuario consideró menos legible/abierta que apilarlos.** Además, la primera ruta de la flecha de egreso (`ecs_box → nat`) cruzaba el hueco entre subredes a una altura que coincidía con el rango vertical de la flecha JWKS existente (`task→cognito`), y su etiqueta aterrizó encima del icono NAT o del ALB en distintos intentos antes de dar con la posición correcta. Fix: NAT apilado directamente arriba del ALB (mismo eje X, ~15px de separación vertical entre ambos), con `label_pos: left` en el NAT (para no competir con la entrada lateral derecha de su propia flecha de egreso, que entra por la derecha); la flecha `ecs_box → nat` cruza el hueco entre subredes MUY por debajo del rango de la flecha JWKS (fuera de su span vertical, en el margen inferior de la AZ), sube por una columna lateral libre a la derecha de la columna ALB/NAT (nunca directamente debajo, para no atravesar el ALB), y entra al NAT por el lado derecho; su etiqueta se reubicó con `label_offset` a un tramo horizontal despejado por debajo de ambos iconos, verificado con render iterativo (probar, renderizar, ajustar `label_offset`, repetir) hasta confirmar que no había superposiciones. Ver "Flechas" arriba, nota sobre iconos apilados verticalmente.
16. **Frontend web (SPA) dibujado como tarea `ecs_task` dentro de Fargate, en la subred privada de aplicación — error arquitectónico detectado por el usuario.** Fix: la SPA pasó a un bucket S3 privado servido por CloudFront con OAC, y Fargate quedó solo con los servicios de backend — ver "Frontend web (SPA) nunca en una subred".
17. **Actores conectados directamente al Internet Gateway aunque el diagrama ya tenía CloudFront — el usuario pidió que todo el tráfico pasara primero por CloudFront.** Fix: los actores van solo a CloudFront, que enruta `/*` al bucket de la SPA y `/api/*` al IGW → ALB — ver "Punto único de entrada".
18. **CloudFront ubicado en la fila superior de servicios regionales, lejos del eje de los clientes y del IGW.** Fix: CloudFront en la franja de la Cloud fuera de la Region, con su centro Y igual al del IGW y el ALB y centrado entre los actores; el IGW con etiqueta `bottom` porque recibe la flecha por la izquierda; además se agregó `cloudfront` al diccionario `ICONS` del script (antes salía con el color por defecto `#232F3E` en vez del morado de Redes) — ver "Alineación del camino de entrada".

## Flujo de trabajo

1. **Reunir el contenido primero**: qué actores, qué región/VPC/AZs/subredes, qué servicios en cada subred, y las conexiones entre ellos.
2. **Definir la jerarquía `parent`** de cada elemento siguiendo la sección anterior — nunca aplanar todo a la raíz, y usar siempre el `parent` que refleje el anidamiento visual REAL (ver nota sobre archivos editados a mano en "Jerarquía de anidamiento"). Dentro de cada AZ, colocar las subredes como hermanas lado a lado (ver "Subredes lado a lado dentro de la AZ"), y recordar las TRES reglas de subredes: (a) el backend SIEMPRE va en una subred privada, nunca en la pública; (b) el backend y la base de datos van en subredes privadas DISTINTAS (app vs. datos); y (c) TODAS las subredes de una misma AZ tienen el mismo tamaño estándar, calculado sobre la subred más exigente — ver "Backend siempre en subred privada", "Backend y base de datos en subredes privadas separadas" y "Tamaño estándar de subredes". Si el backend necesita salida a Internet, agrega un NAT Gateway en la subred pública, apilado con el ALB (ver "Flechas", nota sobre iconos apilados). Si hay frontend web, va en S3 + CloudFront (nunca en una subred), y los actores entran solo por CloudFront, alineado con el IGW y el ALB (ver "Frontend web (SPA) nunca en una subred", "Punto único de entrada" y "Alineación del camino de entrada").
3. **Para cada icono de recurso**, revisar primero la tabla de iconos verificados (incluida su variante badge/nativa); si no está, usar la tabla de estimados (variante nativa por defecto) o pedir el fragmento XML real al usuario.
4. **Calcular coordenadas relativas de ADENTRO HACIA AFUERA**: primero el contenido más interno, LUEGO el tamaño estándar de subred (el que necesita la más exigente — usa `260x200` con márgenes de ~19px como punto de partida por defecto, ver "Tamaño estándar de subredes"), aplicado a TODAS las subredes de la AZ, y LUEGO cada contenedor que envuelve la AZ (AZ → VPC → Region → Cloud → página) con ancho/alto = extremo del hijo más lejano + margen. Si en una iteración posterior cambias el tamaño de una subred, recalcula en cascada TODOS los contenedores que la envuelven y revisa todas las flechas que dependían de las coordenadas viejas.
5. **Construir el JSON** con esa jerarquía de `parent`/coordenadas relativas (subredes lado a lado del mismo tamaño dentro de cada AZ, backend y BD siempre en subredes privadas distintas), dando `entry`/`exit` explícitos a cualquier flecha que comparta destino/origen con otra o que entre/salga por el mismo lado donde el icono tiene su etiqueta, y `label_offset` en cualquier flecha cuyo punto medio de ruta caiga sobre la etiqueta de otro elemento.
6. **Escribir el JSON** a un archivo y **ejecutar el script embebido** (`aws_drawio.py`) con `python3 aws_drawio.py spec.json salida.drawio`.
7. **Antes de fijar los `points`/`entry`/`exit` finales, computa las coordenadas absolutas de todos los elementos con un script corto** (ver ejemplo en "Flechas" arriba) — nunca a mano — sobre todo si el `spec.json` fue reescalado o reposicionado en una iteración anterior. Renderiza primero solo con `exit`/`entry` y agrega `points` únicamente si el render muestra un cruce o rodeo real (ver nota sobre `points` opcional en "Flechas").
8. **Validar el XML** con `xml.etree.ElementTree`: que todo `parent` referenciado exista, que las aristas referencien IDs existentes, que ningún icono use un `resIcon`/variante badge fuera de las tablas de este documento sin haberlo avisado al usuario, que el backend NO esté en la subred pública, que el backend y la BD estén en subredes privadas DISTINTAS, y que TODAS las subredes de cada AZ tengan el mismo `w`/`h`.
9. **Entregar el `.drawio`** al usuario, indicando en la respuesta cuáles iconos (si alguno) son "estimados" y podrían necesitar ajuste.

## Esquema del JSON de especificación

```json
{
  "title": "Nombre del diagrama",
  "page": [1700, 680],
  "elements": [
    {"id": "cloud", "kind": "cloud", "name": "AWS Cloud", "x":260, "y":20, "w":1163, "h":538, "parent": "1"},
    {"id": "region", "kind": "region", "name": "Region", "x":40, "y":60, "w":1087, "h":445, "parent": "cloud"},
    {"id": "vpc", "kind": "vpc", "name": "VPC", "x":40, "y":100, "w":1010, "h":316, "parent": "region"},
    {"id": "az1", "kind": "az", "name": "Availability Zone", "x":157, "y":130, "w":858, "h":255, "parent": "vpc"},
    {"id": "sub_pub", "kind": "public_subnet", "name": "Subred pública", "x":13, "y":40, "w":260, "h":200, "parent": "az1"},
    {"id": "sub_app", "kind": "private_subnet", "name": "Subred privada (app)", "x":292, "y":40, "w":260, "h":200, "parent": "az1"},
    {"id": "sub_data", "kind": "private_subnet", "name": "Subred privada (datos)", "x":571, "y":40, "w":260, "h":200, "parent": "az1"},
    {"id": "alb", "kind": "icon", "icon": "application_load_balancer", "label": "Application<br>Load Balancer", "label_pos": "bottom", "x":103, "y":100, "w":50, "h":50, "parent": "sub_pub"},
    {"id": "nat", "kind": "icon", "icon": "nat_gateway", "label": "NAT<br>Gateway", "label_pos": "left", "x":105, "y":40, "w":45, "h":45, "parent": "sub_pub"},
    {"id": "ecs_box", "kind": "box", "stroke": "#FF8000", "x":15, "y":34, "w":230, "h":142, "parent": "sub_app"},
    {"id": "fargate_box", "kind": "box", "stroke": "#FF8000", "x":10, "y":47, "w":200, "h":80, "parent": "ecs_box"},
    {"id": "igw", "kind": "icon", "icon": "internet_gateway", "label": "Internet<br>Gateway", "label_pos": "left", "x":10, "y":172.5, "w":45, "h":45, "parent": "vpc"},
    {"id": "cognito", "kind": "icon", "icon": "cognito", "label": "Amazon Cognito<br>User Pool", "label_pos": "right", "x":417, "y":36, "w":50, "h":50, "parent": "region"},
    {"id": "task", "kind": "icon", "icon": "ecs_task", "label": "App<br>container", "label_pos": "right", "font_size": 10, "x":12, "y":40, "w":28, "h":28, "parent": "fargate_box"},
    {"id": "db", "kind": "icon", "icon": "rds_mysql_instance", "label": "Base de datos", "label_pos": "bottom", "x":118, "y":95, "w":45, "h":45, "parent": "sub_data"},
    {"id": "cust", "kind": "actor", "label": "Customers", "x":76, "y":352, "w":45, "h":45, "parent": "1"}
  ],
  "edges": [
    {"from": "cust", "to": "igw", "parent": "1", "label": "Llamadas API", "exit": [1,0.5], "entry": [0.5,0]},
    {"from": "igw", "to": "alb", "parent": "1", "exit": [1,0.5], "entry": [0,0.5]},
    {"from": "alb", "to": "task", "parent": "1", "label": "HTTP(S)", "exit": [1,0.5], "entry": [0,0.15]},
    {"from": "task", "to": "db", "parent": "1", "label": "SQL", "exit": [0.5,1], "entry": [0.5,1]},
    {"from": "cust", "to": "cognito", "parent": "1", "label": "1. Login (redirect OIDC)", "exit": [0.5,0], "entry": [0,0.25]},
    {"from": "task", "to": "cognito", "parent": "1", "label": "Obtiene JWKS<br>(cacheado)", "exit": [0,0.85], "entry": [0.5,1], "label_offset": [0.5, 0]},
    {"from": "ecs_box", "to": "nat", "parent": "az1", "label": "Descarga de paquetes<br>(salida a Internet)", "exit": [0.05,1], "entry": [1,0.5], "label_offset": [-0.5, 30]}
  ]
}
```

Nota clave de este ejemplo (verificado, es el layout de 3 subredes del mismo tamaño ESTÁNDAR ACTUAL — `260x200`, márgenes ~19px — tal como quedó en el archivo que el usuario ajustó a mano y confirmó como "el estilo y medidas que me gustaría"; ver bug real #14, y con el NAT Gateway apilado sobre el ALB, ver bug #15): `sub_pub`, `sub_app` y `sub_data` son las TRES hijas directas de `az1` (mismo `parent`), lado a lado en ese orden, y las TRES miden el mismo `w`/`h` — el tamaño mínimo que necesita `sub_app` para alojar la caja ECS/Fargate/tarea completa; ese mismo tamaño se reutiliza en `sub_pub` (con `alb`+`nat` apilados y centrados) y en `sub_data` (con `db` centrado) en vez de dimensionarlas por su propio contenido, más pequeño. `sub_app.x` = `sub_pub.x` + `sub_pub.w` + margen (~19); `sub_data.x` = `sub_app.x` + `sub_app.w` + margen (~19). `az1.w`, `vpc.w`, `region.w` y `cloud.w` deben recalcularse en cascada para acomodar las tres subredes del mismo tamaño más sus márgenes. La flecha `alb→task` entra en `entryY=0.15` (parte alta del icono) y la flecha `task→cognito` sale en `exitY=0.85` (parte baja) — separadas a propósito para no correr pegadas por el mismo lado del icono (bug #12). La flecha `cust→cognito` ("1. Login") entra por la izquierda en `entryY=0.25`, mientras que una flecha de un segundo IdP (no mostrada en este fragmento reducido) entraría por ARRIBA — lados distintos para no converger casi en el mismo punto (bug #11). Nótese que, a diferencia de versiones anteriores de este ejemplo, la mayoría de estas flechas NO llevan `points` explícito — en este layout compacto el router por defecto ya resuelve las rutas limpiamente usando solo `exit`/`entry` (ver nota sobre `points` opcional en "Flechas"); esto SIEMPRE debe confirmarse con un render antes de asumir que no hace falta un waypoint. La arista `task` → `db` ilustra el caso de SALIDA lateral con iconos apilados cruzando HACIA OTRA SUBRED, y `ecs_box` → `nat` ilustra el caso de dos iconos apilados verticalmente (ALB+NAT) recibiendo una flecha desde otra subred — ver la sección "Flechas" para el detalle de ambos casos. Este ejemplo NO tiene frontend web: si el sistema tiene una SPA, agrega CloudFront y el bucket S3 según "Frontend web (SPA) nunca en una subred", "Punto único de entrada" y "Alineación del camino de entrada" (los actores ya no van al IGW). **Antes de fijar cualquiera de estos números en un diagrama nuevo, recomputa las coordenadas absolutas con el script de la sección "Flechas" y renderiza para confirmar — no copies estos valores literalmente ni asumas que las flechas sin `points` seguirán limpias en un diagrama distinto, son específicos de este diagrama.**

Notas:
- `kind`: `cloud|region|vpc|public_subnet|private_subnet` (contenedores AWS4 con icono de grupo) | `az|box` (cajas planas sin icono, dimensionadas por contenido) | `icon` (icono de recurso AWS4, requiere `icon` = sufijo del `resIcon`/`shape`; el generador decide automáticamente si usa la variante badge o nativa según la lista `BADGE_ICONS`) | `actor` (persona, librería cisco_safe).
- `parent`: id del elemento que lo envuelve visualmente. Todo elemento sin contenedor real usa `"1"` (raíz del lienzo). Usa siempre el `parent` que refleje el anidamiento visual REAL, incluso si un archivo de referencia editado a mano trae un `parent` desincronizado (ver nota en "Jerarquía de anidamiento").
- `x`/`y` de cualquier elemento son RELATIVOS al origen de su `parent` (no a la página), excepto los que tienen `parent: "1"`, cuyas coordenadas sí son absolutas de página.
- `label_pos` en `icon`: `bottom` (por defecto, etiqueta debajo centrada), `right`, `left`, o `center`. Si una o más flechas entran o salen de un icono con `label_pos` lateral por ese mismo lado, cambia el lado de entrada/salida (ver sección "Flechas"); si además el icono está apilado junto a otros dentro de la misma caja, el waypoint debe caer en el margen libre de la caja contenedora externa.
- `font_color`/`font_size` en `icon` son opcionales (por defecto `#232F3E` y `11`; los iconos pequeños ECS/Fargate/`ecs_task` usan `font_size: 10`, y ECS/Fargate ADEMÁS usan `font_color: "#808080"`).
- `box.stroke` por defecto es `#FF8000`. El `w`/`h` de una `box` debe calcularse por contenido (dentro de la subred de aplicación) — esta regla NO cambia con la de tamaño estándar de subredes, que aplica a las SUBREDES entre sí, no a las cajas ECS/Fargate dentro de ellas.
- **Dentro de una misma AZ, todas las subredes (2 o 3) son hermanas** (mismo `parent` = id de la AZ), lado a lado, en el orden pública → privada-app → privada-datos (ver "Subredes lado a lado dentro de la AZ") — nunca apiladas.
- **Todas las subredes de una misma AZ tienen el MISMO `w` y el MISMO `h`** (ver "Tamaño estándar de subredes") — calculado por la subred más exigente (normalmente la de aplicación) y reutilizado en las demás, centrando su contenido dentro del espacio disponible. El punto de partida por defecto actual es `260x200` con márgenes ~19px entre subredes.
- **El backend (caja ECS/Fargate/tarea) SIEMPRE va como hija de una subred PRIVADA, nunca de la pública**; la subred pública solo aloja el ALB (y, si hace falta, un NAT Gateway apilado con él).
- **El backend y la base de datos SIEMPRE van en subredes privadas DISTINTAS** (app vs. datos) — nunca como hermanos dentro de la misma subred, aunque ambas sean privadas.
- **Un frontend web (SPA) NUNCA va como `ecs_task` ni dentro de ninguna subred**: va en un bucket S3 en la fila regional (`parent` = Region), servido por CloudFront (`parent` = Cloud).
- **Dos iconos que comparten subred (p. ej. ALB + NAT Gateway) van APILADOS VERTICALMENTE, no lado a lado** — deja más aire y es más legible (pedido explícito del usuario, ver bug #15). Cuando una flecha externa entra/sale de uno de los dos, hazla entrar/salir por un lado LATERAL (no por arriba/abajo hacia el vecino apilado) y asegúrate de que el tramo que cruza hacia otra subred no coincida en altura con el rango vertical de otra flecha que ya use ese mismo hueco entre subredes como corredor.
- `label_offset: [a, o]` en un `edge` (opcional): desplaza el TEXTO de la etiqueta sin cambiar la ruta de la línea — `a` es la posición a lo largo de la ruta (-1 a 1, **0 = punto medio de la ruta completa, no el inicio**), `o` es el desplazamiento perpendicular en píxeles. Usarlo cuando el punto medio por defecto de una ruta cae encima de la etiqueta de otro elemento, e iterar con renders cuando la ruta tiene varios tramos (ver nota en "Flechas").
- **Cuando dos o más flechas tocan el mismo icono, revisa tanto el LADO como la ALTURA/posición de cada `entry`/`exit`** — lados distintos siempre que sea posible, y si deben compartir lado, sepáralas por al menos ~15-20% del tamaño del icono (ver bugs #11 y #12).
- **`points` es opcional, no obligatorio, para cruces entre niveles de anidamiento** — agrégalo solo si el render muestra un cruce, rodeo o jog real (ver nota en "Flechas" y bug #14).

## Script generador

Guarda esto como `aws_drawio.py` (no lo reescribas desde cero, es determinístico):

```python
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
    "az": az_el, "box": box_el, "icon": icon_el, "actor": actor_el,
}


def build(spec):
    b = Builder()
    els = spec["elements"]
    order = ["cloud", "region", "vpc", "az", "public_subnet", "private_subnet", "box", "icon", "actor"]
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
```

## Verificación antes de entregar

- Parsear el `.drawio` con `xml.etree.ElementTree`: confirmar que todo `parent` referenciado existe como `id` de otro elemento (o es `"1"`), y que las aristas referencian IDs existentes.
- Confirmar que la jerarquía de anidamiento sigue el orden Cloud > Region > VPC > (IGW suelto + AZ) > subredes (pública con solo el ALB/NAT; privada-app con ECS/Fargate/tarea; privada-datos con la BD), y que no se aplanó todo a la raíz.
- **Confirmar que dentro de cada AZ, todas las subredes (2 o 3) son hermanas lado a lado en horizontal (pública primero, luego privada-app, luego privada-datos), nunca apiladas.** Si el usuario reporta que "el flujo debería ir de izquierda a derecha pero una subred quedó debajo", es este caso.
- **Confirmar que TODAS las subredes de una misma AZ tienen exactamente el mismo `w` y el mismo `h`** — calculado sobre la subred más exigente (normalmente la de aplicación), nunca cada una dimensionada por su propio contenido. El punto de partida por defecto actual es `260x200` con márgenes ~19px entre subredes (ver "Tamaño estándar de subredes"). Si el usuario reporta que "las subnets deben tener las mismas dimensiones" o que una se ve más ancha/alta que otra, es este caso. Al estandarizar, centra el contenido de las subredes con menos elementos (ALB, BD) dentro del espacio disponible, y recalcula en cascada AZ/VPC/Region/Cloud/página.
- **Confirmar que el backend (caja ECS/Fargate/tarea) está en una subred PRIVADA, nunca en la pública.** Si el usuario reporta "¿por qué pusiste el backend en una subred pública?", es este caso — ver "Backend siempre en subred privada".
- **Confirmar que el backend y la base de datos están en subredes privadas DISTINTAS (app vs. datos), nunca compartiendo la misma subred.** Si el usuario reporta "la BD y el backend no pueden estar en la misma subnet", es este caso — ver "Backend y base de datos en subredes privadas separadas". Al separar, revisa también las flechas relacionadas y recalcula en cascada los anchos de AZ/VPC/Region/Cloud.
- Confirmar que cada icono usado está en la tabla de verificados o de estimados de este documento; si se usó uno fuera de ambas listas, avisarlo explícitamente al usuario en la respuesta.
- **Confirmar que solo `ecs`/`fargate`/`ecr`/`codecommit`/`codepipeline`/`codedeploy` usan la variante "badge"; todos los demás iconos deben usar la variante nativa.** Si el usuario reporta que los iconos se ven como cuadrados sólidos de color y no debería ser así, es indicio de que un icono quedó mal clasificado en `BADGE_ICONS`.
- **Confirmar que ningún icono con etiqueta lateral recibe NI envía una flecha por ESE MISMO lado, y que si ese icono está apilado junto a otros dentro de una caja, el waypoint de desvío cae en el margen libre de la caja contenedora externa** (ver sección "Flechas").
- **Confirmar que ningún icono queda a menos de 30-35px del título de su contenedor, y que si el espacio es ajustado usa `label_pos: right/left` en vez de `bottom`.**
- **Confirmar el punto medio de la ruta de CADA flecha con etiqueta contra las etiquetas de los demás elementos** — si cae encima de otro texto, usar `label_offset`.
- **Confirmar que ninguna etiqueta de FLECHA con `<br>` en el texto aparece como el texto literal `<br>`.**
- **Confirmar que ninguna flecha de "validación de JWT"/JWKS va de Cognito (o cualquier IdP) hacia el backend — siempre debe ir del backend hacia el IdP.**
- **Confirmar que ninguna flecha entra "torcida" a su destino** (un jog lateral pegado justo antes de la entrada) cuando viene por un corredor recto.
- **Confirmar que TODA etiqueta de flecha tiene `labelBackgroundColor=#ffffff` en su estilo** (debe venir automático del script generador) — si el usuario reporta texto "tachado" por la línea (p. ej. "OIDC", "SQL", "1. Login..."), es este caso.
- **Confirmar que ningún par de flechas converge casi en el mismo punto/lado de un mismo icono, ni corre pegado por el mismo lado a alturas muy parecidas** (menos de ~15-20px de separación) — si el usuario reporta que las flechas "no conectan correctamente" o se ven encimadas/como línea doble, es este caso. Sepáralas por LADO distinto cuando sea posible, o por al menos 15-20px de altura si deben compartir lado.
- **Cuando dos iconos comparten subred (p. ej. ALB + NAT), confirmar que están APILADOS VERTICALMENTE (no lado a lado) y que ninguna flecha externa cruza el hueco entre subredes a una altura que coincida con el rango vertical de otra flecha que ya use ese hueco como corredor** — si el usuario reporta que quiere "más espacio" o que algo quedó "encima de otra cosa", es este caso (ver bug #15).
- **Después de cualquier reescalado o reposicionamiento de coordenadas, recomputar las coordenadas absolutas con un script (nunca a mano) antes de fijar/revisar los `points`/`entry`/`exit` de las flechas** — un desfase de pocos píxeles entre un waypoint viejo y la nueva posición real de un icono es una causa real y ya vista de flechas "torcidas".
- **Confirmar que NINGUN contenedor (AZ, VPC, Region, Cloud, caja ECS/Fargate) tiene aire de sobra sin usar**, salvo las subredes hermanas, que por diseño comparten el tamaño de la más exigente (ver "Tamaño estándar de subredes") — esa es la única excepción intencional a la regla de "sin aire de sobra".
- **Confirmar que el `parent` de cada elemento refleja su anidamiento visual REAL** (VPC → AZ → subred → contenido), no un `parent` heredado sin revisar de un archivo editado a mano por el usuario (ver nota en "Jerarquía de anidamiento" y bug #14).
- **Confirmar que ningún frontend web (SPA) está como tarea ECS/Fargate ni dentro de ninguna subred**: va en un bucket S3 privado servido por CloudFront con OAC (ver "Frontend web (SPA) nunca en una subred").
- **Si hay CloudFront, confirmar que ningún actor conecta directamente al IGW ni al ALB**: los actores van solo a CloudFront, y CloudFront tiene una flecha `/*` al bucket de la SPA y otra `/api/*` al IGW (ver "Punto único de entrada"). La única excepción es el login directo a Cognito.
- **Confirmar que el camino de entrada está en un mismo eje horizontal**: centro Y de CloudFront = IGW = ALB, CloudFront centrado verticalmente entre los actores y ubicado en la franja de la Cloud fuera de la Region, nunca en la fila de servicios regionales (ver "Alineación del camino de entrada").
- Confirmar que las subredes públicas usan verde (`#7AA116`/`#F2F6E8`) y las privadas teal (`#00A4A6`/`#E6F6F7`) — nunca al revés.
- Confirmar que las cajas ECS/Fargate son sin relleno con borde naranja `#FF8000` (no confundir con el naranja `#ED7100` de los iconos de recurso).
- Al entregar, mencionar en la respuesta si algún icono usado viene de la tabla "estimados" para que el usuario lo revise al abrir el archivo.
