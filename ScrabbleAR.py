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
import pickle
from random import shuffle, choice, randint
from time import time
from typing import Union
from sys import platform
from datetime import datetime

import PySimpleGUI as sg
from pattern.es import spelling, lexicon, parse
import pygame

if platform == "win32":
    from playsound import playsound
    
elif platform == "linux":
    import sounddevice as sd
    import soundfile as sf
    

PATH_TABLERO = "img/tablero"
PATH_FICHAS = "img/fichas"
PATH_MUSICA = "audio/musica"
PATH_SFX = "audio/sfx"

sg.LOOK_AND_FEEL_TABLE["Fachero"] = {"BACKGROUND": "#191970", # midnight blue
                                    "TEXT": "#D9B382", # BEIGE
                                    "INPUT": "#D9B382",
                                    "TEXT_INPUT": "#191970",
                                    "SCROLL": "#c7e78b",
                                    # "BUTTON": ("black", "#D9B382"),
                                    "BUTTON": ("black", "#d1d6d7"),
                                    "PROGRESS": ("#01826B", "#D0D0D0"),
                                    "BORDER": 1, "SLIDER_DEPTH": 0, "PROGRESS_DEPTH": 0,
                                }

sg.theme("Fachero") # ta fachero no?


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

casillas = {"palabra_x2": os.path.join(PATH_TABLERO, "verde.png"),
        "palabra_x3": os.path.join(PATH_TABLERO, "amarelo.png"),
        "letra_x2": os.path.join(PATH_TABLERO, "marron.png"),
        "letra_x3": os.path.join(PATH_TABLERO, "azul.png"),
        "descuento_x1": os.path.join(PATH_TABLERO, "resta1.png"),
        "descuento_x2": os.path.join(PATH_TABLERO, "resta2.png"),
        "descuento_x3": os.path.join(PATH_TABLERO, "resta3.png"),
        "neutro": os.path.join(PATH_TABLERO, "fondo.png")}

sfx = {"correcto": os.path.join(PATH_SFX, "421002__eponn__correct.wav"),
    "incorrecto": os.path.join(PATH_SFX, "243700__ertfelda__incorrect.wav")}

lista_musica = [os.path.join(PATH_MUSICA, "Sergey_Cheremisinov_-_05_-_The_Healing.mp3"), 
        os.path.join(PATH_MUSICA, "Sergey_Cheremisinov_-_04_-_Northern_Lullaby.mp3"), 
        os.path.join(PATH_MUSICA, "Sergey_Cheremisinov_-_01_-_Gray_Drops.mp3"), 
        os.path.join(PATH_MUSICA, "Pictures_of_the_Floating_World_-_Waves.mp3"), 
        os.path.join(PATH_MUSICA, "Pictures_of_the_Floating_World_-_01_-_Canada.mp3"), 
        os.path.join(PATH_MUSICA, "Kai_Engel_-_05_-_Great_Expectations.mp3"), 
        os.path.join(PATH_MUSICA, "Chad_Crouch_-_Coral.mp3"), 
        os.path.join(PATH_MUSICA, "Chad_Crouch_-_Charcoal.mp3"), 
        os.path.join(PATH_MUSICA, "Chad_Crouch_-_Taut.mp3"), 
        os.path.join(PATH_MUSICA, "Chad_Crouch_-_Ruby.mp3"),
        os.path.join(PATH_MUSICA, "Chad_Crouch_-_Tuscan_Sun.mp3")]
shuffle(lista_musica)
lista_musica.extend(lista_musica) # un cheat para que dure mas jeje

def reproducir_sonido(archivo: str):
    """
    Función que se encarga de reproducir un sonido
    utilizando un respectivo modulo para cada plataforma.
    """
    if platform == "win32":
        playsound(archivo, False)

    elif platform == "linux":
        data, fs = sf.read(archivo, dtype='float32')  
        sd.play(data, fs)

def dibujar_casilla(x: int, y: int, dif: str) -> str:
    """
    Función que se encarga de devolver de que casillero
    se pinta cada casilla del tablero
    """

    for key, value in casilleros[dif.lower()].items(): 
        if (x, y) in value:
            return casillas[key]

    return casillas["neutro"]


def get_premio_descuento_casillero(pos: tuple, dif: str) -> str:
    """
    Función encargada de retornar el premio
    o descuento de un casillero del tablero.
    """
    for key, value in casilleros[dif.lower()].items(): 
        if pos in value:
            return key

    return "nada pues"

def get_datos_letra(letra: str) -> dict:
    """
    Función que devuelve los datos de una letra, estos son
    su puntaje y cantidad establecida.
    """
    try:
        with open("config.cfg") as config:
            datos = json.load(config)
            return datos[letra]

    except FileNotFoundError:
        return config_por_defecto()[letra]


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
    """
    Función encargada de otorgar el puntaje y la cantidad de fichas
    por defecto.
    """
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
    """
    Función encargada de guardar en un archivo JSON la
    configuración por defecto.
    """
    with open("config.cfg", "w") as config:
        json.dump(config_por_defecto(), config, indent=4)

