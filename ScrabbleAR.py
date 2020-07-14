#!/usr/bin/env python3

"""
ScrabbleAR.py: Trabajo integrador de la materia Seminario de Lenguajes Opción Python
"""

__author__ = "Juan Sebastián Peña, Hernan Nahuel Ramos, y Felipe Verdugo"
__credits__ = ["Juan Sebastián Peña", "Hernan Nahuel Ramos", "Felipe Verdugo"]
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Juan Sebastián Peña, Hernan Nahuel Ramos, y Felipe Verdugo"
__email__ = "juanpea.98@gmail.com, herni.ramoss@gmail.com, felipeverdugo016@gmail.com"
__status__ = "Produccion"

import os
import json
from random import shuffle, choice
from time import time as now

import PySimpleGUI as sg
# from pattern.es import verbs, spelling, lexicon

PATH_TABLERO = 'img/tablero'
PATH_FICHAS = 'img/fichas'

sg.LOOK_AND_FEEL_TABLE['Fachero'] = {'BACKGROUND': '#191970', # midnight blue
                                    'TEXT': '#D9B382', # BEIGE
                                    'INPUT': '#D9B382',
                                    'TEXT_INPUT': '#191970',
                                    'SCROLL': '#c7e78b',
                                    # 'BUTTON': ('black', '#D9B382'),
                                    'BUTTON': ('black', '#d1d6d7'),
                                    'PROGRESS': ('#01826B', '#D0D0D0'),
                                    'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                }

sg.theme('Fachero') # tiene que ser cambiado

# casilleros del tablero en dificultad facil

CASILLEROS_LETRA_X2_FACIL = ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14))
CASILLEROS_LETRA_RESTA1_FACIL = ((2, 2), (2, 12), (12, 2), (12, 12))
CASILLEROS_LETRA_RESTA2_FACIL = ((4, 4), (4, 10), (10, 4), (10, 10))
CASILLEROS_LETRA_X3_FACIL = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13))
CASILLEROS_PALABRA_X2_FACIL = ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))
CASILLEROS_PALABRA_X3_FACIL = ((1, 1), (1, 13), (3, 3), (3, 11), (5, 5), (5, 9), (9, 5), (9, 9), (11, 3), (11, 11), (13, 1), (13, 13))

# casilleros del tablero en dificultad medio

CASILLEROS_LETRA_X2_MEDIO = ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14))
CASILLEROS_LETRA_RESTA1_MEDIO = ((2, 2), (2, 12), (12, 2), (12, 12))
CASILLEROS_LETRA_RESTA2_MEDIO = ((4, 4), (4, 10), (1, 7), (7, 1), (7, 13), (10, 4), (10, 10), (13, 7))
CASILLEROS_LETRA_RESTA3_MEDIO = ((5, 7), (7, 5), (7, 9), (9, 7))
CASILLEROS_LETRA_X3_MEDIO = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13))
CASILLEROS_PALABRA_X2_MEDIO = ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))
CASILLEROS_PALABRA_X3_MEDIO = ((1, 1), (1, 13), (3, 3), (3, 11), (5, 5), (5, 9), (9, 5), (9, 9), (11, 3), (11, 11), (13, 1), (13, 13))

# casilleros del tablero en dificultad dificil

CASILLEROS_LETRA_X2_DIFICIL = ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14))
CASILLEROS_LETRA_RESTA2_DIFICIL = ((2, 2), (2, 12), (4, 4), (4, 10), (1, 7), (7, 1), (7, 13), (10, 4), (10, 10), (12, 2), (12, 12), (13, 7))
CASILLEROS_LETRA_RESTA3_DIFICIL = ((1, 1), (1, 13), (5, 5), (5, 7), (5, 9), (7, 5), (7, 9), (9, 5), (9, 7), (9, 9), (13, 1), (13, 13))
CASILLEROS_LETRA_X3_DIFICIL = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13))
CASILLEROS_PALABRA_X2_DIFICIL = ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))
CASILLEROS_PALABRA_X3_DIFICIL = ((3, 3), (3, 11), (11, 3), (11, 11))

