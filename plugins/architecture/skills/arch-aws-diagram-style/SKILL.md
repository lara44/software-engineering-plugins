---
name: "arch-aws-diagram-style"
description: "Usar cuando se pida crear o actualizar un diagrama de despliegue/arquitectura AWS (AWS Cloud > Region > VPC > Availability Zone > subredes > ECS/Fargate, bases de datos, IGW, load balancers, actores) como archivo .drawio editable, replicando el estilo visual exacto de su diagrama de referencia: contenedores anidados con los iconos y colores oficiales de la librería mxgraph.aws4 (AWS Cloud negro, Region teal, VPC morado, subredes públicas verdes y privadas teal con icono de candado, cajas ECS/Fargate naranjas sin relleno), iconos de recursos AWS4 (Internet Gateway, ALB, RDS/MySQL, NAT Gateway, etc.) y actores con la librería mxgraph.cisco_safe (círculos morados de personas), flechas ortogonales grises. No aplica a diagramas C4 (usar la skill arch-c4-diagram-style para esos)."
---

# Estilo de diagramas de despliegue AWS (draw.io)

Genera diagramas de despliegue AWS como `.drawio` editables con el estilo del diagrama de referencia del arquitecto: arquitectura ECS/Fargate detrás de un ALB, con la base de datos en subred privada. Los estilos, colores e identificadores de iconos se extrajeron del `.drawio` real, no se adivinaron. Un `resIcon` mal escrito no da error al generar: se ve como una caja gris ("forma no encontrada") al abrir el archivo.

Si piden un diagrama C4, usar `arch-c4-diagram-style`.

## Generador

El generador está en `scripts/aws_drawio.py`, dentro de la carpeta de esta skill. Se ejecuta tal cual; no se lee, no se copia y no se reescribe:

```bash
python3 <carpeta-de-esta-skill>/scripts/aws_drawio.py spec.json salida.drawio
```

Contiene los estilos de contenedores, la lista `ICONS` de colores, la lista `BADGE_ICONS` y el estilo base de flechas (gris `#666666`, ortogonal, etiqueta con fondo blanco). **No se modifica por proyecto:** si a un icono le falta color, se usa `fill` en el `spec.json`; si se va a repetir, se propone agregarlo a `ICONS` del plugin.

## Iconos

**Regla de oro: nunca inventar un icono sin decirlo.** Antes de usar uno que no esté en la tabla de verificados:
1. Si el arquitecto puede compartir un `.drawio` o fragmento XML que ya lo use, copiar el `shape`/`resIcon` exacto.
2. Si no, usar el nombre del servicio en inglés, en minúsculas y con guiones bajos (`dynamodb`, `lambda_function`), con la variante nativa, y avisar al entregar que es estimado.

**Variantes:** solo `ecs`, `fargate`, `ecr`, `codecommit`, `codepipeline` y `codedeploy` usan el cuadrado de color con borde blanco ("badge"). Todo lo demás es icono plano sin fondo ("nativa"). El script decide la variante según `BADGE_ICONS`; si un icono sale como cuadrado sólido y no debería, el error está en esa lista.

**Contenedores** (`shape=mxgraph.aws4.group`, `container=1`):

| Nivel | `grIcon` | strokeColor | fillColor | fontColor |
|---|---|---|---|---|
| AWS Cloud | `group_aws_cloud_alt` | `#232F3E` | none | `#232F3E` |
| Region | `group_region` | `#00A4A6` | none | (por defecto) |
| VPC | `group_vpc2` | `#8C4FFF` | none | `#AAB7B8` |
| Subred pública | `group_security_group` (`grStroke=0`) | `#7AA116` | `#F2F6E8` | `#248814` |
| Subred privada | `group_security_group` (`grStroke=0`) | `#00A4A6` | `#E6F6F7` | `#147EBA` |

Cajas planas (`kind: az` y `kind: box`): Availability Zone con borde `#147EBA` sin relleno y título de 10 px; cajas ECS y Fargate con borde `#FF8000` sin relleno y sin título propio (el nombre va en el icono pequeño de adentro). No confundir el naranja de las cajas (`#FF8000`) con el de los iconos (`#ED7100`).

**Iconos verificados:**

