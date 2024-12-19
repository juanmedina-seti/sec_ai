# Instalación
## Abrir linea de comando 
Presiona `Win + R`, escribe `cmd` y presiona `Enter`.

## Descargar
Desde la línea de comando cmd
```
cd /
mkdir python_apps
cd ./python_apps

```
En el directorio donde desea instalar *c:/pyathon_apps*
```
git clone --no-checkout https://github.com/juanmedina-seti/sec_ai.git sec_ai
```
## Crear ambiente python
```
cd sec_ai
python -m venv .venv

```
en caso de no encontrar python utilice 
```
"C:\Program Files\Python312\python.exe" -m venv .venv
```
## Activar e instalar librerías requeridad
En el directorio *sec_ai*
```
venv\Scripts\activate.bat
pip install -r requirements.txt
```

# Ejecución
Ejecute el programa `run.bat`
