# Diseño del Mecanismo v2 — Bote Cilindrico con Rampa Giratoria

**Sesion:** S002  
**Autores:** CAD Architect, Mechanical Engineer, Anti-Jam Specialist  
**Fecha:** 2026-02-12  
**Revision:** 2.0 — Rediseño cilindrico basado en boceto del equipo  
**Plano:** S002_sketch_technical-blueprint.png

---

## Concepto general

Bote de basura **cilindrico** con 4 compartimentos internos radiales
(tipo rebanadas de pastel) y una **rampa giratoria central** que dirige
cada objeto al compartimento correcto despues de la clasificacion por IA.

---

## DIMENSIONES GENERALES

| Componente | Medida | Nota |
|-----------|--------|------|
| **Altura total** | 90 cm | Altura comoda para depositar basura de pie |
| **Diametro exterior** | 50 cm | Tamaño similar a bote de basura estandar |
| **Apertura superior** | 20 cm diametro | Suficiente para botellas, latas, papel |
| **Zona de camara** | 15 cm alto | Camara + iluminacion LED |
| **Zona de mecanismo** | 15 cm alto | Rampa giratoria + servo |
| **Zona de compartimentos** | 50 cm alto | 4 contenedores extraibles |
| **Base solida** | 10 cm alto | Estabilidad + electronica |

---

## ZONA 1 — APERTURA Y TAPA (arriba)

```
    ┌──────────────────┐
    │   Apertura 20cm  │  ← El usuario deposita el residuo aqui
    │   ┌──────────┐   │
    │   │  (hueco) │   │     Puede tener tapa abatible opcional
    │   └──────────┘   │
    └──────────────────┘
         50cm diam
```

- Apertura circular de **20 cm** de diametro
- Borde elevado de 2-3 cm para evitar que objetos caigan fuera
- Opcion: tapa abatible con sensor que detecta apertura

---

## ZONA 2 — CAMARA DE INSPECCION (15 cm)

```
    ┌──────────────────────┐
    │                      │
    │    ◉ CAMARA (arriba) │  ← Mira hacia abajo
    │                      │
    │  ○ LED  ○ LED  ○ LED │  ← Anillo de LEDs para luz uniforme
    │                      │
    │  [IR]                │  ← Sensor de proximidad infrarrojo
    │                      │
    │  ══════════════════  │  ← Plataforma de inspeccion (fondo blanco)
    │                      │
    └──────────────────────┘
```

| Componente | Especificacion | Posicion |
|-----------|---------------|----------|
| Camara RPi | 5MP o 12MP, mirando abajo | Centro superior de la zona |
| LEDs | Tira LED blanca en anillo | Perimetro interior |
| Sensor IR | Detector de proximidad | Lateral, a nivel del objeto |
| Fondo | Superficie blanca lisa | Base de la zona de inspeccion |

**Flujo:**
1. Objeto cae por la apertura
2. Aterriza en la plataforma de inspeccion (fondo blanco)
3. Sensor IR detecta presencia → trigger
4. Camara toma foto con iluminacion LED controlada
5. RPi clasifica el objeto (~100ms)
6. Se activa el mecanismo de desvio

---

## ZONA 3 — MECANISMO DE RAMPA GIRATORIA (15 cm)

### Este es el corazon del diseño

```
    Vista lateral (corte):

    ═══════════════════  ← Plataforma de inspeccion
           │
           ▼
    ┌─────────────────┐
    │   ╲    RAMPA   ╱│  ← Rampa inclinada montada en eje central
    │    ╲         ╱  │
    │     ╲      ╱    │     Gira 360° con servo
    │      ╲   ╱      │
    │    [SERVO]      │  ← Servo MG996R en el eje central
    │     (eje)       │
    └─────────────────┘
           │
      ┌────┼────┐
      │ Compartimentos │
```

```
    Vista superior (como funciona la rotacion):

                 90° (PAPEL)
                    │
                    │
    0° (PLASTICO) ──┼── 180° (CARTON)
                    │
                    │
                270° (ALUMINIO)

    La rampa apunta a uno de los 4 cuadrantes.
    Despues de clasificar, el servo rota la rampa
    para que apunte al compartimento correcto.
    La plataforma de inspeccion se abre (o la rampa
    se levanta) y el objeto cae por gravedad.
```

### Funcionamiento paso a paso

```
Estado inicial: Rampa en posicion neutral (centro)
                Plataforma cerrada

1. Objeto detectado en plataforma de inspeccion
2. Camara clasifica → resultado: "ALUMINIO" (270°)
3. Servo rota rampa a 270°
4. Plataforma se abre (o segundo servo inclina la rampa)
5. Objeto cae por la rampa hacia compartimento ALUMINIO
6. Plataforma se cierra
7. Rampa vuelve a posicion neutral
8. Listo para siguiente objeto
```

