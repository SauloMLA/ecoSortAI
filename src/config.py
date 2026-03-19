"""
EcoSort IA — Configuracion central del proyecto
================================================
Todas las constantes y configuraciones en un solo lugar.
"""

# --- Categorias de clasificacion ---
# Decision D-004 (S002): 4 categorias definidas
CLASES = ["plastico", "papel", "carton", "aluminio"]
NUM_CLASES = len(CLASES)

# --- Configuracion del modelo ---
IMG_SIZE = (224, 224)          # Input size para MobileNetV2
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001
VALIDATION_SPLIT = 0.2         # 80% train, 20% validation
CONFIDENCE_THRESHOLD = 0.70    # Minimo 70% para actuar

# --- Rutas ---
DATASET_DIR = "dataset"        # Carpeta con subcarpetas por clase
MODEL_SAVE_PATH = "models/ecosort_model.keras"
TFLITE_MODEL_PATH = "models/ecosort_model.tflite"
TFLITE_INT8_PATH = "models/ecosort_model_int8.tflite"

# --- Hardware (Raspberry Pi 5) ---
# Diseño v4: Bote CUADRADO 40x40x70 cm con piramide invertida
# Camara en arco metalico sobre el bote (~15 cm), mirando al centro
# 4 solapas triangulares (3-5mm) = superficie superior del bote
# EL SERVO ES LA BISAGRA — montado por FUERA de la pared
# Por compuerta: 1 servo + 1 horn + 2 tornillos + 1 agujero en pared
# Total: 4 servos, 4 horns, 8 tornillos, 4 agujeros

# --- Servos SG90 (4 solapas) ---
SERVO_PINS = {
    "plastico": 17,         # GPIO 17 — S1 Frente (azul)
    "papel": 27,            # GPIO 27 — S2 Atras (verde)
    "carton": 22,           # GPIO 22 — S3 Derecha (naranja)
    "aluminio": 23,         # GPIO 23 — S4 Izquierda (gris)
}

# Angulos del servo SG90
SERVO_CERRADO = 20          # 20° — solapa inclinada formando piramide (PWM ~1.0ms)
SERVO_ABIERTO = 75          # 75° — solapa abierta, objeto cae al bote (PWM ~1.8ms)
SERVO_FREQ = 50             # Frecuencia PWM en Hz (estandar para servos)

# PWM para SG90:
# 20° cerrado → pulso ~1.0ms
# 75° abierto → pulso ~1.8ms
# Formula: duty = 2.5 + (angulo / 180.0) * 10.0

# Tiempos del ciclo
TIEMPO_APERTURA_SERVO = 0.5 # Segundos para que el servo llegue a posicion
TIEMPO_ESPERA_CAIDA = 1.5   # Segundos de espera para que el objeto caiga
TIEMPO_DISPLAY = 2.0        # Segundos que la pantalla muestra el resultado

# Trigger sensor (IR)
TRIGGER_PIN = 24             # Pin GPIO para sensor de proximidad IR

# --- LEDs de prueba (RPi) ---
# Un LED por clase. Mismo mapeo que servos para reutilizar pines.
# Plástico=azul, Papel=verde, Cartón=naranja, Aluminio=gris
LED_PINS = {
    "plastico": 17,
    "papel": 27,
    "carton": 22,
    "aluminio": 23,
}
TIEMPO_LED_ENCENDIDO = 2.0   # Segundos que el LED permanece encendido

# --- Dashboard ---
DASHBOARD_HOST = "0.0.0.0"
DASHBOARD_PORT = 5000
