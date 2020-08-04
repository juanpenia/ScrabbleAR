#!/usr/bin/env python3

"""
ScrabbleAR.py: Trabajo integrador de la materia Seminario de Lenguajes Opción Python
"""

_author_ = "Juan Sebastián Peña, Hernan Nahuel Ramos, y Felipe Verdugo"
_credits_ = ["Juan Sebastián Peña", "Hernan Nahuel Ramos", "Felipe Verdugo"]
_license_ = "GPL"
_version_ = "3.0"
_maintainer_ = "Juan Sebastián Peña, Hernan Nahuel Ramos, y Felipe Verdugo"
_email_ = "juanpea.98@gmail.com, herni.ramoss@gmail.com, felipeverdugo016@gmail.com"
_status_ = "Produccion"

import os
import json
from random import shuffle, choice, getrandbits, randint as random
from time import time as now, sleep
from typing import Union
from sys import platform
print(platform)


import PySimpleGUI as sg
from pattern.es import verbs, spelling, lexicon, parse
import pygame
from playsound import playsound




PATH_TABLERO = 'img/tablero'
PATH_FICHAS = 'img/fichas'
PATH_MUSICA = 'audio/musica'
PATH_SFX = 'audio/sfx'

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


casilleros = {"facil": {
                "letra_x2": ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14)),
                "descuento_x1": ((2, 2), (2, 12), (12, 2), (12, 12)),
                "descuento_x2": ((4, 4), (4, 10), (10, 4), (10, 10)),
                "letra_x3": ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13)),
                "palabra_x2": ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)),
                "palabra_x3": ((1, 1), (1, 13), (3, 3), (3, 11), (5, 5), (5, 9), (9, 5), (9, 9), (11, 3), (11, 11), (13, 1), (13, 13))
            },
            "medio": {
                "letra_x2": ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14)),
                "descuento_x1": ((2, 2), (2, 12), (12, 2), (12, 12)),
                "descuento_x2": ((4, 4), (4, 10), (1, 7), (7, 1), (7, 13), (10, 4), (10, 10), (13, 7)),
                "descuento_x3": ((5, 7), (7, 5), (7, 9), (9, 7)),
                "letra_x3": ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13)),
                "palabra_x2": ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)),
                "palabra_x3": ((1, 1), (1, 13), (3, 3), (3, 11), (5, 5), (5, 9), (9, 5), (9, 9), (11, 3), (11, 11), (13, 1), (13, 13))
            },
            "dificil": {
                "letra_x2": ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14)),
                "descuento_x2": ((2, 2), (2, 12), (4, 4), (4, 10), (1, 7), (7, 1), (7, 13), (10, 4), (10, 10), (12, 2), (12, 12), (13, 7)),
                "descuento_x3": ((1, 1), (1, 13), (5, 5), (5, 7), (5, 9), (7, 5), (7, 9), (9, 5), (9, 7), (9, 9), (13, 1), (13, 13)),
                "letra_x3": ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13)),
                "palabra_x2": ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)),
                "palabra_x3": ((3, 3), (3, 11), (11, 3), (11, 11))
            }
        }


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
        "?": os.path.join(PATH_FICHAS, "question_mark.png"),
        "vacio": os.path.join(PATH_FICHAS, "vacio.png")}

casillas = {"palabra_x2": os.path.join(PATH_TABLERO, 'beta_verde2.png'), # cambiar, no precisamente son esas
        "palabra_x3": os.path.join(PATH_TABLERO, "amarelo.png"),
        "letra_x2": os.path.join(PATH_TABLERO, 'beta_marron.png'),
        "letra_x3": os.path.join(PATH_TABLERO, "beta_azul2.png"),
        "descuento_x1": os.path.join(PATH_TABLERO, "resta1.png"),
        "descuento_x2": os.path.join(PATH_TABLERO, "resta2.png"),
        "descuento_x3": os.path.join(PATH_TABLERO, "resta3.png"),
        "neutro": os.path.join(PATH_TABLERO, "fondo3.png")}

