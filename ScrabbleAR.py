#!/usr/bin/env python3

"""ScrabbleAR.py: Trabajo integrador de la materia Seminario de Lenguajes Opción Python"""

__author__ = "Juan Sebastián Peña, Hernan Nahuel Ramos, y Felipe Verdugo"
__credits__ = ["Juan Sebastián Peña", "Hernan Nahuel Ramos", "Felipe Verdugo"]
__license__ = "GPL"
__version__ = "3.0"
__maintainer__ = "Juan Sebastián Peña, Hernan Nahuel Ramos, y Felipe Verdugo"
__email__ = "juanpea.98@gmail.com, herni.ramoss@gmail.com, felipeverdugo016@gmail.com"
__status__ = "Produccion"

import os
from sys import platform
from json import load, dump
from random import shuffle, choice
from time import time as now
from os.path import isfile
import json

import PySimpleGUI as sg
#from pattern.es import verbs, spelling, lexicon 

PATH_TABLERO = 'img/tablero'
PATH_FICHAS = 'img/fichas'

sg.LOOK_AND_FEEL_TABLE['Fachero'] = {'BACKGROUND': '#191970', # midnight blue
										'TEXT': '#D9B382', # BEIGE
										'INPUT': '#D9B382',
										'TEXT_INPUT': '#191970',
										'SCROLL': '#c7e78b',
										#'BUTTON': ('black', '#D9B382'),
										'BUTTON': ('black', '#d1d6d7'),
										'PROGRESS': ('#01826B', '#D0D0D0'),
										'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
									}

sg.theme('Fachero') # tiene que ser cambiado

# esto va a tener que ser cambiado, ya que corresponden a un solo tablero
TUPLA_MARRONES = ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14))
TUPLA_ROJOS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (1, 13), (2, 12), (3, 11), (4, 10), (5, 9), (9, 5), (10, 4), (11, 3), (12, 2), (13, 1), (13, 13), (12, 12), (11, 11), (10, 10), (9, 9))
TUPLA_AZULES = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13))
TUPLA_VERDES = ((0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))

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

def casillero_segun_color(x, y): # acomodar
	if (x, y) in TUPLA_MARRONES:
		return os.path.join(PATH_TABLERO, 'beta_marron.png')

	elif (x, y) in TUPLA_ROJOS:
		return os.path.join(PATH_TABLERO, "beta_rojo3.png")

	elif (x, y) in TUPLA_AZULES:
		return os.path.join(PATH_TABLERO, "beta_azul2.png")

	elif (x, y) in TUPLA_VERDES:
		return os.path.join(PATH_TABLERO, "beta_verde2.png")

	else:
		return os.path.join(PATH_TABLERO, "fondo3.png") # nada

# podriamos hacer que la bolsa quede asi o se seleccione de un archivo configurable
def generar_bolsa():
	lista = list("aaaaaaaaaaabbbccccddddeeeeeeeeeeeffgghhiiiiiijjkllllmmmnnnnnooooooooppqrrrrsssssssttttuuuuuuvvwxyz")
	shuffle(lista)
	return lista

def sacar_letra(bolsa): 
	letra = choice(bolsa)
	bolsa.remove(letra)
	return letra

def dar_fichas_maquina(bolsa):
	return [sacar_letra(bolsa) for x in range(7)]

def cambiar_fichas_maquina(bolsa, fm, cambios): # deberia haber una funcion para cambiar fichas del usuario tambien, asi esta mas organizado
	for _i in range(7):
		bolsa.extend(fm)
	shuffle(bolsa)
	fm = dar_fichas_maquina(bolsa)
	return fm, cambios+1

def generar_tablero():
	tablero = []
	for i in range(15):
		tablero.append([])
		for j in range(15):
			tablero[i].append(sg.Button(image_filename=casillero_segun_color(i, j), image_size=(32, 32), key=(i,j), pad=(0, 0)))
	return tablero

