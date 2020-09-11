# versión 0.2.1
import colorama # https://pypi.python.org/pypi/colorama/0.3.3

colorama.init(autoreset=True)

# COLORES CONSTANTES
ROJO=0
VERDE=1
AMARILLO=2
AZUL=3

COLOR_FICHAS = [
    colorama.Back.BLACK + colorama.Fore.RED + colorama.Style.NORMAL,
    colorama.Back.BLACK + colorama.Fore.GREEN + colorama.Style.NORMAL,
    colorama.Back.BLACK + colorama.Fore.YELLOW + colorama.Style.NORMAL,
    colorama.Back.BLACK + colorama.Fore.BLUE + colorama.Style.NORMAL
    ]

ESTILO_NORMAL1 = colorama.Back.BLACK + colorama.Fore.WHITE + colorama.Style.DIM
ESTILO_NORMAL2 = colorama.Back.BLACK + colorama.Fore.WHITE + colorama.Style.BRIGHT
ESTILO_ESPECIAL = colorama.Back.LIGHTWHITE_EX + colorama.Fore.BLACK + colorama.Style.BRIGHT
ESTILO_COLORES = [
     colorama.Back.LIGHTRED_EX + colorama.Fore.BLACK + colorama.Style.DIM,
     colorama.Back.LIGHTGREEN_EX + colorama.Fore.BLACK + colorama.Style.DIM,
     colorama.Back.LIGHTYELLOW_EX + colorama.Fore.BLACK + colorama.Style.DIM,
     colorama.Back.LIGHTBLUE_EX + colorama.Fore.BLACK + colorama.Style.DIM
    ]
ESTILO_FINALES = colorama.Back.BLACK + colorama.Fore.BLACK + colorama.Style.NORMAL

SÍMBOLOS = "ABCD"

# Estos valores no representan índices sino posiciones de juego.
TOTAL_CASILLAS = 96
ÚLTIMA_CASILLA_COMÚN = 68

CASILLAS_INICIALES = [5, 22, 39, 56]
CASILLAS_FINALES = [75, 82, 89, 96]
CASILLAS_ESPECIALES = [12, 17, 29, 34, 46, 51, 63, 68]
# definir el valor en la inicialización del módulo

CASILLA_CASA = 0

TAMAÑO_CASILLA = 2


def _crea_lista_casillas(fichas):
    '''
    Crea una estructura lineal para representar el juego. Cada casilla se
    numera, se colorea con gris las casillas especiales (donde no se puede comer
    una ficha ajena), se colorea las casillas de inicio de cada color y se
    colorea las casillas del tramo final de cada ficha.

    Entrada - list
        Fichas es una matriz que representa las posiciones de las fichas. Es una
        matriz de n (1-4) filas y 4 columnas. Todos los valores de la matriz son
        numéricos y deben corresponder a posiciones válidas.

    Salida: list
        Estructura lineal con las casillas coloreadas y las fichas colocadas en su
        posición.
'''

    #lista. añade un elemento que se ignorará
    lista_casillas = ['parchís']            #Inicialización

    # establece números y colores a las casillas de la estructura lineal del tablero
    for casilla in range(1, TOTAL_CASILLAS + 1):                                                #Se va recorreidno casilla por casilla hasta llegar al tamaño
        if casilla in CASILLAS_INICIALES:                                                       #Se consulta si pertenecen a alguna casilla especial por medio de constantes
            lista_casillas.append( ESTILO_COLORES[CASILLAS_INICIALES.index(casilla)]
                                   + str(casilla).zfill(2) )                                    #zfill() agrega 0 a todos al principio antes de los caracteres por parametro
        elif casilla in CASILLAS_ESPECIALES:
            lista_casillas.append( ESTILO_ESPECIAL + str(casilla).zfill(2) )            
        elif casilla < ÚLTIMA_CASILLA_COMÚN:
            if casilla % 2 == 0: 
                lista_casillas.append( ESTILO_NORMAL1 + str(casilla).zfill(2) )
            else:
                lista_casillas.append( ESTILO_NORMAL2 + str(casilla).zfill(2) )
        elif casilla in CASILLAS_FINALES:
            lista_casillas.append( ESTILO_COLORES[CASILLAS_FINALES.index(casilla)]
                                   + ' ' * TAMAÑO_CASILLA )
        else: #tramo final
            lista_casillas.append( ESTILO_FINALES + (' ' * TAMAÑO_CASILLA) )

    # acomoda fichas en la lista_casillas
    num_jugadores = len(fichas)
    for color_jugador in range(num_jugadores):
        _agrega_fichas(lista_casillas, color_jugador, fichas)

    ## Debug
    #print("lista_casillas:", len(lista_casillas))

    return lista_casillas


