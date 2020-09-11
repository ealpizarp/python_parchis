import cli
import tablero
import random
import os

ULTIMA_CASILLA_COMUN_ESPECIALES = [17, 34, 51]

FICHAS_ROJAS_EN_META = [75, 75, 75, 75]
FICHAS_VERDES_EN_META = [82, 82, 82, 82]
FICHAS_AMARILLAS_EN_META = [89, 89, 89, 89]
FICHAS_AZULES_EN_META = [96, 96, 96, 96]

TRAMOS_FINALES_ESPECIALES = [[76, 77, 78, 79, 80, 81], [83, 84, 85, 86, 87, 88], [90, 91, 92, 93, 94, 95]]

#Aquí se declaran las constantes que se van a utilizar en la implementación

vuelta_casilla_comun = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def crear_matriz_fichas(jugadores):
    matriz = []

    for num_jugadores in range(jugadores):
        matriz.append([0,0,0,0])

    return matriz


def gestionar_movimiento(jugador,dados, nombre_jugadores, barreras, fichas):
    

    '''
    Función que se encarga de interactuar con la usuaria y  manejar todas 
    las validaciones necesarias para realizar un movimiento en el tablero. 
    Estas validaciones se hacen con las posiciones de las fichas en el tablero.

    Entradas:

    int - posicion del jugador en la matriz de fichas

    list - conjunto de los dados que se obtubieron 

    list - nombre de los jugadores que participan en el juego 

    list - lista de barreras generadas por los movimientos de los jugadores

    list/matrix - La matriz de fichas de todos los jugadores


    Salida: list

       Una matriz de fichas con la nueva posición de los movimientos que pueda hacer el jugador

    '''

    casilla_inicial = tablero.CASILLAS_INICIALES[jugador]

    print(tablero.COLOR_FICHAS[jugador] + 'Ahora es turno del jugador: ' + nombre_jugadores[jugador])
    fichas_tablero = fichas_en_tablero(jugador, fichas)                                  #Se tiran los dados y se sacan que fichas tiene el jugador en el tablero

    print('El resultado de sus dados fue:', dados)

    if(fichas_en_casa(fichas, jugador) and dados_en_cinco(dados) and validacion_barreras(barreras, jugador, casilla_inicial, casilla_inicial)): #Si tiene fichas en casa y algun dado en 5 entonces el jugador puede sacar esa ficha

        if(solicita_sacar_ficha_casa()):

            fichas[jugador][posicion_ficha(fichas, jugador, 0)] = casilla_inicial                          #Se saca una ficha que este en casa a su casilla inicial

            estado = True

            while (estado == True):

                if (dados[2] != 5 and fichas_en_tablero(jugador, fichas) > 1):

                    print('A que ficha le desea agregarle +', dado_alterno_a(dados, 5))

                    ficha_seleccionada = cli.solicita_movimiento_ficha()
                    
                    nueva_posicion = fichas[jugador][ficha_seleccionada]

                    if not posicion_en_casa(nueva_posicion) and not posicion_en_meta(nueva_posicion):    #Si la ficha seleccionada no esta en casa entoces se le suma el valor de los dados

                        nueva_posicion = valida_posición(jugador,ficha_seleccionada, nueva_posicion + dado_alterno_a(dados, 5))             #Se valida la posición debido a los casos especiales

                        if not validacion_barreras(barreras,jugador, nueva_posicion - dado_alterno_a(dados, 5), nueva_posicion):
                            print('No se puede mover la ficha, hay una barrera')
                            input()
                            if (pasar_jugada()):

                                return fichas
                        else:

                            if(verificar_comida(fichas, jugador, nueva_posicion) and nueva_posicion not in tablero.CASILLAS_ESPECIALES and nueva_posicion not in tablero.CASILLAS_INICIALES):  #Se verifica si la nueva posicion se come a una ficha

                                    fichas = comer_ficha(fichas, jugador, ficha_seleccionada, barreras, nueva_posicion)

                                    return fichas
                            else:

                                fichas[jugador][ficha_seleccionada] = nueva_posicion

                                fichas = bonus_meta(fichas, jugador, barreras, nueva_posicion)
                                
                                estado = False

                    else:
                        print('No se puede realizar este movimiento')
                        input()
                
                else:
                    print('No tiene más movimientos disponibles')
                    input()

                return fichas
    
    fichas_tablero = fichas_en_tablero(jugador, fichas)

    if fichas_tablero == 0:                                                                                     #Si no se encuentran fichas en el tablero, no hay movimientos disponibles
        print('No tienes movimientos disponibles')
        input()
        return fichas
    
    else:
        estado = True
        dado_seleccionado = cli.solicita_movimiento_dado()                                                       #Si existen fichas  del jugador en el tablero el usuario selecciona un dado                                            
        while (estado == True):

            ficha_seleccionada = cli.solicita_movimiento_ficha()

            nueva_posicion = fichas[jugador][ficha_seleccionada]

            if not posicion_en_casa(nueva_posicion) and not posicion_en_meta(nueva_posicion):                     #Si la ficha seleccionada no esta en casa entoces se le suma el valor de los dados

                nueva_posicion = valida_posición(jugador,ficha_seleccionada, nueva_posicion + dados[dado_seleccionado])

                if not validacion_barreras(barreras,jugador, nueva_posicion - dados[dado_seleccionado], nueva_posicion):
                    print('No se puede mover la ficha, hay una barrera')
                    input()
                    if(pasar_jugada()):
                        return fichas
                else:
                    if (dado_seleccionado == 2):                                                                   #En caso de que el dado seleccionado sea el acumulado

                        if(verificar_comida(fichas, jugador, nueva_posicion) and nueva_posicion not in tablero.CASILLAS_ESPECIALES and nueva_posicion not in tablero.CASILLAS_INICIALES):
                            
                            fichas = comer_ficha(fichas, jugador, ficha_seleccionada, barreras, nueva_posicion)
        
                            return fichas

                        fichas[jugador][ficha_seleccionada] = nueva_posicion

                        fichas = bonus_meta(fichas, jugador, barreras, nueva_posicion)

                        return fichas
                
                    if verificar_comida(fichas, jugador, nueva_posicion) and nueva_posicion not in tablero.CASILLAS_ESPECIALES and nueva_posicion not in tablero.CASILLAS_INICIALES:

                        fichas = comer_ficha(fichas,jugador, ficha_seleccionada, barreras, nueva_posicion)

                        estado = False

                    else:

                        fichas[jugador][ficha_seleccionada] = nueva_posicion

                        fichas = bonus_meta(fichas, jugador, barreras, nueva_posicion)

                        estado = False

        fichas_tablero = fichas_en_tablero(jugador, fichas) 
        
        if (fichas_tablero < 2):
            print('No hay más movimientos disponibles')
            input()
            return fichas
        
        estado = True
        while (estado == True and fichas_tablero >= 2):                                             #Si existen dos o mas fichas del jugador en el tablero se pregunta a cual se le agrega

            if dado_seleccionado == 0:
                print('Seleccione a que ficha le desea agregar +', dados[1] )
                dado_seleccionado = 1
            elif dado_seleccionado == 1:
                print('Seleccione a que ficha le desea agregar +', dados[0] )
                dado_seleccionado = 0
            
            ficha_seleccionada = cli.solicita_movimiento_ficha()

            nueva_posicion = fichas[jugador][ficha_seleccionada]

            if not validacion_barreras(barreras, jugador,nueva_posicion, nueva_posicion + dados[dado_seleccionado]) and not posicion_en_casa(nueva_posicion):
                print('No se puede mover la ficha, hay una barrera')
                input()
                if (pasar_jugada()):
                    return fichas
            else:

                if not posicion_en_casa(nueva_posicion) and not posicion_en_meta(nueva_posicion):

                    nueva_posicion = valida_posición(jugador, ficha_seleccionada, nueva_posicion + dados[dado_seleccionado])

                    if verificar_comida(fichas, jugador, nueva_posicion) and nueva_posicion not in tablero.CASILLAS_ESPECIALES and nueva_posicion not in tablero.CASILLAS_INICIALES:

                        fichas = comer_ficha(fichas, jugador, ficha_seleccionada, barreras, nueva_posicion)

                        return fichas

                    else:
                        
                        fichas[jugador][ficha_seleccionada] = nueva_posicion

                        fichas = bonus_meta(fichas, jugador, barreras, nueva_posicion)

                        estado = False
                else:
                    print('No se puede realizar este movimiento')
                    input()

            fichas_tablero = fichas_en_tablero(jugador, fichas) 

        return fichas



