# Manual — Subir EcoSort IA a GitHub

**Objetivo:** Crear un repositorio en GitHub (con otra cuenta) y hacer push desde tu proyecto local.

---

## Paso 1 — Crear el repositorio en GitHub

1. **Inicia sesión** en [github.com](https://github.com) con la cuenta donde quieres el repo.

2. **Crear nuevo repositorio:**
   - Clic en el **+** (arriba derecha) → **New repository**
   - O ve a [github.com/new](https://github.com/new)

3. **Configuración del repo:**
   | Campo | Valor sugerido |
   |-------|----------------|
   | Repository name | `trash-bot` o `ecosort-ia` |
   | Description | `Clasificador de residuos reciclables con IA — EcoSort IA` |
   | Visibility | **Private** o **Public** |
   | **NO** marcar | "Add a README file" |
   | **NO** marcar | "Add .gitignore" |
   | **NO** marcar | "Choose a license" |

   > Importante: deja el repo vacío. No agregues README ni .gitignore desde GitHub, porque ya tienes archivos locales.

4. **Crear** el repositorio. Verás una página con instrucciones; **no las ejecutes aún**.

5. **Copia la URL del repo.** Será algo como:
   ```
   https://github.com/TU_USUARIO/trash-bot.git
   ```
   o con SSH:
   ```
   git@github.com:TU_USUARIO/trash-bot.git
   ```

---

## Paso 2 — Preparar el proyecto local

### 2.1 Crear `.gitignore` (si no existe)

En la raíz del proyecto (`trash-bot/`), crea o verifica que exista `.gitignore` con algo como:

```
# Python
venv/
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
dist/
build/

# Modelos (grandes — subir solo si quieres)
# models/*.keras
# models/*.tflite

# Dataset (muy grande — no subir)
dataset/

# IDE
.idea/
.vscode/
*.swp

# Logs
logs/
*.log

# OS
.DS_Store
Thumbs.db
```

### 2.2 Inicializar Git (si el proyecto no es repo aún)

Abre terminal en la carpeta del proyecto:

```bash
cd "/Users/salaniz/practice folder/trash-bot"

# Inicializar Git
git init

# Ver estado
git status
```

### 2.3 Agregar archivos y primer commit

```bash
# Agregar todo (respetando .gitignore)
git add .

# Ver qué se va a subir
git status

# Primer commit
git commit -m "Initial commit: EcoSort IA — clasificador de residuos con MobileNetV2"
```

---

## Paso 3 — Conectar con GitHub y hacer push

### Opción A — HTTPS (más simple)

```bash
# Agregar el remoto (reemplaza TU_USUARIO y NOMBRE_REPO con los tuyos)
git remote add origin https://github.com/TU_USUARIO/NOMBRE_REPO.git

# Verificar
git remote -v

# Subir (rama main)
git branch -M main
git push -u origin main
```

Te pedirá usuario y contraseña. En GitHub ya no se usan contraseñas normales; debes usar un **Personal Access Token (PAT)**:

1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Marca `repo`
4. Copia el token y úsalo como contraseña cuando `git push` lo pida.

### Opción B — SSH (recomendado si ya tienes clave)

```bash
git remote add origin git@github.com:TU_USUARIO/NOMBRE_REPO.git
git branch -M main
git push -u origin main
```

Si no tienes clave SSH configurada: [GitHub: Connecting with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).

---

## Paso 4 — Verificar

1. Refresca la página del repo en GitHub.
2. Deberías ver los archivos del proyecto.
3. Para futuros cambios:

```bash
git add .
git commit -m "Descripción del cambio"
git push
```

---

## Resumen rápido

| Paso | Comando / Acción |
|------|------------------|
| 1 | Crear repo vacío en GitHub |
| 2 | `git init` (si aplica) |
| 3 | Crear `.gitignore` |
| 4 | `git add .` y `git commit -m "Initial commit"` |
| 5 | `git remote add origin https://github.com/USUARIO/REPO.git` |
| 6 | `git push -u origin main` |

---

## Notas

- **Dataset y modelos:** Por tamaño, suelen excluirse con `.gitignore`. Si quieres compartir el modelo entrenado, puedes subir solo `models/ecosort_model.tflite` (o INT8) y documentar cómo entrenar.
- **Cuenta distinta:** Si usas otra cuenta, asegúrate de que esa sesión esté activa en el navegador al crear el repo, y que el token/SSH corresponda a esa cuenta.

---

**Siguiente paso:** llevar el proyecto a la Raspberry Pi → [`RASPBERRY_PI_PRIMERA_VEZ.md`](RASPBERRY_PI_PRIMERA_VEZ.md)