| Icono | `icon` | Color | Variante | Etiqueta |
|---|---|---|---|---|
| ECS (dentro de su caja) | `ecs` | `#ED7100` | badge | derecha, `font_color: "#808080"`, `font_size: 10` |
| Fargate (dentro de su caja) | `fargate` | `#ED7100` | badge | derecha, `font_color: "#808080"`, `font_size: 10` |
| Tarea/contenedor | `ecs_task` | `#ED7100` | nativa | derecha, `font_size: 10` |
| ECR | `ecr` | `#ED7100` | badge | abajo |
| Internet Gateway | `internet_gateway` | `#8C4FFF` | nativa | izquierda (abajo si una flecha entra por su izquierda, p. ej. desde CloudFront) |
| Application Load Balancer | `application_load_balancer` | `#8C4FFF` | nativa | abajo |
| RDS MySQL | `rds_mysql_instance` | `#C925D1` | nativa | abajo |
| IAM | `identity_access_management_iam_roles_anywhere` | `#DD344C` | nativa | abajo |
| Cognito User Pool | `cognito` | `#DD344C` | nativa | derecha |
| AWS Certificate Manager | `certificate_manager` | `#DD344C` | nativa | derecha |
| CodeCommit / CodePipeline / CodeDeploy | `codecommit` / `codepipeline` / `codedeploy` | `#C925D1` | badge | abajo |

**Iconos estimados** (nativa, color por categoría; avisar al entregar):
- Cómputo `#ED7100`: `ec2`, `lambda_function`, `eks_cloud`, `ecs_service`.
- Redes `#8C4FFF`: `network_load_balancer`, `classic_load_balancer`, `nat_gateway`, `vpc`, `route_53`, `api_gateway`, `cloudfront`.
- Bases de datos `#C925D1`: `rds_postgresql_instance`, `dynamodb`.
- Almacenamiento `#7AA116`: `s3`.
- Integración y monitoreo `#E7157B`: `sqs`, `sns`, `cloudwatch`.

**Actores:** no son AWS4. Usar `kind: "actor"` (librería `mxgraph.cisco_safe`, círculo morado `#A153A0`). Nunca `mxgraph.aws4.user`.

## Reglas de arquitectura

Son reglas de diseño, no de estilo. Se aplican siempre, aunque nadie las pida:

1. **El backend nunca va en la subred pública.** La subred pública tiene ruta directa al Internet Gateway; lo que esté ahí es alcanzable desde internet. Solo aloja el ALB (único componente hecho para recibir tráfico público) y, si el backend necesita salida a internet, un NAT Gateway. Cualquier servicio de cómputo nuevo va en la subred privada de aplicación.
2. **Backend y base de datos en subredes privadas distintas** (app y datos). Así la capa de datos puede tener reglas de red más estrictas: solo acepta tráfico desde la subred de app y en el puerto de la base. La subred pública sigue haciendo falta como único punto con ruta al IGW.
3. **La SPA nunca va en una subred ni como tarea ECS.** Es contenido estático: va en un bucket S3 privado servido por CloudFront con OAC. En Fargate solo quedan servicios de backend.
4. **Con CloudFront, ningún actor conecta directo al IGW ni al ALB.** CloudFront es el único punto de entrada: `/*` va al bucket de la SPA y `/api/*` al IGW → ALB. El ALB debe aceptar tráfico solo de CloudFront (security group con la prefix list de CloudFront o encabezado secreto); no se dibuja, pero se menciona al entregar. Si se pide WAF, va en CloudFront. Excepción: el login con Cognito Hosted UI usa su propio dominio, así que la flecha actor → Cognito ("Login (OIDC)") se mantiene.
5. **La flecha de JWKS va del backend hacia el IdP,** con etiqueta tipo "Obtiene JWKS (cacheado)". El backend valida el JWT localmente con las llaves públicas del IdP; el IdP nunca llama al backend.

Flujos resultantes: entrada actor → (CloudFront →) IGW → ALB (pública) → backend (privada app) → base de datos (privada datos); salida backend → NAT (pública) → IGW → internet.

Vocabulario: el arquitecto puede llamar "API gateway" al Internet Gateway. Si el diagrama no tiene Amazon API Gateway, aclarar la diferencia.

## Reglas de layout

