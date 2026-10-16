# Guía de Ejecución - DistriGest

Instrucciones rápidas para configurar y ejecutar el proyecto.

---

## 1. ¿Por qué ocurrió el error de `pip`?
El error:
```
pip : El término 'pip' no se reconoce...
```
Ocurre porque **el entorno virtual (`.venv`) no está activado** en la terminal de PowerShell o Python no está en el `PATH` del sistema.

---

## 2. Pasos para ejecutar el proyecto

### Paso 1: Activar el entorno virtual
En la terminal de PowerShell dentro de la carpeta del proyecto, ejecuta:
```powershell
.\.venv\Scripts\Activate.ps1
```
> **Nota:** Si PowerShell bloquea los scripts por directivas de seguridad, ejecuta primero:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> .\.venv\Scripts\Activate.ps1
> ```

### Paso 2: Instalar dependencias
Con el entorno activado `(.venv)`, instala las librerías necesarias:
```powershell
pip install -r requirements.txt
```

### Paso 3: Iniciar la aplicación
```powershell
python main.py
```

---

## ⚡ Método Rápido (Sin activar el entorno)
Puedes ejecutar la aplicación directamente con el Python del entorno virtual:
```powershell
.\.venv\Scripts\python.exe main.py
```
