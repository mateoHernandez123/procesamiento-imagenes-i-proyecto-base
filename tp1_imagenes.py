"""
Trabajo Práctico 1 - Procesamiento de Imágenes I
Análisis de imagen en escala de grises: resoluciones, estadísticos,
reducción de muestreo y cuantificación. Todo el procesamiento con OpenCV.
"""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np


def _ruta_archivo(ruta: str | Path) -> Path:
    """Normaliza la ruta (expande ~, absoluta)."""
    return Path(ruta).expanduser().resolve()


def cargar_imagen(ruta: str | Path) -> np.ndarray:
    """Carga la imagen en escala de grises. Si está en color, la convierte.

    En Windows, cv2.imread falla con rutas que tienen caracteres no ASCII
    (ej. 'Año'). Se lee el archivo con NumPy y se decodifica con cv2.imdecode.
    """
    p = _ruta_archivo(ruta)
    if not p.is_file():
        raise FileNotFoundError(f"No existe el archivo: {p}")

    buf = np.fromfile(p, dtype=np.uint8)
    if buf.size == 0:
        raise FileNotFoundError(f"Archivo vacio o no legible: {p}")

    img = cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE)
    if img is None:
        img_bgr = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        if img_bgr is None:
            raise FileNotFoundError(
                f"No se pudo decodificar la imagen (formato no soportado o corrupto): {p}"
            )
        img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    return img


def guardar_png_gris(destino: Path, img: np.ndarray) -> None:
    """Guarda imagen en escala de grises; compatible con rutas Unicode en Windows."""
    ok, encoded = cv2.imencode(".png", img)
    if not ok:
        raise OSError(f"No se pudo codificar PNG: {destino}")
    destino.write_bytes(encoded.tobytes())


def analizar_imagen(img: np.ndarray) -> dict:
    """Extrae tamaño, tipo de dato y estadísticos de la imagen."""
    alto, ancho = img.shape
    dtype = img.dtype

    # Resolución radiométrica según dtype
    if dtype == np.uint8:
        bits = 8
        niveles = 256
    elif dtype == np.uint16:
        bits = 16
        niveles = 65536
    else:
        bits = "N/A"
        niveles = "N/A"

    # OpenCV: media y desvío estándar con cv2.meanStdDev
    mean_std = cv2.meanStdDev(img)
    media = float(mean_std[0].flat[0])
    std = float(mean_std[1].flat[0])
    # Moda con NumPy (OpenCV no tiene función de moda)
    moda = int(np.argmax(np.bincount(img.ravel(), minlength=256)))

    return {
        "ancho": ancho,
        "alto": alto,
        "dtype": str(dtype),
        "bits": bits,
        "niveles": niveles,
        "media": media,
        "std": std,
        "moda": moda,
    }


def reducir_muestreo(img: np.ndarray) -> np.ndarray:
    """Submuestrea la imagen tomando una fila y una columna de cada dos (equivalente a [::2, ::2]).

    La matriz decimada tiene forma aproximada (⌈H/2⌉, ⌈W/2⌉): menos *muestras espaciales*
    independientes. Para conservar el **mismo tamaño digital** (H×W) que la original al guardar
    o comparar con la imagen base, se re-escala la decimada con interpolación por **vecino más
    cercano**; cada valor de la grilla fina se repite en un bloque 2×2 (salvo bordes si H o W es impar).
    """
    alto, ancho = img.shape
    decimada = img[::2, ::2]
    return cv2.resize(decimada, (ancho, alto), interpolation=cv2.INTER_NEAREST)


