# Trabajo Práctico 1 – Procesamiento de Imágenes

## Cómo ejecutar

1. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

2. **Poner tu imagen en escala de grises**
   - Opción A: Guardar la imagen como `imagen.png` (o `.jpg`) en la carpeta del proyecto (junto a `tp1_imagenes.py`).
   - Opción B: Poner la imagen en la carpeta `assets/` (cualquier nombre `.png` o `.jpg`).
   - Opción C: Pasar la ruta por línea de comandos (ver abajo).

3. **Ejecutar el script**

   ```bash
   python tp1_imagenes.py
   ```

   O con ruta explícita:

   ```bash
   python tp1_imagenes.py ruta/a/tu_imagen.png
   ```

4. **Solo informe por consola (sin ventanas de gráficos)**
   ```bash
   python tp1_imagenes.py --sin-graficos
   ```

## Qué hace el script

Todo el procesamiento y la visualización se realizan con **OpenCV** (`cv2`): carga, conversión a grises, estadísticos (media y desvío con `cv2.meanStdDev`), redimensionado (`cv2.resize`), visualización (`cv2.imshow`) y guardado en PNG (`cv2.imencode` + escritura en disco). Solo se usa NumPy para la moda (OpenCV no la provee).

- Carga la imagen en escala de grises (si está en color, la convierte con `cv2.cvtColor`).
- Imprime en consola: escena, tamaño digital, formato, resoluciones (espacial, radiométrica, espectral, temporal), sensor y estadísticos (media, desvío estándar, moda).
- Muestra la imagen original.
- Reduce el **muestreo** espacial con paso 2 en fila y columna (`img[::2, ::2]`) y vuelve a la misma resolución digital **H×W** con re-escalado por vecino más cercano; muestra y guarda el resultado.
- Reduce la **cuantificación** a la mitad (resolución radiométrica) y muestra el resultado.
- Guarda las tres imágenes en `resultados_tp1/` para que puedas usarlas en el informe.

## Documentación matemática (cuentas y fórmulas del TP)

Esta sección concentra **qué se calcula** en cada paso del script: definiciones, expresiones y vínculo con las funciones en `tp1_imagenes.py`. Sirve como base para el **informe** (descripción del procedimiento y resultados).

### Notación y tipo de dato

- La imagen en escala de grises es una matriz **I** con **H** filas (alto) y **W** columnas (ancho). En NumPy/OpenCV: `H, W = img.shape` (orden **fila, columna**).
- Cada píxel **I(i, j)** (con **i = 0 … H−1**, **j = 0 … W−1**) es un entero en el rango de grises definido por el tipo. Lo habitual en este TP es **`uint8`**: **I(i, j) ∈ {0, 1, …, 255}** → **L = 256** niveles distintos (**8 bits** por píxel).
- **Número total de píxeles:** **N = H · W**.
- Si la entrada está en color, antes de analizar se obtiene un canal de luminancia en gris con `cv2.cvtColor(..., COLOR_BGR2GRAY)` (combinación lineal estándar de canales B, G, R; la implementación exacta la fija OpenCV). A partir de ahí valen las mismas cuentas sobre **I**.

### Imagen original (`original.png`)

- **Operación:** decodificar el archivo y, si corresponde, pasar a una sola banda de grises. **No** hay una fórmula pixel a pixel propia del TP sobre **I** más que la conversión a gris del visor/cámara; la matriz resultante es **`uint8`** de tamaño **H × W**.

### Estadísticos (consola; no producen una imagen nueva)

Se trabaja con la lista de **N** intensidades **x₁, x₂, …, x_N** (todos los **I(i, j)** en cualquier orden).

1. **Media aritmética** (intensidad promedio), sumando los **N** píxeles:

   **μ = (1/N) · (x₁ + x₂ + … + x_N)**

   En el código: `cv2.meanStdDev(img)` devuelve **μ** en el canal de grises.

2. **Desvío estándar** de las intensidades (dispersión alrededor de la media), en el sentido que usa OpenCV para el arreglo completo (desviación típica de la población de píxeles):

   **σ = √( (1/N) · Σ (x_k − μ)² )**, donde la suma recorre **k = 1 … N**.

   En el código: segunda salida de `cv2.meanStdDev(img)`.

3. **Histograma** (conteo por nivel de gris): para cada **g ∈ {0,…,255}**,

   **h(g) = #{ (i, j) : I(i, j) = g }**

   (cantidad de píxeles con valor **g**).