def puntajes_por_defecto() -> dict:
    """
    Función encargada de generar el diccionario con 
    el puntaje de cada letra.
    """
    puntajes = {"a": 1, "b": 3, "c": 2, "d": 2, "e": 1,
                "f": 4, "g": 2, "h": 4, "i": 1, "j": 6, 
                "k": 8, "l": 1, "m": 3, "n": 1, "o": 1,
                "p": 3, "q": 8, "r": 1, "s": 1, "t": 1,
                "u": 1, "v": 4, "w": 8, "x": 8, "y": 4, "z": 10}
    return puntajes

def cargar_puntajes_letras() -> dict:
    """
    Función encargada de guardar en un archivo JSON
    los puntajes por defecto de cada letra.
    """
    try:
        with open("config.cfg") as config:
            datos = json.load(config)
            puntajes = {}
            for x, y in datos.items():
                puntajes[x] = y["puntaje"]

            return puntajes
    except FileNotFoundError:
        sg.Popup("El archivo de configuración no ha sido encontrado!", title="Error Critico")


def dar_fichas_maquina(bolsa: list) -> list:
    """
    Función encargada de otorgar las 7 fichas random
    utilizando la funcion sacar_letra.
    """
    return [sacar_letra(bolsa) for x in range(7)]


def cambiar_fichas_maquina(bolsa: list, fm: list):
    """
    Función encargada de cambiar las fichas de la maquina
    """
    bolsa.extend(fm)
    shuffle(bolsa)
    fm = dar_fichas_maquina(bolsa)


def generar_tablero(dificultad: str, pr: bool, tl: Union[list, None] = None) -> list:
    """
    Función encargada de generar los 3 tableros con una dimesion de 15x15
    utilizando la funcion casillero_segun_color
    """
    tablero = []
    for i in range(15):
        tablero.append([])
        for j in range(15):
            tablero[i].append(sg.Button(image_filename=letras[tl[i][j]] if (tl is not None and tl[i][j] != " ") else dibujar_casilla(i, j, dificultad), image_size=(32, 32), key=(i, j), pad=(0, 0)))
    return tablero

def verificar_palabra(palabra: Union[list, dict], dif: str, cat_azar: Union[None, str] = None) -> bool:
    """
    Función encargada de verificar si la palabra colocada en el tablero
    está en la lista de palabras de la libreria Pattern.
    """
    p = "".join(palabra.values() if type(palabra) == dict else palabra)
    s = parse(p).split()
    for cada in s:
        for pal in cada:
            if dif == "Facil":
                ok = pal[1] in ("VB", "NNS", "NN", "JJ")
            elif dif == "Medio":
                ok = pal[1] in ("VB", "NNS", "NN")
            elif dif == "Dificil":
                ok = pal[1] in cat_azar
    return ok and ((p in lexicon) or (p in spelling))

def ordenar_dic(dic: dict) -> dict:
    """
    Simple función que se encarga de ordenar un diccionario.
    """
    return {key: dic[key] for key in sorted(dic)}

     
def turno_computadora(pj: bool, 
                    fichas_maquina: list, 
                    cambios_maquina: int, 
                    tablero_logico: list, 
                    window: sg.PySimpleGUI.Window, 
                    bolsa: list, 
                    puntajes_partida: list, 
                    dif: str, 
                    puntajes_letras: dict, 
                    intentos_fallidos_maquina: int,
                    cat_azar: Union[None, str]) -> tuple:
    """
    Función que se encarga del turno de la computadora y su inteligencia.
    """
    found = False
    for i in range(50):
        palabra = []
        copia_bolsa = fichas_maquina.copy() 
        for _j in range(randint(2, len(copia_bolsa))):
            letra_random = choice(copia_bolsa)
            palabra.append(letra_random)
            copia_bolsa.remove(letra_random)
        if(verificar_palabra(palabra, dif, cat_azar)):
            found = True
            break

    posiciones_afectadas = {}
    if found:
        if(pj):
            sentido = randint(0, 1)
            for i in range(7, 7+len(palabra)):
                tupuntajes_letrasa = (i, 7) if sentido == 0 else (i, 7)
                window[tupuntajes_letrasa].Update(image_filename=letras[palabra[i-7]])
                tablero_logico[tupuntajes_letrasa[0]][tupuntajes_letrasa[1]] = palabra[i-7]
                posiciones_afectadas[tupuntajes_letrasa] = palabra[i-7]
            pj = False
        else:
            while True:
                posiciones = tuple([randint(0, 14) for i in range(2)])
                if(tablero_logico[posiciones[0]][posiciones[1]] == " "):
                    todo_libre = True
                    sentido = randint(0, 1)
                    pos_actual = 0
                    if(posiciones[sentido] + len(palabra) > 14):
                        continue

                    for i in range(posiciones[sentido], posiciones[sentido]+len(palabra)):
                        if sentido == 0:
                            if tablero_logico[i][posiciones[1]] != " ":
                                todo_libre = False
                                break
                        else:
                            if tablero_logico[posiciones[0]][i] != " ":
                                todo_libre = False
                                break

                    if todo_libre:
                        for i in range(posiciones[sentido], posiciones[sentido]+len(palabra)):
                            tupuntajes_letrasa = (i, posiciones[1]) if sentido == 0 else (posiciones[0], i)
                            window[tupuntajes_letrasa].Update(image_filename=letras[palabra[pos_actual]])
                            tablero_logico[tupuntajes_letrasa[0]][tupuntajes_letrasa[1]] = palabra[pos_actual]
                            posiciones_afectadas[tupuntajes_letrasa] = palabra[pos_actual]
                            pos_actual+=1
                        break
                    else:
                        continue
        p = "".join(palabra) 
        puntos_obtenidos = calcular_puntaje_jugada(posiciones_afectadas, dif, puntajes_letras)
        agregar_puntaje_tabla(puntajes_partida, "CPU", p, puntos_obtenidos)
        global puntos_maquina
        puntos_maquina += puntos_obtenidos
        window["tabla_puntos"].Update(values=puntajes_partida)
        window["bolsa_fichas"].Update(value=f"Fichas restantes: {len(bolsa)}")
        window["puntajes_totales"].Update(f"{nombre_jugador}: {puntos_jugador}\n\nCPU: {puntos_maquina}")
        try:
            for i in palabra:
                fichas_maquina[fichas_maquina.index(i)] = sacar_letra(bolsa)
        except IndexError:
            pass
        intentos_fallidos_maquina = 0
            
    else:
        intentos_fallidos_maquina += 1
        if(intentos_fallidos_maquina == 3):
            if(cambios_maquina < 3):
                cambiar_fichas_maquina(bolsa, fichas_maquina)
                cambios_maquina += 1
                sg.Popup("El CPU pasó de turno y realizó un cambio de fichas.", title="Aviso", non_blocking=True)
                intentos_fallidos_maquina = 0
            else:
                sg.Popup("El CPU pasó de turno.", title="Aviso", non_blocking=True)
        else:
            sg.Popup("El CPU pasó de turno.", title="Aviso", non_blocking=True)
    
    return pj, cambios_maquina, intentos_fallidos_maquina


