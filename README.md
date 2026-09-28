# MCP Polygon Renderer

Servidor MCP (Model Context Protocol) para que IAs locales (Claude, opencode, etc.) puedan poligonizar imagenes con OpenCV.

## Instalacion

```bash
pip install -e .
```

## Uso con Claude Desktop

Agrega a `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "polygon-renderer": {
      "command": "python",
      "args": ["-m", "mcp_polygon_renderer"]
    }
  }
}
```

## Uso con opencode

Agrega a `opencode.json`:

```json
{
  "mcp": {
    "polygon-renderer": {
      "command": "python",
      "args": ["-m", "mcp_polygon_renderer"]
    }
  }
}
```

## Herramientas disponibles

| Tool | Descripcion |
|------|-------------|
| `preparar_imagen` | Fase 1: superpone grilla etiquetada (A1, B2...) y devuelve mapa de celdas |
| `renderizar_desde_grid` | Fase 3: renderiza poligonos desde celdas de grilla |
| `renderizar_poligonos` | Renderiza poligonos con coordenadas directas en pixeles |
| `detectar_regiones` | Detecta y colorea regiones delimitadas por lineas naranjas |
| `ver_imagen` | Devuelve una imagen en base64 para que la IA la vea |

## Flujo de trabajo con grilla

1. La IA llama `preparar_imagen` con la ruta de la imagen.
2. La IA analiza la imagen con grilla y define poligonos usando celdas (ej: "B3", "C3").
3. La IA llama `renderizar_desde_grid` con el JSON de poligonos y el mapa de celdas.
4. La IA llama `ver_imagen` para ver el resultado.

## Ejemplo de JSON para renderizar_desde_grid

```json
{
  "poligonos_grid": [
    {"id": "Lomo", "celdas": ["B3", "C3", "D3"]},
    {"id": "Costilla", "celdas": ["A2", "B2", "B3"]}
  ]
}
```

## Ejemplo de JSON para renderizar_poligonos

```json
[
  {"id": "Triangulo", "puntos": [[100, 100], [200, 50], [300, 100]]},
  {"id": "Rectangulo", "puntos": [[400, 100], [600, 100], [600, 300], [400, 300]]}
]
```