def validacion_barreras(barreras, jugador, posicion_inicial, posicion_final):

    if posicion_inicial > posicion_final and jugador != 0:
        posicion_inicial = 0
        posicion_final = posicion_final - ULTIMA_CASILLA_COMUN_ESPECIALES[jugador -1]

    posicion_inicial = posicion_inicial + 1

    if (posicion_final in barreras):
        return False
    
    while posicion_inicial < posicion_final:

        if posicion_inicial in barreras:
            return False

        posicion_inicial = posicion_inicial + 1

    return True




def bonus_meta(fichas, jugador, barreras, posicion):

    if posicion == tablero.CASILLAS_FINALES[jugador]:

        print('Felicidades, llegaste a la meta con una ficha!')

        estado = True

        while estado == True:

            print('A que ficha le desea agregar + 10')

            ficha_seleccionada = cli.solicita_movimiento_ficha()

            nueva_posicion = fichas[jugador][ficha_seleccionada] + 10

            valida_posición(jugador, ficha_seleccionada, nueva_posicion)
    
            if fichas_en_tablero(jugador, fichas) >= 1:

                if not validacion_barreras(barreras,jugador, nueva_posicion - 10, nueva_posicion):

                    print('No se puede mover la ficha, hay una barrera')
                    input()
                    
                    if(pasar_jugada()):
                        return fichas
                else:

                    if (verificar_comida(fichas, jugador, nueva_posicion) and not nueva_posicion in tablero.CASILLAS_ESPECIALES and not nueva_posicion in tablero.CASILLAS_INICIALES):

                        fichas = comer_ficha(fichas, jugador, ficha_seleccionada, barreras, nueva_posicion)

                        return fichas

                    else:

                        fichas[jugador][ficha_seleccionada] = nueva_posicion

                        estado = False
        
            else:
                print('Ohh no, no hay ninguna ficha en el tablero, para aplicar el bonus')
                estado = False
                input()

        return fichas

    return fichas