def sentido_palabra_actual(pos: list, ultimo: int) -> str:
    """
    Función encargada de verificar si la palabra que se ingreso esta
    horizontal o vertical
    """
    if(len(pos) > 1):
        pos = [x for x in pos]
        if pos[ultimo-1][0] == pos[ultimo-2][0]:
            return "Horizontal"
        elif pos[ultimo-1][1] == pos[ultimo-2][1]: 
            return "Vertical"
    else:
        return "?"


def get_sentido_correcto(pos: tuple, actual: tuple, ultimo: int) -> bool:
    """
    Función que revisa si la proxima letra a ingresar esta
    siendo insertada correctamente.
    """
    if(len(pos) > 1):
        pos = [x for x in pos]
        if(sentido_palabra_actual(pos, ultimo) == "Horizontal"): 
            return True if actual[1] in (pos[0][1]-1, pos[ultimo-1][1]+1) else False
        elif(sentido_palabra_actual(pos, ultimo) == "Vertical"): 
            return True if actual[0] in (pos[0][0]-1, pos[ultimo-1][0]+1) else False
    else:
        return True

def letra_cerca(pos: Union[None, list], actual: tuple, ultimo: int) -> bool:
    """
    Función que se encarga de verificar letras cercanas
    para determinar que la palabra se esta colocando
    de forma correcta.
    """
    if(pos != None):
        pos = [x for x in pos]
        posibles = ((pos[0][0]-1, pos[0][1]),
        (pos[ultimo-1][0]+1, pos[ultimo-1][1]), 
        (pos[0][0], pos[0][1]-1), 
        (pos[ultimo-1][0], pos[ultimo-1][1]+1))

    return (("posibles" in locals()) and (actual in posibles)) or pos is None


def calcular_puntaje_jugada(data: dict, dif: str, pl:dict) -> int: 
    """
    Función encargada de calcular el puntaje de la jugada.
    """
    total = 0
    for key, value in data.items():
        x = get_premio_descuento_casillero(key, dif) # para mayor prolijidad
        if x == "letra_x2":
            total += pl[value]*2
        elif x == "letra_x3":
            total += pl[value]*3
        elif x == "descuento_x1":
            total += pl[value]-1
        elif x == "descuento_x2":
            total += pl[value]-2
        elif x == "descuento_x3":
            total += pl[value]-3
        elif x == "palabra_x2":
            total = (total + pl[value]) * 2
        elif x == "palabra_x3":
            total = (total + pl[value]) * 3
        else:
            total += pl[value]

    return total

def agregar_puntaje_tabla(pp: list, nombre: str, palabra: str, puntaje: int):
    """
    Función encargada de agregar a la tabla ,el puntaje,el nombre del usuario
    y la palabra.
    """
    pp.append([nombre, palabra, puntaje])

def guardar_puntaje_finalizado(nombre: str, dif: str, punt: int):
    """
    Función encargada de guardar la partida del jugador al terminar 
    """
    try:
        with open("puntajes.json") as arc:
            datos = list(json.load(arc))
            datos.append([nombre, dif, punt])
            datos = sorted(datos, reverse=True, key=lambda x: x[2])[:10]
        with open("puntajes.json", "w") as p:        
            json.dump(datos, p, indent=4)

    except FileNotFoundError:
        with open("puntajes.json", "w") as p:
            json.dump([[nombre, dif, punt]], p)

def guardar_json(datos: dict):
    """
    Funcion encargada de guardar datos en un 
    archivo JSON, utilizada para el top 10.
    """
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