sfx = {"correcto": os.path.join(PATH_SFX, "421002__eponn__correct.wav"),
    "incorrecto": os.path.join(PATH_SFX, "243700__ertfelda__incorrect.wav")}

lista_musica = [os.path.join(PATH_MUSICA, "Sergey_Cheremisinov_-_05_-_The_Healing.mp3"), 
        os.path.join(PATH_MUSICA, "Sergey_Cheremisinov_-_04_-_Northern_Lullaby.mp3"), 
        os.path.join(PATH_MUSICA, "Sergey_Cheremisinov_-_01_-_Gray_Drops.mp3"), 
        os.path.join(PATH_MUSICA, "Pictures_of_the_Floating_World_-_Waves.mp3"), 
        os.path.join(PATH_MUSICA, "Pictures_of_the_Floating_World_-_01_-_Canada.mp3"), 
        os.path.join(PATH_MUSICA, "Kai_Engel_-_05_-_Great_Expectations.mp3"), 
        os.path.join(PATH_MUSICA, "Kai_Engel_-_07_-_Interception.mp3")]
shuffle(lista_musica)


def dibujar_casilla(x: int, y: int, dif: str) -> str:
    """
    Función que se encarga de devolver de que casillero
    se pinta cada casilla del tablero
    """

    for key, value in casilleros[dif.lower()].items(): 
        if (x, y) in value:
            return casillas[key]

    return casillas["neutro"]


def get_premio_descuento_casillero(pos, dif):
    for key, value in casilleros[dif.lower()].items(): 
        if pos in value:
            return key

    return "nada pues"


