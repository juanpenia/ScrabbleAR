import PySimpleGUI as sg
import os
import json
from random import shuffle, choice
#from pattern.es import verbs, spelling, lexicon 

PATH_TABLERO = 'img/tablero'
PATH_FICHAS = 'img/fichas'

sg.LOOK_AND_FEEL_TABLE['Fachero'] = {'BACKGROUND': '#191970', # midnight blue
										'TEXT': '#D9B382', # BEIGE
										'INPUT': '#D9B382',
										'TEXT_INPUT': '#191970',
										'SCROLL': '#c7e78b',
										#'BUTTON': ('black', '#D9B382'),
										'BUTTON': ('black', '#F5F5F5'),
										'PROGRESS': ('#01826B', '#D0D0D0'),
										'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
									}


sg.theme('Fachero') # tiene que ser cambiado

# no se bo
TUPLA_MARRONES = ((0, 0), (0, 7), (0, 14), (7, 0), (7, 7), (7, 14), (14, 0), (14, 7), (14, 14))
TUPLA_ROJOS = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (1, 13), (2, 12), (3, 11), (4, 10), (5, 9), (9, 5), (10, 4), (11, 3), (12, 2), (13, 1), (13, 13), (12, 12), (11, 11), (10, 10), (9, 9))
TUPLA_AZULES = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13))
TUPLA_VERDES = ((1, 5), (1, 9), (13, 9), (13, 5), (6, 6), (6, 8), (8, 6), (8, 8), (5, 1), (9, 1), (5, 13), (9, 13), (0, 3), (0, 10), (2, 6), (2, 8), (3, 0), (3, 7), (3, 14), (6, 2), (7, 3), (8, 2), (6, 12), (7, 11), (8, 12), (11, 0), (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11))

#letras = {a:"a.png", b: "b.png",c: "c.png", d: "d.png",e: "e.png", f: "f.png",g: "g.png", h: "h.png",i: "i.png", j: "j.png",k: "k.png", l: "l.png",m: "m.png", n: "n.png",o: "o.png", p: "p.png",q: "q.png", r: "r.png",s: "s.png", t: "t.png",u: "u.png", v: "v.png",w: "w.png", x: "x.png",y: "y.png", z: "z.png"}

def ImagenSegunColor(x, y): # cambiar nombre
	# cambiar ruta, obviamente
	if (x, y) in TUPLA_MARRONES:
		return os.path.join(PATH_TABLERO, 'beta_marron.png')
    
	elif (x, y) in TUPLA_ROJOS:
		return os.path.join(PATH_TABLERO, "beta_rojo2.png")


def dibujar_casilla(x, y, dif):

	'''Funcion que se encarga de devolver de que casillero
	se pinta cada casilla del tablero'''
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

	elif (x, y) in TUPLA_VERDES:
		return os.path.join(PATH_TABLERO, "beta_verde.png")

	else:
		return os.path.join(PATH_TABLERO, "fondo.png") # nada


def generar_bolsa():

	'''Funcion encargada de generar la bolsa de 98 fichas.
	'''
	string = ""
	try:
		with open("config.cfg") as config:
			datos = json.load(config)

	except FileNotFoundError:
		# de paso al no existir, genero el archivo
		with open("config.cfg", "w") as config:
			datos = bolsa_por_defecto()
			json.dump(datos, config, indent=4)
	for key, value in datos.items():
		string = string + key*value
	lista = list(string)
	shuffle(lista)
	return lista

def generar_tablero():
	
	Bolsa = GenerarBolsa()

def bolsa_por_defecto():

	'''Funcion que devuelve el estado original pretendido
	de la bolsa en caso de querer restablaecer a su valor
	por defecto.'''
	original = "aaaaaaaaaaabbbccccddddeeeeeeeeeeeffgghhiiiiiijjkllllmmmnnnnnooooooooppqrrrrsssssssttttuuuuuuvvwxyz"
	bolsa = {}
	for char in original:
		if char in bolsa:
			bolsa[char] += 1
		else:
			bolsa.setdefault(char, 1)
	return bolsa


def sacar_letra(bolsa):

	'''Funcion encargada de "sacar" una letra
	random de la bolsa.
	'''
	letra = choice(bolsa)
	bolsa.remove(letra)
	return letra


def dar_fichas_maquina(bolsa):

	'''Funcion encargada de otorgar las 7 fichas random
	utilizando la funcion sacar_letra.
	'''
	return [sacar_letra(bolsa) for x in range(7)]


def cambiar_fichas_maquina(bolsa, fm, cambios):
	bolsa.extend(fm)
	shuffle(bolsa)
	fm = dar_fichas_maquina(bolsa)
	return fm, cambios+1


def generar_tablero(dificultad):

	'''Funcion encargada de generar los 3 tableros con una dimesion de 15x15
	utilizando la funcion casillero_segun_color
	'''
	tablero = []
	for i in range(15):
		matriz.append([])
		for j in range(15):
			tablero[i].append(sg.Button(image_filename=dibujar_casilla(i, j, dificultad), image_size=(32, 32), key=(i, j), pad=(0, 0)))
	return tablero


