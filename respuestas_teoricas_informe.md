# Guía de texto para el informe – TP1 (Procesamiento de Imágenes I)

Este archivo sigue la **misma numeración** que conviene usar en el documento de entrega. Copiá cada bloque a tu Word/PDF y reemplazá los datos de consola si tu imagen cambia. Las figuras deben ser las de `resultados_tp1/` generadas con `tp1_imagenes.py`.

**Mapeo rápido**

| En tu informe | Contenido en este archivo |
|---------------|---------------------------|
| Carátula / repo | Bloque inicial (completar grupo, nombres, link) |
| **1.** Imagen utilizada | §1 |
| **2.** Cuatro resoluciones | §2 |
| **3.** Muestreo a la mitad | §3 (+ Fig. 1 y 2) |
| **4.** Cuantificación a la mitad | §4 (+ Fig. 3) |
| **5.** Preguntas de análisis | §5.1 a §5.4 |
| **6.** Síntesis | §6 |

---

## Carátula (ejemplo – ajustar si hace falta)

**Trabajo práctico 1 – Grupo 1**  
**Materia:** Procesamiento de Imágenes I  
**Alumnos:** Mateo Hernández, Felipe Lucero  
**Repositorio de GitHub:** https://github.com/mateoHernandez123/procesamiento-imagenes-i-tp-1  

---

## 1. Imagen utilizada

Imagen en **escala de grises** (una sola banda).

**Datos obtenidos del análisis** (ejemplo de una corrida; actualizar con la salida de consola de `python tp1_imagenes.py`):

- **Dimensiones:** 622 × 350 píxeles  
- **Total de píxeles:** 217 700  
- **Tipo de dato:** `uint8`  
- **Profundidad:** 8 bits (256 niveles de gris, valores 0 a 255)  
- **Media:** 223,73  
- **Desvío estándar:** 57,40  
- **Moda:** 248  

---

## 2. Los cuatro tipos de resolución (según la clase)

- **Resolución espacial:** cantidad de píxeles en la imagen (ancho × alto). Define cuánto detalle espacial se puede representar.

- **Resolución radiométrica:** cantidad de niveles de gris que puede tomar cada píxel (relacionado con los bits por píxel; p. ej. 8 bits → 256 niveles). Define la precisión tonal.

- **Resolución espectral:** número de bandas o canales. En escala de grises hay **una sola banda**.

- **Resolución temporal:** información en el tiempo. En una **foto estática** **no aplica** (una sola captura).

---

## 3. Modificación del muestreo a la mitad

En el código se aplica **submuestreo espacial** tomando **una fila y una columna de cada dos**, equivalente a **`I[::2, ::2]`**. Para una imagen de **622 × 350** píxeles, la **grilla decimada** tiene **311 × 175** valores (menos muestras espaciales independientes).

A continuación, esa grilla se **re-escala** al tamaño original **622 × 350** con **interpolación por vecino más cercano** (`INTER_NEAREST`), de modo que el archivo **`muestreo_mitad.png`** conserva el **mismo tamaño digital** que la original y se puede comparar en el informe. **No** disminuye la cantidad de píxeles del archivo; lo que baja es la **resolución espacial efectiva** (cada valor de la grilla fina se repite en bloques aproximadamente 2×2).

**Figura 1 – Original** (`resultados_tp1/original.png`)

**Figura 2 – Muestreo a la mitad** (`resultados_tp1/muestreo_mitad.png`)

**Observación:** se percibe **menor detalle** y **pérdida de definición** en bordes y texturas, con aspecto más **pixelado o en bloques**, coherente con un submuestreo seguido de expansión por vecino más cercano (no es solo “menos píxeles en el archivo”).

---

## 4. Modificación de la cuantificación a la mitad

