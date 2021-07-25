#! python 3.9.5
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    
    import sys
    import pygame
    import pygame.locals as globales
    import pygame.event as eventos
    import pygame.time as tiempo
    from pygame import mixer
    import random
    import figuras

    ancho, alto = 720, 825

    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    reloj = tiempo.Clock()
    fps = 15

    ventana = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("MiTetris")

    #variables de juego
    tamanoCaja = 40
    casillas = [10, 24]
    siguientePieza = None
    pieza = None

    fin = False
    inicio = True
    jugando = False
    pausa = False
    grabarMarcadores = False
    mostrarMarcadores = False

    abajo = False
    ultimoAbajo = 0
    izquierda = False
    ultimoIzqierda = 0
    derecha = False
    ultimoDerecha = 0
    rotando = False
    ultimoRotando = 0

    piezas = 0
    lineas = 0
    puntos = 0
    nivel = 0

    ciclosPorNivel = 10
    ultimoAumentoNivel = 0
    pasoInicial = 500
    paso = pasoInicial
    tiempoUltimoPaso = 0
    restaPasosPorNivel = 10

    #Variable que asignan la suma de puntos
    puntosPorCaidaRapida = 1
    puntosPorLinea = 100
    puntosPorDobleLinea = 300
    puntosPorTripleLinea = 500
    puntosPorCuatrupleLinea = 800

    #Variable que altera el movimiento de las piezas obteniendo la velicidad a través de la multiplicación de este con Var paso
    factorVelocidad = 0.25

    #Variables para restringir la veloicidad de movimiento y giro
    velMovMax = 100
    velGiroMax = 110

    matriz = []

    for i in range(casillas[1]):
        fila = []
        for j in range(casillas[0]):
            fila.append(0)
        matriz.append(fila)

    sonidos = ['assets/sonidos/Can-Can.wav', 'assets/sonidos/Rondo.wav', 'assets/sonidos/Tetris.wav', 'assets/sonidos/Polkka1.wav',
               'assets/sonidos/Polkka2.wav', 'assets/sonidos/Polkka2.wav']

    sonidosFx = {'nivel' : mixer.Sound('assets/sonidos/nivel.wav'), 'integrar' : mixer.Sound('assets/sonidos/integrar.wav'),
                 'fin' : mixer.Sound('assets/sonidos/fin.wav'), 'mover' : mixer.Sound('assets/sonidos/movimiento.wav'),
                 'girar' : mixer.Sound('assets/sonidos/giro.wav'), 'abajo' : mixer.Sound('assets/sonidos/abajo.wav'),
                 'fila' : mixer.Sound('assets/sonidos/fila.wav')}

    fxVolumen = 0.3
    sonidosFx['fin'].set_volume(fxVolumen)
    sonidosFx['nivel'].set_volume(0.9)
    sonidosFx['integrar'].set_volume(1.0)
    sonidosFx['mover'].set_volume(fxVolumen)
    sonidosFx['girar'].set_volume(0.5)
    sonidosFx['abajo'].set_volume(0.2)
    sonidosFx['fila'].set_volume(fxVolumen)


    def musicaFondo():
        mixer.music.stop()
        mixer.music.load(sonidos[random.randint(0, len(sonidos) - 1)])
        mixer.music.set_volume(1.0)
        mixer.music.play()

    def musicaInicio():
        mixer.music.stop()
        mixer.music.load('assets/sonidos/inicio.wav')
        mixer.music.set_volume(1.0)
        mixer.music.play()

    musicaInicio()

    def musicaFin():
        mixer.music.stop()
        mixer.music.load('assets/sonidos/musicaFin.wav')
        mixer.music.set_volume(0.7)
        mixer.music.play()

    def salir():
        pygame.font.quit()
        pygame.quit()
        mixer.quit()
        sys.exit()

    matrizTetris = (
        [1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1],
        [0,1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,1,0,1,0,0],
        [0,1,0,0,1,1,0,0,0,1,0,0,1,1,0,0,1,0,1,1,1],
        [0,1,0,0,1,0,0,0,0,1,0,0,1,0,1,0,1,0,0,0,1],
        [0,1,0,0,1,1,1,0,0,1,0,0,1,0,1,0,1,0,1,1,1]
    )
    tamanoCajaInicio = 30

    #Variables para grabar marcadores
    letras = 'ABCDEFGHIJKLMNÑOPQRTUVWXYZ0123456789'
    indiceLetrasJugador = [0, 0, 0]
    jugador = "AAA"
    modificadorLetra = 0
    velocidadLetra = 100
    marcadores = []
    lugar = 0

    try:
        cursor = open('marcadores', 'r')
    except:
        print('No existe el fichero "marcadores"')
        cursor = None

    if cursor:
        for j, linea in enumerate(cursor):
            marcadores.append({'jugador' : '', 'punteo' : ''})
            for i, letra in enumerate(linea):
                    if i < 3:
                        marcadores[j]['jugador'] += letra
                    if i > 3:
                        if letra != '\n':
                            marcadores[j]['punteo'] += letra
        cursor.close()

    else:
        marcadores.append({'jugador' : 'AAA', 'punteo' : '9999999'})

    jugador = marcadores[0]['jugador']
    indiceLetrasJugador[0] = letras.find(jugador[0])
    indiceLetrasJugador[1] = letras.find(jugador[1])
    indiceLetrasJugador[2] = letras.find(jugador[2])

    def dibujarFondo():
        global jugador
        ventana.fill((0, 0, 0))

        if inicio:
            for j, fila in enumerate(matrizTetris):
                for i, punto, in enumerate(fila):
                    if punto == 1:
                        pygame.draw.rect(ventana, (255, 255, 255), (i * tamanoCajaInicio + 45,
                        j * tamanoCajaInicio + 250 - 4 * tamanoCajaInicio, tamanoCajaInicio - 2, tamanoCajaInicio - 2))

            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 30)
            texto = 'Pulza las flachas para mover la pieza'
            img = fuente.render(texto, True, (255, 255, 255))
            centro = img.get_rect()[2]/2
            ventana.blit(img, (ancho/2 - centro, 400))

            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 32)
            texto = 'Pulza ESPACIO para inicial y pausar tu juego'
            img = fuente.render(texto, True, (255, 255, 255))
            centro = img.get_rect()[2] / 2
            ventana.blit(img, (ancho / 2 - centro, 500))

            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 25)
            texto = 'Pulza ESC para cerrar el juego'
            img = fuente.render(texto, True, (255, 255, 255))
            ventana.blit(img, (25, 750))

        elif jugando:
            pygame.draw.rect(ventana, (255 ,255, 255), (7, 7, 406, 806), 1)
            pygame.draw.rect(ventana, (255, 255, 255), (446, 7, 89, 167), 1)

            if pausa:
                fuente = pygame.font.SysFont("SpaceClaim ASME CB", 65)
                texto = 'PAUSA'
                img = fuente.render(texto, True, (255, 255, 255))
                ventana.blit(img, (110, 250))

        elif fin:
            pygame.draw.rect(ventana, (255, 255, 255), (7, 7, 406, 806), 1)
            pygame.draw.rect(ventana, (255, 255, 255), (446, 7, 89, 167), 1)
            dibujarMatriz()
            dibujarMarcadores()
            pygame.draw.rect(ventana, (0, 0, 0), (30, 250, 365, 125), 0)
            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 50)
            texto = 'FIN DEL JUEGO'
            img = fuente.render(texto, True, (255, 255, 255))
            ventana.blit(img, (45, 250))

        elif grabarMarcadores:

            jugador = letras[indiceLetrasJugador[0]] + letras[indiceLetrasJugador[1]] + letras[indiceLetrasJugador[2]]

            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 100)

            texto = jugador[0]
            img = fuente.render(texto, True, (255, 255, 255))
            centro = img.get_rect()[2] / 2
            ventana.blit(img, (250 / 2 - centro, alto/2 - 75))
            texto = jugador[1]
            img = fuente.render(texto, True, (255, 255, 255))
            centro = img.get_rect()[2] / 2
            ventana.blit(img, (400 / 2 - centro, alto / 2 - 75))
            texto = jugador[2]
            img = fuente.render(texto, True, (255, 255, 255))
            centro = img.get_rect()[2] / 2
            ventana.blit(img, (550 / 2 - centro, alto / 2 - 75))

            texto = str(puntos)
            img = fuente.render(texto, True, (255, 255, 255))
            centro = img.get_rect()[2] / 2
            ventana.blit(img, (1000 / 2 - centro, alto / 2 - 75))

            x1 = 100 + modificadorLetra * 75
            x2 = x1 + 25
            x3 = x2 + 25
            y1 = alto/2 -25
            y2 = y1 - 50
            pygame.draw.lines(ventana, (255, 255, 255), True, ((x1, y1), (x2, y2), (x3, y1)), 1)
            pygame.draw.lines(ventana, (255, 255, 255), True, ((x1, y1+150), (x2, y2+250), (x3, y1+150)), 1)

            if lugar <= 10:
                fuente = pygame.font.SysFont("SpaceClaim ASME CB", 80)
                texto = '¡¡¡FELICIDADES!!!'
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (ancho / 2 - centro, 50))

                fuente = pygame.font.SysFont("SpaceClaim ASME CB", 35)
                texto = 'estás dentro de los primeros 10 lugares'
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (ancho / 2 - centro, 200))

            else:
                fuente = pygame.font.SysFont("SpaceClaim ASME CB", 50)
                texto = 'Lo hiciste muy bien'
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (ancho / 2 - centro, 80))

                texto = 'pero puedes mejorar'
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (ancho / 2 - centro, 150))

            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 25)
            texto = 'Pulsa ESPACIO para grabar tu record'
            img = fuente.render(texto, True, (255, 255, 255))
            ventana.blit(img, (25, 750))

        elif mostrarMarcadores:
            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 35)
            for i, marcador in enumerate(marcadores):
                if i == 0:
                    continue
                texto = str(i) + '.'
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (200 - centro, 90 + 50 * i))

                texto = str(marcador['jugador'])
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (325 - centro, 90 + 50 * i))

                texto = str(marcador['punteo'])
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (475 - centro, 90 + 50 * i))

                if i == 10:
                    break

            if lugar > 10:
                texto = str(lugar) + '.'
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (200 - centro, 665))

                texto = str(marcadores[lugar]['jugador'])
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (325 - centro, 665))

                texto = str(marcadores[lugar]['punteo'])
                img = fuente.render(texto, True, (255, 255, 255))
                centro = img.get_rect()[2] / 2
                ventana.blit(img, (475 - centro, 665))

            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 45)
            texto = '¡LOS 10 MEJORES JUGADORES!'
            img = fuente.render(texto, True, (255, 255, 255))
            centro = img.get_rect()[2] / 2
            ventana.blit(img, (ancho / 2 - centro, 25))

            fuente = pygame.font.SysFont("SpaceClaim ASME CB", 25)
            texto = 'Pulsa ESPACIO para regresar a inicio'
            img = fuente.render(texto, True, (255, 255, 255))
            ventana.blit(img, (25, 750))

            pygame.draw.rect(ventana, (255, 255, 255), (125, 145, 450, 530), 1)

            if lugar <= 10 and len(marcadores) > 2:
                pygame.draw.rect(ventana, (255, 255, 255), (125, 108 + 50 * lugar, 450, 50), 1)

    def dibujarMatriz():
        for j, fila in enumerate(matriz):
            for i, punto, in enumerate(fila):
                if punto == 1:
                    pygame.draw.rect(ventana, (255, 255, 255), (i * tamanoCaja + 11,
                                j * tamanoCaja + 11 - 4 * tamanoCaja, tamanoCaja-2, tamanoCaja-2))

    def generarFigura():
        global siguientePieza

        siguientePieza = figuras.pieza([10, 4], pygame, ventana, tamanoCaja, casillas)

    def comprobarFilasLlenas():
        global matriz, lineas, puntos
        filasLlenas = []

        for j, fila in enumerate(matriz):
            borrar = True
            for i, dato, in enumerate(fila):
                if dato == 1:
                    continue
                else:
                    borrar = False
                    break
            if borrar == True:
                filasLlenas.append(j)
                lineas += 1

        if len(filasLlenas) == 1:
            puntos += puntosPorLinea
        elif len(filasLlenas) == 2:
            puntos += puntosPorDobleLinea
        elif len(filasLlenas) == 3:
            puntos += puntosPorTripleLinea
        elif len(filasLlenas) == 4:
            puntos += puntosPorCuatrupleLinea

        if len(filasLlenas) > 0:
            sonidosFx['fila'].play(len(filasLlenas)-1)

        for fila in filasLlenas:
            for y in range(fila, 0, -1):
                for i in range(casillas[0]):
                    matriz[y][i] = matriz[y-1][i]
                for i in range(casillas[0]):
                    matriz[0][i] = 0


    def integrarPieza():
        global pieza, matriz

        for j, fila in enumerate(pieza.figura):
            for i, dato, in enumerate(fila):
                if dato == 1:
                    matriz[j+pieza.posicion[1]][i+pieza.posicion[0]] = 1
        sonidosFx['integrar'].play()
        pieza = None

    def comprobarFin():
        global fin, fps

        for j, fila in enumerate (matriz):
            if j > 3:
                break
            if fin:
                break
            for i, punto in enumerate(fila):
                if punto == 1:
                    fin = True
                    fps = 15
                    break

    def dibujarMarcadores():

        fuente = pygame.font.SysFont("SpaceClaim ASME CB", 40)
        texto = str(f"Nivel: {nivel + 1}")
        img = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(img, (440, 250))

        fuente = pygame.font.SysFont("SpaceClaim ASME CB", 30)
        texto = str(f"Piezas: {piezas}")
        img = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(img, (440, 350))

        '''texto = str(f"Velocidad: {velocidad}")
        img = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(img, (440, 300))'''

        texto = str(f"Líneas: {lineas}")
        img = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(img, (440, 400))

        fuente = pygame.font.SysFont("SSpaceClaim ASME CB", 55)
        texto = str("PUNTEO")
        img = fuente.render(texto, True, (255, 255, 255))
        ventana.blit(img, (480, 550))

        fuente = pygame.font.SysFont("SpaceClaim ASME CB", 60)
        texto = str(puntos)
        img = fuente.render(texto, True, (255, 255, 255))
        centro = img.get_rect()[2]/2
        ventana.blit(img, (570 - centro, 600))


    def ordenarMarcadores():

        global marcadores
        marcador = marcadores[-1]
        if len(marcadores) > 1:
            for i in range(-1, - (len(marcadores)), -1):
                if int(marcador['punteo']) >= int(marcadores[i-1]['punteo']):
                    marcadores[i] = marcadores [i-1]
                    marcadores[i-1] = marcador
                else:
                    break

        escribirMarcadores()

    def escribirMarcadores():

        texto = ''
        for i, marcador in enumerate(marcadores):
            texto = texto + str(marcador['jugador']) + ' ' + str(marcador['punteo']) + '\n'
            if i > 100:
                break

        archivo = open('marcadores', 'w')
        archivo.write(texto)
        archivo.close()

    def inicializar():
        global siguientePieza,pieza, abajo, ultimoAbajo, izquierda, ultimoIzqierda, derecha, ultimoDerecha, rotando
        global ultimoRotando, matriz, modificadorLetra

        matriz = []

        for i in range(casillas[1]):
            fila = []
            for j in range(casillas[0]):
                fila.append(0)
            matriz.append(fila)

        siguientePieza = None
        pieza = None

        abajo = False
        ultimoAbajo = 0
        izquierda = False
        ultimoIzqierda = 0
        derecha = False
        ultimoDerecha = 0
        rotando = False
        ultimoRotando = 0

        global piezas, lineas, puntos, ultimoAumentoNivel, paso, tiempoUltimoPaso, nivel

        piezas = 0
        lineas = 0
        puntos = 0
        nivel = 0

        ultimoAumentoNivel = 0
        paso = pasoInicial
        tiempoUltimoPaso = 0

        modificadorLetra = 0

    def determinarPosicion():
        global lugar

        for i, marcador in enumerate(marcadores):
            if puntos < int(marcador['punteo']):
                continue
            else:
                lugar = i
                #print(lugar)
                break

    while True:

        dibujarFondo()
        microsegundos = tiempo.get_ticks()

        if jugando:
            velocidad = int(paso * factorVelocidad)
            comprobarFilasLlenas()
            dibujarMarcadores()

            if not pausa:

                dibujarMatriz()

                if not mixer.music.get_busy():
                    musicaFondo()

                if siguientePieza == None:
                    generarFigura()
                siguientePieza.dibujar()

                if pieza == None:
                    pieza = siguientePieza
                    pieza.posicion = [3, 0]
                    siguientePieza = None

                pieza.dibujar()


        for evento in eventos.get():
            
            if evento.type == pygame.KEYDOWN:

                if evento.key == pygame.K_DOWN:
                        abajo = True

                if evento.key == pygame.K_RIGHT:
                        derecha = True

                if evento.key == pygame.K_LEFT:
                        izquierda = True

                if evento.key == pygame.K_UP:
                        rotando = True

                if evento.key == pygame.K_SPACE:

                    if pausa:
                        pausa = False
                        mixer.music.unpause()
                        fps = 60

                    elif jugando:
                        pausa = True
                        mixer.music.pause()
                        fps = 15

                    elif inicio:
                        jugando = True
                        fin = False
                        inicio = False
                        inicializar()
                        mixer.music.stop()
                        fps = 60

                    elif fin:
                        jugando = False
                        fin = False
                        grabarMarcadores = True
                        determinarPosicion()
                        fps = 60

                    elif grabarMarcadores:
                        jugador = letras[indiceLetrasJugador[0]] + letras[indiceLetrasJugador[1]] + letras[indiceLetrasJugador[2]]
                        marcadores.append({'jugador' : jugador, 'punteo' : puntos})
                        puntos = 0
                        ordenarMarcadores()
                        marcadores[0]['jugador'] = jugador
                        indiceLetrasJugador[0] = letras.find(jugador[0])
                        indiceLetrasJugador[1] = letras.find(jugador[1])
                        indiceLetrasJugador[2] = letras.find(jugador[2])
                        grabarMarcadores = False
                        mostrarMarcadores = True
                        fps = 15

                    elif mostrarMarcadores:
                        mostrarMarcadores = False
                        inicio = True
                        musicaInicio()


                if evento.key == pygame.K_ESCAPE:
                    salir()

            if evento.type == pygame.KEYUP:

                if evento.key == pygame.K_DOWN:
                    abajo = False

                if evento.key == pygame.K_LEFT:
                    izquierda = False

                if evento.key == pygame.K_RIGHT:
                    derecha = False

                if evento.key == pygame.K_UP:
                    rotando = False



            if evento.type == globales.QUIT:
                salir()

        if jugando and not pausa and pieza:
            if izquierda:
                if velocidad > velGiroMax:
                    if microsegundos > ultimoIzqierda + velocidad:
                        pieza.mover("izquierda", matriz)
                        sonidosFx['mover'].play()
                        ultimoIzqierda = microsegundos
                else:
                    if microsegundos > ultimoIzqierda + velMovMax:
                        pieza.mover("izquierda", matriz)
                        sonidosFx['mover'].play()
                        ultimoIzqierda = microsegundos

            if derecha:
                if velocidad > velGiroMax:
                    if microsegundos > ultimoDerecha + velocidad:
                        pieza.mover("derecha", matriz)
                        sonidosFx['mover'].play()
                        ultimoDerecha = microsegundos
                else:
                    if microsegundos > ultimoDerecha + velMovMax:
                        pieza.mover("derecha", matriz)
                        sonidosFx['mover'].play()
                        ultimoDerecha = microsegundos

            if abajo:
                if microsegundos > ultimoAbajo + velocidad:
                    pieza.mover("abajo", matriz)
                    sonidosFx['abajo'].play()
                    ultimoAbajo = microsegundos
                    tiempoUltimoPaso = microsegundos
                    puntos += puntosPorCaidaRapida

            if rotando:
                if velocidad > velGiroMax:
                    if microsegundos > ultimoRotando + velocidad * 1.5:
                        pieza.rotar(matriz)
                        sonidosFx['girar'].play()
                        ultimoRotando = microsegundos
                else:
                    if microsegundos > ultimoRotando + velGiroMax * 1.5:
                        pieza.rotar(matriz)
                        sonidosFx['girar'].play()
                        ultimoRotando = microsegundos

        if grabarMarcadores:
            if izquierda:
                if microsegundos > ultimoIzqierda + velocidadLetra:
                    modificadorLetra -= 1
                    if modificadorLetra < 0:
                        modificadorLetra = 0
                    sonidosFx['mover'].play()
                    ultimoIzqierda = microsegundos

            if derecha:
                if microsegundos > ultimoDerecha + velocidadLetra:
                    modificadorLetra += 1
                    if modificadorLetra > 2:
                        modificadorLetra = 2
                    sonidosFx['mover'].play()
                    ultimoDerecha = microsegundos

            if abajo:
                if microsegundos > ultimoAbajo + velocidadLetra:
                    indiceLetrasJugador[modificadorLetra] -= 1
                    if indiceLetrasJugador[modificadorLetra] < 0:
                        indiceLetrasJugador[modificadorLetra] = len(letras) - 1
                    sonidosFx['abajo'].play()
                    ultimoAbajo = microsegundos

            if rotando:
                if microsegundos > ultimoRotando + velocidadLetra:
                    indiceLetrasJugador[modificadorLetra] += 1
                    if indiceLetrasJugador[modificadorLetra] > len(letras) - 1:
                        indiceLetrasJugador[modificadorLetra] = 0
                    sonidosFx['abajo'].play()
                    ultimoRotando = microsegundos

        if fin:
            if jugando:
                sonidosFx['fin'].play()
                musicaFin()
            jugando = False
            pausa = False


        if jugando and not pausa:
            if pieza:
                if pieza.posicionada == True:
                    integrarPieza()
                    piezas += 1
                    tiempoUltimoPaso = microsegundos
                    comprobarFin()
                    if piezas >= ciclosPorNivel + ultimoAumentoNivel:
                        nivel += 1
                        sonidosFx['nivel'].play()
                        paso = pasoInicial - (nivel * restaPasosPorNivel)
                        ultimoAumentoNivel = piezas

                elif  microsegundos > tiempoUltimoPaso + paso:
                    (pieza.mover('abajo', matriz))
                    tiempoUltimoPaso = microsegundos

        reloj.tick(fps)
        pygame.display.update()