### Componentes del mecanismo

| Componente | Funcion | Especificacion |
|-----------|---------|---------------|
| Servo MG996R | Rotar la rampa | Torque: 10 kg·cm, angulo: 0-360° (o 0-270° con posiciones fijas) |
| Eje central | Soporte de rotacion | Tubo de aluminio o impresion 3D, 8-10mm diametro |
| Rampa | Guiar el objeto por gravedad | Impresion 3D o acrilico, angulo 30-45° |
| Plataforma abatible | Sostener/soltar el objeto | Servo SG90 secundario o mecanismo de bisagra |

### Angulos de rotacion por clase

| Clase | Angulo | Cuadrante |
|-------|--------|-----------|
| Plastico | 0° | Superior-izquierdo |
| Papel | 90° | Superior-derecho |
| Carton | 180° | Inferior-derecho |
| Aluminio | 270° | Inferior-izquierdo |

---

## ZONA 4 — COMPARTIMENTOS (50 cm)

```
    Vista superior de los compartimentos:

         ┌─────────────────────┐
        ╱           │           ╲
       ╱  PLASTICO  │   PAPEL    ╲
      ╱      0°     │    90°      ╲
     │──────────────┼──────────────│
      ╲   ALUMINIO  │   CARTON   ╱
       ╲    270°    │   180°    ╱
        ╲           │          ╱
         └─────────────────────┘

    4 contenedores en forma de cuarto de circulo
    Cada uno es EXTRAIBLE para vaciarlo
```

| Propiedad | Medida |
|-----------|--------|
| Forma | Cuarto de circulo (90° cada uno) |
| Alto | 50 cm |
| Radio | ~23 cm (diametro interior 46 cm con paredes) |
| Capacidad estimada | ~12-15 litros por compartimento |
| Material del contenedor | Plastico reciclado o carton rigido |
| Extraccion | Puerta lateral con bisagra o contenedor deslizable |

### Acceso para vaciar

Opciones:
1. **Puerta lateral** — El cilindro tiene una puerta (o se abre por la mitad) para sacar los contenedores
2. **Parte superior desmontable** — La zona de camara + mecanismo se levanta y se sacan los contenedores por arriba
3. **Cajones deslizables** — Cada compartimento se desliza hacia afuera desde la base

> **Recomendacion:** Opcion 1 (puerta lateral) es la mas practica para un prototipo.

---

## ZONA 5 — BASE (10 cm)

| Componente | Ubicacion |
|-----------|-----------|
| Raspberry Pi 5 | Montada en la base, protegida |
| Fuente de alimentacion | Base, cable de poder sale por atras |
| Cables GPIO | Suben por un canal lateral hacia los servos |
| Ventilacion | Rejillas en la base para circulacion de aire |

---

## ELECTRONICA EN EL EXTERIOR

| Componente | Ubicacion en el bote |
|-----------|---------------------|
| Pantalla/LEDs de estado | Frente, a 70 cm de altura (nivel de vista) |
| Boton de encendido | Atras, en la base |
| Puerto USB (debug) | Atras, en la base |
| Indicador de categoria | Frente — LED de color o mini pantalla |

---

## LISTA DE MATERIALES PARA LA ESTRUCTURA

| Material | Uso | Cantidad estimada | Costo MXN |
|---------|-----|-------------------|-----------|
| Tubo PVC o carton industrial | Cilindro exterior | 1 (50cm diam x 90cm) | $200-400 |
| MDF o acrilico 3mm | Divisiones internas | 2 piezas cortadas | $150-300 |
| Filamento PLA | Rampa, soportes, tolva | ~300g | $100-200 |
| Eje metalico 8mm | Eje central de rotacion | 20cm | $30-50 |
| Rodamiento | Base del eje giratorio | 1 | $30-50 |
| Tornillos, tuercas | Ensamblaje | Kit | $50-100 |
| Pintura | Acabado exterior | 1 lata | $80-150 |
| **Total estructura** | | | **$640-1,250 MXN** |

---

## RESUMEN DE SERVOS NECESARIOS

| Servo | Funcion | Modelo | Torque necesario |
|-------|---------|--------|-----------------|
| Servo 1 (principal) | Rotar rampa a 4 posiciones | MG996R | Alto — carga del objeto + rampa |
| Servo 2 (secundario) | Abrir/cerrar plataforma de inspeccion | SG90 | Bajo — solo abrir compuerta |

> **Nota:** Con este diseño solo necesitas **2 servos** en vez de 4.
> El MG996R rota la rampa y el SG90 abre la plataforma.
> Mas simple, menos puntos de fallo.