def generar_ventana_de_juego(tj, dif):

	'''Funcion encargada de iniciar el juego,utilizando los procesos
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

	col_derecha = matriz.copy()

	col_derecha.append([sg.Text()])
	col_derecha.append([sg.Button("test")])

	col_izquierda = [[sg.Listbox([], size=(30, 10), key='lista_puntos')],
					[sg.Text("Fichas restantes: {}".format(len(Bolsa)))],
					[sg.Text("Tiempo restante: 10 años")],
					[sg.Button("Cambiar Fichas")],
					[sg.Button("TERMINAR"), sg.Button("POSPONER")]]

	letras_jugador = [sg.Text(" "*45)]
	for i in range(0, 7):
		letra = sacar_letra(bolsa)
		letras_jugador.append(sg.Button(letra, font="Arial 1", image_filename=letras[letra], button_color=('black', '#191970'), border_width=0, key="ficha_jugador_{}".format(i)))

	window = sg.Window("ScrabbleAR", layout).Finalize()
	window.Maximize()

	while True:

		# el "_" detras de una variable significa que no se usa, es para que no salte warning
		# cuando la usemos, le sacamos el "_"
		event, _values = window.Read()

		if event is None:
			break

		if event is "TERMINAR": # cuando finaliza :   En ese momento se muestran las fichas que posee cada jugador y se recalcula el puntaje restando al mismo el valor de dichas fichas
			exit = sg.PopupOKCancel("¿Esta seguro que desea salir?", title="!")
			if(exit == "OK"):
				break
		
		if event is "POSPONER": # Al elegir esta opción se podrá guardar la partida para continuarla luego. En este caso, se podrá guardar la partida actual teniendo en cuenta la información del tablero y el tiempo restante. Al momento de iniciar el juego, se pedirá si se desea continuar con la partida guardada (si es que hay una) o iniciar una nueva. En cualquier caso siempre habrá una única partida guardada.
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
							letra = sacar_letra(bolsa)
							for i in range(7):
								if(estado_fichas["ficha_jugador_{}".format(i)]):
									window["ficha_jugador_{}".format(i)].Update(text=letra, image_filename=letras[letra])
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
	'''Funcion encargada de visualizar un top 10 con los puntajes obtenidos del tipo: fecha + puntaje + nivel.
	'''
	ancho_columnas = (10, 10)
	headings = ("Jugador", "Nivel", "Puntaje")
	layout = [[sg.Table(puntajes, headings, select_mode="browse", col_widths=ancho_columnas, num_rows=10, auto_size_columns=False)]]
	window = sg.Window("TOP 10", layout, resizable=True, finalize=True).Finalize()
	while True:
		event, _values = window.read()
		if event is None:
			break


def mostrar_opciones(letras):
	'''Esta funcion muestra al usuario las opciones avanzadas por defecto y permite la edicion del mismo'''

	def get_cant_letra(letra):
		try:
			with open("config.cfg") as config:
				datos = json.load(config)
				return datos[letra]

		except FileNotFoundError:
			return bolsa_por_defecto()[letra]

	def intefaz():
		# Preparo la sublista
		lista = sorted(letras, reverse=False)
		lista.remove('?')
		mitad = int(len(lista)/2)
		primera = lista[:mitad]
		segunda = lista[mitad:]

		colum_arriba = [[sg.Text("       CANTIDAD    "*2)]]
		colum_izq = [[sg.Text(letra.upper()+':', key=letra, size=(2, 1)), sg.InputText(default_text=get_cant_letra(letra), size=(8, 3), key=('cant'+letra))] for letra in primera]
		col_der = [[sg.Text(letra.upper()+':', key=letra, size=(2, 1)), sg.InputText(default_text=get_cant_letra(letra), size=(8, 3), key=('cant'+letra))] for letra in segunda]
		col_abajo = [[sg.Button('Guardar', button_color=('black', '#D9B382')), sg.Button('Restablecer', key='reset', pad=(24, 0), button_color=('black', '#D9B382')), sg.Button('Atras', button_color=('black', '#D9B382'))]]

		layout = [[sg.Column(colum_arriba)],
				[sg.Column(colum_izq), sg.Column(col_der)],
				[sg.Column(col_abajo)]]

		return layout

	def guardar_json(datos):
		temp_dic = {}
		for key, _value in datos.items():
			temp_dic[key.replace("cant", "")] = int(datos[key])
		del datos

		with open("config.cfg", "w") as arc:
			json.dump(temp_dic, arc, indent=4)

	window = sg.Window('Opciones avanzadas ', intefaz())

	while True:
		event, values = window.read()

		if event is 'Guardar':
			guardar_json(values)
			window.Close()

		if event is 'reset':
			'''Se resetea por defecto los valores del tablero y el json'''
			if sg.PopupOKCancel('Seguro que quieres restablecer los  valores de fabrica?',
								title='Aviso', button_color=('black', '#D9B382')) is 'OK':
				for key, _valor in values.items():
					valor_nuevo = bolsa_por_defecto()["{}".format(key.replace("cant", ""))]
					window[key].update(valor_nuevo)
					values[key] = valor_nuevo
				guardar_json(values)

		if event == sg.WIN_CLOSED or event is 'Atras':
			break

	window.close()


def popup_top10_vacio():
	'''Funcion encargada de mostrar una imagen
	en caso de que el top 10 este vacio
	'''
	sg.popup_animated(image_source="img/vacioves.png", message="Esta vacio, ves? No hay puntajes aqui.", no_titlebar=False, title=":(")


# comienzo de "main"

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
	[sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), key="niveles")],
	[sg.Text("Tiempo de juego:"), sg.Combo(values=(20, 40, 60), key="tiempo")],
	[sg.Button("INICIAR")]]

window = sg.Window("ScrabbleAR", layout, size=(250, 250)).Finalize()

while True:
	event, values = window.Read()

	if event is None:
		break

	if event is "INICIAR":
		window.Close()
		generar_ventana_de_juego(values["tiempo"], values["nivel"])

	if event is "CONTINUAR PARTIDA": # Se debe poder seguir la partida que fue pospuesta anteriormente.
		pass

	if event is "TOP 10":
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

	if event is "OPCIONES AVANZADAS":
		mostrar_opciones(letras.keys())

window.Close()
