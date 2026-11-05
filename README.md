# software-engineering-plugins

Plugins de ingeniería de software para **Claude Code** y **GitHub Copilot CLI**. Cada plugin conduce un método: el arquitecto decide y el asistente propone, redacta, dibuja y verifica la coherencia.

## Plugins

| Plugin | Método | Versión | Para empezar | Manual |
|---|---|---|---|---|
| `add` | Diseño de arquitectura con ADD 3.0 (Attribute-Driven Design) | 2.0.0 | `/add:start` | [plugins/add](plugins/add/README.md) |
| `ddd` | Event Storming y modelo de dominio (Domain-Driven Design) | 0.1.0 | `/ddd:start` | [plugins/ddd](plugins/ddd/README.md) |

Se pueden usar juntos: comparten `inputs/` y `questions.md` en la carpeta del proyecto, y el modelo de dominio de `ddd` sirve de insumo para el diseño con `add` (cada contexto es candidato a módulo). Ninguno depende del otro.

## Instalación

En Claude Code:
```
/plugin marketplace add lara44/software-engineering-plugins
/plugin install add@luisrojas-plugins
/plugin install ddd@luisrojas-plugins
```

En GitHub Copilot CLI:
```
copilot plugin marketplace add lara44/software-engineering-plugins
copilot plugin install add@luisrojas-plugins
copilot plugin install ddd@luisrojas-plugins
```

Instala solo los que vayas a usar. Después, abre la carpeta de tu proyecto y escribe el comando para empezar del plugin (o pídelo en lenguaje natural, por ejemplo *"Arranquemos la arquitectura"* o *"Hagamos el Event Storming"*).

## Actualizar

1. Descarga la versión nueva del marketplace:
   ```
   /plugin marketplace update luisrojas-plugins
   ```
2. Abre `/plugin`, entra a los plugins instalados, selecciona el plugin y elige actualizar.
3. Reinicia Claude Code (`/exit` y luego `claude`), porque las skills se cargan al iniciar la sesión.

Si la versión no cambia, desinstálalo y vuelve a instalarlo.

**Si tenías `architecture` o `domain-driven-design`:** desde esta versión se llaman `add` y `ddd`. Para el marketplace son plugins distintos, así que no se actualizan solos:
```
/plugin uninstall architecture@luisrojas-plugins
/plugin uninstall domain-driven-design@luisrojas-plugins
/plugin install add@luisrojas-plugins
/plugin install ddd@luisrojas-plugins
```
Tus proyectos no cambian.

## Requisitos

- Python 3, para los scripts que dibujan los diagramas (los dos plugins).
- draw.io Desktop, para exportar los diagramas a PNG (los dos plugins).
- Node.js con la librería `docx`, LibreOffice y poppler, para los documentos en Word (solo `add`).

Cada manual detalla los requisitos de su plugin.

## Estructura del repositorio

```
.claude-plugin/marketplace.json        Catálogo para Claude Code
.github/plugin/marketplace.json        Catálogo para GitHub Copilot
plugins/<plugin>/
  .claude-plugin/plugin.json           Manifiesto para Claude Code
  .github/plugin/plugin.json           Manifiesto para GitHub Copilot
  README.md                            Manual del plugin
  docs/                                Imágenes del manual
  skills/<skill>/SKILL.md              Skills del plugin
  skills/<skill>/references/           Detalle que la skill lee solo cuando lo necesita
  skills/<skill>/scripts/              Generadores (diagramas y Word)
```

## Contribuir

¿Encontraste un problema o tienes una idea? Abre un *issue* con el caso en el que lo usaste y lo que esperabas que pasara.

### Publicar una nueva versión

1. Modifica las skills del plugin.
2. Sube el número de versión en los tres archivos: `plugins/<plugin>/.claude-plugin/plugin.json`, `plugins/<plugin>/.github/plugin/plugin.json` y la entrada del plugin en `.github/plugin/marketplace.json`.
3. Valida con `claude plugin validate .`
4. Haz commit y push.

Versionado: el número del medio sube cuando se agrega una fase o cambian los nombres de las skills; el último, con ajustes a skills existentes.

Los usuarios reciben la actualización siguiendo los pasos de [Actualizar](#actualizar).

### Agregar un plugin

1. Crea la carpeta `plugins/<nuevo-plugin>/` con sus dos manifiestos, su carpeta `skills/`, su `README.md` y sus imágenes en `docs/`.
2. Agrega una entrada en cada catálogo: `.claude-plugin/marketplace.json` y `.github/plugin/marketplace.json`.
3. Usa el mismo `name` en los manifiestos del plugin y en las entradas de los catálogos.
4. Agrega el plugin a la tabla de este README.
5. Nombra el plugin por su método (`add`, `arc42`, `c4`…) y sus skills con nombres cortos en inglés (`start`, `design`, `document`…): Claude Code ya les antepone el nombre del plugin (`/<plugin>:<skill>`).

## Autor

Luis Rojas — arquitecto de soluciones.

## Licencia

[MIT](LICENSE). Puedes usar, modificar y compartir estas skills, incluso en proyectos comerciales, siempre que conserves el aviso de copyright.