def comer_ficha(fichas, jugador, ficha_seleccionada, barreras, posicion):

    estado = True

    while (estado == True):

        ficha_comida = buscar_ficha(posicion)

        nueva_posicion = valida_posición(jugador, ficha_seleccionada, posicion)

        print('Te has comido la ficha de', nombre_jugadores[ficha_comida[0]],'!')

        fichas[ficha_comida[0]][ficha_comida[1]] = tablero.CASILLA_CASA


        if validacion_barreras(barreras, jugador, nueva_posicion, nueva_posicion + 20):
            print('Te ganaste avanzar + 20 casillas con esta ficha!')  
            input()
            nueva_posicion = nueva_posicion + 20

            nueva_posicion = valida_posición(jugador, ficha_seleccionada, nueva_posicion)

            fichas[jugador][ficha_seleccionada] = nueva_posicion

            fichas = bonus_meta(fichas, jugador, barreras, nueva_posicion)

            if not verificar_comida(fichas, jugador, nueva_posicion) or nueva_posicion in tablero.CASILLAS_INICIALES or nueva_posicion in tablero.CASILLAS_ESPECIALES:

                return fichas

        else:
            print('No se le puede agregar a la ficha + 20, hay barrera en camino')            
            input()
            nueva_posicion = posicion
            fichas[jugador][ficha_seleccionada] = nueva_posicion
            return fichas



def buscar_ficha(posicion):
    resultado = []
    for fila in range(len(fichas)):
        for columna in range(len(fichas[0])):
            if(posicion == fichas[fila][columna]):
                resultado.append(fila)
                resultado.append(columna)
    return resultado



def dado_alterno_a(dados, numero_dado):
    if(dados[0] == numero_dado):
        return dados[1]
    elif(dados[1] == numero_dado):
        return dados[0]



