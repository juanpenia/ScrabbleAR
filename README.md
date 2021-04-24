# ScrabbleAR
Trabajo integrador de la materia Seminario de Lenguajes Opción Python

Juego basado en el Scrabble original, con ciertos cambios en su reglamento.

### Integrantes:

Juan Sebastián Peña 

Hernán Nahuel Ramos

Felipe Verdugo

### Requerimientos:

* Python 3.6+ (1)
* PySimpleGUI 4.19.0 - 4.28.0 (2)
* Pattern 3.6
* Pygame
* Playsound (3)
* Sounddevice (4)

(1) Se puede utilizar con versiones de Python posteriores a 3.6, pero se deben hacer modificaciones al modulo Pattern para que funcione correctamente. Mas información en el archivo "pattern-guia-37.md".

(2) El programa fue testeado con la version 4.19.0 en adelante. Se recomienda usar versiones menores o iguales a 4.28.0 ya que en la version 4.29.0 en adelante, cambia algo en las columnas que hace que no se vea como se espera.

(3) Solo en Windows, no funciona como esperamos en Linux.

(4) Probado solo en Linux, no sabemos si funciona en Windows.

### Como ejecutar:

Primero debemos descargar las dependencias necesarias para correr el proyecto y el codigo fuente del mismo.

Esto lo hacemos de las siguientes maneras dependiendo del sistema operativo.

### Windows:

* Descargar instalador de Python (https://www.python.org/downloads/release/python-368/)
* En cmd o powershell ejecutar: `pip3 install PySimpleGUI pattern pygame playsound`

### Linux:

Los pasos aquí varian ya que no todas las distribuciones usan el mismo gestor de paquetes, y porque algunos programas ya pueden venir instalados en ellas, como es el caso de Python 3 en Ubuntu.

Para ambas distribuciones se tienen que ejecutar los siguientes comandos desde una terminal:

Ubuntu: 

* `sudo apt install python3-pip python3-tk libmysqlclient-dev libportaudio2 libasound2-dev`

Si la version de Python es 3.6:
* `pip3 install pattern pygame sounddevice soundfile PySimpleGUI==4.28.0`

Si la version de Python es mayor o igual a 3.7:
* `pip3 install pygame sounddevice soundfile PySimpleGUI==4.28.0`
* `pip3 install pattern-dev_fixing_issues.zip`

Arch:

* `sudo pacman -S python3 python-pip python-pygame tk --needed`
* `pip3 install sounddevice soundfile PySimpleGUI==4.28.0`
* `pip3 install pattern-dev_fixing_issues.zip`


**Nota:** Probado en Arch Linux y Ubuntu 18.04 en adelante.

Una vez descargado el codigo fuente, se debera ejecutar invocando al interprete con el nombre del archivo.

En Windows se puede ejecutar haciendo doble click en el mismo (en caso de tener instalado pylauncher), o llamandolo desde cmd o powershell, tipicamente como `py ScrabbleAR.py`

En linux, para ejecutar con doble click se le debe dar permiso de ejecucion con el comando `chmod +x ./ScrabbleAR.py`, o invocandolo desde la terminal como `python3 ScrabbleAR.py`

Musica obtenida de https://freemusicarchive.org.

Efectos de sonido obtenidos de https://freesound.org.
