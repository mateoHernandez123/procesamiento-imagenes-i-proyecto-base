# Respuestas teóricas para el informe – TP1

Use estas respuestas como guía para redactar la parte teórica de su informe.

---

## 1. ¿Cuál es la diferencia del proceso aplicado en el punto 3 (reducir muestreo) y aplicar un zoom 50% a una imagen?

**Reducir el muestreo** (punto 3) implica **cambiar la resolución espacial real** de la imagen: se disminuye la cantidad de píxeles (por ejemplo, de 624×351 a 312×175). Se **elimina información**: menos muestras espaciales, menos detalle, bordes más “pixelados” o perdidos.

**Aplicar zoom al 50%** en un visor o editor solo **reduce la forma en que se muestra** la imagen en pantalla (se ve más chica), pero **no modifica los datos**: la imagen sigue teniendo el mismo número de píxeles y la misma información. No hay pérdida de resolución espacial.**Conclusión:** El muestreo cambia la resolución espacial real (y con ello la información); el zoom solo cambia la presentación visual.

---

## 2. ¿Cuál es la diferencia del proceso aplicado en el punto 4 (reducir cuantificación) y mejorar la resolución radiométrica de una imagen?

**Reducir la cuantificación** (punto 4) implica **usar menos niveles de gris** (por ejemplo, de 256 a 128). Se **pierde precisión tonal**: aparecen “bandas” o contornos falsos en zonas de gradientes suaves (efecto de posterización). Es una **degradación** de la imagen.

**Mejorar la resolución radiométrica** significa **aumentar el número de niveles** (por ejemplo, de 8 a 12 o 16 bits). Hay **más precisión** en los tonos, transiciones más suaves y mejor detalle en sombras y luces. Es una **mejora** de la imagen.

**Conclusión:** Reducir cuantificación degrada la imagen (menos niveles); aumentar la resolución radiométrica la mejora (más niveles y mejor precisión tonal).

---

## 3. ¿Qué implicaría cambiar la resolución espacial de una imagen?

- **Aumentar la resolución espacial** (más píxeles): más detalle espacial, mejor definición de bordes y texturas; pero archivos más pesados y mayor costo de almacenamiento y procesamiento.
- **Disminuir la resolución espacial** (menos píxeles): menos detalle, bordes más gruesos o perdidos, posible pérdida de objetos pequeños o finos; ventaja: archivos más livianos y procesamiento más rápido.

En resumen: la resolución espacial determina **cuánto detalle** se puede representar en la imagen y **cuánta información** se conserva o se pierde a nivel de píxeles.

---

## 4. ¿Qué implicaría cambiar la resolución radiométrica de una imagen?

- **Aumentar la resolución radiométrica** (más bits por píxel): más niveles de gris (o de color), transiciones más suaves, mejor detalle en sombras y luces; posiblemente archivos más grandes.
- **Disminuir la resolución radiométrica** (menos bits): menos niveles, efecto de “bandas” o posterización en gradientes, pérdida de detalle tonal; archivos más pequeños.

En resumen: la resolución radiométrica determina la **precisión tonal** de la imagen (cuántos tonos distintos se pueden representar).

---

## BONUS (recomendado para el informe)

Puede agregar:

_“La reducción del muestreo afecta la **percepción de detalles espaciales** (cantidad de píxeles y nitidez de bordes), mientras que la reducción de la cuantificación afecta la **calidad tonal** de la imagen (suavidad de gradientes y cantidad de niveles de gris).”_