**Anidamiento real con `parent`.** Cada elemento apunta al contenedor que lo envuelve visualmente y sus `x`/`y` son relativas a ese padre (solo los de `parent: "1"` son absolutas). Así, mover la VPC mueve todo su contenido. Jerarquía:
1. Actores fuera de la AWS Cloud, a la izquierda (`parent: "1"`).
2. AWS Cloud → Region → VPC.
3. CloudFront (servicio global de borde): dentro de la Cloud pero fuera de la Region, en una franja a la izquierda de 150–170 px. Nunca en la fila regional.
4. Servicios regionales fuera de la VPC (Cognito, S3, SNS, CodePipeline…): fila superior de la Region, `y` relativa ≈ 70, `label_pos: right`.
5. Dentro de la VPC: el IGW suelto (sin subred) y una Availability Zone por zona.
6. Dentro de cada AZ: las subredes. Dentro de la privada de app: `ecs_box` → `fargate_box` → tareas, una debajo de otra.

Si un archivo editado a mano trae un `parent` que no coincide con el contenedor visual, en un spec nuevo usar siempre el `parent` real.

**Subredes lado a lado y del mismo tamaño.**
- En cada AZ, en una misma fila y en este orden: pública → privada app → privada datos (el orden en que las atraviesa el tráfico). Nunca apiladas. Por qué: con varias AZ, cada zona es una fila autocontenida y la segunda se apila debajo sin complicar el diagrama.
- Todas las subredes de una AZ miden exactamente lo mismo: el tamaño mínimo que necesita la más exigente (normalmente la de app). Por qué: tamaños distintos sugieren una jerarquía que no existe; las tres capas son igual de importantes.
- Medidas por defecto (las del archivo que el arquitecto ajustó a mano y aprobó): subred `260x200`, ~19 px entre subredes, `ecs_box` a ~15 px del borde de la subred, ~34–40 px de aire bajo cada título, ~15 px de margen inferior en la AZ. Si el contenido no cabe, el tamaño mayor se aplica a las tres por igual. Para achicar, apretar primero los márgenes internos de ECS/Fargate.
- En las subredes con menos contenido (ALB, base de datos), centrar el contenido en el espacio disponible.

**Ningún otro contenedor tiene aire de sobra.** AZ, VPC, Region, Cloud y las cajas ECS/Fargate se dimensionan por contenido: ancho = borde derecho del hijo más lejano + ~20–30 px. Calcular de adentro hacia afuera; si algo cambia de tamaño o se agrega una subred, recalcular en cascada hasta la página y revisar todas las flechas que tocaban ese subárbol.

**Dos iconos en la misma subred van apilados en vertical** (por ejemplo, NAT y ALB, ~15 px entre ellos), nunca lado a lado. Lo pidió el arquitecto para dejar más aire y legibilidad: "no coloques cosas encima de otras".

**Camino de entrada en un mismo eje horizontal:** centro Y de CloudFront = IGW = ALB. Los actores van simétricos arriba y abajo de ese eje (±120 px), con CloudFront centrado entre ellos. Calcular la Y de CloudFront a partir de la Y absoluta del IGW, no a ojo. El NAT se alinea con la salida de egreso de `ecs_box`; si eso deja el ALB arriba y el NAT abajo, está bien: manda la alineación, siempre que sigan apilados.

**Iconos cerca del título de su contenedor:** dejar 30–35 px de aire con el borde superior, o usar `label_pos: right/left` en vez de `bottom`, porque la etiqueta de abajo compite con el título.

**Notas:** las aclaraciones del diagrama (por ejemplo, "Prototipo en una sola zona de disponibilidad") van como `kind: "note"`, sin flechas.

## Flechas

**Coordenadas absolutas siempre con script, nunca de memoria.** Después de fijar el tamaño final de todo, calcular las coordenadas absolutas sumando `x`/`y` por la cadena de `parent`. Un desfase de 3–4 px entre un waypoint y la entrada real produce un codo visible.

```python
import json
spec = json.load(open("spec.json"))
els = {e["id"]: e for e in spec["elements"]}
def abs_origin(i):
    e = els[i]
    if e.get("parent", "1") == "1": return (e["x"], e["y"])
    px, py = abs_origin(e["parent"]); return (px + e["x"], py + e["y"])
for i, e in els.items():
    ox, oy = abs_origin(i)
    print(i, ox, oy, "right=", ox + e.get("w", 0), "bottom=", oy + e.get("h", 0))
```

