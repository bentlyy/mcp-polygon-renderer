# MCP Polygon Renderer

[![PyPI](https://img.shields.io/badge/pypi-mcp--polygon--renderer-blue)](https://pypi.org/project/mcp-polygon-renderer/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-Compatible-purple.svg)](https://modelcontextprotocol.io)

> Servidor MCP que permite a agentes de IA poligonizar imágenes con OpenCV, usando grillas de referencia o coordenadas directas en píxeles.

## Por qué existe

Los modelos de lenguaje no pueden dibujar sobre imágenes. Esta herramienta les da esa capacidad: el agente razonifica sobre una imagen con grilla, define regiones usando celdas (ej: `"B3", "C3", "D3"`), y el servidor las renderiza con precisión de píxeles.

## Instalación

```bash
pip install mcp-polygon-renderer
```

O desde fuente:

```bash
git clone https://github.com/bentlyy/mcp-polygon-renderer.git
cd mcp-polygon-renderer
pip install -e .
```

## Configuración

### Claude Desktop

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

### opencode

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

## Herramientas

| Herramienta | Descripción |
|-------------|-------------|
| `preparar_imagen` | Superpone grilla etiquetada (A1, B2...) y devuelve el mapa de celdas en píxeles |
| `renderizar_desde_grid` | Renderiza polígonos a partir de celdas de grilla |
| `renderizar_poligonos` | Renderiza polígonos con coordenadas directas en píxeles |
| `detectar_regiones` | Detecta y colorea automáticamente regiones delimitadas por líneas |
| `ver_imagen` | Devuelve una imagen en base64 para que el agente la visualice |

## Flujo de trabajo

### Modo grilla (recomendado para imágenes complejas)

```
1. Agente llama: preparar_imagen("vaca.png", filas=10, columnas=10)
   → Recibe: imagen con grilla + mapa de celdas en píxeles

2. Agente analiza la imagen con grilla y define regiones:
   {"poligonos_grid": [{"id": "Lomo", "celdas": ["F2", "G2", "G3", "H2"]}]}

3. Agente llama: renderizar_desde_grid("vaca.png", json_ia, mapa_celdas)
   → Recibe: ruta de la imagen con polígonos renderizados

4. Agente llama: ver_imagen(ruta_final)
   → Ve el resultado y continúa trabajando
```

### Modo directo (para formas geométricas)

```
1. Agente define polígonos con coordenadas en píxeles:
   [{"id": "Triangulo", "puntos": [[100,100], [200,50], [300,100]]}]

2. Agente llama: renderizar_poligonos("imagen.png", poligonos)
   → Recibe: ruta de la imagen con polígonos renderizados
```

### Detección automática

```
1. Agente llama: detectar_regiones("vaca.png")
   → Recibe: imagen coloreada + número de regiones detectadas
```

## Imágenes de prueba

Prompts para generar imágenes de prueba con cualquier IA generadora de imágenes:

**1. Diagrama con regiones delimitadas (para `detectar_regiones`):**
```
A top-down map of a neighborhood with 15 irregularly shaped zones separated by bright orange lines on a dark background. Each zone is a solid dark gray color. Clean vector style, high contrast, no text.
```

**2. Formas geométricas simples (para `renderizar_poligonos`):**
```
Six geometric shapes on a dark background: a circle, a triangle, a pentagon, an irregular hexagon, a star, and a rectangle. All shapes are light gray with no outlines, evenly spaced, flat 2D style, no shadows.
```

**3. Objeto con subdivisiones internas (para modo grilla):**
```
A side view of a fish with 20 internal sections separated by thin orange lines on a black silhouette. The fish faces left. Clean diagram style, dark background, no text, no scales texture.
```

## Ejemplos

### Cortes de carne (35 regiones detectadas)

```python
# El agente analiza la vaca con grilla y define los cortes
poligonos = {
    "poligonos_grid": [
        {"id": "Cabeza", "celdas": ["A2", "A3", "B2", "B3"]},
        {"id": "Cuello", "celdas": ["B4", "C3", "C4"]},
        {"id": "Paleta", "celdas": ["B5", "C5", "D4", "D5"]},
        {"id": "Costilla", "celdas": ["D3", "E3", "E4", "F4", "F5"]},
        {"id": "Lomo", "celdas": ["F2", "G2", "G3", "H2", "H3"]},
        {"id": "Cuadril", "celdas": ["H4", "I3", "I4", "J3", "J4"]},
    ]
}
```

### Polígonos con curvas

```python
# Círculo con 36 puntos para simular curva suave
import math
puntos_circulo = [
    [int(200 + 80 * math.cos(2 * math.pi * i / 36)),
     int(150 + 80 * math.sin(2 * math.pi * i / 36))]
    for i in range(36)
]
poligonos = [{"id": "Circulo", "puntos": puntos_circulo}]
```

## Características

- **Optimizado para agentes**: sin ventanas emergentes, todo se guarda en disco
- **Eficiente en RAM**: carga reducida de imágenes grandes automáticamente
- **Colores vivos**: paleta de 40 colores distintos para diferenciar regiones
- **Curvas por densidad**: más puntos = más suavidad en bordes curvos
- **Detección automática**: identifica regiones delimitadas por líneas de color

## Licencia

MIT