def generar_bolsa() -> list:
    """
    Función encargada de generar la bolsa de 98 fichas.
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

def sacar_letra(bolsa: list) -> str:
    """
    Función encargada de "sacar" una letra
    random de la bolsa.
    """
    letra = choice(bolsa)
    bolsa.remove(letra)
    return letra



def config_por_defecto() -> dict:
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

def puntajes_por_defecto() -> dict:
    puntajes = {"a": 1, "b": 3, "c": 2, "d": 2, "e": 1,
                "f": 4, "g": 2, "h": 4, "i": 1, "j": 6, 
                "k": 8, "l": 1, "m": 3, "n": 1, "o": 1,
                "p": 3, "q": 8, "r": 1, "s": 1, "t": 1,
                "u": 1, "v": 4, "w": 8, "x": 8, "y": 4, "z": 10}
    return puntajes

def cargar_puntajes_letras() -> dict:
    try:
        with open("config.cfg") as config:
            datos = json.load(config)
            puntajes = {}
            for x, y in datos.items():
                puntajes[x] = y["puntaje"]

            return puntajes
    except FileNotFoundError:
        sg.Popup("El archivo de configuración no ha sido enlength_palabrarado!", title="Error Critico")


def dar_fichas_maquina(bolsa: list) -> list:
    """
    Función encargada de otorgar las 7 fichas random
    utilizando la funcion sacar_letra.
    """
    return [sacar_letra(bolsa) for x in range(7)]


def cambiar_fichas_maquina(bolsa: list, fm: list, cambios: int) -> tuple:
    """
    Función encargada de cambiar las fichas de la maquina
    """
    bolsa.extend(fm)
    shuffle(bolsa)
    fm = dar_fichas_maquina(bolsa)
    return fm, cambios+1


def generar_tablero(dificultad: str) -> list:

    """
    Función encargada de generar los 3 tableros con una dimesion de 15x15
    utilizando la funcion casillero_segun_color
    """
    tablero = []
    for i in range(15):
        tablero.append([])
        for j in range(15):
            tablero[i].append(sg.Button(image_filename=dibujar_casilla(i, j, dificultad), image_size=(32, 32), key=(i, j), pad=(0, 0)))
    return tablero

def verificar_palabra(palabra: Union[list, dict]):
    p = "".join(palabra.values() if type(palabra) == dict else palabra)
    s = parse(p).split()
    for cada in s:
        for pal in cada:
            ok = pal[1] in ('VB', 'NNS', 'NN', 'JJ')
    return ok and ((p in lexicon) or (p in spelling))

def ordenar_dic(dic: dict) -> dict:
    return {key: dic[key] for key in sorted(dic)}
    
     
def turno_computadora(pj: bool, fm: list, cm: int, tablero_logico: list, window, bolsa, pp, dif, pl):
    """...
    Parametros:
    pj: primera jugada
    """
    # FALTA:
    # ajustar lo del puntaje, que actualize
    # cambiar fichas si no encuentra combo 3 veces
    # despues en verificar a lo ultimo, turnocomputadora


    # esto tiene dos etapas: encontrar combo valido y encontrar lugar
    found = False
    # encontrar palabra
    for i in range(50):
        palabra = []
        copia_bolsa = fm.copy() 
        for j in range(random(2, len(copia_bolsa))):
            letra_random = choice(copia_bolsa)
            palabra.append(letra_random)
            copia_bolsa.remove(letra_random)
        print("{}:".format(i), "".join(palabra), verificar_palabra(palabra)) # debug
        if(verificar_palabra(palabra)):
            found = True
            break
    # si not found, then if intentos fallidos > 3 o 5, cambiar fichas, no? we should
    # buscar lugar disponible con sample, chequear si desde lugar en ambos sentidos la palabra se puede colocar
    if found:
        while True:
            pos = tuple([random(0, 14) for i in range(2)])
            if(tablero_logico[pos[0]][pos[1]] == " "):
                todo_libre = True
                nose2 = random(0, 1)
                nose4 = 0 # pos actual
                if(pos[nose2] + len(palabra) > 14):
                    continue

                for nose in range(pos[nose2], pos[nose2]+len(palabra)):
                    if nose2 == 0:
                        if tablero_logico[nose][pos[1]] != " ":
                            todo_libre = False
                            break
                    else:
                        if tablero_logico[pos[0]][nose] != " ":
                            todo_libre = False
                            break

                if todo_libre:
                    for nose in range(pos[nose2], pos[nose2]+len(palabra)):
                        tupla = (nose, pos[1]) if nose2 == 0 else (pos[0], nose)
                        window[tupla].Update(image_filename=letras[palabra[nose4]])
                        tablero_logico[tupla[0]][tupla[1]] = palabra[nose4]
                        nose4+=1
                        # aca
                    p = "".join(palabra) # cambiar a palabra formada or something
                    #agregar_puntaje_tabla(pp, "CPU", p, calcular_puntaje_jugada([(x, pos[1]) for x in range(pos[0], pos[0]+len(palabra))], dif, palabra, pl))
                    #window["tabla_puntos"].Update(values=pp)
                    window["bolsa_fichas"].Update(value="Fichas restantes: {}".format(len(bolsa)))
                    try:
                        for nose5 in palabra:
                            fm[fm.index(nose5)] = sacar_letra(bolsa)
                    except IndexError:
                        sg.Popup("Termino la wea")
                        # deberia ser terminar_juego()

                    break
                else:
                    continue
            
    else:
        sg.Popup("la pc paso")

    # ahora la parte de colocar la palabra
    # for i in range(palabra):
    #     fm[fm.index(i)] = sacar_letra(bolsa)
    #     tablero_logico[key[0]][key[1]] = i # key[0] key[1] valores de donde irian que encontramos disponibles
    #     
    # if(primera_jugada):
    #     primera_jugada = False
    # p = "".join(palabra) # cambiar a palabra formada or something
    # agregar_puntaje_tabla(puntajes_partida, "CPU", p, calcular_puntaje_jugada(palabra_actual.keys(), dif, palabra, puntajes_letras))
    # window["tabla_puntos"].Update(values=puntajes_partida)
    
    if pj:
        # return el pj o hacerlo que cambie alla
        pass
    else:
        pass

def sentido_palabra_actual(pos: list, ultimo: int) -> str:
    if(len(pos) > 1):
        pos = [x for x in pos]
        if pos[ultimo-1][0] == pos[ultimo-2][0]:
            return "Horizontal"
        elif pos[ultimo-1][1] == pos[ultimo-2][1]: 
            return "Vertical"
    else:
        return "?"


def get_sentido_correcto(pos, actual, ultimo):
    if(len(pos) > 1):
        pos = [x for x in pos]
        if(sentido_palabra_actual(pos, ultimo) == "Horizontal"): 
            return True if actual[1] in (pos[0][1]-1, pos[ultimo-1][1]+1) else False
        elif(sentido_palabra_actual(pos, ultimo) == "Vertical"): 
            return True if actual[0] in (pos[0][0]-1, pos[ultimo-1][0]+1) else False
    else:
        return True

def letra_cerca(pos: Union[None, list], actual, ultimo):
    if(pos != None):
        pos = [x for x in pos]
        posibles = ((pos[0][0]-1, pos[0][1]),
        (pos[ultimo-1][0]+1, pos[ultimo-1][1]), 
        (pos[0][0], pos[0][1]-1), 
        (pos[ultimo-1][0], pos[ultimo-1][1]+1))

    return (("posibles" in locals()) and (actual in posibles)) or pos is None


def calcular_puntaje_jugada(pos: list, dif: str, td: dict, pl:dict) -> int: # cambiar td por algo mejor, td es palabra_actual de abajo
    total = 0
     
    for item in pos:
        x = get_premio_descuento_casillero(item, dif) # para mayor prolijidad
        if x == "letra_x2":
            total += pl[td[item]]*2
        elif x == "letra_x3":
            total += pl[td[item]]*3
        elif x == "descuento_x1":
            total += pl[td[item]]-1
        elif x == "descuento_x2":
            total += pl[td[item]]-2
        elif x == "descuento_x3":
            total += pl[td[item]]-3
        elif x == "palabra_x2":
            total = (total + pl[td[item]]) * 2
        elif x == "palabra_x3":
            total = (total + pl[td[item]]) * 3
        else:
            total += pl[td[item]]

    return total

def agregar_puntaje_tabla(pp, nombre, palabra, puntaje):
    pp.append([nombre, palabra, puntaje])
    #return pp

def generar_ventana_de_juego(tj: int, dif: str):

    """
    Función encargada de iniciar el juego,utilizando los procesos
    declarados anteriormente.Tambien se encarga de generar el cronometro.
    """
    # settings musica:
    musica_muteada = False
    pygame.mixer.init()
    pygame.mixer.music.load(lista_musica[0])
    for i in range(1, len(lista_musica)):
        pygame.mixer.music.queue(lista_musica[i])
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play()
    # fin musica

    puntajes_letras = cargar_puntajes_letras()
    puntajes_partida = []
    # cambio de fichas
    cambios_jugador = 0
    cambios_maquina = 0 # todavia no se usa
    # la idea es que en algun momento de la logica del cpu se use asi:
    #fichas_maquina, cambios_maquina = cambiar_fichas_maquina(bolsa, fichas_maquina, cambios_maquina)

    cambiando_fichas = False

    # turno de jugador
    turno_jugador = bool(random(0, 1))

    # bolsa de fichas
    bolsa = generar_bolsa()

    estado_fichas = {}

    for i in range(0, 7):
        estado_fichas["ficha_jugador_{}".format(i)] = {"letra": sacar_letra(bolsa), "cambiando": False, "colocando":False}
    

    # cronometro related
    fin = now() + (tj * 60)

    # fichas de la maquina:
    fichas_maquina = dar_fichas_maquina(bolsa)

    # columnas:

    # fichas computadora:
    col_arriba = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18)), sg.Text(" "*10)]]
    for i in range(7):
        col_arriba[0].append(sg.Button(image_filename=letras["?"], border_width=0, pad=((9, 0), (10, 0)), button_color=('black', '#191970')))
    col_arriba[0].extend([sg.Text(" "*93), sg.Button("MUSIC: ON", button_color=('black', '#D9B382'), key="music_toggle")])
    # tablero de juego:
    col_tablero = generar_tablero(dif)
    # crear tablero logico
    tablero_logico  = [[' ' for j in range(15)] for i in range(15)]

    tl2 = {}

    
    # letras del jugador:
    fichas_seleccionadas = []
    col_jugador = [[sg.Text(" "*45), sg.Text("Letras seleccionadas: ", key="letras_selecc", size=(180, None))]]

    letras_jugador = [sg.Text(" "*45)]
    for i in range(0, 7):
        letras_jugador.append(sg.Button(image_filename=letras[estado_fichas["ficha_jugador_{}".format(i)]["letra"]], button_color=('black', '#191970'), border_width=0, key="ficha_jugador_{}".format(i)))


    letras_jugador.append(sg.Text(" "*37))
    letras_jugador.append(sg.Button("VERIFICAR", button_color=('black', '#D9B382')))

    col_jugador.append(letras_jugador)

    # panel izquierdo:
    headings_tabla = ("Jugador", "Palabra", "Pts")
    col_izquierda = [[sg.Text("Jugadas: ")],
                    [sg.Table(puntajes_partida, headings_tabla, select_mode="browse", col_widths=(8, 8, 4), num_rows=10, auto_size_columns=False, key="tabla_puntos")],
                    [sg.Text("Fichas restantes: {}".format(len(bolsa)), key="bolsa_fichas")],
                    [sg.Text("Tiempo restante: ?", key="cronometro")],
                    [sg.Text("\n\n\n\n\n\n\n\n\n\n", pad=(None, 7))],
                    [sg.Button("Cambiar Fichas", button_color=('black', '#D9B382'), key="cambiar_fichas"), sg.Button("PASAR", button_color=('black', '#D9B382'))],
                    [sg.Button("TERMINAR", button_color=('black', '#D9B382')), (sg.Button("POSPONER", button_color=('black', '#D9B382')))]]


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

    letra_seleccionada = ' '

    palabra = []
    palabra2 = []

    fichas_seleccionadas = [] # originales
    llaves_seleccionadas = [] # 
    length_palabra = 0
    ficha_actual = None
    llave_actual = None
    palabra_actual = {}
    primera_jugada = True
    ppa = [] # posiciones palabra actual (seria muy largo el nombre de la variable sino, como este commment :D)

    while True:

        # el "_" detras de una variable significa que no se usa, es para que no salte warning
        # cuando la usemos, le sacamos el "_"
        event, _values = window.Read(timeout=10)

        # tiempo de juego
        if now() < fin:
            # para mayor legibilidad
            # llegado de hacer la funcion de posponer, habria que guardar el tiempo restante
            min_restantes = int((fin - now()) // 60)
            seg_restantes = int((fin - now()) % 60)
            window["cronometro"].Update(value="Tiempo: {:02d}:{:02d}".format(min_restantes, seg_restantes))

            if event is None:
                break

            if type(event) is tuple:
                if letra_seleccionada == ' ':
                    print('no seleccionaste ninguna letra')
                else:
                    if(get_sentido_correcto(palabra_actual.keys(), event, length_palabra)):
                    #if True:
                        if letra_cerca(palabra_actual.keys() if len(palabra_actual) else None, event, length_palabra):
                        #if True:
                            #if event not in ppa:
                            #    palabra_actual.keys().append(event)
                            #else:
                            #    palabra_actual.keys()[ppa.index(event)] = event
                            #ppa.append(event)
                            #ppa = sorted(ppa)
                            tl2[event] = letra_seleccionada
                            #tablero_logico[event[0]][event[1]] = letra_seleccionada
                            window[event].update(image_filename=letras[letra_seleccionada])
                            palabra.append(letra_seleccionada)
                            fichas_seleccionadas.append(ficha_actual)
                            llaves_seleccionadas.append(llave_actual)
                            palabra_actual[event] = letra_seleccionada
                            letra_seleccionada = ' '
                            ficha_actual = None
                            llave_actual = None
                            window[llaves_seleccionadas[length_palabra]].update(image_filename=letras["vacio"])
                            estado_fichas[llaves_seleccionadas[length_palabra]] = {"letra": None, "cambiando": False, "colocando": False}
                            length_palabra += 1
                    #print("================")
                    


            
            if event == 'VERIFICAR':
                if(len(palabra_actual)):
                    #2lista_aux = sorted(lista_aux)
                    palabra_actual = ordenar_dic(palabra_actual)
                    todo = verificar_palabra(palabra_actual)
                    # ta aca
                    #print(todo)

                    if(primera_jugada and (7, 7) not in palabra_actual.keys()):
                        # de aca
                        for i in range(length_palabra):
                            estado_fichas[llaves_seleccionadas[i]] = fichas_seleccionadas[i]
                            window[llaves_seleccionadas[i]].update(image_filename=letras[estado_fichas[llaves_seleccionadas[i]]["letra"]]) # repite
                        for elem in palabra_actual.keys(): #else
                            window[elem].Update(image_filename=dibujar_casilla(elem[0], elem[1], dif)) #else
                        # a aca, se puede transformar en una funcion. ej: devolver_fichas() o restaurar_fichas()
                        sg.Popup("La primera palabra tiene que tener una ficha en el centro del tablero.")
                    else:
                        if(todo):
                            try:
                                for i in range(length_palabra):
                                    estado_fichas[llaves_seleccionadas[i]] = {"letra": sacar_letra(bolsa), "cambiando": False, "colocando": False} #if
                                    window[llaves_seleccionadas[i]].update(image_filename=letras[estado_fichas[llaves_seleccionadas[i]]["letra"]]) # repite
                            except IndexError:
                                #terminar_juego()
                                sg.Popup("Aca deberia terminar el juego, pues no more fixas bro")
                            for key, value in palabra_actual.items(): #if
                                tablero_logico[key[0]][key[1]] = value #if
                            if(primera_jugada):
                                primera_jugada = False
                            p = "".join(palabra_actual.values()) # cambiar a palabra formada or something
                            agregar_puntaje_tabla(puntajes_partida, "penia", p, calcular_puntaje_jugada(palabra_actual.keys(), dif, palabra_actual, puntajes_letras))
                            window["tabla_puntos"].Update(values=puntajes_partida)
                            playsound(sfx["correcto"], False)
                        else:
                            for i in range(length_palabra):
                                estado_fichas[llaves_seleccionadas[i]] = fichas_seleccionadas[i]
                                window[llaves_seleccionadas[i]].update(image_filename=letras[estado_fichas[llaves_seleccionadas[i]]["letra"]]) # repite
                            for elem in palabra_actual.keys(): #else
                                window[elem].Update(image_filename=dibujar_casilla(elem[0], elem[1], dif)) #else
                            playsound(sfx["incorrecto"], False)

                    print("ppa",ppa)
                    print("l2",fichas_seleccionadas)
                    print("l3",llaves_seleccionadas)
                    print("td", palabra_actual)
                    llaves_seleccionadas = []
                    fichas_seleccionadas = []
                    p = ""
                    palabra = []
                    palabra2 = []
                    palabra_actual = {}
                    #for row in tablero_logico:
                    #    print(row)
                    length_palabra = 0
                    ppa = []
                    lista_aux = []
                else:
                    sg.Popup("No se puso ninguna palabra en el tablero.")

            # # devuelve el valor del atril jugador
            # #print(estado_fichas[event]["letra"])

            if event == "TERMINAR": # cuando finaliza :   En ese momento se muestran las fichas que posee cada jugador y se recalcula el puntaje restando al mismo el valor de dichas fichas
                exit = sg.PopupOKCancel("¿Esta seguro que desea salir?", title="!")
                if(exit == "OK"):
                    break

            if event == "POSPONER": # Al elegir esta opción se podrá guardar la partida para length_palabrainuarla luego. En este caso, se podrá guardar la partida actual teniendo en cuenta la información del tablero y el tiempo restante. Al momento de iniciar el juego, se pedirá si se desea length_palabrainuar con la partida guardada (si es que hay una) o iniciar una nueva. En cualquier caso siempre habrá una única partida guardada.
                turno_computadora(True, fichas_maquina, 0, tablero_logico, window, bolsa, puntajes_partida, dif, puntajes_letras)
            
            if event == "music_toggle":
                if(musica_muteada):
                    pygame.mixer.music.set_volume(0.05)
                    window["music_toggle"].Update("MUSIC: ON")
                else:
                    pygame.mixer.music.set_volume(0)
                    window["music_toggle"].Update("MUSIC: OFF")
                musica_muteada = not musica_muteada

            if event == "cambiar_fichas": # me gustaria hacer que esto sea una funcion, asi queda mejor y mas prolijo aca

                if(cambios_jugador >= 999):
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
                            #pasar_turno()
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
                letra_seleccionada = estado_fichas[event]["letra"]
                ficha_actual = estado_fichas[event]
                llave_actual = str(event)
                
                if(cambiando_fichas):
                    if(not estado_fichas[event]["cambiando"]):
                        fichas_seleccionadas.append(estado_fichas[event]["letra"])
                    else:
                        fichas_seleccionadas.remove(estado_fichas[event]["letra"])
                    window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(fichas_seleccionadas).upper()))
                    estado_fichas[event]["cambiando"] = not estado_fichas[event]["cambiando"]


            window["bolsa_fichas"].Update(value="Fichas restantes: {}".format(len(bolsa)))

        else:
            #finalizar_juego()
            break

        
    sg.Popup("Juego finalizado.")


def mostrar_top10(puntajes: list):
    """
    Función encargada de visualizar un top 10 con los puntajes obtenidos del tipo: fecha + puntaje + nivel.
    """
    ancho_columnas = (10, 10)
    headings = ("Jugador", "Nivel", "Puntaje")
    layout = [[sg.Table(puntajes, headings, select_mode="browse", col_widths=ancho_columnas, num_rows=10, auto_size_columns=False)]]
    window = sg.Window("TOP 10", layout, resizable=True, finalize=True).Finalize()
    while True:
        event, _values = window.read()
        if event is None:
            break

def mostrar_opciones(letras: list): # recibe un dict_keys pero es la forma mas apropiada de definirlo
    """
    Esta función muestra al usuario las opciones avanzadas por defecto y permite la edicion del mismo
    """


    def get_datos_letra(letra: str) -> dict:
        try:
            with open("config.cfg") as config:
                datos = json.load(config)
                return datos[letra]
              
        except FileNotFoundError:
            return config_por_defecto()[letra]
            
    def interfaz() -> list:
      
        # Preparo la sublista
        lista = sorted(letras, reverse=False)
        lista.remove('?')
        lista.remove("vacio")
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

    def guardar_json(datos: dict):
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
    Función encargada de mostrar una imagen
    en caso de que el top 10 este vacio
    """
    sg.popup_animated(image_source="img/vacioves.png", message="Esta vacio, ves? No hay puntajes aqui.", no_titlebar=False, title=":(")


# comienzo de "main"

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
        [sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), default_value="Facil", key="nivel")],
        [sg.Text("Tiempo de juego:"), sg.Combo(values=(5, 20, 40, 60), default_value=5, key="tiempo")],
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
        pass

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