def devolver_fichas(window: sg.PySimpleGUI.Window, 
                largo_palabra: int, 
                estado_fichas: dict, 
                llaves_seleccionadas: list, 
                fichas_seleccionadas: list, 
                palabra_actual: dict,
                dif: str):
    """
    Procedimiento para devolver al atril las fichas
    del jugador en caso de que la palabra
    no se pueda poner en el tablero.
    """

    for i in range(largo_palabra):
        estado_fichas[llaves_seleccionadas[i]] = fichas_seleccionadas[i]
        window[llaves_seleccionadas[i]].update(image_filename=letras[estado_fichas[llaves_seleccionadas[i]]["letra"]]) 
    for elem in palabra_actual.keys(): 
        window[elem].Update(image_filename=dibujar_casilla(elem[0], elem[1], dif)) 

def get_cat_azar(cat: str) -> str:
    """
    Función que devuelve de una forma mas legible
    la categoria al azar a jugar en la dificultad
    Dificil.
    """
    if cat == "VB":
        return "Verbos"
    elif cat == ("NNS", "NN"):
        return "Sustantivos"
    elif cat == "JJ":
        return "Adjetivos"

def generar_ventana_de_juego(tj: int = None, dif: str = None, pr: bool = False, dpr: Union[dict, None] = None):
    """
    Función encargada de iniciar el juego,utilizando los procesos
    declarados anteriormente.Tambien se encarga de generar el cronometro.
    """
    if(pr):
        dif = dpr["dificultad"]
        cat_azar = dpr["cat_azar"]
    else:
        if dif == "Dificil":
            cat_azar = choice(["VB", ("NNS", "NN"), "JJ"])
        else:
            cat_azar = None
    

    # settings musica:
    cant_canciones = len(lista_musica)
    cancion_actual = 0
    musica_muteada = False
    pygame.mixer.init()
    pygame.mixer.music.load(lista_musica[cancion_actual])
    pygame.mixer.music.set_volume(0.1)
    pygame.mixer.music.play()

    # esto se va a poner feo
    puntajes_letras = cargar_puntajes_letras()
    puntajes_partida = [] if not pr else dpr["lista_jugadas"]

    cambios_jugador = 0 if not pr else dpr["cambios_jugador"]
    cambios_maquina = 0 if not pr else dpr["cambios_maquina"]
    cambiando_fichas = False

    # turno de jugador
    primer_turno_jugador = bool(randint(0, 1)) if not pr else dpr["primer_turno_jugador"]

    # bolsa de fichas
    bolsa = generar_bolsa() if not pr else dpr["bolsa"]

    estado_fichas = {} if not pr else dpr["fichas_jugador"]

    if not pr:
        for i in range(0, 7):
            estado_fichas[f"ficha_jugador_{i}"] = {"letra": sacar_letra(bolsa), "cambiando": False}
    

    # cronometro related
    fin = time() + (tj * 60) if not pr else time() + dpr["tiempo_restante"]

    # fichas de la maquina:
    fichas_maquina = dar_fichas_maquina(bolsa) if not pr else dpr["fichas_maquina"]
    intentos_fallidos_maquina = 0 if not pr else dpr["intentos_fallidos_maquina"]

    # columnas:

    # fichas computadora:
    col_arriba = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18)), sg.Text(" "*13)]]
    for i in range(7):
        col_arriba[0].append(sg.Button(image_filename=letras["?"], border_width=0, pad=((9, 0), (10, 0)), button_color=("black", "#191970"), key=f"fichas_maquina{i}"))
    col_arriba[0].extend([sg.Text(" "*91), sg.Button("MUSIC: ON", button_color=("black", "#D9B382"), key="music_toggle")])

    # tablero de juego:
    col_tablero = generar_tablero(dif, pr, dpr["estado_tablero"] if pr else None)

    # crear tablero logico
    tablero_logico  = [[" " for j in range(15)] for i in range(15)] if not pr else dpr["estado_tablero"]

    # letras del jugador:
    fichas_seleccionadas = []
    col_jugador = [[sg.Text(" "*49), sg.Text("Letras seleccionadas: ", key="letras_selecc", size=(180, None))]]

    letras_jugador = [sg.Text(" "*49)]
    for i in range(0, 7):
        letras_jugador.append(sg.Button(image_filename=letras[estado_fichas[f"ficha_jugador_{i}"]["letra"]], button_color=("black", "#191970"), border_width=0, key=f"ficha_jugador_{i}"))


    letras_jugador.append(sg.Text(" "*33))
    letras_jugador.append(sg.Button("VERIFICAR", button_color=("black", "#D9B382")))

    col_jugador.append(letras_jugador)

    if not pr:
        global nombre_jugador
        global puntos_jugador
        global puntos_maquina
    else:
        nombre_jugador = dpr["nombre_jugador"]
        puntos_jugador = dpr["puntos_jugador"]
        puntos_maquina = dpr["puntos_maquina"]

    # panel izquierdo:
    headings_tabla = ("Jugador", "Palabra", "Pts")
    col_izquierda = [[sg.Text("Jugadas: ")],
                    [sg.Table(puntajes_partida, headings_tabla, select_mode="browse", col_widths=(8, 8, 4), num_rows=10, auto_size_columns=False, key="tabla_puntos")],
                    [sg.Frame(layout=[[sg.Text(f"{nombre_jugador}: {puntos_jugador}\n\nCPU: {puntos_maquina}", size=(20, 5), font=("Arial Bold", 10), key="puntajes_totales")]], title="Puntaje Total:")],
                    [sg.Text(f"Fichas restantes: {len(bolsa)}", key="bolsa_fichas")],
                    [sg.Text("Tiempo restante: ?", key="cronometro")],
                    [sg.Text(f"Nivel: {dif}" if dif != "Dificil" else f"Nivel: {dif} ({get_cat_azar(cat_azar)})")],
                    [sg.Text("\n", pad=(None, 5))],
                    [sg.Button("Cambiar Fichas", button_color=("black", "#D9B382"), key="cambiar_fichas"), sg.Button("PASAR", button_color=("black", "#D9B382"))],
                    [sg.Button("TERMINAR", button_color=("black", "#D9B382")), (sg.Button("POSPONER", button_color=("black", "#D9B382")))]]

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

    letra_seleccionada = " "

    fichas_seleccionadas = [] 
    llaves_seleccionadas = [] 
    length_palabra = 0
    ficha_actual = None
    llave_actual = None
    palabra_actual = {}
    primera_jugada = True

    while True:
        event, _values = window.Read(timeout=10)

        if not(len(bolsa)):
            terminar_juego(window, fichas_maquina, estado_fichas, dif)
        if (pygame.mixer.music.get_busy() == 0) and (cancion_actual < cant_canciones):
            cancion_actual += 1
            pygame.mixer.music.load(lista_musica[cancion_actual])
            pygame.mixer.music.play()

        # tiempo de juego
        if time() < fin:
            # para mayor legibilidad
            # llegado de hacer la funcion de posponer, habria que guardar el tiempo restante
            min_restantes = int((fin - time()) // 60)
            seg_restantes = int((fin - time()) % 60)
            window["cronometro"].Update(value="Tiempo: {:02d}:{:02d}".format(min_restantes, seg_restantes))

            if event is None:
                break

            if(not primer_turno_jugador):
                primera_jugada, cambios_maquina, intentos_fallidos_maquina = turno_computadora(primera_jugada, fichas_maquina, 0, tablero_logico, window, bolsa, puntajes_partida, dif, puntajes_letras, intentos_fallidos_maquina, cat_azar if "cat_azar" in locals() else None)
                primer_turno_jugador = True

            if type(event) is tuple:
                if letra_seleccionada == " ":
                    sg.Popup("No has seleccionado ninguna letra.", title="Aviso", non_blocking=True)
                else:
                    if(tablero_logico[event[0]][event[1]] != " "):
                        reproducir_sonido(sfx["incorrecto"])
                    else:
                        if(get_sentido_correcto(palabra_actual.keys(), event, length_palabra)):
                            if letra_cerca(palabra_actual.keys() if len(palabra_actual) else None, event, length_palabra):
                                window[event].update(image_filename=letras[letra_seleccionada])
                                fichas_seleccionadas.append(ficha_actual)
                                llaves_seleccionadas.append(llave_actual)
                                palabra_actual[event] = letra_seleccionada
                                letra_seleccionada = " "
                                ficha_actual = None
                                llave_actual = None
                                window[llaves_seleccionadas[length_palabra]].update(image_filename=letras["vacio"])
                                estado_fichas[llaves_seleccionadas[length_palabra]] = {"letra": None, "cambiando": False}
                                length_palabra += 1
                    
            
            if event == "VERIFICAR":
                if(len(palabra_actual)):
                    palabra_actual = ordenar_dic(palabra_actual)
                    todo = verificar_palabra(palabra_actual, dif, cat_azar if "cat_azar" in locals() else None)

                    if(primera_jugada and (7, 7) not in palabra_actual.keys()):
                        devolver_fichas(window, length_palabra, estado_fichas, llaves_seleccionadas, fichas_seleccionadas, palabra_actual, dif)
                        sg.Popup("La primera palabra tiene que tener una ficha en el centro del tablero.", non_blocking=True)
                    else:
                        if(len(palabra_actual) >= 2):
                            if(todo):
                                try:
                                    for i in range(length_palabra):
                                        estado_fichas[llaves_seleccionadas[i]] = {"letra": sacar_letra(bolsa), "cambiando": False} 
                                        window[llaves_seleccionadas[i]].update(image_filename=letras[estado_fichas[llaves_seleccionadas[i]]["letra"]]) # repite
                                except IndexError:
                                    terminar_juego(window, fichas_maquina, estado_fichas, dif)
                                for key, value in palabra_actual.items(): 
                                    tablero_logico[key[0]][key[1]] = value 
                                if(primera_jugada):
                                    primera_jugada = False
                                p = "".join(palabra_actual.values()) 
                                puntos_obtenidos = calcular_puntaje_jugada(palabra_actual, dif, puntajes_letras)
                                puntos_jugador += puntos_obtenidos
                                agregar_puntaje_tabla(puntajes_partida, nombre_jugador, p, puntos_obtenidos)
                                window["tabla_puntos"].Update(values=puntajes_partida)
                                reproducir_sonido(sfx["correcto"])
                                window["puntajes_totales"].Update(f"{nombre_jugador}: {puntos_jugador}\n\nCPU: {puntos_maquina}")
                                if(len(bolsa)):
                                    primera_jugada, cambios_maquina, intentos_fallidos_maquina = turno_computadora(False, fichas_maquina, 0, tablero_logico, window, bolsa, puntajes_partida, dif, puntajes_letras, intentos_fallidos_maquina, cat_azar if "cat_azar" in locals() else None)
                            else:
                                devolver_fichas(window, length_palabra, estado_fichas, llaves_seleccionadas, fichas_seleccionadas, palabra_actual, dif)
                                reproducir_sonido(sfx["incorrecto"])
                        else:
                            devolver_fichas(window, length_palabra, estado_fichas, llaves_seleccionadas, fichas_seleccionadas, palabra_actual, dif)
                            sg.Popup("La palabra debe contener al menos dos letras.", title="Aviso", non_blocking=True)
                            reproducir_sonido(sfx["incorrecto"])

                    llaves_seleccionadas = []
                    fichas_seleccionadas = []
                    p = ""
                    palabra_actual = {}
                    length_palabra = 0
                    lista_aux = []
                else:
                    sg.Popup("No se puso ninguna palabra en el tablero.", title="Aviso", non_blocking=True)

            if event == "TERMINAR": 
                salida = sg.PopupOKCancel("¿Esta seguro que desea salir?", title="Aviso", button_color=("black", "#D9B382"))
                if(salida == "OK"):
                    terminar_juego(window, fichas_maquina, estado_fichas, dif)
            
            if event == "PASAR":
                if(len(bolsa)):
                    primera_jugada, cambios_maquina, intentos_fallidos_maquina = turno_computadora(primera_jugada, fichas_maquina, 0, tablero_logico, window, bolsa, puntajes_partida, dif, puntajes_letras, intentos_fallidos_maquina, cat_azar if "cat_azar" in locals() else None)

            if event == "POSPONER":
                if(hay_partida_guardada()):
                    salida = sg.PopupOKCancel("Ya hay una partida guardada. ¿Desea posponer la partida actual?", 
                                        "De ser asi, perderá la ultima partida guardada.", 
                                        title="Aviso", 
                                        button_color=("black", "#D9B382"))
                else:
                    salida = sg.PopupOKCancel("¿Está seguro que desea posponer esta partida?", title="Aviso", button_color=("black", "#D9B382"))
                if(salida == "OK"):
                    fecha = str(datetime.fromtimestamp(time()))
                    fecha_formateada = (f"{fecha[8:10]}/{fecha[5:7]}/{fecha[0:4]} - {fecha[11:13]}:{fecha[14:16]}:{fecha[17:19]}")
                    datos_partida = {"dificultad": dif,
                        "cat_azar": cat_azar,
                        "bolsa": bolsa,
                        "tiempo_restante": fin - time(),
                        "estado_tablero": tablero_logico,
                        "lista_jugadas": puntajes_partida,
                        "nombre_jugador": nombre_jugador,
                        "fichas_jugador": estado_fichas,
                        "puntos_jugador": puntos_jugador,
                        "cambios_jugador": cambios_jugador,
                        "primer_turno_jugador": primer_turno_jugador,
                        "fichas_maquina": fichas_maquina,
                        "puntos_maquina": puntos_maquina,
                        "cambios_maquina": cambios_maquina,
                        "intentos_fallidos_maquina": intentos_fallidos_maquina,
                        "fecha": fecha_formateada}
                    posponer_partida(datos_partida)
                    pygame.mixer.music.stop()
                    sg.Popup("Tu partida ha sido pospuesta con exito. Hasta la proxima!", title="Enhorabuena!", button_color=("black", "#D9B382"))
                    break
                    

            if event == "music_toggle":
                if(musica_muteada):
                    pygame.mixer.music.set_volume(0.05)
                    window["music_toggle"].Update("MUSIC: ON")
                else:
                    pygame.mixer.music.set_volume(0)
                    window["music_toggle"].Update("MUSIC: OFF")
                musica_muteada = not musica_muteada

            if event == "cambiar_fichas": 

                if(cambios_jugador >= 3):
                    sg.Popup("Ya no tienes cambios de fichas restantes.", title="Aviso", non_blocking=True)
                else:
                    if((cambiando_fichas) and len(fichas_seleccionadas)):
                        salida = sg.PopupOKCancel("Esta seguro que desea cambiar las fichas?", title="!!", button_color=("black", "#D9B382"))
                        if(salida == "OK"):
                            bolsa.extend(fichas_seleccionadas)
                            shuffle(bolsa)
                            for _x in fichas_seleccionadas:
                                letra = sacar_letra(bolsa)
                                for i in range(7):
                                    if(estado_fichas[f"ficha_jugador_{i}"]["cambiando"]):
                                        estado_fichas[f"ficha_jugador_{i}"]["cambiando"] = False
                                        estado_fichas[f"ficha_jugador_{i}"]["letra"] = letra
                                        window[f"ficha_jugador_{i}"].Update(image_filename=letras[letra])
                                        break
                            cambios_jugador += 1
                            if(len(bolsa)):
                                primera_jugada, cambios_maquina, intentos_fallidos_maquina = turno_computadora(primera_jugada, fichas_maquina, 0, tablero_logico, window, bolsa, puntajes_partida, dif, puntajes_letras, intentos_fallidos_maquina, cat_azar if "cat_azar" in locals() else None)
                        else:
                            for i in range(7):
                                estado_fichas[f"ficha_jugador_{i}"]["cambiando"] = False
                        fichas_seleccionadas = []
                        window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(fichas_seleccionadas).upper()))
                    cambiando_fichas = not cambiando_fichas

                # cambio de color del boton para indicar que el jugador esta realizando un cambio de fichas
                if(cambiando_fichas):
                    window["cambiar_fichas"].Update(button_color=("white", "#008000"))
                else:
                    window["cambiar_fichas"].Update(button_color=("black", "#D9B382"))

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


            window["bolsa_fichas"].Update(value=f"Fichas restantes: {len(bolsa)}")
            
        else:
            terminar_juego(window, fichas_maquina, estado_fichas, dif)