letras = {"a": os.path.join(PATH_FICHAS, "A.png"),
        "b": os.path.join(PATH_FICHAS, "B.png"),
        "c": os.path.join(PATH_FICHAS, "C.png"),
        "d": os.path.join(PATH_FICHAS, "D.png"),
        "e": os.path.join(PATH_FICHAS, "E.png"),
        "f": os.path.join(PATH_FICHAS, "F.png"),
        "g": os.path.join(PATH_FICHAS, "G.png"),
        "h": os.path.join(PATH_FICHAS, "H.png"),
        "i": os.path.join(PATH_FICHAS, "I.png"),
        "j": os.path.join(PATH_FICHAS, "J.png"),
        "k": os.path.join(PATH_FICHAS, "K.png"),
        "l": os.path.join(PATH_FICHAS, "L.png"),
        "m": os.path.join(PATH_FICHAS, "M.png"),
        "n": os.path.join(PATH_FICHAS, "N.png"),
        "o": os.path.join(PATH_FICHAS, "O.png"),
        "p": os.path.join(PATH_FICHAS, "P.png"),
        "q": os.path.join(PATH_FICHAS, "Q.png"),
        "r": os.path.join(PATH_FICHAS, "R.png"),
        "s": os.path.join(PATH_FICHAS, "S.png"),
        "t": os.path.join(PATH_FICHAS, "T.png"),
        "u": os.path.join(PATH_FICHAS, "U.png"),
        "v": os.path.join(PATH_FICHAS, "V.png"),
        "w": os.path.join(PATH_FICHAS, "W.png"),
        "x": os.path.join(PATH_FICHAS, "X.png"),
        "y": os.path.join(PATH_FICHAS, "Y.png"),
        "z": os.path.join(PATH_FICHAS, "Z.png"),
        "?": os.path.join(PATH_FICHAS, "question_mark.png")}

casillas = {"palabra_x2": os.path.join(PATH_TABLERO, 'beta_verde2.png'), # cambiar, no precisamente son esas
        "palabra_x3": os.path.join(PATH_TABLERO, "amarelo.png"),
        "letra_x2": os.path.join(PATH_TABLERO, 'beta_marron.png'),
        "letra_x3": os.path.join(PATH_TABLERO, "beta_azul2.png"),
        "descuento_x1": os.path.join(PATH_TABLERO, "resta1.png"),
        "descuento_x2": os.path.join(PATH_TABLERO, "resta2.png"),
        "descuento_x3": os.path.join(PATH_TABLERO, "resta3.png"),
        "neutro": os.path.join(PATH_TABLERO, "fondo3.png")}


def dibujar_casilla(x, y, dif):
    """
    Funcion que se encarga de devolver de que casillero
    se pinta cada casilla del tablero
    """
    if dif == "Facil":
        if (x, y) in CASILLEROS_LETRA_X2_FACIL:
            return casillas["letra_x2"]
        elif (x, y) in CASILLEROS_LETRA_RESTA1_FACIL:
            return casillas["descuento_x1"]
        elif (x, y) in CASILLEROS_LETRA_RESTA2_FACIL:
            return casillas["descuento_x2"]
        elif (x, y) in CASILLEROS_LETRA_X3_FACIL:
            return casillas["letra_x3"]
        elif (x, y) in CASILLEROS_PALABRA_X2_FACIL:
            return casillas["palabra_x2"]
        elif (x, y) in CASILLEROS_PALABRA_X3_FACIL:
            return casillas["palabra_x3"]
        else:
            return casillas["neutro"]

    elif dif == "Medio":
        if (x, y) in CASILLEROS_LETRA_X2_MEDIO:
            return casillas["letra_x2"]
        elif (x, y) in CASILLEROS_LETRA_RESTA1_MEDIO:
            return casillas["descuento_x1"]
        elif (x, y) in CASILLEROS_LETRA_RESTA2_MEDIO:
            return casillas["descuento_x2"]
        elif (x, y) in CASILLEROS_LETRA_RESTA3_MEDIO:
            return casillas["descuento_x3"]
        elif (x, y) in CASILLEROS_LETRA_X3_MEDIO:
            return casillas["letra_x3"]
        elif (x, y) in CASILLEROS_PALABRA_X2_MEDIO:
            return casillas["palabra_x2"]
        elif (x, y) in CASILLEROS_PALABRA_X3_MEDIO:
            return casillas["palabra_x3"]
        else:
            return casillas["neutro"]

    elif dif == "Dificil":
        if (x, y) in CASILLEROS_LETRA_X2_DIFICIL:
            return casillas["letra_x2"]
        elif (x, y) in CASILLEROS_LETRA_RESTA2_DIFICIL:
            return casillas["descuento_x2"]
        elif (x, y) in CASILLEROS_LETRA_RESTA3_DIFICIL:
            return casillas["descuento_x3"]
        elif (x, y) in CASILLEROS_LETRA_X3_DIFICIL:
            return casillas["letra_x3"]
        elif (x, y) in CASILLEROS_PALABRA_X2_DIFICIL:
            return casillas["palabra_x2"]
        elif (x, y) in CASILLEROS_PALABRA_X3_DIFICIL:
            return casillas["palabra_x3"]
        else:
            return casillas["neutro"]