def pasar_jugada():
    print("Desea terminar esta jugada?")
    continuar = False
    while continuar == False:
        print('Si                     opc 1')
        print('No                     opc 2')
        entrada = input("-> ")
        try:
            opc = int(entrada)

            if opc == 1:
                return True
            elif opc == 2:
                return False
        except ValueError:
            print("No digitó un número de dado válido.")



def tirar_dados():
    dados = []
    for dado in range(2):
        dados.append(random.randint(1,6))
    dados.append(dados[0] + dados[1])
    return dados




def valida_posición(jugador, ficha_seleccionada, posicion):

    casilla_meta = tablero.CASILLAS_FINALES[jugador]

    if jugador != 0:

        if posicion > tablero.ÚLTIMA_CASILLA_COMÚN and vuelta_casilla_comun[jugador - 1][ficha_seleccionada] == 0:
            posicion = posicion - tablero.ÚLTIMA_CASILLA_COMÚN
            vuelta_casilla_comun[jugador - 1][ficha_seleccionada] = 1
        elif posicion > ULTIMA_CASILLA_COMUN_ESPECIALES[jugador - 1] and vuelta_casilla_comun[jugador - 1][ficha_seleccionada] == 1 and posicion not in TRAMOS_FINALES_ESPECIALES[jugador-1]: 
            posicion = TRAMOS_FINALES_ESPECIALES[jugador-1][0] + (posicion - ULTIMA_CASILLA_COMUN_ESPECIALES[jugador-1] -1)
    
    if posicion >= casilla_meta:

        return casilla_meta

    return posicion



def posicion_ficha(fichas, jugador, posicion):
    return fichas[jugador].index(posicion)

    

def fichas_en_casa(fichas, jugador):
    if 0 in fichas[jugador]:
        return True
    return False



def posicion_en_meta(posicion):
    if posicion in tablero.CASILLAS_FINALES:
        return True
    return False



def posicion_en_casa(posicion):
    if posicion == 0:
        return True
    return False


def barrera_fichas(fichas, posicion):
    contador = 0
    for ficha in range(len(fichas)):
        if fichas[ficha] == posicion:
            contador += 1
        if contador == 2:
            return ficha
    return -1



def verificar_comida(fichas, jugador, posicion):
    for fila in range(len(fichas)):
        for columna in range(len(fichas[0])):
            if(posicion == fichas[fila][columna] and jugador != fila):
                return True
    return False



def definir_barreras(fichas, jugadores):
    lista_fichas = []
    fichas_duplicadas = []
    for set_fichas in range(jugadores):
        lista_fichas.extend(fichas[set_fichas])
    
    for i in range(len(lista_fichas)):
        j = i + 1
        while j < len(lista_fichas):
            if (lista_fichas[i] == lista_fichas[j] and not lista_fichas[i] == tablero.CASILLA_CASA and not lista_fichas[i] in tablero.CASILLAS_FINALES):
                fichas_duplicadas.append(lista_fichas[i])
            j += 1
    return fichas_duplicadas



def solicita_sacar_ficha_casa():
    print("\nDesea sacar ficha en casa?")
    continuar = False
    while continuar == False:
        print('Si                     opc 1')
        print('No                     opc 2')
        entrada = input("-> ")
        try:
            opc = int(entrada)

            if opc == 1:
                return True
            elif opc == 2:
                return False
        except ValueError:
            print("No digitó una opción valida.")



def fichas_en_tablero(jugador, fichas):
    contador = 0
    for ficha in range(len(fichas[jugador])):
        ficha_jugador = fichas[jugador][ficha]
        if(ficha_jugador != 0 and not ficha_jugador in tablero.CASILLAS_FINALES):
            contador +=1
    return contador



def actualiza_vueltas(fichas):
    fila = 1
    while fila < len(fichas):
        columna = 0
        while columna < len(fichas[0]):
            if fichas[fila][columna] == tablero.CASILLA_CASA:
                vuelta_casilla_comun[fila - 1][columna] = 0
            columna = columna + 1
        fila = fila + 1
    
    return vuelta_casilla_comun



