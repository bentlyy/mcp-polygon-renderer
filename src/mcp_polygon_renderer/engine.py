import os
import gc
import unicodedata

import cv2
import numpy as np


def _sin_acentos(texto):
    return "".join(
        c for c in unicodedata.normalize("NFKD", str(texto)) if not unicodedata.combining(c)
    )


def _cargar_imagen_eficiente(ruta):
    tam = os.path.getsize(ruta)
    if tam > 10 * 1024 * 1024:
        flag = cv2.IMREAD_REDUCED_COLOR_4
    elif tam > 5 * 1024 * 1024:
        flag = cv2.IMREAD_REDUCED_COLOR_2
    else:
        flag = cv2.IMREAD_COLOR
    return cv2.imread(ruta, flag)


def _ruta_salida(ruta_imagen):
    carpeta = os.path.join(os.path.dirname(os.path.abspath(ruta_imagen)), "salida")
    os.makedirs(carpeta, exist_ok=True)
    return carpeta


COLORES_VIVOS = [
    (0, 165, 255), (255, 255, 0), (0, 255, 0), (255, 0, 255),
    (0, 255, 255), (255, 0, 0), (0, 0, 255), (128, 255, 128),
    (0, 100, 255), (255, 255, 128), (128, 0, 255), (255, 128, 0),
    (0, 128, 255), (128, 255, 0), (0, 255, 128), (255, 0, 128),
    (64, 64, 255), (255, 64, 64), (64, 255, 64), (64, 64, 64),
    (0, 191, 255), (255, 191, 0), (191, 255, 0), (255, 0, 191),
    (0, 255, 191), (191, 0, 255), (255, 191, 191), (191, 255, 191),
    (100, 100, 255), (255, 100, 100), (100, 255, 100), (100, 100, 100),
    (150, 150, 255), (255, 150, 150), (150, 255, 150), (150, 150, 150),
    (200, 200, 255), (255, 200, 200), (200, 255, 200), (200, 200, 200),
]


