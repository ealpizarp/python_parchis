# versión 0.2.1
import os

import tablero
import colorama

colorama.init(autoreset=True)

# TODO: hacer la consola en pantalla completa. #mejora
def pantalla_inicio():
    '''
    Da la bienvenida al juego y solicita que se presione enter.
'''    

    # AsciiArt generado en http://www.patorjk.com/software/taag/
    bienvenida = """


  ____    _                                         _       _                    _
 |  _ \  (_)                                       (_)     | |                  | |
 | |_) |  _    ___   _ __   __   __   ___   _ __    _    __| |   ___      __ _  | |
 |  _ <  | |  / _ \ | '_ \  \ \ / /  / _ \ | '_ \  | |  / _` |  / _ \    / _` | | |
 | |_) | | | |  __/ | | | |  \ V /  |  __/ | | | | | | | (_| | |  __/   | (_| | | |
 |____/  |_|  \___| |_| |_|   \_/    \___| |_| |_| |_|  \__,_|  \___|    \__,_| |_|


              _____                          _       __
             |  __ \                        | |     /_/
             | |__) |   __ _   _ __    ___  | |__    _   ___
             |  ___/   / _` | | '__|  / __| | '_ \  | | / __|
             | |      | (_| | | |    | (__  | | | | | | \__ \\
             |_|       \__,_| |_|     \___| |_| |_| |_| |___/

    """

    # Limpia la pantalla
    os.system("clear")
    print("\n\n")

    for color in tablero.COLOR_FICHAS:
        print(color + "".center(20, '*'), end=" ")
    print("\n\n")

    print(bienvenida)
    print("\n\n")

    for color in tablero.COLOR_FICHAS:
        print(color + "".center(20, '*'), end=" ")
    print("\n\n")

    print("Para una mejor visualización utilice pantalla completa".center(80))
    print("\n\n")
    input("presione ENTER para continuar".center(80))


def solicita_numero_jugadores():
    '''
    Solicita el número de les jugadores para el juego

    Salida: int
        Número de jugadores entre 1 y 4.
'''
    continuar = False
    os.system("clear")

    while continuar == False:
        print("\n\nDigite la cantidad de les jugadores para iniciar partida")
        jugadores = input("-> ")
        try:
            jugadores = int(jugadores)

            if jugadores <= 4 and jugadores >= 1:
                continuar = True
            else:
                print("No digitó un número de jugadores válido. ")

        except ValueError:
            print("No digitó un número de jugadores válido. ")
    else:
        return jugadores


def solicita_nombre_jugadores(num_jugadores):
    '''
    Solicita *num_jugadores* nombres y los retonar en una lista de cadenas.

    Entrada:
        num_jugadores - int: cantidad de nombres a solicitar.

    Salida: list
        Una lista de cadenas donde cada elemento es el nombre de jugadore

'''
    nombre_jugadores = []

    for jugador in range(num_jugadores):
        nombre = input(tablero.COLOR_FICHAS[jugador]
                       + "\nIngrese el nombre para jugadore #"
                       + str(jugador + 1) + ": ")
        nombre_jugadores.append(nombre)

    return nombre_jugadores


def solicita_movimiento_dado():
    '''
    Solicita cuál dado desea usar para mover la ficha

    Salida: int
        dado1 - 0
        dado2 - 1
        ambos - 2
'''
    continuar = False
    while continuar == False:
        print("\nCon qué dado desea mover la ficha: 1, 2 o 3 (para ambos)")
        entrada = input("-> ")
        try:
            dado = int(entrada)

            if dado >= 1 and dado <= 3:
                dado = dado -1  #rango 0-2
                continuar = True
            else:
                #os.system("clear")
                print("No digitó un número de dado válido.")

        except ValueError:
            #os.system("clear")
            print("No digitó un número de dado válido.")
    else:
        return dado


def solicita_movimiento_ficha():
    '''
    Solicita cuál ficha desea mover.

    return int
        ficha A=0, B=1, C=2, D=3
'''
    continuar = False
    while continuar == False:
        print("\nQué ficha desea mover: A, B, C o D")
        entrada = input("-> ").upper()
        if len(entrada) == 1 and entrada in tablero.SÍMBOLOS:
            return tablero.SÍMBOLOS.index(entrada)
        else:
            print("No digitó una ficha válido.")

#pantalla_inicio()

#solicita_movimiento_dado()