def _agrega_fichas(lista_casillas, color_jugador, fichas):
    '''
    Coloca las fichas del *color_jugador* en la posición correspondiente dentro
    de la estructura lineal de `lista_casillas`.
'''
    # índice del SÍMBOLO de ficha que se está agregando
    actual = 0

    for posición_ficha in fichas[color_jugador]:                                #El color ROJO es la primera iteración
        if posición_ficha == CASILLAS_FINALES[color_jugador]:                   #Si es igual a las fichas finales
            # En otro lugar se mostrará
            pass

        elif posición_ficha != CASILLA_CASA:
            #ficha2 es la derecha.
            valor_ficha2 = lista_casillas[posición_ficha][-1]                          #Asigna en la fila posicion_dicha y en la columna su ultima posición
            if valor_ficha2.isnumeric() or valor_ficha2.isspace():                     #Si la casilla esta vacia
                # [-2:] porque colorama le agrega unicode al incio de la hilera.
                estilo_casilla = lista_casillas[posición_ficha][:-2]                    #los ultimos dos caracteres para atras
                lista_casillas[posición_ficha] = (estilo_casilla
                                           + valor_ficha2
                                           + COLOR_FICHAS[color_jugador]
                                           + SÍMBOLOS[actual])
            else:                                                                      #Significa que hay otra ficha en esta posición
                # Estilo y valor de ficha derecha
                largo_estilo_valor = len(COLOR_FICHAS[0]) + 1                          #Se le asigna el largo del valor y estilo de la segunda ficha 
                ficha2 = lista_casillas[posición_ficha][-largo_estilo_valor:]
                lista_casillas[posición_ficha] = (ficha2
                                           + COLOR_FICHAS[color_jugador]
                                           + SÍMBOLOS[actual])
        actual = actual + 1


