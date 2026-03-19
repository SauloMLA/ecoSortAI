# Diagrama de Vision General — EcoSort IA MVP

**Sesion:** S002  
**Autor:** Product Strategist + Technical Director

---

## Flujo del sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     EcoSort IA — MVP                         │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │ ENTRADA  │──▶│ VISION   │──▶│ DECISION │──▶│ DESVIO   │ │
│  │          │   │          │   │          │   │          │  │
│  │ El objeto│   │ Camara + │   │ Modelo   │   │ Mecanismo│ │
│  │ entra al │   │ ilumina- │   │ de IA    │   │ fisico   │ │
│  │ sistema  │   │ cion     │   │ clasifica│   │ redirige │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                     │        │
│                                              ┌──────▼──────┐ │
│                    ┌──────────┐               │ CONTENEDORES│ │
│                    │DASHBOARD │◀──── datos ───│ 3-5 tipos   │ │
│                    │ feedback │               └─────────────┘ │
│                    │ visual   │                               │
│                    └──────────┘                               │
└─────────────────────────────────────────────────────────────┘
```

## Clases de residuos MVP

| # | Tipo | Ejemplo |
|---|------|---------|
| 1 | PET / Plastico | Botellas de agua |
| 2 | Aluminio / Metal | Latas de refresco |
| 3 | Papel / Carton | Hojas, cajas |
| 4 | Organico | Cascaras, restos |
| 5 | No reciclable | Envolturas, unicel |

## Pipeline del Software Lead

```
Camara → [Captura frame] → [Preprocesamiento] → [Modelo IA] → [Clasificacion]
                                                        │
                                                        ├──▶ [Señal GPIO → Servo]
                                                        └──▶ [Datos → Dashboard]
```
