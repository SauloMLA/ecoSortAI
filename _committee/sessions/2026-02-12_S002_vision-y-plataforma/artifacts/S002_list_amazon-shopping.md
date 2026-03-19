# Lista de Compras Amazon — EcoSort IA MVP

**Sesion:** S002  
**Autor:** Embedded Engineer + Chair  
**Fecha:** 2026-02-12

---

## Componentes criticos (comprar primero)

### 1. Raspberry Pi 5 (4GB)
- **Link:** https://www.amazon.com/CanaKit-Raspberry-Starter-Kit-PRO/dp/B0CRSNCJ6Y
- **Precio estimado:** ~$60–90 (segun kit)
- **Nota:** El kit CanaKit incluye case + disipador. Si compras solo la placa, necesitas case aparte.

### 2. Fuente de alimentacion oficial 27W USB-C
- **Link:** https://www.amazon.com/Official-Type-C-Supply-Raspberry-XYGStudy/dp/B0CSMBR63K
- **Precio estimado:** ~$12
- **CRITICO:** No usar cargador de celular. La RPi 5 necesita 5.1V/5A estable.

### 3. Active Cooler oficial
- **Link:** https://www.amazon.com/Raspberry-Pi-Active-Cooler/dp/B0CLXZBR5P
- **Precio estimado:** ~$5–8
- **Nota:** Imprescindible si vas a correr inferencia IA continua.

### 4. MicroSD 32GB (Samsung EVO Select)
- **Link:** https://www.amazon.com/Samsung-Select-Memory-MB-ME32DA-AM/dp/B01DOB6Y5Q
- **Precio estimado:** ~$8–10
- **Nota:** Clase U1 minimo. 32GB es suficiente para el OS + modelo + datos.

### 5. Camara Raspberry Pi Module 3
- **Link:** https://www.amazon.com/Raspberry-Pi-Camera-Module/dp/B0BRY6MVXL
- **Precio estimado:** ~$25–35
- **Specs:** 12MP, autofocus, HDR, 75° FOV, conector MIPI CSI-2
- **Alternativa barata:** Webcam USB generica (~$10-15), pero menor calidad y control.

## Componentes para mecanismo de desvio

### 6. Servomotores SG90 (pack de 4-10)
- **Link (pack 4):** https://www.amazon.com/Smraza-Geared-Control-Arduino-Project/dp/B09Y55C21K
- **Link (pack 10):** https://www.amazon.com/ACEIRMC-Helicopter-Airplane-Remote-Control/dp/B09MHHPHLY
- **Precio estimado:** ~$7–17 segun cantidad
- **Nota:** SG90 para prototipo liviano. Si se necesita mas torque: MG996R (~$3-5 c/u)

## Componentes opcionales (segunda compra)

### 7. LEDs + resistencias (kit)
- **Buscar en Amazon:** "LED assortment kit resistor Arduino"
- **Precio estimado:** ~$5–8
- **Para:** Feedback visual basico (clasificacion exitosa, error, etc.)

### 8. Jumper wires + breadboard
- **Buscar en Amazon:** "breadboard jumper wire kit Arduino"
- **Precio estimado:** ~$8–12
- **Para:** Prototipado de conexiones GPIO ↔ servos/sensores

### 9. Sensor infrarrojo de proximidad (opcional)
- **Buscar en Amazon:** "IR obstacle sensor Arduino"
- **Precio estimado:** ~$3–5
- **Para:** Detectar cuando un objeto entra al sistema (trigger de captura)

---

## Resumen de presupuesto

| Prioridad | Items | Total estimado |
|-----------|-------|---------------|
| Criticos (1-5) | RPi5 + fuente + cooler + SD + camara | ~$110–145 |
| Mecanismo (6) | Servos | ~$7–17 |
| Opcionales (7-9) | LEDs, cables, sensor | ~$16–25 |
| **TOTAL** | **Todo** | **~$133–187 USD** |

---

*Nota: Precios aproximados a febrero 2026. Verificar disponibilidad y envio al momento de compra.*