4. **Moda** (nivel de gris más frecuente):

   **g\* = arg max_g h(g)**

   En el código: `numpy.bincount` sobre los píxeles aplanados (conteos por **g**) y **`argmax`** para obtener **g\***.

### Reducción del muestreo a la mitad — resolución espacial (`muestreo_mitad.png`)

Objetivo: **bajar la frecuencia de muestreo espacial** (una muestra cada dos filas y cada dos columnas), manteniendo **256** niveles por píxel (`uint8`), y —si se pide el **mismo tamaño digital** que la original— devolver una matriz otra vez **H × W**.

**Paso 1 — submuestreo (decimación):** la imagen intermedia **D** se obtiene con el mismo efecto que **`I[::2, ::2]`**:

- **D(k, l) = I(2k, 2l)** para los índices válidos.
- **D** tiene tamaño aproximado **⌈H/2⌉ × ⌈W/2⌉**. Cantidad de muestras espacialmente **independientes** tras este paso: **N_dec ≈ ⌈H/2⌉ · ⌈W/2⌉** (para **H** y **W** pares, **N_dec = N/4**).

En una matriz **H×W** siempre hay **N** valores almacenados; la frase “menos píxeles” aquí significa **menos información espacial distinta**: solo esos **N_dec** valores provienen de la escena; el resto se **reconstruye** al paso 2.

**Paso 2 — mismo tamaño digital H×W:** se re-escala **D** al tamaño original **(W, H)** con **`cv2.resize(..., INTER_NEAREST)`** (vecino más cercano). Cada valor de **D** se repite en un bloque local 2×2 (hasta ajustes en bordes si **H** o **W** es impar). La salida **I′** tiene forma **H × W**, **`uint8`**, y se ve en “bloques” o más pixelada que **I**, coherente con menor resolución espacial efectiva.

**Nota:** Si la consigna solo pidiera “submuestrear” sin mantener **H×W**, bastaría con guardar **D** (imagen más chica). Este proyecto también hace el paso 2 para comparar con la original **misma grilla** y mismo número de celdas en el archivo.

### Reducción de la cuantificación a la mitad — resolución radiométrica (`cuantificacion_mitad.png`)

Objetivo: **menos niveles de gris** por píxel, **sin cambiar** **H** ni **W**.

**Hipótesis del código:** imagen **uint8**, **L = 256** niveles en **{0,…,255}**.

1. **Niveles de salida (cardinal teórico):** **L′ = L // 2** → para **L = 256**, **L′ = 128** niveles representables (el script informa “256 → 128”).

2. **Paso de cuantificación uniforme** en el eje 0–255:

   **Δ = 256 // L′**

   (división entera). Para **L′ = 128** resulta **Δ = 2**: se agrupan los enteros consecutivos de a **2** valores (**{0,1}**, **{2,3}**, …, **{254,255}**).

3. **Función de cuantificación** por píxel, para cada intensidad **v ∈ {0,…,255}**:

   **Q(v) = ⌊v / Δ⌋ · Δ**

   que en Python/NumPy con enteros es **`(v // Δ) * Δ`**. Para **Δ = 2** los valores posibles de **Q(v)** son **0, 2, 4, …, 254** (**128** valores distintos).

4. **Imagen cuantizada:** **I_q(i, j) = Q( I(i, j) )**, mismas dimensiones **H × W**, tipo **`uint8`** tras acotar al rango válido.

En resumen: es un **cuantizador uniforme** que reduce la precisión radiométrica a la mitad de niveles respecto de **256**, sin alterar el muestreo espacial.

### Resumen de fórmulas (para copiar al informe)

| Bloque | Entrada / notación | Cuenta principal |
| ------ | ------------------ | ---------------- |
| Píxeles | **H, W**, **N = H·W** | — |
| Media | **x_k** intensidades | **μ = (1/N) Σ x_k** |
| Desvío | **μ** | **σ = √((1/N) Σ (x_k − μ)²)** |
| Histograma | **I(i,j)** | **h(g)** = píxeles con valor **g** |
| Moda | **h(g)** | **g\* = arg max_g h(g)** |
| Muestreo ½ | **H, W** | **D = I[::2,::2]**; salida **H×W**: **`resize(D, (W,H), NEAREST)`** |
| Cuantif. ½ | **L = 256** | **L′ = L//2**, **Δ = 256//L′**, **Q(v) = (v//Δ)·Δ** |