def generar_bolsa():

    """
    Funcion encargada de generar la bolsa de 98 fichas.
    """
    string = ""
    try:
        with open("config.cfg") as config:
            datos = json.load(config)

    except FileNotFoundError:
        # de paso al no existir, genero el archivo
        generar_archivo_config()

    # si existia el archivo de configuracion, iterará sobre lo que leyo, sino, sobre la configuración por defecto, me explico?
    for key, value in datos.items() if "datos" in locals() else config_por_defecto().items():
        string = string + key*value["cantidad"]
    lista = list(string)
    shuffle(lista)
    return lista


def sacar_letra(bolsa):
    """
    Funcion encargada de "sacar" una letra
    random de la bolsa.
    """
    letra = choice(bolsa)
    bolsa.remove(letra)
    return letra


def config_por_defecto():
    return {"a": {"puntaje": 1, "cantidad": 11},
            "b": {"puntaje": 3, "cantidad": 3},
            "c": {"puntaje": 2, "cantidad": 4},
            "d": {"puntaje": 2, "cantidad": 4},
            "e": {"puntaje": 1, "cantidad": 11},
            "f": {"puntaje": 4, "cantidad": 2},
            "g": {"puntaje": 2, "cantidad": 2},
            "h": {"puntaje": 4, "cantidad": 2},
            "i": {"puntaje": 1, "cantidad": 6},
            "j": {"puntaje": 6, "cantidad": 2},
            "k": {"puntaje": 8, "cantidad": 1},
            "l": {"puntaje": 1, "cantidad": 4},
            "m": {"puntaje": 3, "cantidad": 3},
            "n": {"puntaje": 1, "cantidad": 5},
            "o": {"puntaje": 1, "cantidad": 8},
            "p": {"puntaje": 3, "cantidad": 2},
            "q": {"puntaje": 8, "cantidad": 1},
            "r": {"puntaje": 1, "cantidad": 4},
            "s": {"puntaje": 1, "cantidad": 7},
            "t": {"puntaje": 1, "cantidad": 4},
            "u": {"puntaje": 1, "cantidad": 6},
            "v": {"puntaje": 4, "cantidad": 2},
            "w": {"puntaje": 8, "cantidad": 1},
            "x": {"puntaje": 8, "cantidad": 1},
            "y": {"puntaje": 4, "cantidad": 1},
            "z": {"puntaje": 10, "cantidad": 1}}

def generar_archivo_config():
    with open("config.cfg", "w") as config:
        json.dump(config_por_defecto(), config, indent=4)

def puntajes_por_defecto():
    puntajes = {"a": 1, "b": 3, "c": 2, "d": 2, "e": 1,
                "f": 4, "g": 2, "h": 4, "i": 1, "j": 6, 
                "k": 8, "l": 1, "m": 3, "n": 1, "o": 1,
                "p": 3, "q": 8, "r": 1, "s": 1, "t": 1,
                "u": 1, "v": 4, "w": 8, "x": 8, "y": 4, "z": 10}
    return puntajes

def cargar_puntajes_letra():
    try:
        with open("config.cfg") as config:
            datos = json.load(config)
            puntajes = {}
            for x, y in datos.items():
                puntajes[x] = y["puntaje"]

            return puntajes
    except FileNotFoundError:
        sg.Popup("El archivo de configuración no ha sido encontrado!", title="Error Critico")


def dar_fichas_maquina(bolsa):

    """
    Funcion encargada de otorgar las 7 fichas random
    utilizando la funcion sacar_letra.
    """
    return [sacar_letra(bolsa) for x in range(7)]


def cambiar_fichas_maquina(bolsa, fm, cambios):
    """
    Funcion encargada de cambiar las fichas de la maquina
    """
    bolsa.extend(fm)
    shuffle(bolsa)
    fm = dar_fichas_maquina(bolsa)
    return fm, cambios+1


