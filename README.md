# ScrabbleAR
Trabajo integrador de la materia Seminario de Lenguajes Opción Python

Juego basado en el Scrabble original, con ciertos cambios en su reglamento.

### Requerimientos:

* Python 3.6 (es necesaria esta versión ya que pattern tiene problemas con versiones posteriores)
* PySimpleGUI 4.19.0+
* Pattern 3.6


### Como ejecutar:

Primero debemos descargar las dependencias necesarias para correr el proyecto y el codigo fuente del mismo.

Esto lo hacemos de las siguientes maneras dependiendo del sistema operativo.

### Windows:

* Descargar instalador de Python (https://www.python.org/downloads/release/python-368/)
* En cmd o powershell ejecutar: `pip3 install PySimpleGUI pattern`

### Linux:

Aquí no es necesario instalar python3 ya que viene por defecto con Linux, pero si son necesarias otras dependencias.

* Desde la terminal ejecutaremos lo siguiente: `sudo apt install python3-pip python3-tk`
* Luego instalaremos PySimpleGUI `pip3 install PySimpleGUI pattern`

Una vez descargado el codigo fuente, se debera ejecutar invocando al interprete con el nombre del archivo.

En Windows se puede ejecutar haciendo doble click en el mismo (en caso de tener instalado pylauncher), o llamandolo desde cmd o powershell, tipicamente como `py ScrabbleAR.py`

En linux, para ejecutar con doble click se le debe dar permiso de ejecucion con el comando `chmod +x ./ScrabbleAR.py`, o invocandolo desde la terminal como `python3 ScrabbleAR.py`