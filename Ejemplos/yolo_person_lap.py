"""
@author: Luis Guerrero
"""

import cv2
import time
import winsound
from ultralytics import YOLO

# CONFIGURACIÓN GENERAL

CAMERA_INDEX = 1 
# Modelo YOLO seleccionado                
MODEL_PATH = "yolo26n.pt" 
# Umbral mínimo para considerar válida la detección de una persona       
PERSON_CONFIDENCE = 0.70

SHOW_FPS = True                  
BEEP_ENABLED = True              
BEEP_FREQ = 2000                 
BEEP_DURATION_MS = 300           
BEEP_COOLDOWN_S = 1.0            

# CARGAR MODELO Y ABRIR CÁMARA

model = YOLO(MODEL_PATH)
cap = cv2.VideoCapture(CAMERA_INDEX)   # Abre la cámara indicada

# Verifica si la cámara se abrió correctamente
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    #print("Prueba cambiando CAMERA_INDEX a 0, 1 o 2.")
    raise SystemExit

print("Cámara abierta correctamente.")
print("Presiona 'q' para salir.")

# Variables para calcular FPS y controlar tiempo entre beeps
prev_time = time.perf_counter()
last_beep_time = 0.0

# BUCLE PRINCIPAL

while True:
    # Lee un frame de la cámara
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer frame de la cámara.")
        break

    # Ejecuta inferencia con YOLO sobre el frame actual
    # conf=0.25 significa que YOLO mostrará detecciones desde 0.25,
    # pero nosotros aparte filtraremos persona con 0.70
    results = model(frame, conf=0.25, verbose=False)

    # Dibuja automáticamente las cajas y etiquetas detectadas
    annotated_frame = results[0].plot()

    # Variables para saber si hubo persona detectada
    person_detected = False
    best_person_conf = 0.0

    # Obtiene las cajas detectadas en este frame
    boxes = results[0].boxes

    # Si sí hubo detecciones, recorre cada una
    if boxes is not None and len(boxes) > 0:
        for box in boxes:
            # Clase detectada (por ejemplo person, book, tv, etc.)
            cls_id = int(box.cls[0].item())

            # Confianza de la detección
            conf = float(box.conf[0].item())

            # Nombre de la clase detectada
            class_name = model.names[cls_id]

            # Si la clase es "person" y la confianza supera el umbral,
            # marcamos que sí se detectó persona
            if class_name == "person" and conf >= PERSON_CONFIDENCE:
                person_detected = True
                best_person_conf = max(best_person_conf, conf)

    # Si detectó persona y está habilitado el beep,
    # hace un sonido con cierto tiempo de espera entre cada beep
    if person_detected and BEEP_ENABLED:
        now = time.perf_counter()

        # Solo hace beep si ya pasó suficiente tiempo desde el último
        if now - last_beep_time >= BEEP_COOLDOWN_S:
            winsound.Beep(BEEP_FREQ, BEEP_DURATION_MS)
            last_beep_time = now

    # Texto de estado
    if person_detected:
        status_text = f"PERSONA DETECTADA ({best_person_conf:.2f})"
        status_color = (0, 0, 255)   # Rojo
    else:
        status_text = "Sin persona >= 0.70"
        status_color = (0, 255, 0)   # Verde

    # Escribe el texto de estado en la imagen
    cv2.putText(
        annotated_frame,
        status_text,
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        status_color,
        2
    )

    # Calcula y muestra FPS si está activado
    if SHOW_FPS:
        current_time = time.perf_counter()
        fps = 1.0 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.1f}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (255, 255, 0),
            2
        )

    # Muestra la ventana principal
    cv2.imshow("YOLO Detección de personas", annotated_frame)

    # Si se presiona la tecla q, termina el programa
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# CIERRE DEL PROGRAMA

cap.release()              
cv2.destroyAllWindows()     
print("Programa terminado.")