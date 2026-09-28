"""Ejemplo: flujo completo con grilla (Fase 1 y Fase 3)."""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_polygon_renderer.engine import (
    preparar_imagen_para_ia,
    renderizar_poligonos_desde_grid,
)


def main():
    ruta_imagen = os.path.join(os.path.dirname(__file__), "..", "vaca.png")

    print("Fase 1: preparando imagen con grilla...")
    resultado = preparar_imagen_para_ia(ruta_imagen, filas=10, columnas=10)
    mapa_celdas = resultado["mapa_celdas"]
    print(f"  Imagen con grilla: {resultado['imagen_con_grilla']}")
    print(f"  Dimensiones: {resultado['dimensiones']}")

    json_ia = {
        "poligonos_grid": [
            {"id": "Cabeza", "celdas": ["A2", "A3", "B2", "B3"]},
            {"id": "Cuello", "celdas": ["B4", "C3", "C4"]},
            {"id": "Paleta", "celdas": ["B5", "C5", "D4", "D5"]},
            {"id": "Pecho", "celdas": ["B6", "B7", "C6", "C7"]},
            {"id": "Costilla", "celdas": ["D3", "E3", "E4", "F4", "F5"]},
            {"id": "Lomo", "celdas": ["F2", "G2", "G3", "H2", "H3"]},
            {"id": "Vacío", "celdas": ["D6", "D7", "E6", "E7", "F6"]},
            {"id": "Cuadril", "celdas": ["H4", "I3", "I4", "J3", "J4"]},
            {"id": "Cola", "celdas": ["I6", "I7", "J6"]},
            {"id": "Pata Delantera", "celdas": ["C8", "C9", "D8", "D9"]},
            {"id": "Pata Trasera", "celdas": ["F8", "F9", "G8", "G9"]},
        ]
    }

    print("\nFase 3: renderizando poligonos...")
    ruta_final = renderizar_poligonos_desde_grid(ruta_imagen, json_ia, mapa_celdas)
    print(f"  Resultado: {ruta_final}")


if __name__ == "__main__":
    main()