def posponer_partida(datos_partida: dict):
    """
    Función encargada de guardar los datos
    en formato pickle de la partida pospuesta.
    """
    # uso pickle para que el jugador no haga "trampa" y mire ni modifique las fichas que le quedan a la maquina, bolsa, etc
    with open("partida_guardada.dat", "wb") as arc:
        pickle.dump(datos_partida, arc)

def terminar_juego(window: sg.PySimpleGUI.Window, fm: list, estado_fichas: dict, dif: str):
    """
    Función encargada de finalizar el juego.
    """
    global puntos_maquina
    global puntos_jugador
    restantes_maquina = 0
    restantes_jugador = 0
    for i in range(0, 7):
        restantes_maquina += get_datos_letra(fm[i])["puntaje"]
        window[f"fichas_maquina{i}"].Update(image_filename=letras[fm[i]])
        restantes_jugador += get_datos_letra(estado_fichas[f"ficha_jugador_{i}"]["letra"])["puntaje"] if estado_fichas[f"ficha_jugador_{i}"]["letra"] != None else 0
    puntos_maquina -= restantes_maquina
    puntos_jugador -= restantes_jugador
    if(puntos_jugador > 0):
        guardar_puntaje_finalizado(nombre_jugador, dif, puntos_jugador)
    if(puntos_jugador > puntos_maquina):
        sg.Popup("Has ganado la partida!", "Puntajes:", f"Tú: {puntos_jugador}", f"CPU: {puntos_maquina}", title="Enhorabuena!")
    else:
        sg.Popup("Has perdido la partida.", "Puntajes:", f"Tú: {puntos_jugador}", f"CPU: {puntos_maquina}", title="Mejor suerte la proxima!")
    exit()