def crea_tablero(fichas, imprime=True):
    '''
    Crea una matriz (tablero) para mostrar en la terminal una representación visual del
    tablero de juego de parchís. En la matriz se insertan en la posición
    correspondiente, las fichas a partir del argumento recibido.

    Entrada:
        fichas - list
        Fichas es una matriz que representa las posiciones de las fichas. Es una
        matriz de n (1-4) filas y 4 columnas. Todos los valores de la matriz son
        numéricos y deben corresponder a posiciones válidas.

        imprime - boolean
        En caso de verdadero se imprime el tablero al finalizar la creación.

    Salida - list
        Una matriz de *filas_tablero* x *columnas_tablero*
'''
    lista_casillas = _crea_lista_casillas(fichas)

    #constantesta para crear la visualización del tablero
    índice_filas_mínimas = 18
    índice_columnas_mínimas = 18
    filas_marco = 2 # filas en marco superior e inferior
    columnas_marco = 7 # columnas en marco vertical izquierdo y derecho
    filas_tablero = índice_filas_mínimas + (filas_marco * 2)
    columnas_tablero = índice_columnas_mínimas + (columnas_marco * 2)
    largo_segmento_lineal = 8 #lo que mide cada segmento lineal 

    tablero = _crea_matriz(filas_tablero, columnas_tablero)


    #índice de incio de la lista de posiciones.
    posición = 1

    '''
        Para la visualización se establecen los siguientes segmentos:

            +-C-+
            |   |
            D   B
            |   |
        --E--   --A--
        F           L
        --G--   --K--
            |   |
            H   J
            |   |
            +-I-+

        Cada segmento es recorrido para añadir las fichas y casillas en el tablero.
    '''

    #segmento A
    #debería ser + 1 pero para pasarlo a índice no se suma
    fila = filas_marco + largo_segmento_lineal                      #Esto es por el manejo de indices, debido a que empiezan desde cero
    #debería ser + 3 pero para pasarlo a índice es + 2
    columna = columnas_marco + (2 * largo_segmento_lineal) + 2      #Se ubica al final del segmento A
    for casilla in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]           
        posición = posición + 1
        columna = columna - 1

    #segmento B
    fila = fila - 1
    #columna ya se decrementó anteriormente.
    for casilla in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]
        posición = posición + 1
        fila = fila - 1

    #segmento C
    fila = fila + 1 # anteriormente se había decrementado 1 vez de más
    columna = columna - 1
    tablero[fila][columna] = lista_casillas[posición]
    posición = posición + 1

    #segmento D
    # la variable ya tiene el índice correcto.
    columna = columna - 1
    for casilla in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]
        posición = posición + 1
        fila = fila + 1

    #segmento E
    columna = columna - 1
    for casilla in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]
        posición = posición + 1
        columna = columna - 1

    #segmento F
    fila = fila + 1
    columna = columna + 1 # anteriormente se había decrementado 1 vez más
    tablero[fila][columna] = lista_casillas[posición]
    posición = posición + 1

    #segmento G
    fila = fila + 1
    # Inicia en la misma columna de segmento F
    for casilla in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]
        posición = posición + 1
        columna = columna + 1

    #segmento H
    fila = fila + 1
    # ya en el anterior segmento se incrementó la columna
    for casilla in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]
        posición = posición + 1
        fila = fila + 1

    #segmento I
    fila = fila - 1 # anteriormente se incrementó de más.
    columna = columna + 1
    tablero[fila][columna] = lista_casillas[posición]
    posición = posición + 1

    #segmento J
    # misma fila del segmento I
    columna = columna + 1
    for casillas in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]
        posición = posición + 1
        fila = fila - 1

    #segmento K
    # fila ya se decrementó anteriormente
    columna = columna + 1
    for casillas in range(largo_segmento_lineal):
        tablero[fila][columna] = lista_casillas[posición]
        posición = posición + 1
        columna = columna + 1

    #segmento L
    fila = fila - 1
    columna = columna - 1 # anteriormente se incrementó de más.
    tablero[fila][columna] = lista_casillas[posición]
    posición = posición + 1


    #Caminos especiales
    # Segmento M
    columna = columna - 1
    for desplazamiento in range(largo_segmento_lineal - 1):
        tablero[fila][columna] = lista_casillas[posición]
        columna = columna - 1
        posición = posición + 1

    # Segmento N
    columna = columna - 1
    fila = fila - largo_segmento_lineal
    for desplazamiento in range(largo_segmento_lineal - 1):
        tablero[fila][columna] = lista_casillas[posición]
        fila = fila + 1
        posición = posición + 1

    # Segmento O
    columna = columna - largo_segmento_lineal
    fila = fila + 1
    for desplazamiento in range(largo_segmento_lineal - 1):
        tablero[fila][columna] = lista_casillas[posición]
        columna = columna + 1
        posición = posición + 1

    # Segmento P
    columna = columna + 1
    fila = fila + largo_segmento_lineal
    for desplazamiento in range(largo_segmento_lineal - 1):
        tablero[fila][columna] = lista_casillas[posición]
        fila = fila - 1
        posición = posición + 1

    ##Casas de las fichas
    _dibuja_casa(tablero, fichas, filas_marco, columnas_marco)

    if imprime:
        imprime_tablero(tablero)

    return tablero


