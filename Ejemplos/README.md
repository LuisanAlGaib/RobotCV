# Detección de personas con YOLO + Beep

Pruebas preliminar de CV en la que se utiliza **YOLO** para detectar personas en tiempo real mediante una cámara web.  
Si el sistema detecta una **persona** con un nivel de confianza igual o superior a **0.70**, se genera un **beep de alerta** en la computadora.

Esta versión corresponde a una etapa inicial de prueba en laptop, sin integración todavía con Arduino, buzzer físico o motores.

## Funcionamiento general

1. Se carga el modelo YOLO.
2. Se abre la cámara.
3. Se capturan frames en tiempo real.
4. Cada frame se procesa con YOLO.
5. Si se detecta una **persona** con confianza suficiente, se activa un beep.
6. Se muestra la imagen anotada junto con el valor de FPS.

## Parámetros principales

- `CAMERA_INDEX`: cámara a utilizar (`0`, `1`, `2`, etc.).
- `MODEL_PATH`: ruta o nombre del modelo YOLO.
- `PERSON_CONFIDENCE`: umbral mínimo de confianza para persona.
- `SHOW_FPS`: mostrar FPS en pantalla.
- `BEEP_ENABLED`: activar o desactivar beep.
- `BEEP_COOLDOWN_S`: tiempo mínimo entre beeps.

## Salida esperada

Al ejecutar el programa:

- se abre una ventana con la cámara,
- se muestran las detecciones de YOLO,
- aparece un texto indicando si se detectó una persona,
- se muestran los FPS,
- y se reproduce un beep cuando la detección cumple el umbral.