def hay_partida_guardada():
    """
    Función que se encarga de retornar
    si hay una partida guardada o no.
    """
    try:
        with open("partida_guardada.dat", "rb") as arc:
            data = pickle.load(arc)
            return bool(len(data))
    except FileNotFoundError:
        return False

def mostrar_top10():
    """
    Función encargada de visualizar un top 10 con los puntajes obtenidos del tipo: fecha + puntaje + nivel.
    """
    try:
        with open("puntajes.json") as arc:
            datos = json.load(arc)
        
        if not datos:
            popup_top10_vacio()
        else:
            ancho_columnas = (10, 10)
            headings = ("Jugador", "Nivel", "Puntaje")
            layout = [[sg.Table(datos, headings, select_mode="browse", col_widths=ancho_columnas, num_rows=10, auto_size_columns=False)]]
            window = sg.Window("TOP 10", layout, resizable=True).Finalize()

            while True:
                event, _values = window.read()
                if event is None:
                    break

    except FileNotFoundError:
        popup_top10_vacio()

def mostrar_opciones_avanzadas(letras: list): # recibe un dict_keys pero es la forma mas apropiada de definirlo
    """
    Esta función muestra al usuario las opciones avanzadas por defecto y permite la edicion del mismo
    """ 
    # Preparo la sublista
    lista = sorted(letras, reverse=False)
    lista.remove("?")
    lista.remove("vacio")
    mitad = int(len(lista)/2)
    primera = lista[:mitad]
    segunda = lista[mitad:]


    colum_arriba = [[sg.Text("       CANTIDAD  PUNTAJE     "*2)]]
    colum_izq = [[sg.Text(letra.upper()+":", key=letra, size=(2, 1)), sg.InputText(default_text=get_datos_letra(letra)["cantidad"], size=(8, 3), key=("cantidad"+letra)), sg.InputText(default_text=get_datos_letra(letra)["puntaje"], size=(8, 3), key=("puntaje"+letra))] for letra in primera]
    col_der = [[sg.Text(letra.upper()+":", key=letra, size=(2, 1)), sg.InputText(default_text=get_datos_letra(letra)["cantidad"], size=(8, 3), key=("cantidad"+letra)), sg.InputText(default_text=get_datos_letra(letra)["puntaje"], size=(8, 3), key=("puntaje"+letra))] for letra in segunda]

    col_abajo = [[sg.Button("Guardar", button_color=("black", "#D9B382")), sg.Button("Restablecer", key="reset", pad=(24, 0), button_color=("black", "#D9B382")), sg.Button("Atras", button_color=("black", "#D9B382"))]]

    layout = [[sg.Column(colum_arriba)],
            [sg.Column(colum_izq), sg.Column(col_der)],
            [sg.Column(col_abajo)]]

    window = sg.Window("Opciones avanzadas", layout)


    while True:
        event, values = window.read()

        if event == "Guardar":
            esta_mal = False
            for k, v in values.items():
                if(k[:-1] == "cantidad" and int(v) <= 0):
                    esta_mal = True
                    break
            if(esta_mal):
                sg.Popup("No se puede guardar una cantidad de fichas igual o menor a 0. Por favor, corrija esto.", title="Error!", button_color=("black", "#D9B382"))
            else:
                guardar_json(values)
                window.Close()

        if event == "reset":
            if sg.PopupOKCancel("Seguro que quieres restablecer los  valores de fabrica?",
                                title="Aviso", button_color=("black", "#D9B382")) == "OK":
                for key, _valor in values.items():
                    valor_nuevo = config_por_defecto()[key[-1]][key[:-1]]
                    window[key].update(valor_nuevo)
                    values[key] = valor_nuevo

        if event in (sg.WIN_CLOSED, "Atras"):

            break

    window.close()