def generar_tablero(dificultad):
    """
    Funcion encargada de generar los 3 tableros con una dimesion de 15x15
    utilizando la funcion casillero_segun_color
    """
    tablero = []
    for i in range(15):
        tablero.append([])
        for j in range(15):
            tablero[i].append(sg.Button(image_filename=dibujar_casilla(i, j, dificultad), image_size=(32, 32), key=(i, j), pad=(0, 0)))
    return tablero



def generar_ventana_de_juego(tj, dif):

    """
    Funcion encargada de iniciar el juego,utilizando los procesos
    declarados anteriormente.Tambien se encarga de generar el cronometro.
    """
    # cambio de fichas
    cambios_jugador = 0
    _cambios_maquina = 0 # todavia no se usa
    # la idea es que en algun momento de la logica del cpu se use asi:
    # fichas_maquina, cambios_maquina = cambiar_fichas_maquina(bolsa, fichas_maquina, cambios_maquina)

    cambiando_fichas = False

    # bolsa de fichas
    bolsa = generar_bolsa()

    estado_fichas = {}

    for i in range(0, 7):
        estado_fichas["ficha_jugador_{}".format(i)] = {"letra": sacar_letra(bolsa), "cambiando": False}

    # cronometro related
    fin = now() + (tj * 60)

    # fichas de la maquina:
    _fichas_maquina = dar_fichas_maquina(bolsa)

    # columnas:

    # fichas computadora:
    col_arriba = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18)), sg.Text(" "*10)]]
    for i in range(7):
        col_arriba[0].append(sg.Button(image_filename=letras["?"], border_width=0, pad=((9, 0), (10, 0)), button_color=('black', '#191970')))

    # tablero de juego:
    col_tablero = generar_tablero(dif)

    # letras del jugador:
    fichas_seleccionadas = []
    col_jugador = [[sg.Text(" "*45), sg.Text("Letras seleccionadas: ", key="letras_selecc", size=(180, None))]]

    letras_jugador = [sg.Text(" "*45)]
    for i in range(0, 7):
        letras_jugador.append(sg.Button(image_filename=letras[estado_fichas["ficha_jugador_{}".format(i)]["letra"]], button_color=('black', '#191970'), border_width=0, key="ficha_jugador_{}".format(i)))

    col_jugador.append(letras_jugador)

    # panel izquierdo:
    headings_tabla = ("Jugador", "Puntaje")
    col_izquierda = [[sg.Text("Puntajes: ")],
                    [sg.Table([], headings_tabla, select_mode="browse", col_widths=(10, 10), num_rows=10, auto_size_columns=False, key="tabla_puntos")],
                    [sg.Text("Fichas restantes: {}".format(len(bolsa)), key="bolsa_fichas")],
                    [sg.Text("Tiempo restante: ?", key="cronometro")],
                    [sg.Text("\n\n\n\n\n\n\n\n\n\n", pad=(None, 7))],
                    [sg.Button("Cambiar Fichas", button_color=('black', '#D9B382'), key="cambiar_fichas")],
                    [sg.Button("TERMINAR", button_color=('black', '#D9B382')), sg.Button("POSPONER", button_color=('black', '#D9B382'))]]

    # panel derecho: (referencias)

    col_derecha = [[sg.Text("Referencias:")],
                [sg.Button(image_filename=casillas["palabra_x2"]), sg.Text("Duplica valor de la palabra")],
                [sg.Button(image_filename=casillas["palabra_x3"]), sg.Text("Triplica valor de la palabra")],
                [sg.Button(image_filename=casillas["letra_x2"]), sg.Text("Duplica letra")],
                [sg.Button(image_filename=casillas["letra_x3"]), sg.Text("Triplica letra")],
                [sg.Button(image_filename=casillas["descuento_x1"]), sg.Text("Resta 1 punto")],
                [sg.Button(image_filename=casillas["descuento_x2"]), sg.Text("Resta 2 puntos")],
                [sg.Button(image_filename=casillas["descuento_x3"]), sg.Text("Resta 3 puntos")]]

    layout = [[sg.Column(col_arriba)],
            [sg.Column(col_izquierda), sg.Column(col_tablero, element_justification="right"), sg.Column(col_derecha)],
            [sg.Column(col_jugador)]]

    window = sg.Window("ScrabbleAR", layout, size=(1000, 700), location=(300, 0), resizable=True).Finalize()
    # window.Maximize()

    while True:

        # el "_" detras de una variable significa que no se usa, es para que no salte warning
        # cuando la usemos, le sacamos el "_"
        event, _values = window.Read(timeout=10)

        if event is None:
            break

        if event == "TERMINAR": # cuando finaliza :   En ese momento se muestran las fichas que posee cada jugador y se recalcula el puntaje restando al mismo el valor de dichas fichas
            exit = sg.PopupOKCancel("¿Esta seguro que desea salir?", title="!")
            if(exit == "OK"):
                break
        
        if event == "POSPONER": # Al elegir esta opción se podrá guardar la partida para continuarla luego. En este caso, se podrá guardar la partida actual teniendo en cuenta la información del tablero y el tiempo restante. Al momento de iniciar el juego, se pedirá si se desea continuar con la partida guardada (si es que hay una) o iniciar una nueva. En cualquier caso siempre habrá una única partida guardada.
            #cargar_puntajes_letra()
            generar_archivo_config()

        if event == "cambiar_fichas": # me gustaria hacer que esto sea una funcion, asi queda mejor y mas prolijo aca
            if(cambios_jugador >= 3):
                sg.Popup("Ya no tienes cambios de fichas restantes.")
            else:
                if((cambiando_fichas) and len(fichas_seleccionadas)):
                    salida = sg.PopupOKCancel("Esta seguro que desea cambiar las fichas?", title="!!")
                    if(salida == "OK"):
                        bolsa.extend(fichas_seleccionadas)
                        shuffle(bolsa)
                        for _x in fichas_seleccionadas:
                            letra = sacar_letra(bolsa)
                            for i in range(7):
                                if(estado_fichas["ficha_jugador_{}".format(i)]["cambiando"]):
                                    estado_fichas["ficha_jugador_{}".format(i)]["cambiando"] = False
                                    estado_fichas["ficha_jugador_{}".format(i)]["letra"] = letra
                                    window["ficha_jugador_{}".format(i)].Update(image_filename=letras[letra])
                                    break
                        cambios_jugador += 1
                    else:
                        for i in range(7):
                            estado_fichas["ficha_jugador_{}".format(i)]["cambiando"] = False
                    fichas_seleccionadas = []
                    window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(fichas_seleccionadas).upper()))
                cambiando_fichas = not cambiando_fichas

            # cambio de color del boton para indicar que el jugador esta realizando un cambio de fichas
            if(cambiando_fichas):
                window["cambiar_fichas"].Update(button_color=('white', '#008000'))
            else:
                window["cambiar_fichas"].Update(button_color=('black', '#D9B382'))

        if event in estado_fichas.keys():
            if(cambiando_fichas):
                if(not estado_fichas[event]["cambiando"]):
                    fichas_seleccionadas.append(estado_fichas[event]["letra"])
                else:
                    fichas_seleccionadas.remove(estado_fichas[event]["letra"])
                window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(fichas_seleccionadas).upper()))
                estado_fichas[event]["cambiando"] = not estado_fichas[event]["cambiando"]

        window["bolsa_fichas"].Update(value="Fichas restantes: {}".format(len(bolsa)))

        # cronometro

        if now() < fin:
            # para mayor legibilidad
            # llegado de hacer la funcion de posponer, habria que guardar el tiempo restante
            min_restantes = int((fin - now()) // 60)
            seg_restantes = int((fin - now()) % 60)
            window["cronometro"].Update(value="Tiempo: {:02d}:{:02d}".format(min_restantes, seg_restantes))

    window.Close()


def mostrar_top10(puntajes):
    """
    Funcion encargada de visualizar un top 10 con los puntajes obtenidos del tipo: fecha + puntaje + nivel.
    """
    ancho_columnas = (10, 10)
    headings = ("Jugador", "Nivel", "Puntaje")
    layout = [[sg.Table(puntajes, headings, select_mode="browse", col_widths=ancho_columnas, num_rows=10, auto_size_columns=False)]]
    window = sg.Window("TOP 10", layout, resizable=True, finalize=True).Finalize()
    while True:
        event, _values = window.read()
        if event is None:
            break


def mostrar_opciones(letras):
    """
    Esta funcion muestra al usuario las opciones avanzadas por defecto y permite la edicion del mismo
    """

    def get_datos_letra(letra):
        try:
            with open("config.cfg") as config:
                datos = json.load(config)
                return datos[letra]
              
        except FileNotFoundError:
            config_por_defecto()[letra]

    def interfaz():
        # Preparo la sublista
        lista = sorted(letras, reverse=False)
        lista.remove('?')
        mitad = int(len(lista)/2)
        primera = lista[:mitad]
        segunda = lista[mitad:]

        colum_arriba = [[sg.Text("       CANTIDAD  PUNTAJE     "*2)]]
        colum_izq = [[sg.Text(letra.upper()+':', key=letra, size=(2, 1)), sg.InputText(default_text=get_datos_letra(letra)["cantidad"], size=(8, 3), key=('cantidad'+letra)), sg.InputText(default_text=get_datos_letra(letra)["puntaje"], size=(8, 3), key=('puntaje'+letra))] for letra in primera]
        col_der = [[sg.Text(letra.upper()+':', key=letra, size=(2, 1)), sg.InputText(default_text=get_datos_letra(letra)["cantidad"], size=(8, 3), key=('cantidad'+letra)), sg.InputText(default_text=get_datos_letra(letra)["puntaje"], size=(8, 3), key=('puntaje'+letra))] for letra in segunda]
        col_abajo = [[sg.Button('Guardar', button_color=('black', '#D9B382')), sg.Button('Restablecer', key='reset', pad=(24, 0), button_color=('black', '#D9B382')), sg.Button('Atras', button_color=('black', '#D9B382'))]]

        layout = [[sg.Column(colum_arriba)],
                [sg.Column(colum_izq), sg.Column(col_der)],
                [sg.Column(col_abajo)]]

        return layout

    def guardar_json(datos):
        temp_dic = {}
        for key, value in datos.items():
            # si no hay nada, ingresamos la cantidad, ya que es lo primero en datos
            if(key[-1] not in temp_dic):
                temp_dic[key[-1]] = {"cantidad": int(value)}

            # una vez que ya esta creada la key digamos, solo falta ingresar el puntaje
            else:
                temp_dic[key[-1]]["puntaje"] = int(value)
        del datos

        with open("config.cfg", "w") as arc:
            json.dump(temp_dic, arc, indent=4)

    window = sg.Window('Opciones avanzadas', interfaz())

    while True:
        event, values = window.read()

        if event == 'Guardar':
            guardar_json(values)
            window.Close()

        if event == 'reset':
        """
        Se resetea por defecto los valores del tablero y el json
        """
            if sg.PopupOKCancel('Seguro que quieres restablecer los  valores de fabrica?',
                                title='Aviso', button_color=('black', '#D9B382')) == 'OK':
                for key, _valor in values.items():
                    valor_nuevo = config_por_defecto()[key[-1]][key[:-1]]
                    window[key].update(valor_nuevo)
                    values[key] = valor_nuevo
                # guardar_json(values) # no deberia guardar a no ser que apretemos "guardar" justamente pero si quieren lo dejamos
                # estaria mal pero no tan mal?

        if event in (sg.WIN_CLOSED, 'Atras'):
            break

    window.close()


def popup_top10_vacio():
    """
    Funcion encargada de mostrar una imagen
    en caso de que el top 10 este vacio
    """
    sg.popup_animated(image_source="img/vacioves.png", message="Esta vacio, ves? No hay puntajes aqui.", no_titlebar=False, title=":(")

# comienzo de "main"

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
        [sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), default_value="Facil", key="nivel")],
        [sg.Text("Tiempo de juego:"), sg.Combo(values=(20, 40, 60), default_value=20, key="tiempo")],
        [sg.Button("TOP 10", button_color=('black', '#D9B382')), sg.Button("OPCIONES AVANZADAS", button_color=('black', '#D9B382'))],
        [sg.Button('CONTINUAR PARTIDA', button_color=('black', '#D9B382'), pad=((45, 0), (30, 0)))],
        [sg.Button('INICIAR', button_color=('black', '#D9B382'), pad=((80, 0), (30, 0)))]]


window = sg.Window("ScrabbleAR", layout, size=(250, 250)).Finalize()
while True:
    event, values = window.Read()

    if event is None:
        break

    if event == "INICIAR":
        window.Close()
        generar_ventana_de_juego(values["tiempo"], values["nivel"])

    if event == "CONTINUAR PARTIDA": # Se debe poder seguir la partida que fue pospuesta anteriormente.
        print("aaaaaaaaa")

    if event == "TOP 10":
        try:
            with open("puntajes.json") as arc:
                datos = json.load(arc)
                if not datos:
                    popup_top10_vacio()
                else:
                    puntajes = sorted(datos, reverse=True, key=lambda x: x[2])
                    mostrar_top10(puntajes)

        except FileNotFoundError:
            popup_top10_vacio()

    if event == "OPCIONES AVANZADAS":
        mostrar_opciones(letras.keys())
window.Close()