def verifica_ganador(fichas, num_jugadores):
    if fichas[0] == FICHAS_ROJAS_EN_META:
        return 0
    elif num_jugadores >= 2:
        if fichas[1] == FICHAS_VERDES_EN_META:
            return 1
    elif num_jugadores >= 3:
        if fichas[2] == FICHAS_AMARILLAS_EN_META:
            return 2
    elif num_jugadores == 4:
        if fichas[3] == FICHAS_AZULES_EN_META:
            return 3
    return -1



def dados_en_cinco(dados):
    for dado in range(len(dados)):
        if(dados[dado] ==  5):
            return True
    return False



def mandar_ficha_casa(jugador, fichas):
    for ficha in range(len(fichas[0])):
        if fichas[jugador][ficha] != tablero.CASILLA_CASA and fichas[jugador][ficha] != tablero.CASILLAS_FINALES[jugador]:
            fichas[jugador][ficha] = tablero.CASILLA_CASA
            return fichas
    return fichas






# ***************************************************************************************************************************************************************


cli.pantalla_inicio()

barreras = []

jugadores = cli.solicita_numero_jugadores()

nombre_jugadores = cli.solicita_nombre_jugadores(jugadores)

fichas = crear_matriz_fichas(jugadores)

tablero.crea_tablero(fichas)
estado = True
while(estado == True):
    i=0
    while i < jugadores:

        if verifica_ganador(fichas, jugadores) != -1:                   #Caso en que se dan los dados repetidos en la primera tirada
            os.system('clear')
            print('Felicidades ' + nombre_jugadores[verifica_ganador(fichas, jugadores)] + ', has ganado la partida!')
            estado = False
            break

        else:
            dados = tirar_dados()
            if dados[0] == dados[1]:
                print(tablero.COLOR_FICHAS[i] + 'Felicidades ' + nombre_jugadores[i] +', has sacado dados dobles, puedes jugar dos veces!')
                input()

                fichas = gestionar_movimiento(i, dados, nombre_jugadores, barreras, fichas)
                os.system('clear')
                tablero.crea_tablero(fichas)
                barreras = definir_barreras(fichas, jugadores)
                vuelta_casilla_comun = actualiza_vueltas(fichas)
                dados_secundarios = tirar_dados()

                print('Este es el segundo movimiento')
                fichas = gestionar_movimiento(i, dados_secundarios, nombre_jugadores, barreras, fichas)
                os.system('clear')
                tablero.crea_tablero(fichas)
                barreras = definir_barreras(fichas, jugadores)
                vuelta_casilla_comun = actualiza_vueltas(fichas)

                if (dados_secundarios[0] == dados_secundarios[1]):                      #Caso en que se dan los dados repetidos en la segunda tirada

                    print(tablero.COLOR_FICHAS[i] + 'Felicidades ' + nombre_jugadores[i] +', has sacado dados dobles dos veces consecutivas!')
                    input()
                    print('Este es el tercer movimiento')
                    dados_terciarios = tirar_dados()

                    if (dados_terciarios[0] == dados_terciarios[1]):                    #Caso en que se dan los dados repetidos en la tercera tirada

                        print('El resultado de sus dados fue', dados)
                        print('Ohh no, has sacado tres veces consecutivas dados repetidos')
                        input()

                        if fichas_en_tablero(i, fichas) >= 1:

                            fichas = mandar_ficha_casa(i, fichas)
                            os.system('clear')
                            tablero.crea_tablero(fichas)
                            barreras = definir_barreras(fichas, jugadores)
                            vuelta_casilla_comun = actualiza_vueltas(fichas)

                        else:
                            print('No tienes fichas en el tablero')
                            input()               
                    else:                                                              

                        fichas = gestionar_movimiento(i, dados_terciarios, nombre_jugadores, barreras, fichas)
                        os.system('clear')
                        tablero.crea_tablero(fichas)
                        barreras = definir_barreras(fichas, jugadores)
                        vuelta_casilla_comun = actualiza_vueltas(fichas)

                i += 1

            else:                                                                         #Caso donde no se dan los dados repetidos 
        
                fichas = gestionar_movimiento(i, dados, nombre_jugadores, barreras, fichas)
                os.system('clear')
                tablero.crea_tablero(fichas)
                barreras = definir_barreras(fichas, jugadores)
                vuelta_casilla_comun = actualiza_vueltas(fichas)
                i+=1