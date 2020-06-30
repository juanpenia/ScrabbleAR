import PySimpleGUI as sg

sg.LOOK_AND_FEEL_TABLE['Fachero'] = {'BACKGROUND': '#191970', # midnight blue (cambiar)
                                        'TEXT': '#D9B382', # BEIGE
                                        'INPUT': '#D9B382',
                                        'TEXT_INPUT': '#191970',
                                        'SCROLL': '#c7e78b',
                                        'BUTTON': ('black', '#D9B382'),
                                        'PROGRESS': ('#01826B', '#D0D0D0'),
                                        'BORDER': 1, 'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0,
                                        }


sg.theme('Fachero')

layout = [[sg.Text("ScrabbleAR", justification="center", font=("Arial Bold", 18))],
    [sg.Text("Nivel:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), key="niveles")],
    [sg.Text("Tiempo de juego:"), sg.Combo(values=(20, 40, 60), key="tiempo")],
    #[sg.Text("Prueba de primera ficha:"), sg.Button(image_filename="C:/Users/juanp/Desktop/scrablear/A2.png", size=(48, 48), key="a")],
    #[sg.Text("Prueba de segunda ficha:"), sg.Button(image_filename="C:/Users/juanp/Desktop/scrablear/F.png")],
    [sg.Button("INICIAR", pad=((150, 0), (170, 0)))]]

window = sg.Window("ScrabbleAR", layout, size=(400, 400))

while True:
    event, values = window.Read()

    if event is None:
        break

    if event is "Iniciar":
        #ComenzarJuego()
        pass

    if event is "a":
        print("aa")