**Primero `exit`/`entry`, después renderizar.** Fijar `exit`/`entry` explícitos cuando dos flechas comparten origen o destino, o cuando tocan un icono con etiqueta lateral. Agregar `points` solo si el render muestra un cruce, un rodeo o un codo real.

**Etiqueta lateral = lado prohibido.** Si un icono tiene `label_pos: left/right`, su etiqueta ocupa una banda a ese lado y ninguna flecha entra ni sale por ahí; cambiar el `entryY` no basta, hay que cambiar de lado:
- Entrada: por arriba o por abajo (`entry=[0.5,0]` o `[0.5,1]`), con un waypoint en `(centro_x_del_icono, y_del_origen)`. Ejemplo verificado (IGW con dos actores): actor de arriba `exit=[1,0.5]`, `points=[[cx, y_actor]]`, `entry=[0.5,0]`; actor de abajo igual con `entry=[0.5,1]`.
- Salida de un icono solo: lo mismo en espejo.
- Salida de un icono apilado con otros en su caja (la tarea bajo los iconos ECS y Fargate): "arriba" no está libre. Salir por el lado opuesto a lo apilado y llevar la línea al margen libre de la caja externa (entre el último icono y el borde inferior de `ecs_box`). Ejemplo verificado (tarea → base de datos en otra subred): tarea en x=996, su borde inferior en y=422, `ecs_box` termina en y=450 → `exit=[0.5,1]`, `points=[[996,436],[1440.5,436]]`, `entry=[0.5,1]`.

**Iconos apilados en la misma subred (ALB + NAT):** la flecha hacia uno de ellos desde otra subred entra por un lado lateral, nunca por el lado que mira al vecino. Si cruza el hueco entre subredes y otra flecha ya usa ese hueco como corredor, cruzarlo fuera del rango vertical de esa flecha. Ejemplo verificado: la flecha JWKS ocupaba el hueco entre y≈145 y 396, así que `ecs_box → nat` lo cruzó en y≈432 (margen inferior de la AZ), subió por una columna libre a la derecha de ALB/NAT y entró al NAT por la derecha.

**Convergencias y paralelas:**
- Dos flechas que llegan casi al mismo punto se ven encimadas: llevar una a otro lado del icono. Ejemplo verificado: el IdP de Google entra a Cognito por arriba (`entry=[0.7,0]`) y el login por la izquierda (`entry=[0,0.25]`).
- Dos flechas por el mismo lado a alturas parecidas se ven como una línea doble: separarlas al menos 15–20 % del alto del icono. Ejemplo verificado: en la tarea (28 px), ALB → tarea entra en `entryY=0.15` y JWKS sale en `exitY=0.85`.
- Dejar 60–80 px entre un icono con etiqueta lateral y el origen o destino de sus flechas.

**Etiquetas de flecha:** el texto se ubica en el punto medio de la ruta completa, aunque la línea esquive todo. Si cae sobre otro texto, moverlo con `label_offset: [a, o]` (`a` de -1 a 1 con **0 = punto medio, no el inicio**; `o` = desplazamiento perpendicular en px). En rutas en escalón, probar valores y renderizar; el tramo que corresponde a cada `a` no es obvio.

**Rodeos y codos:**
- Actor fuera de la Cloud hacia un icono anidado adentro: si el render muestra un rodeo por encima de todo, usar el corredor vertical libre más cercano. Ejemplo verificado: actor → Cognito por la columna `x≈210`, entre los IdP externos (terminan en x=190) y el borde de la Cloud (x=260): `exit=[0.5,0]`, `points=[[210, y_actor],[210, y_entrada]]`, `entry=[0,0.1]`.
- Codo final pegado a la entrada: mover el icono destino para que quede alineado con el corredor; no agregar waypoints para disimularlo.