Se reduce la **resolución radiométrica** pasando de **256 a 128** niveles de gris, agrupando valores consecutivos de a dos en el rango 0–255 (cuantización uniforme: **Q(v) = (v // 2) × 2**). La **resolución espacial** (622 × 350) **no cambia**.

**Figura 3 – Cuantificación a la mitad** (`resultados_tp1/cuantificacion_mitad.png`)

**Observación:** puede verse **menor suavidad** en los gradientes y, en algunas zonas, **bandas** o **posterización** entre tonos vecinos.

---

## 5. Preguntas de análisis

### 5.1 ¿Cuál es la diferencia entre reducir el muestreo (punto 3) y aplicar zoom 50%?

**Reducir el muestreo** en este proyecto: se **submuestrea** la imagen (equivalente a **`I[::2, ::2]`**), con **menos muestras espaciales independientes**. La salida se **re-escala** al **mismo tamaño digital H×W** que la original con **vecino más cercano** para el informe; **se pierde detalle espacial** (bloques / menor resolución efectiva). Si solo se guardara la grilla decimada **sin** re-escalar, las dimensiones serían la mitad en cada eje (en el ejemplo, de **622×350** a **311×175**).

**Aplicar zoom al 50%** en un visor solo cambia **cómo se muestra** la imagen en pantalla; **no modifica los datos** almacenados: siguen siendo los mismos píxeles y la misma información.

**Conclusión:** el muestreo **sí** reduce la **información espacial útil**; el zoom solo cambia la **presentación visual** sin alterar los valores del archivo.

---

### 5.2 ¿Cuál es la diferencia entre reducir la cuantificación (punto 4) y mejorar la resolución radiométrica?

**Reducir la cuantificación** implica **usar menos niveles de gris** (p. ej. de 256 a 128). Se **pierde precisión tonal** y pueden aparecer **bandas** o contornos falsos en gradientes suaves (**posterización**). Es una **degradación** de la imagen.

**Mejorar la resolución radiométrica** implica **aumentar** los niveles (p. ej. más bits por píxel: 10, 12, 16 bits). Hay **más precisión** tonal, transiciones más suaves y mejor detalle en sombras y luces. Es una **mejora**.

**Conclusión:** reducir cuantificación **degrada** la imagen (menos niveles); aumentar la resolución radiométrica la **mejora** (más niveles y mejor precisión tonal).

---

### 5.3 ¿Qué implicaría cambiar la resolución espacial?

- **Aumentarla** (más píxeles): más detalle espacial y mejor definición de bordes y texturas; archivos más pesados y más costo de almacenamiento y procesamiento.

- **Disminuirla** (menos píxeles): menos detalle, bordes más gruesos o perdidos, posible pérdida de objetos pequeños; ventaja: archivos más livianos y procesamiento más rápido.

**En resumen:** la resolución espacial determina **cuánto detalle** se puede representar y **cuánta información** se conserva o se pierde a nivel de la grilla de píxeles.

---

### 5.4 ¿Qué implicaría cambiar la resolución radiométrica?

- **Aumentarla** (más bits por píxel): más niveles de gris, transiciones más suaves, mejor detalle tonal en sombras y luces; posiblemente archivos más grandes.

- **Disminuirla** (menos bits): menos niveles, **bandas** o posterización en gradientes, pérdida de detalle tonal; archivos más pequeños.

**En resumen:** la resolución radiométrica determina la **precisión tonal** (cuántos tonos distintos se pueden representar).

---

## 6. Síntesis

La **reducción del muestreo** afecta los **detalles espaciales** (cantidad de muestras en la escena y nitidez aparente). La **reducción de la cuantificación** afecta la **calidad tonal** (suavidad de gradientes y cantidad de niveles de gris).

Ambos procesos pueden implicar **pérdida de información**, pero en **dimensiones distintas**: el muestreo impacta en la **estructura espacial** (qué tan fina es la grilla de muestreo y cuánta información espacial distinta queda) y la cuantificación en la **representación de la intensidad** (con cuánta precisión se representa cada píxel).

---