def generar_ventana_de_juego(tj): # tj = tiempo de juego

	'''Esta funcion es la que que inicia el juego,utilizando los procesos
	declarados anteriormente.Tambien se encarga de generar el cronometro.
	'''
  # cambio de fichas
	cambios_jugador = 0
	_cambios_maquina = 0 # todavia no se usa
	# la idea es que en algun momento de la logica del cpu se use asi:
	# fichas_maquina, cambios_maquina = cambiar_fichas_maquina(bolsa, fichas_maquina, cambios_maquina)

	cambiando_fichas = False
	estado_fichas = {"ficha_jugador_0": False, 
				"ficha_jugador_1": False, 
				"ficha_jugador_2": False, 
				"ficha_jugador_3": False, 
				"ficha_jugador_4": False,
				"ficha_jugador_5": False,
				"ficha_jugador_6": False}

	# cronometro related
	fin = now() + (tj * 60)

	# bolsa de fichas
	bolsa = generar_bolsa()

	# fichas de la maquina:
	_fichas_maquina = dar_fichas_maquina(bolsa)

	# columnas: 

	# fichas computadora: 
	col_arriba = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18)),sg.Text(" "*10)]]
	for i in range(7):
		col_arriba[0].append(sg.Button(image_filename=letras["?"], border_width=0, pad =((9,0),(10,0)),button_color=('black', '#191970')))

	# tablero de juego:
	col_tablero = generar_tablero()

	# letras del jugador:
	fichas_seleccionadas = []
	col_jugador = [[sg.Text(" "*45), sg.Text("Letras seleccionadas: ", key="letras_selecc",size=(180, None))]]

	letras_jugador = [sg.Text(" "*45)]
	for i in range(0, 7):
		l = sacar_letra(bolsa) # deberia devolver un objeto y no una letra
		letras_jugador.append(sg.Button(l, font="Arial 1", image_filename=letras[l], button_color=('black', '#191970'), border_width=0,key="ficha_jugador_{}".format(i)))
		#letras_jugador.append(sg.Button(l, font="Arial 1", image_filename=letras[l], key="ficha_jugador_{}".format(i)))

	col_jugador.append(letras_jugador)

	# panel izquierdo:
	headings_tabla = ("Jugador", "Puntaje")
	col_izquierda = [[sg.Text("Puntajes: ")],
					[sg.Table([], headings_tabla, select_mode="browse", col_widths=(10, 10), num_rows=10, auto_size_columns=False,key="tabla_puntos")],
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
	#window.Maximize()

	while True:

		# el "_" detras de una variable significa que no se usa, es para que no salte warning
		# cuando la usemos, le sacamos el "_"
		event, _values = window.Read(timeout=10)

		if event is None:
			break


		if event is "TERMINAR": #cuando finaliza :   En ese momento se muestran las fichas que posee cada jugador y se recalcula el puntaje restando al mismo el valor de dichas fichas
			sg.PopupOKCancel("¿Esta seguro que desea salir?", title="!")
			break

		if event is "POSPONER": #  Al elegir esta opción se podrá guardar la partida para continuarla luego. En este caso, se podrá guardar la partida actual teniendo en cuenta la información del tablero y el tiempo restante. Al momento de iniciar el juego, se pedirá si se desea continuar con la partida guardada (si es que hay una) o iniciar una nueva. En cualquier caso siempre habrá una única partida guardada.
			pass

		if event is "cambiar_fichas": # me gustaria hacer que esto sea una funcion, asi queda mejor y mas prolijo aca
			if(cambios_jugador >= 3):
				sg.Popup("Ya no tienes cambios de fichas restantes.")
			else:
				if((cambiando_fichas) and len(fichas_seleccionadas)):
					salida = sg.PopupOKCancel("Esta seguro que desea cambiar las fichas?", title="!!")
					if(salida == "OK"):
						bolsa.extend(fichas_seleccionadas)
						shuffle(bolsa)
						for _x in fichas_seleccionadas:
							l = sacar_letra(bolsa)
							for i in range(7):
								if(estado_fichas["ficha_jugador_{}".format(i)]):
									window["ficha_jugador_{}".format(i)].Update(text=l, image_filename=letras[l])
									estado_fichas["ficha_jugador_{}".format(i)] = False
									break
						cambios_jugador += 1
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
				if(not estado_fichas[event]):
					fichas_seleccionadas.append(window[event].GetText())
				else:
					fichas_seleccionadas.remove(window[event].GetText())
				window["letras_selecc"].Update(value="Letras seleccionadas: {}".format(" ".join(fichas_seleccionadas).upper()))	
				estado_fichas[event] = not estado_fichas[event]

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
	ancho_columnas = (10, 10)
	headings = ("Jugador", "Puntaje")
	layout = [[sg.Table(puntajes, headings, select_mode="browse", col_widths=ancho_columnas, num_rows=10, auto_size_columns=False)]]
	window = sg.Window("TOP 10", layout, resizable=True, finalize=True).Finalize()
	while True:
		event, _values = window.read()
		if event is None:
			break


def mostrar_opc(letras):
	'''Esta funcion muestra al usuario las opciones avanzadas por defecto y permite la edicion del mismo'''
	
	def FileNameJugadores():
		return ('jugadores.json')
	
	
	def intefaz():
	
		cant_letras = len(letras)
		#Preparo la sublista
		lista = sorted(letras,reverse = False)
		lista.remove('?')
		mitad = int(len(lista)/2)
		primera = lista[:mitad] 
		segunda = lista[mitad:]


		colum_arriba = [[sg.Text("       cantidad  puntaje     ".upper()*2)]]
		colum_izq = [ [sg.Text(letra.upper()+':',key=letra,size=(2,1)),sg.InputText(default_text=15,size=(8,3),key=('cant'+letra)),sg.InputText(default_text=1,size=(8,3),key=('punt'+letra))]for letra in primera]
		col_der = [ [sg.Text(letra.upper()+':',key=letra,size=(2,1)),sg.InputText(default_text=15,size=(8,3),key=('cant'+letra)),sg.InputText(default_text=1,size=(8,3),key=('punt'+letra))]for letra in segunda]
		col_abajo = [ [sg.Button('Guardar', button_color=('black', '#D9B382')),sg.Button('Restablecer Valores de Fabrica',key='reset',pad=(24,0), button_color=('black', '#D9B382')),sg.Button('Atras', button_color=('black', '#D9B382'))]]
		
		layout = [[sg.Column(colum_arriba)],
				[sg.Column(colum_izq),sg.Column(col_der)],
				[sg.Column(col_abajo)]]
	
		return layout

	def guardar_json(datos):
		if(isfile(FileNameJugadores())): # se podria usar un try except
			with open(FileNameJugadores()) as arc:
				dic = json.load(arc)
		else:
			dic = {}
		for key,dato in datos:
			#Dato en la primer instacia tiene el valor de cantidad 
			#Dato en la segunda instancia tiene el valor de puntaje
			letra =str(key[4])
			if not(letra in dic.keys()):
				dic[letra] = {}
			if key.startswith('c'):
				#Guardo el valor de cant
				cant = dato
			else: 
				dic[letra]= {"cantidad ":int(cant),"puntaje ":int(dato)}

		
		with open(FileNameJugadores(),'w') as arc:
			json.dump(dic,arc,indent = 4)
		sg.popup_ok('Se guardo correctamente los datos en ',FileNameJugadores(),title='Aviso', button_color=('black', '#D9B382'))



	layout =intefaz()

	window=sg.Window('Opciones avanzadas ',layout)


	while True:
		
		event,values=window.read()

		
		if event is 'Guardar':
			guardar_json(values.items())	
		
		if event is 'reset':
			'''Se resetea por defecto los valores del tablero y el json'''
			if sg.PopupOKCancel('Seguro que quieres restablecer los  valores de fabrica',title='Aviso', button_color=('black', '#D9B382')) is'OK':
				for  key,valor in  values.items():
					if key.startswith('c'):
						window[key].update(15)
						values[key] = 15
					else :
						window[key].update(1)
						values[key] = 1
				guardar_json(values.items())
			
		
		if event == sg.WIN_CLOSED or event is 'Atras':
			break
	window.close()


def popup_top10_vacio():
	'''Esta funcion muestra una imagen
	en caso de que el top 10 este vacio
	'''	
	#sg.Popup("No hay puntajes registrados.", title=":(")
	sg.popup_animated(image_source="img/vacioves.png", message="Esta vacio, ves? No hay puntajes aqui.", no_titlebar=False, title=":(") # cambiar despues jeje


# comienzo de "main"

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
		[sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), default_value="Facil", key="niveles")],
		[sg.Text("Tiempo de juego:"), sg.Combo(values=(20, 40, 60), default_value=20, key="tiempo")],
		[sg.Button("TOP 10", button_color=('black', '#D9B382')), sg.Button("OPCIONES AVANZADAS", button_color=('black', '#D9B382'))],
		
		[sg.Button('CONTINUAR PARTIDA',button_color=('black', '#D9B382'),pad=((45, 0),(30, 0)))],
		[sg.Button('INICIAR',button_color=('black', '#D9B382'),pad=((80, 0),(30, 0)))]]


window = sg.Window("ScrabbleAR", layout, size=(250, 250)).Finalize()

while True:
	event, values = window.Read()

	if event is None:
		break

	if event is "INICIAR":
		window.Close()
		#aca hay que hacer if,para preguntar que nivel es y asi mostrar el tablero correspondiente a cada nivel
		generar_ventana_de_juego(values["tiempo"])

	if event is "CONTINUAR PARTIDA": #Se debe  poder seguir la partida que fue pospuesta anteriormente.
		pass

	if event is "TOP 10":
		if(os.path.isfile("puntajes.json")):
			with open("puntajes.json") as arc:
				datos = load(arc)
				if not datos:
					popup_top10_vacio()
				else:
					puntajes = sorted(datos.items(), reverse=True, key=lambda x:x[1])
					mostrar_top10(puntajes)

		else:
			popup_top10_vacio()

	if event is "OPCIONES AVANZADAS":
		mostrar_opc(letras.keys())
		


window.Close()