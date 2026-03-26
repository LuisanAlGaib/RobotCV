# Prueba de YOLO en laptop (usando CONDA)

Prueba básica de detección de objetos con **YOLO (Ultralytics)** usando una **webcam USB** en una laptop con Windows.

## Objetivo
Validar que YOLO funcione correctamente en Python con video en vivo antes de migrar a Raspberry Pi.

## Modelos incluidos

Este repositorio incluye algunos archivos de modelos YOLO preentrenados:

- `yolo26n.pt`
- `yolo26s.pt`
- `yolo26m.pt`

Estos archivos corresponden a los pesos del modelo y permiten cargar distintas variantes de YOLO desde Python.

### Descripción de variantes

- **n = nano**: más ligero y rápido.
- **s = small**: balance entre velocidad y capacidad.
- **m = medium**: más pesado y con mayor capacidad.

## Configuración del entorno
Se creó un environment nuevo en Conda para evitar conflictos de dependencias.

```bash
conda create --name yolo_test python=3.11 -y
conda activate yolo_test
conda install -c conda-forge ultralytics --solver=libmamba -y
conda install -c conda-forge opencv -y
python -m pip install torch torchvision