def preparar_imagen_para_ia(ruta_imagen, filas=10, columnas=10):
    img = _cargar_imagen_eficiente(ruta_imagen)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar: {ruta_imagen}")

    h, w = img.shape[:2]
    paso_x = w / columnas
    paso_y = h / filas

    mapa_celdas = {}
    for i in range(filas):
        for j in range(columnas):
            x0 = int(j * paso_x)
            y0 = int(i * paso_y)
            x1 = int((j + 1) * paso_x)
            y1 = int((i + 1) * paso_y)
            clave = f"{chr(65 + j)}{i + 1}"
            mapa_celdas[clave] = {
                "x": x0, "y": y0, "x1": x1, "y1": y1,
                "cx": (x0 + x1) // 2, "cy": (y0 + y1) // 2,
            }

    for j in range(columnas + 1):
        x = int(j * paso_x)
        cv2.line(img, (x, 0), (x, h), (100, 100, 100), 1, cv2.LINE_AA)
    for i in range(filas + 1):
        y = int(i * paso_y)
        cv2.line(img, (0, y), (w, y), (100, 100, 100), 1, cv2.LINE_AA)

    for j in range(columnas):
        x = int((j + 0.5) * paso_x)
        cv2.putText(img, chr(65 + j), (x - 5, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    for i in range(filas):
        y = int((i + 0.5) * paso_y)
        cv2.putText(img, str(i + 1), (4, y + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    ruta_grilla = os.path.join(_ruta_salida(ruta_imagen), "imagen_con_grilla.png")
    cv2.imwrite(ruta_grilla, img)

    del img
    gc.collect()

    return {
        "imagen_con_grilla": ruta_grilla,
        "mapa_celdas": mapa_celdas,
        "dimensiones": {"ancho": w, "alto": h},
    }


def renderizar_poligonos_desde_grid(ruta_imagen_original, json_ia, mapa_celdas):
    img = _cargar_imagen_eficiente(ruta_imagen_original)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar: {ruta_imagen_original}")

    poligonos = json_ia.get("poligonos_grid", [])
    overlay = img.copy()

    for idx, poly in enumerate(poligonos):
        color = COLORES_VIVOS[idx % len(COLORES_VIVOS)]
        celdas = poly.get("celdas", [])
        nombre = poly.get("id", f"Poly{idx}")

        puntos = []
        for celda in celdas:
            info = mapa_celdas.get(celda)
            if info is None:
                continue
            cv2.rectangle(overlay, (info["x"], info["y"]), (info["x1"], info["y1"]), color, -1)
            puntos.append((info["cx"], info["cy"]))

        if len(puntos) >= 3:
            hull = cv2.convexHull(np.array(puntos, dtype=np.int32))
            cv2.polylines(overlay, [hull], True, color, 2, cv2.LINE_AA)

        if puntos:
            cx = int(np.mean([p[0] for p in puntos]))
            cy = int(np.mean([p[1] for p in puntos]))
            cv2.putText(overlay, _sin_acentos(nombre), (cx - 30, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)

    ruta_final = os.path.join(_ruta_salida(ruta_imagen_original), "imagen_con_poligonos.png")
    cv2.imwrite(ruta_final, img)

    del img, overlay
    gc.collect()

    return ruta_final


def renderizar_poligonos_directos(ruta_imagen_original, poligonos):
    img = _cargar_imagen_eficiente(ruta_imagen_original)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar: {ruta_imagen_original}")

    overlay = img.copy()

    for idx, poly in enumerate(poligonos):
        color = COLORES_VIVOS[idx % len(COLORES_VIVOS)]
        puntos = np.array(poly.get("puntos", []), dtype=np.int32)
        nombre = poly.get("id", f"Poly{idx}")

        if len(puntos) < 3:
            continue

        cv2.fillPoly(overlay, [puntos], color)
        cv2.polylines(overlay, [puntos], True, color, 2, cv2.LINE_AA)

        moments = cv2.moments(puntos)
        if moments["m00"] > 0:
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
        else:
            cx = int(np.mean(puntos[:, 0]))
            cy = int(np.mean(puntos[:, 1]))

        (tw, th), _ = cv2.getTextSize(_sin_acentos(nombre), cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(overlay, (cx - tw // 2 - 4, cy - th - 4), (cx + tw // 2 + 4, cy + 6), (0, 0, 0), -1)
        cv2.putText(overlay, _sin_acentos(nombre), (cx - tw // 2, cy + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

    cv2.addWeighted(overlay, 0.45, img, 0.55, 0, img)

    ruta_final = os.path.join(_ruta_salida(ruta_imagen_original), "imagen_poligonos_directos.png")
    cv2.imwrite(ruta_final, img)

    del img, overlay
    gc.collect()

    return ruta_final


def detectar_y_colorear_regiones(ruta_imagen, area_min=20):
    img = cv2.imread(ruta_imagen)
    if img is None:
        raise FileNotFoundError(f"No se pudo cargar: {ruta_imagen}")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_vaca = cv2.bitwise_not(mask_white)

    kernel_close = np.ones((5, 5), np.uint8)
    mask_vaca = cv2.morphologyEx(mask_vaca, cv2.MORPH_CLOSE, kernel_close)

    lower_orange = np.array([5, 60, 60])
    upper_orange = np.array([35, 255, 255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)

    mask_cortes = cv2.bitwise_and(mask_vaca, cv2.bitwise_not(mask_orange))

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(mask_cortes, connectivity=8)

    regiones = []
    for i in range(1, num_labels):
        area = stats[i, cv2.CC_STAT_AREA]
        if area > area_min:
            cx, cy = int(centroids[i][0]), int(centroids[i][1])
            regiones.append({"label": i, "area": int(area), "centroid": [cx, cy]})

    overlay = img.copy()
    for idx, r in enumerate(regiones):
        color = COLORES_VIVOS[idx % len(COLORES_VIVOS)]
        mask_single = (labels == r["label"]).astype(np.uint8) * 255
        contours, _ = cv2.findContours(mask_single, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            cnt = max(contours, key=cv2.contourArea)
            cv2.drawContours(overlay, [cnt], -1, color, -1)

    cv2.addWeighted(overlay, 0.45, img, 0.55, 0, img)

    for idx, r in enumerate(regiones):
        cx, cy = r["centroid"]
        num = str(idx + 1)
        (tw, th), _ = cv2.getTextSize(num, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
        cv2.rectangle(img, (cx - tw // 2 - 3, cy - th - 3), (cx + tw // 2 + 3, cy + 5), (0, 0, 0), -1)
        cv2.putText(img, num, (cx - tw // 2, cy + 2), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)

    ruta_final = os.path.join(_ruta_salida(ruta_imagen), "imagen_coloreada.png")
    cv2.imwrite(ruta_final, img)

    del img, overlay, mask_vaca, mask_orange, mask_cortes, labels, stats
    gc.collect()

    return ruta_final, len(regiones)
