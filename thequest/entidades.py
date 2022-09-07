import os

import pygame as pg
from . import ALTO, ANCHO
from pygame.sprite import Sprite

class Nave(Sprite):

    MARGEN_LATERAL = 20
    VELOCIDAD = 5
    TAMAÑO_NAVE = (80, 80)   

    def __init__(self, tq_game):
        super().__init__()
        self.pantalla = tq_game.pantalla
        self.pantalla_rect = tq_game.pantalla.get_rect()

        # Cargar imagen de nave
        self.nave_imagen = pg.image.load(os.path.join("resources", "images", "Main Ship.png"))

        # Rotacion de la imagen
        self.nave_imagen = pg.transform.rotate(self.nave_imagen, -90)

        # Escalar imagen de la nave
        self.nave_imagen = pg.transform.scale(self.nave_imagen, self.TAMAÑO_NAVE)

        # Posicion inicial de la nave
        self.rect = self.nave_imagen.get_rect(midleft=(self.MARGEN_LATERAL, ALTO/2))

        # Guardado el valor decimal para la posicion vertical de la nave
        self.y = float(self.rect.y)

        # Chivatos de movimiento 
        self.mueve_arriba = False
        self.mueve_abajo = False

    def actualizaNave(self):

        # Definiendo los limites de movimiento de la nave
        if self.mueve_arriba and self.rect.top < self.pantalla_rect.top:
            self.y += self.VELOCIDAD
        if self.mueve_abajo and self.rect.bottom > 700:
            self.y -= self.VELOCIDAD

        self.rect.y = self.y

    def blitNave(self):
        self.pantalla.blit(self.nave_imagen, self.rect)