def popup_top10_vacio():
    """
    Función encargada de mostrar una imagen
    en caso de que el top 10 este vacio
    """
    sg.popup_animated(image_source="img/vacioves.png", message="Esta vacio, ves? No hay puntajes aqui.", no_titlebar=False, title=":(")


# comienzo de "main"

# is this bad? (pues variables globales)

puntos_jugador = 0
puntos_maquina = 0

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
        [sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), default_value="Facil", key="nivel")],
        [sg.Text("Tiempo de juego:"), sg.Combo(values=(20, 40, 60), default_value=20, key="tiempo")],
        [sg.Button("TOP 10", button_color=("black", "#D9B382")), sg.Button("OPCIONES AVANZADAS", button_color=("black", "#D9B382"))],
        [sg.Button("REGLAMENTO", button_color=("black", "#D9B382"), pad=((64, 0), (5, 0)))],
        [sg.Button("CONTINUAR PARTIDA", button_color=("black", "#D9B382"), pad=((43, 0), (15, 0)))],
        [sg.Button("INICIAR", button_color=("black", "#D9B382"), pad=((83, 0), (15, 0)))]]


window = sg.Window("ScrabbleAR", layout, size=(280, 280) if platform == "linux" else (250, 250)).Finalize()


while True:
    event, values = window.Read()


    if event is None:
        break

    if event == "INICIAR":
        window.Close()

        while True:
            nombre_jugador = sg.popup_get_text("Por favor, ingrese su nombre: ", "Nombre" , button_color=("black", "#D9B382"))
            if(nombre_jugador is None):
                exit()
            elif(len(nombre_jugador)):
                break

        generar_ventana_de_juego(values["tiempo"], values["nivel"])

    if event == "CONTINUAR PARTIDA":
        try:
            with open("partida_guardada.dat", "rb") as arc:
                data = pickle.load(arc)
        except FileNotFoundError:
            data = {}

        if not len(data):
            sg.Popup("No hay partida guardada.", title="Aviso", button_color=("black", "#D9B382"))
        else:
            salida = sg.PopupOKCancel("Desea restaurar la partida guardada?", 
                        "Nombre: {}".format(data["nombre_jugador"]), 
                        "Dificultad: {}".format(data["dificultad"]) if data["dificultad"] != "Dificil" else "Dificultad: Dificil ({})".format(get_cat_azar(data["cat_azar"])),
                        "Fecha: {}".format(data["fecha"]),
                        button_color=("black", "#D9B382"))
            if salida == "OK":
                window.Close()
                generar_ventana_de_juego(pr=True, dpr=data)
                with open("partida_guardada.dat", "wb") as arc:
                    pickle.dump({}, arc)
    
    if event == "REGLAMENTO":
        sg.Popup("El jugador debe formar una palabra usando dos (2) o más letras, colocándolas horizontalmente (las letras ubicadas de izquierda a derecha) o verticalmente (en orden descendente) sobre el tablero.","En la primera jugada, una de las letras deberá estar situada en el cuadro de “inicio del juego”.","Para comenzar la partida, cada jugador retira siete (7) fichas de la bolsa. Luego combina dos o más de sus letras para formar una palabra, y la coloca en el tablero horizontal o verticalmente. Está obligado a poner una de las letras que forman su palabra en la casilla central.Una vez ingresada la palabra se debería confirmar la misma en el tablero y automáticamente se chequeará si la palabra corresponde a la clasificación que se está usando en el juego."," Las únicas palabras admitidas en el tablero serán adjetivos, sustantivos y verbos, de acuerdo a las opciones de configuración establecidas previamente. En caso de no corresponder, las fichas serán devueltas al jugador para que vuelva a intentar.Una vez que el jugador haya ingresado y confirmado correctamente la palabra, se le repondrá la cantidad de fichas que utilizó sin contar las preexistentes en el tablero. De esta manera el jugador nunca tendrá más de siete (7) fichas en su poder.","Cuando el turno lo tiene la computadora, se tratará de armar palabras con las fichas propias de la computadora. La primera combinación que concuerde es la que se tomará como válida. En caso de no encontrar combinación, pasará su turno.","En cualquier momento del juego, el jugador puede decidir usar un turno para cambiar algunas o todas sus fichas, devolviéndolas a la bolsa de fichas del juego y reemplazándolas por la misma cantidad; al final, siempre debe tener siete (7). En este mismo turno, el jugador no podrá colocar ninguna palabra sobre el tablero. Esta opción no está disponible para la computadora y el jugador sólo podrá usarla como máximo tres veces durante el juego.",title="Reglamento",button_color=("black", "#D9B382"))

    if event == "TOP 10":
        mostrar_top10()

    if event == "OPCIONES AVANZADAS":
        mostrar_opciones_avanzadas(letras.keys())

window.Close()
