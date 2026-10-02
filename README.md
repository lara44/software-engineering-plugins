# software-engineering-plugins

Marketplace de plugins de ingeniería de software para Claude Code y GitHub Copilot. Cada plugin agrupa las skills de un rol.

## Plugins

| Plugin | Versión | Contenido |
|---|---|---|
| architecture | 1.0.0 | Documento de arquitectura en Word, diagramas C4, diagramas de despliegue AWS y diagramas de modelo de datos. |

### architecture

| Skill | Uso |
|---|---|
| architecture-document-style | Documento de arquitectura de software en Word (.docx). |
| c4-diagram-style | Diagramas C4 de contexto, contenedores y componentes en draw.io. |
| aws-deployment-diagram-style | Diagramas de despliegue AWS en draw.io. |
| database-diagram-style | Diagramas de modelo de datos en draw.io. |

## Instalación

### Claude Code

```
/plugin marketplace add <usuario>/software-engineering-plugins
/plugin install architecture@luisrojas-plugins
```

Las skills se invocan con el prefijo del plugin, por ejemplo `/architecture:c4-diagram-style`.

### GitHub Copilot CLI

```
copilot plugin marketplace add <usuario>/software-engineering-plugins
copilot plugin install architecture@luisrojas-plugins
```

Si el repositorio es privado, cada usuario necesita acceso de lectura y credenciales de git guardadas en su máquina (`gh auth login` y luego `gh auth setup-git`).

## Requisitos

- Python 3, para los scripts que generan los archivos .drawio.
- Node.js, para generar el documento de arquitectura en Word.
- draw.io Desktop, para exportar los diagramas a PNG (`drawio -x -f png archivo.drawio`).

## Estructura

```
.claude-plugin/marketplace.json        Catálogo para Claude Code
.github/plugin/marketplace.json        Catálogo para GitHub Copilot
plugins/<plugin>/
  .claude-plugin/plugin.json           Manifiesto para Claude Code
  .github/plugin/plugin.json           Manifiesto para GitHub Copilot
  skills/<skill>/SKILL.md              Skills del plugin
```

## Publicar una nueva versión

1. Modifica las skills del plugin.
2. Sube el número de versión en los tres archivos: `plugins/<plugin>/.claude-plugin/plugin.json`, `plugins/<plugin>/.github/plugin/plugin.json` y la entrada del plugin en `.github/plugin/marketplace.json`.
3. Valida con `claude plugin validate .`
4. Haz commit y push.

Los usuarios reciben la actualización con `/plugin marketplace update luisrojas-plugins` en Claude Code, o de forma automática si activaron la actualización automática del marketplace.

## Agregar un plugin

1. Crea la carpeta `plugins/<nuevo-plugin>/` con sus dos manifiestos y su carpeta `skills/`.
2. Agrega una entrada en cada catálogo: `.claude-plugin/marketplace.json` y `.github/plugin/marketplace.json`.
3. Usa el mismo `name` en los manifiestos del plugin y en las entradas de los catálogos.