def _dibuja_casa(tablero, fichas, filas_marco, columnas_marco):

    etiquetas = [
        [ [1, 13, "CA"], [1, 14, "SA"], [4, 13, "ME"], [4, 14, "TA"] ],     # ROJO
        [ [1, 1, "CA"], [1, 2, "SA"], [4, 1, "ME"], [4, 2, "TA"] ],         # VERDE
        [ [13, 1, "CA"], [13, 2, "SA"], [16, 1, "ME"], [16, 2, "TA"] ],     # AMARILLO
        [ [13, 13, "CA"], [13, 14, "SA"], [16, 13, "ME"], [16, 14, "TA"] ]  # AZUL
    ]

    #Posiciones para espacios de fichas en casa

    casas = [
        [ [2, 13], [2, 14], [2, 15], [2, 16] ],     # ROJO
        [ [2, 1], [2, 2], [2, 3], [2, 4] ],         # VERDE
        [ [14, 1], [14, 2], [14, 3], [14, 4] ],     # AMARILLO
        [ [14, 13], [14, 14], [14, 15], [14, 16] ]  # AZUL
    ]
    #Posiciones para espacios de fichas en metas
    metas = [
        [ [5, 13], [5, 14], [5, 15], [5, 16] ],     # ROJO
        [ [5, 1], [5, 2], [5, 3], [5, 4] ],         # VERDE
        [ [17, 1], [17, 2], [17, 3], [17, 4] ],     # AMARILLO
        [ [17, 13], [17, 14], [17, 15], [17, 16] ]  # AZUL
    ]

    num_jugadores = len(fichas)
    for color in range(num_jugadores):

        for fil, col, val in etiquetas[color]:
            tablero[fil + filas_marco][col + columnas_marco] = COLOR_FICHAS[color] + val

        casas_color = casas[color]                  #Asigna a constantes de colores del jugador actual
        metas_color = metas[color]
        fichas_color = fichas[color]
        índice = 0  # índice para símbolo actual y para ficha actual

        while índice < len(fichas_color):           #Recorre todas las fichas del jugador
            ficha = fichas_color[índice]
            if ficha == CASILLA_CASA:               #Si la ficha esta en la casa 
                fil = casas_color[índice][0] + filas_marco
                col = casas_color[índice][1] + columnas_marco           #Se asignan columnas respectivas para casa con respecto al simbolo de la ficha actual          
                tablero[fil][col] = COLOR_FICHAS[color] + ' ' + SÍMBOLOS[índice]
            elif ficha == CASILLAS_FINALES[color]:                          
                fil = metas_color[índice][0] + filas_marco              #Se asignan columnas respectivas para metas con respecto al simbolo de la ficha actual    
                col = metas_color[índice][1] + columnas_marco
                tablero[fil][col] = COLOR_FICHAS[color] + ' ' + SÍMBOLOS[índice]
            índice = índice + 1                               


def _crea_matriz(índice_filas, índice_columnas):
    '''
    Crea una matriz de tamaño índice_filas + 1 x índice_columnas + 1.

    Cada elemento de la matriz es una cadena con dos espacios vacíos. Esta
    cadena permitirá que los elementos que se usen como casillas del tablero
    puedan representar dos fichas en la misma posición.
    '''
    #while
    matriz = []
    i=0
    while i <= índice_filas:                        #Se crea la matriz vacia
        fila = []
        j=0
        while j <= índice_columnas:
            fila = fila + [' ' * TAMAÑO_CASILLA]     #Se crean las casillas con el tamaño necesario
            j = j+1

        matriz = matriz + [fila]
        i= i+1
    return matriz


##Imprime matriz

def imprime_tablero(matriz):
    for fila in matriz:                         #Imprime la matriz
        for elemento in fila:
            print(elemento, end='')
        print('')
    print('')



