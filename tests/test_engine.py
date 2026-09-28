import os
import sys

import cv2
import numpy as np
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from mcp_polygon_renderer.engine import (
    preparar_imagen_para_ia,
    renderizar_poligonos_desde_grid,
    renderizar_poligonos_directos,
    detectar_y_colorear_regiones,
)


@pytest.fixture
def imagen_prueba(tmp_path):
    ruta = str(tmp_path / "test.png")
    img = np.full((200, 200, 3), 50, np.uint8)
    cv2.rectangle(img, (50, 50), (150, 150), (200, 200, 200), -1)
    cv2.imwrite(ruta, img)
    return ruta


def test_preparar_imagen_crea_salida(imagen_prueba):
    resultado = preparar_imagen_para_ia(imagen_prueba, filas=10, columnas=10)
    assert os.path.exists(resultado["imagen_con_grilla"])
    assert resultado["dimensiones"]["ancho"] == 200
    assert resultado["dimensiones"]["alto"] == 200
    assert len(resultado["mapa_celdas"]) == 100
    assert "A1" in resultado["mapa_celdas"]
    assert "J10" in resultado["mapa_celdas"]


def test_preparar_imagen_mapa_celdas_valido(imagen_prueba):
    resultado = preparar_imagen_para_ia(imagen_prueba, filas=10, columnas=10)
    celda = resultado["mapa_celdas"]["A1"]
    assert celda["x"] == 0
    assert celda["y"] == 0
    assert celda["x1"] == 20
    assert celda["y1"] == 20
    assert celda["cx"] == 10
    assert celda["cy"] == 10


def test_preparar_imagen_mas_filas(imagen_prueba):
    resultado = preparar_imagen_para_ia(imagen_prueba, filas=5, columnas=5)
    assert len(resultado["mapa_celdas"]) == 25


def test_preparar_imagen_archivo_no_existe(tmp_path):
    with pytest.raises(FileNotFoundError):
        preparar_imagen_para_ia(str(tmp_path / "no_existe.png"))


def test_renderizar_desde_grid(imagen_prueba):
    prep = preparar_imagen_para_ia(imagen_prueba, filas=10, columnas=10)
    json_ia = {"poligonos_grid": [{"id": "Test", "celdas": ["E5", "F5", "E6", "F6"]}]}
    ruta_final = renderizar_poligonos_desde_grid(imagen_prueba, json_ia, prep["mapa_celdas"])
    assert os.path.exists(ruta_final)


def test_renderizar_poligonos_directos(imagen_prueba):
    poligonos = [{"id": "Triangulo", "puntos": [[50, 50], [150, 50], [100, 150]]}]
    ruta_final = renderizar_poligonos_directos(imagen_prueba, poligonos)
    assert os.path.exists(ruta_final)


def test_renderizar_poligonos_directos_dos_poligonos(imagen_prueba):
    poligonos = [
        {"id": "T1", "puntos": [[20, 20], [60, 20], [40, 60]]},
        {"id": "T2", "puntos": [[100, 100], [150, 100], [125, 150]]},
    ]
    ruta_final = renderizar_poligonos_directos(imagen_prueba, poligonos)
    assert os.path.exists(ruta_final)


def test_detectar_regiones_vaca():
    ruta = os.path.join(os.path.dirname(__file__), "..", "vaca.png")
    if not os.path.exists(ruta):
        pytest.skip("vaca.png no disponible")
    ruta_final, num_regiones = detectar_y_colorear_regiones(ruta)
    assert os.path.exists(ruta_final)
    assert num_regiones >= 30