def reducir_cuantificacion(img: np.ndarray, niveles_originales: int = 256) -> np.ndarray:
    """Reduce la resolución radiométrica a la mitad (mitad de niveles de gris)."""
    niveles_nuevos = niveles_originales // 2  # ej: 256 -> 128
    paso = 256 // niveles_nuevos  # para mapear 0-255 a niveles_nuevos
    # Cuantificar: agrupar niveles y reescalar para visualización
    img_quant = (img // paso) * paso
    return np.clip(img_quant, 0, 255).astype(np.uint8)


def imprimir_informe(info: dict, ruta_imagen: str):
    """Imprime el informe de análisis para incluir en el TP."""
    print("\n" + "=" * 60)
    print("INFORME DE IMAGEN - TRABAJO PRÁCTICO 1")
    print("=" * 60)
    print(f"\nArchivo: {ruta_imagen}")
    print("\n--- ESCENA ---")
    print("Imagen en escala de grises (una sola banda).")
    print("\n--- TAMAÑO DIGITAL (Resolución espacial) ---")
    print(f"Dimensiones: {info['ancho']} x {info['alto']} píxeles")
    print(f"Total de píxeles: {info['ancho'] * info['alto']}")

    print("\n--- FORMATO ---")
    print(f"Tipo de dato en memoria: {info['dtype']}")

    print("\n--- RESOLUCIÓN RADIOMÉTRICA ---")
    print(f"Profundidad: {info['bits']} bits -> {info['niveles']} niveles de gris (0 a {info['niveles'] - 1})")

    print("\n--- RESOLUCIÓN ESPECTRAL ---")
    print("1 banda (escala de grises).")

    print("\n--- RESOLUCIÓN TEMPORAL ---")
    print("No aplica / imagen estática (una sola captura).")

    print("\n--- SENSOR ---")
    print("Se asume sensor de cámara digital (CMOS/CCD) si la imagen proviene de foto.")

    print("\n--- ESTADÍSTICOS (escala de grises) ---")
    print(f"Media (valor medio):     {info['media']:.2f}")
    print(f"Desvío estándar:         {info['std']:.2f}")
    print(f"Moda:                    {info['moda']}")

    print("\n--- LOS 4 TIPOS DE RESOLUCIÓN ---")
    print("1. Espacial:    número de píxeles (ancho x alto)")
    print("2. Radiométrica: cantidad de niveles de gris (bits por píxel)")
    print("3. Espectral:   número de bandas (1 en gris, 3 en RGB)")
    print("4. Temporal:    información de tiempo (no aplica en foto estática)")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="TP1 - Análisis y procesamiento de imagen en escala de grises")
    parser.add_argument(
        "imagen",
        nargs="?",
        default=None,
        help="Ruta a la imagen (por defecto: imagen.png o assets/*.png en el directorio del script)",
    )
    parser.add_argument(
        "--sin-graficos",
        action="store_true",
        help="No mostrar ventanas con gráficos (solo imprimir informe)",
    )
    args = parser.parse_args()

    base = Path(__file__).resolve().parent
    ruta = args.imagen

    if not ruta:
        candidatos = []
        # Primero buscar en carpeta assets (ej. imagen del TP)
        assets = base / "assets"
        if assets.is_dir():
            for ext in ("*.png", "*.jpg", "*.jpeg", "*.bmp"):
                candidatos.extend(assets.glob(ext))
        candidatos.extend([
            base / "imagen.png",
            base / "imagen.jpg",
            base / "imagen.jpeg",
            base / "imagen.bmp",
        ])
        for c in candidatos:
            if c.exists():
                ruta = str(c)
                break
        if not ruta:
            print("No se encontró ninguna imagen. Pase la ruta como argumento:")
            print("  python tp1_imagenes.py ruta/a/imagen.png")
            print("O coloque 'imagen.png' en el mismo directorio que este script.")
            sys.exit(1)

    ruta_resuelta = str(_ruta_archivo(ruta))
    img = cargar_imagen(ruta)
    info = analizar_imagen(img)
    imprimir_informe(info, ruta_resuelta)

    if not args.sin_graficos:
        cv2.imshow("Imagen original - Escala de grises", img)
        cv2.waitKey(0)

    # --- Punto 3: Muestreo a la mitad (resolución espacial), misma forma H×W en salida ---
    img_mitad_espacial = reducir_muestreo(img)
    dec = img[::2, ::2]
    print("--- MUESTREO REDUCIDO (PASO 2 EN FILA Y COLUMNA, [::2, ::2]) ---")
    print(f"Grilla decimada (muestras independientes): {dec.shape[1]} x {dec.shape[0]}")
    print(
        f"Imagen de salida (mismo tamaño digital que la original): "
        f"{img_mitad_espacial.shape[1]} x {img_mitad_espacial.shape[0]} "
        "(re-escalado NEAREST desde la decimada)"
    )

    if not args.sin_graficos:
        cv2.imshow("Resolucion espacial a la mitad (muestreo reducido)", img_mitad_espacial)
        cv2.waitKey(0)

    # --- Punto 4: Cuantificación a la mitad (resolución radiométrica) ---
    niveles = info["niveles"] if isinstance(info["niveles"], int) else 256
    img_mitad_radiometrica = reducir_cuantificacion(img, niveles)
    print("\n--- CUANTIFICACIÓN REDUCIDA A LA MITAD ---")
    print(f"Niveles originales: {niveles} -> Niveles resultantes: {niveles // 2}")

    if not args.sin_graficos:
        cv2.imshow("Resolucion radiometrica reducida (menos niveles de gris)", img_mitad_radiometrica)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Opcional: guardar resultados para el informe
    out_dir = base / "resultados_tp1"
    out_dir.mkdir(exist_ok=True)
    guardar_png_gris(out_dir / "original.png", img)
    guardar_png_gris(out_dir / "muestreo_mitad.png", img_mitad_espacial)
    guardar_png_gris(out_dir / "cuantificacion_mitad.png", img_mitad_radiometrica)
    print(f"\nImágenes guardadas en: {out_dir}")


if __name__ == "__main__":
    main()