**CloudFront y fila regional:**
- Actores → CloudFront: el de arriba entra por arriba y el de abajo por abajo (`exit=[1,0.5]`, `points=[[x_cf + 0.3*w_cf, y_actor]]`, `entry=[0.3,0]` o `[0.3,1]`). CloudFront lleva `label_pos: left`.
- CloudFront → IGW: recta, `exit=[1,0.5]` → `entry=[0,0.5]`; el IGW pasa a `label_pos: bottom`. IGW → ALB recta a la misma altura.
- CloudFront → bucket de la SPA: sale por arriba (`exit=[0.8,0]`), sube por la franja de la Cloud y entra por la izquierda del bucket; dejar ≥120 px para la etiqueta ("/* (SPA) origen OAC").
- Login actor → Cognito: corredor horizontal en la franja entre el título de la Region y la fila regional (`y ≈ y_region + 30`), entrando por arriba de Cognito (`entry=[0.5,0]`).
- Entre la fila regional y la VPC, dejar ≈75 px. Las flechas que suben desde `ecs_box` salen por su borde superior a la derecha de los títulos de la subred y de la AZ (fracciones `0.72`, `0.85`, `0.97`) y giran a alturas distintas (+42 y +58 bajo la fila). El icono al que se llega recto se centra sobre su punto de salida, y la etiqueta de esa flecha se sube con `label_offset` ≈ `[0.7, 0]`.

## Formato del spec.json

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

Este ejemplo es el layout aprobado de 3 subredes (sin CloudFront ni SPA). Sus números son de este diagrama: en uno nuevo, recalcular coordenadas con el script y renderizar antes de confiar en que las flechas sin `points` quedan limpias.

Campos:
- `kind`: `cloud | region | vpc | public_subnet | private_subnet` (contenedores con icono de grupo), `az | box` (cajas planas), `icon` (requiere `icon`; el script decide la variante), `actor`, `note` (nota amarilla con `text`).
- En `icon`: `label_pos` (`bottom` por defecto, `right`, `left`, `center`), `font_size` (11 por defecto), `font_color` (`#232F3E` por defecto) y `fill` (color del icono cuando no está en `ICONS`; usar el de su categoría).
- En `box`: `stroke` (`#FF8000` por defecto).
- En flechas: `from`, `to`, `parent`, `label`, `exit`/`entry` (`[x, y]` de 0 a 1), `points` (absolutos) y `label_offset`.
- Los saltos de línea se escriben como `<br>` crudo.

## Flujo de trabajo

1. Reunir el contenido: actores, región, zonas, subredes, servicios por subred y conexiones.
2. Armar la jerarquía `parent` y aplicar las reglas de arquitectura y de layout.
3. Elegir cada icono en las tablas (verificado, estimado o pedir el XML).
4. Calcular tamaños de adentro hacia afuera: contenido → tamaño estándar de subred → AZ → VPC → Region → Cloud → página.
5. Escribir el `spec.json`, calcular las coordenadas absolutas con el script de "Flechas" y fijar `exit`/`entry` (y `label_offset` donde haga falta).
6. Generar con `scripts/aws_drawio.py`.
7. Renderizar a PNG y mirarlo (draw.io Desktop: `drawio -x -f png -o salida.png salida.drawio`; en Mac, si `drawio` no está en el PATH, `/Applications/draw.io.app/Contents/MacOS/draw.io`). Corregir y repetir hasta que no haya cruces ni etiquetas encimadas. Si no se puede renderizar, decirlo y entregar como "sin verificación visual".
8. Entregar diciendo qué iconos son estimados.

## Verificación antes de entregar

- [ ] Todo `parent` y toda flecha apuntan a IDs que existen (parsear con `xml.etree.ElementTree`), y la jerarquía no se aplanó a la raíz.
- [ ] Reglas de arquitectura: backend en privada, backend y base de datos en subredes distintas, SPA en S3 + CloudFront, actores solo por CloudFront (salvo el login), JWKS del backend al IdP.
- [ ] Subredes de cada AZ lado a lado, en orden, y con el mismo `w`/`h`; ningún otro contenedor con aire de sobra.
- [ ] Pública verde (`#7AA116`/`#F2F6E8`), privadas teal (`#00A4A6`/`#E6F6F7`); cajas ECS/Fargate sin relleno con borde `#FF8000`.
- [ ] Solo los iconos de la lista badge usan esa variante; los estimados o desconocidos están avisados.
- [ ] En el render: ninguna flecha por el lado de una etiqueta lateral, ninguna etiqueta encimada, ningún codo final, ninguna convergencia ni paralela pegada, ningún `<br>` visible como texto.
- [ ] Camino de entrada alineado en un eje; iconos apilados (no lado a lado) cuando comparten subred; iconos a 30–35 px de los títulos.
- [ ] Después de cualquier cambio de tamaño o posición, coordenadas recalculadas con el script y flechas revisadas.
