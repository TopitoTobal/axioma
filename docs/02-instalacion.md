# Instalacion

Axioma se distribuye como un ejecutable standalone para Windows. No requiere instalar Python ni ninguna dependencia.

## Requisitos

- Sistema operativo: Windows 10 o superior
- Arquitectura: 64 bits

## Opcion 1: Ejecutable Standalone (Recomendado)

Descarga `axioma.exe` desde la seccion de releases del repositorio:

```bash
# O clona el repositorio
git clone https://github.com/TopitoTobal/axioma.git

# El ejecutable se encuentra en la carpeta dist/
cd axioma
.\dist\axioma.exe ejemplos/hola_mundo.ax
```

Para usarlo desde cualquier lugar del sistema, agrega la carpeta `dist/` a tu PATH:

```bash
# Desde PowerShell como administrador
$distPath = "C:\ruta\a\axioma\dist"
[Environment]::SetEnvironmentVariable("Path", "$distPath;$env:Path", "User")
```

O ejecuta el script `instalar.bat` incluido en el proyecto.

## Opcion 2: Desde Python

Si tienes Python 3.8+ instalado:

```bash
# Clonar el repositorio
git clone https://github.com/TopitoTobal/axioma.git
cd axioma

# Instalar como paquete
pip install -e .

# Ejecutar
axioma archivo.ax
```

## Opcion 3: Compilar tu propio .exe

```bash
pip install pyinstaller
pyinstaller --onefile --name=axioma --distpath=dist --clean --noconfirm --console run.py
```

## Verificar la Instalacion

```bash
axioma
```

Deberias ver el logo de Axioma y el prompt interactivo `>>>`.
