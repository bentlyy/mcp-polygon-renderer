# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/),
y este proyecto se adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [0.1.0] - 2026-09-27

### Agregado

- Servidor MCP con 5 herramientas: `preparar_imagen`, `renderizar_desde_grid`, `renderizar_poligonos`, `detectar_regiones`, `ver_imagen`
- Motor de renderizado con OpenCV: grilla etiquetada, polígonos directos, detección automática de regiones
- Carga eficiente de imágenes con flags reducidos para ahorrar RAM
- Paleta de 40 colores vívidos para diferenciar regiones
- Soporte de curvas por densidad de puntos
- Tests unitarios con pytest (8 tests)
- CI/CD con GitHub Actions (Python 3.10, 3.11, 3.12)
- Ejemplos de uso: `grid_workflow.py`, `direct_polygons.py`, `auto_detect.py`
- Documentación de API en `API.md`
- Licencia MIT
