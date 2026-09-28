"""Ejemplo: deteccion y color automatico de regiones delimitadas por lineas naranjas."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_polygon_renderer.engine import detectar_y_colorear_regiones


def main():
    ruta_imagen = os.path.join(os.path.dirname(__file__), "..", "vaca.png")

    print("Detectando y coloreando regiones...")
    ruta_final, num_regiones = detectar_y_colorear_regiones(ruta_imagen, area_min=20)
    print(f"  Regiones detectadas: {num_regiones}")
    print(f"  Resultado: {ruta_final}")


if __name__ == "__main__":
    main()
