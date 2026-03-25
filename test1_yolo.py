
"""
@author: Luis Guerrero
"""

import cv2
from ultralytics import YOLO

# Elegir source (cámara)
# Generalmente, Webcam integrada = 0, Cámara USB = 1 o 2
CAMERA_INDEX = 1

# Escoger modelo YOLO preentrenado
# YOLO26 cuenta con varios modelos (n, s, m, l, x)
# El más preciso es el modelo yolo26x, pero muy demandante en hardware
# Para utilizar en RaspBerry Pi se recomienda usar yolo26n o yolo26s
model = YOLO("yolo26s.pt")

# Definir la fuente de captura
cap = cv2.VideoCapture(CAMERA_INDEX)

# Validación de cámara
if not cap.isOpened():
    print("No se pudo abrir la cámara.")
    print("Prueba cambiando CAMERA_INDEX a 1 o 2.")
    exit()

print("Cámara abierta correctamente.")
print("Presiona 'q' para salir.")

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer frame de la cámara.")
        break

    # Inferencia YOLO, definimos el nivel de confianza aceptable
    results = model(frame, conf=0.15)

    # Dibuja automáticamente las cajas y etiquetas
    annotated_frame = results[0].plot()
    
    # Mostrar la ventana 
    cv2.imshow("YOLO Webcam", annotated_frame)
    
#Cerrar ventana e interrumpir kernel
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
print("Programa terminado.")