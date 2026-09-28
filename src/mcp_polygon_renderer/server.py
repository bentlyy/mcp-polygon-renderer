import base64
import json

from mcp.server.mcpserver import MCPServer

from .engine import (
    preparar_imagen_para_ia,
    renderizar_poligonos_desde_grid,
    renderizar_poligonos_directos,
    detectar_y_colorear_regiones,
)

mcp = MCPServer("polygon-renderer")


def _img_a_base64(ruta):
    with open(ruta, "rb") as f:
        return base64.b64encode(f.read()).decode()


@mcp.tool()
def preparar_imagen(ruta_imagen: str, filas: int = 10, columnas: int = 10) -> str:
    """Fase 1: superpone una grilla etiquetada (A1, B2...) sobre la imagen.

    Args:
        ruta_imagen: Ruta absoluta a la imagen.
        filas: Numero de filas de la grilla (default 10).
        columnas: Numero de columnas de la grilla (default 10).

    Returns:
        JSON con la ruta de la imagen con grilla, el mapa de celdas en pixeles
        y las dimensiones de la imagen.
    """
    resultado = preparar_imagen_para_ia(ruta_imagen, filas, columnas)
    return json.dumps(resultado, ensure_ascii=False)


@mcp.tool()
def renderizar_desde_grid(
    ruta_imagen: str,
    json_ia: str,
    mapa_celdas: str,
) -> str:
    """Fase 3: renderiza poligonos a partir de celdas de grilla.

    Args:
        ruta_imagen: Ruta a la imagen original.
        json_ia: JSON string con estructura {"poligonos_grid": [{"id": "...", "celdas": ["B3", "C3"]}]}.
        mapa_celdas: JSON string con el mapa de celdas devuelto por preparar_imagen.

    Returns:
        Ruta de la imagen final con los poligonos renderizados.
    """
    json_ia_dict = json.loads(json_ia)
    mapa = json.loads(mapa_celdas)
    ruta_final = renderizar_poligonos_desde_grid(ruta_imagen, json_ia_dict, mapa)
    return ruta_final


@mcp.tool()
def renderizar_poligonos(
    ruta_imagen: str,
    poligonos: str,
) -> str:
    """Renderiza poligonos con coordenadas directas en pixeles (sin grilla).

    Args:
        ruta_imagen: Ruta a la imagen original.
        poligonos: JSON string con estructura [{"id": "...", "puntos": [[x, y], ...]}].

    Returns:
        Ruta de la imagen final con los poligonos renderizados.
    """
    poligonos_list = json.loads(poligonos)
    ruta_final = renderizar_poligonos_directos(ruta_imagen, poligonos_list)
    return ruta_final


@mcp.tool()
def detectar_regiones(ruta_imagen: str, area_min: int = 20) -> str:
    """Detecta y colorea automaticamente las regiones delimitadas por lineas naranjas.

    Args:
        ruta_imagen: Ruta a la imagen con las regiones marcadas.
        area_min: Area minima en pixeles para considerar una region (default 20).

    Returns:
        JSON con la ruta de la imagen coloreada y el numero de regiones detectadas.
    """
    ruta_final, num_regiones = detectar_y_colorear_regiones(ruta_imagen, area_min)
    return json.dumps({"ruta": ruta_final, "num_regiones": num_regiones}, ensure_ascii=False)


@mcp.tool()
def ver_imagen(ruta_imagen: str) -> str:
    """Devuelve una imagen en base64 para que la IA pueda verla.

    Args:
        ruta_imagen: Ruta a la imagen.

    Returns:
        String base64 de la imagen (PNG).
    """
    return _img_a_base64(ruta_imagen)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
