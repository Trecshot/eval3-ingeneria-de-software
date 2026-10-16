# DistriGest - Sistema de Gestión Comercial e Inventario

**Prototipo Modular de Interfaz (Evaluación 3 - Ingeniería de Software)**  
*Firma Desarrolladora: Bomcode | Cliente: DistriSur Araucanía SpA*

---

## 1. Requisitos Previos

* **Intérprete:** Python 3.10 o superior (64-bit).
* **Gestor de paquetes:** `pip` actualizado.
* **Sistema Operativo:** Windows 10/11, Linux o macOS.

---

## 2. Protocolo de Despliegue y Ejecución

Abrir una terminal (PowerShell o CMD) en la raíz del proyecto y ejecutar los siguientes pasos:

### Paso 1: Creación del Entorno Virtual
```powershell
python -m venv .venv
```

### Paso 2: Activación del Entorno

**En Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

> *(En caso de restricción por directivas de ejecución de scripts, habilitar temporalmente con:)*
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\.venv\Scripts\Activate.ps1
> ```

**En Windows (CMD tradicional):**
```cmd
.\.venv\Scripts\activate.bat
```

### Paso 3: Instalación de Dependencias
```powershell
pip install -r requirements.txt
```

### Paso 4: Inicialización del Sistema
```powershell
python main.py
```

---

## 3. Ejecución Rápida (Alternativa sin activación de shell)

Si el entorno `.venv` ya fue creado y sus dependencias instaladas, el sistema puede inicializarse directamente invocando el binario local:

```powershell
.\.venv\Scripts\python.exe main.py
```
