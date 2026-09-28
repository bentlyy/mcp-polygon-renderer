"""Ejemplo: poligonos con coordenadas directas en pixeles (sin grilla)."""

import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_polygon_renderer.engine import renderizar_poligonos_directos


def generar_circulo(cx, cy, radio, num_puntos=36):
    return [
        [int(cx + radio * math.cos(2 * math.pi * i / num_puntos)),
         int(cy + radio * math.sin(2 * math.pi * i / num_puntos))]
        for i in range(num_puntos)
    ]


def main():
    ruta_imagen = os.path.join(os.path.dirname(__file__), "..", "vaca.png")

    poligonos = [
        {"id": "Circulo Arriba", "puntos": generar_circulo(350, 100, 60)},
        {"id": "Circulo Abajo", "puntos": generar_circulo(350, 400, 60)},
        {"id": "Triangulo", "puntos": [[100, 300], [200, 200], [300, 300]]},
        {"id": "Estrella", "puntos": [[550, 300], [570, 340], [620, 340], [585, 370], [600, 420], [550, 395], [500, 420], [515, 370], [480, 340], [530, 340]]},
    ]

    print("Renderizando poligonos directos...")
    ruta_final = renderizar_poligonos_directos(ruta_imagen, poligonos)
    print(f"Resultado: {ruta_final}")


if __name__ == "__main__":
    main()
