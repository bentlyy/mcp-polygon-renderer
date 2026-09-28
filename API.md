# API Reference

## `preparar_imagen_para_ia(ruta_imagen, filas=10, columnas=10)`

Fase 1: superpone una grilla etiquetada sobre la imagen y devuelve el mapa de celdas.

**Parámetros:**

| Nombre | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `ruta_imagen` | `str` | — | Ruta absoluta a la imagen |
| `filas` | `int` | `10` | Número de filas de la grilla |
| `columnas` | `int` | `10` | Número de columnas de la grilla |

**Retorna:** `dict`

```json
{
  "imagen_con_grilla": "/ruta/a/imagen_con_grilla.png",
  "mapa_celdas": {
    "A1": {"x": 0, "y": 0, "x1": 70, "y1": 46, "cx": 35, "cy": 23},
    "B1": {"x": 70, "y": 0, "x1": 140, "y1": 46, "cx": 105, "cy": 23}
  },
  "dimensiones": {"ancho": 707, "alto": 497}
}
```

**Excepciones:** `FileNotFoundError` si la imagen no existe.

---

## `renderizar_poligonos_desde_grid(ruta_imagen_original, json_ia, mapa_celdas)`

Fase 3: renderiza polígonos a partir de celdas de grilla.

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `ruta_imagen_original` | `str` | Ruta a la imagen original (sin grilla) |
| `json_ia` | `dict` | Diccionario con estructura `{"poligonos_grid": [...]}` |
| `mapa_celdas` | `dict` | Mapa de celdas devuelto por `preparar_imagen_para_ia` |

**Estructura de `json_ia`:**

```json
{
  "poligonos_grid": [
    {"id": "Lomo", "celdas": ["F2", "G2", "G3", "H2"]},
    {"id": "Costilla", "celdas": ["D3", "E3", "E4", "F4"]}
  ]
}
```

**Retorna:** `str` — ruta de la imagen final con polígonos renderizados.

---

## `renderizar_poligonos_directos(ruta_imagen_original, poligonos)`

Renderiza polígonos con coordenadas directas en píxeles (sin grilla).

**Parámetros:**

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `ruta_imagen_original` | `str` | Ruta a la imagen original |
| `poligonos` | `list[dict]` | Lista de polígonos con coordenadas en píxeles |

**Estructura de `poligonos`:**

```json
[
  {"id": "Triangulo", "puntos": [[100, 100], [200, 50], [300, 100]]},
  {"id": "Rectangulo", "puntos": [[400, 100], [600, 100], [600, 300], [400, 300]]}
]
```

**Retorna:** `str` — ruta de la imagen final.

---

## `detectar_y_colorear_regiones(ruta_imagen, area_min=20)`

Detecta automáticamente regiones delimitadas por líneas naranjas y las colorea.

**Parámetros:**

| Nombre | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `ruta_imagen` | `str` | — | Ruta a la imagen con regiones marcadas |
| `area_min` | `int` | `20` | Área mínima en píxeles para considerar una región |

**Retorna:** `tuple[str, int]` — ruta de la imagen coloreada y número de regiones detectadas.

---

## Constantes

### `COLORES_VIVOS`

Lista de 40 colores BGR vívidos usados para diferenciar regiones automáticamente.

```python
from mcp_polygon_renderer.engine import COLORES_VIVOS
```
