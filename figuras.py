import random
import main

import pygame.draw


class pieza():



    def asignar(self):

        matrices = [

                    [   (0, 1, 0, 0),
                        (0, 1, 0, 0),
                        (0, 1, 0, 0),
                        (0, 1, 0, 0),  ],

                    [   (0, 0, 0, 0),
                        (0, 1, 1, 0),
                        (0, 1, 1, 0),
                        (0, 0, 0, 0),  ],

                    [   (0, 0, 0, 0),
                        (0, 1, 0, 0),
                        (0, 1, 1, 0),
                        (0, 1, 0, 0),  ],

                    [   (0, 0, 0, 0),
                        (0, 1, 0, 0),
                        (0, 1, 0, 0),
                        (0, 1, 1, 0),  ],

                    [   (0, 0, 0, 0),
                        (0, 0, 1, 0),
                        (0, 0, 1, 0),
                        (0, 1, 1, 0),  ],

                    [   (0, 0, 0, 0),
                        (0, 0, 1, 0),
                        (0, 1, 1, 0),
                        (0, 1, 0, 0),  ],

                        [(0, 0, 0, 0),
                         (0, 1, 0, 0),
                         (0, 1, 1, 0),
                         (0, 0, 1, 0), ]

        ]

        return matrices[random.randint(0, len(matrices)-1)]

    def dibujar(self):

        for j, fila in enumerate(self.figura):
            for i, dato in enumerate(fila):
                if dato == 1:
                    self.pygame.draw.rect(self.ventana, (255, 255, 255), ((i * self.tamanoCaja + 11) + self.posicion[0] * self.tamanoCaja,
                                                        (j * self.tamanoCaja + 11) + self.posicion[1] * self.tamanoCaja - 4 * self.tamanoCaja,
                                                                          self.tamanoCaja - 2, self.tamanoCaja - 2))

    def mover(self, direccion, matriz):

        if direccion == 'abajo':
            tope = False
            for j, linea in enumerate(self.figura):
                if tope:
                    break
                for i, punto in enumerate(linea):
                    if j + self.posicion[1] >= -1:
                        if punto == 1:
                            if j + self.posicion[1] + 2 > self.casillas[1] \
                                    or matriz[j+1+self.posicion[1]][i+self.posicion[0]] == 1:
                                tope = True
                                break

            if tope:

                self.posicionada = True

            else:
                self.posicion[1] += 1

        elif direccion == 'izquierda':
            tope = False
            for j, linea in enumerate(self.figura):
                if tope:
                    break
                for i, punto in enumerate(linea):
                    if punto == 1:
                        if i + self.posicion[0] - 1 < 0 or matriz[j + self.posicion[1]][i -1 + self.posicion[0]] == 1:
                            tope = True
                            break

            if not tope:
                self.posicion[0] -= 1


        elif direccion == 'derecha':
            tope = False
            for j, linea in enumerate(self.figura):
                if tope:
                    break
                if j + self.posicion[1] >= 0:
                    for i, punto in enumerate(linea):
                        if punto == 1:
                            if i + self.posicion[0] + 1 > self.casillas[0]-1:
                                tope = True
                                break
                            elif matriz[j + self.posicion[1]][i + 1 + self.posicion[0]] == 1:
                                tope = True
                                break
            if not tope:
                self.posicion[0] += 1

    def rotar(self, matriz):

        piezaRotada = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for j, linea in enumerate(self.figura):
            for i, punto in enumerate(linea):
                piezaRotada[i][3-j] = punto

        tope = False
        adentro = False
        corDePos = 0
        while not adentro:
            for j, linea in enumerate(piezaRotada):
                for i, punto in enumerate(linea):
                    if punto == 1:
                        if i+self.posicion[0] + corDePos < 0:
                            corDePos += 1
                        elif i+self.posicion[0] + corDePos > self.casillas[0] - 1 :
                            corDePos -= 1
                        else:
                            adentro = True

        for j, linea in enumerate(piezaRotada):
            if tope:
                break
            for i, punto in enumerate(linea):
                if punto == 1:
                    if matriz[j+ self.posicion[1]][i + self.posicion[0] + corDePos] == 1:
                        tope = True
                        break
                    elif j + self.posicion[1] > self.casillas[1]-1:
                        tope = True
                        break

        if not tope:
            self.figura = piezaRotada
            self.posicion[0] += corDePos

    def __init__(self, posicion, pygame, ventana, tamanoCaja, casillas):

        self.posicion = posicion
        self.pygame = pygame
        self.ventana = ventana
        self.tamanoCaja = tamanoCaja

        self.figura = self.asignar()
        self.posicion = posicion

        self.casillas = casillas

        self.posicionada = False

        self.matriz = None