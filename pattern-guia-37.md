# Pattern y Python 3.7+
 
## Índice:
 
1. ¿Qué es Pattern?
2. ¿Por qué no funciona con versiones de Python posteriores a 3.6?
3. ¿Qué significa PEP?
4. ¿Qué propone PEP 479?
5. ¿Cómo se soluciona?
6. Pasos adicionales para Python 3.9

### 1. ¿Qué es Pattern?
 
Pattern es un módulo de minería web para Python. Cuenta con herramientas para:
 
* Minería de datos: servicios web (Google, Twitter, Wikipedia), rastreador web, analizador de HTML DOM.
* Procesamiento de lenguaje natural: etiquetadores para tipos de palabras, búsqueda de n-gramas, análisis de sentimientos, WordNet.
* Aprendizaje automático: modelo de espacio vectorial, agrupamiento, clasificación (KNN, SVM, Perceptron).
* Análisis de red: centralidad gráfica y visualización.
 
### 2. ¿Por qué no funciona con versiones de Python posteriores a 3.6?
 
La simple respuesta a esto es que al salir a la luz la versión 3.7 de Python, la PEP 479 fue implementada.
 
Pero...
 
### 3. ¿Qué significa PEP?
 
PEP (Python Enhancement Proposal) significa propuesta de mejora de Python. Un PEP es un documento de diseño que proporciona información a la comunidad de Python o describe una nueva característica para Python o sus procesos o entorno. El PEP debe proporcionar una especificación técnica concisa de la característica y una justificación de la característica.
 
### 4. ¿Qué propone PEP 479?

Este PEP propone un cambio a los generadores: cuando StopIteration se genera dentro de un generador, se reemplaza con RuntimeError. (Más precisamente, esto sucede cuando la excepción está a punto de salir del marco de la pila del generador). Debido a que el cambio es incompatible con versiones anteriores, la característica se introduce inicialmente utilizando una declaración en __future__ (desde Python 3.5). Finalmente, esto fue implementado a partir de Python 3.7.
 
### 5. ¿Cómo se soluciona?

![Problema](https://i.imgur.com/HKXCqvi.png)

Para solucionar este problema, habría que implementar los cambios que propone PEP 479 en ciertos archivos. Esto se puede hacer manualmente (abajo se indicará como), o se puede descargar Pattern con ciertos arreglos (incluidos este y más) que fueron proporcionados por parte de la comunidad de Pattern.
 
#### De forma manual: (al haber instalado Pattern mediante "pip3 install pattern")
 
Debemos cambiar las sentencias "raise StopIteration" dentro de generadores simplemente por "return". Por ejemplo:

**Antes:**

```Python
def _read(path, encoding="utf-8", comment=";;;"):
    """ Returns an iterator over the lines in the file at the given path,
        strippping comments and decoding each line to Unicode.
    """
    if path:
        if isinstance(path, str) and os.path.exists(path):
            # From file path.
            f = open(path, "r", encoding="utf-8")
        elif isinstance(path, str):
            # From string.
            f = path.splitlines()
        else:
            # From file or buffer.
            f = path
        for i, line in enumerate(f):
            line = line.strip(BOM_UTF8) if i == 0 and isinstance(line, str) else line
            line = line.strip()
            line = decode_utf8(line, encoding)
            if not line or (comment and line.startswith(comment)):
                continue
            yield line
    raise StopIteration
```

**Después:**

```Python
def _read(path, encoding="utf-8", comment=";;;"):
    """ Returns an iterator over the lines in the file at the given path,
        strippping comments and decoding each line to Unicode.
    """
    if path:
        if isinstance(path, str) and os.path.exists(path):
            # From file path.
            f = open(path, "r", encoding="utf-8")
        elif isinstance(path, str):
            # From string.
            f = path.splitlines()
        else:
            # From file or buffer.
            f = path
        for i, line in enumerate(f):
            line = line.strip(BOM_UTF8) if i == 0 and isinstance(line, str) else line
            line = line.strip()
            line = decode_utf8(line, encoding)
            if not line or (comment and line.startswith(comment)):
                continue
            yield line
    return
```
Los archivos de pattern se pueden encontrar en:

**Windows**: `C:\Users\{usuario}\AppData\Local\Programs\Python\Python3x\Lib\site-packages` o tambien `C:\Python3x\Lib\site-packages`

**Linux**: `~/.local/lib/python3.x/site-packages`

**Nota**: x vendria a ser la versión que ustedes tengan instalada de Python.

Y las sentencias se encuentran en:

`pattern/text/__init__.py` (linea 609)

`pattern/web/__init__.py` (lineas 2387, 2912)

`pattern/metrics.py` (lineas 669, 1080, 1102)

**De forma "automática":**

Se debe descargar este fichero zip (https://github.com/clips/pattern/archive/dev_fixing_issues.zip) (es el source code de la rama "dev_fixing_issues" del repositorio de Pattern)

A continuación, se debe ir a nuestra consola/terminal y ejecutar:

```
cd pattern-dev_fixing_issues
py (o python3) setup.py install
```

Una vez hecho esto, Pattern debería estar instalado y corriendo normalmente.

### 6. Pasos adicionales para Python 3.9

**Nota**: Estos son los pasos para instalar pattern usando Python 3.9 en Windows. Todavia no fue probado en Linux. Tambien, se espera que con el paso del tiempo, esto no sea necesario y se pueda instalar normalmente.

Para instalar en esta versión de Python, se debe instalar de antemano Microsoft Build Tools 2015.

Se debe descargar desde este link (http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe) e instalar con la opción "Windows 8.1 SDK" marcada.

Además, las siguientes librerías deben ser descargadas desde esta página (https://www.lfd.uci.edu/~gohlke/pythonlibs/) (ya que no pueden ser instaladas con las versiones provenientes de PyPI):

* numpy+mkl
* scipy
* mysqlclient
* lxml
* pygame

Al descargar las versiones correspondientes de cada una (las que incluyen "cp39"), se instalan de la siguiente forma:

```
pip3 install nombre_de_la_lib.whl
```

Tras finalizar, se debería poder proceder a instalar pattern con cualquiera de los procesos antes mencionados.

## Fuentes:

~~Yo (creeme)~~

https://github.com/clips/pattern

https://www.python.org/dev/peps/pep-0001/

https://www.python.org/dev/peps/pep-0479/

https://github.com/clips/pattern/commit/50a36dbb5287d2b1a44325bf05a5196523d53def
