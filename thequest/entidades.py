import os
import random

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
        self.nave_imagen = pg.image.load(os.path.join("resources", "images", "Main_Ship.png"))

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
        if self.mueve_arriba and self.rect.top >= self.pantalla_rect.top:
            self.y -= self.VELOCIDAD
        if self.mueve_abajo and self.rect.bottom <= self.pantalla_rect.bottom:
            self.y += self.VELOCIDAD

        self.rect.y = self.y

    def blitNave(self):
        # Pintar imagen de la nave
        self.pantalla.blit(self.nave_imagen, self.rect)

class Asteroide(Sprite):
    # Establezco tamaños predeterminados de asteroides como atributos de clase
    SIZE_SMALL_ASTER = (500, 400)
    SIZE_MEDIUM_ASTER = (700, 600)
    SIZE_BIG_ASTER = (900, 800)    
    
    def __init__(self):
        super().__init__()
        # Cargar imagen de asteroide
        self.aster_imagen = pg.image.load(os.path.join("resources", "images", "asteroide.png"))

    
        '''Esta parte sirve para aleatorizar la 
        aparicion de asteroides en pantalla de manera que por
        cada vuelta de ciclo se instancie una imagen con un escalado
        diferente'''
        self.aster_random = random.randrange(0, 2)
        if self.aster_random == 0:
            self.aster_imagen = pg.transform.scale(self.aster_imagen, self.SIZE_SMALL_ASTER)
            
        elif self.aster_random == 1:
            self.aster_imagen = pg.transform.scale(self.aster_imagen, self.SIZE_MEDIUM_ASTER)
            
        elif self.aster_random == 2:
            self.aster_imagen = pg.transform.scale(self.aster_imagen, self.SIZE_BIG_ASTER)
            
        
        '''
        Con esta parte se generan aleatoriamente 
        los asteroides por todo la pantalla y desde 
        fuera del ancho''' 
        self.rect = self.aster_imagen.get_rect()
        self.margen_asteroide = (ALTO - self.rect.height)
        self.rect.y = random.randrange(self.margen_asteroide)
        self.rect.x = +self.rect.width
        
        # Velocidad aleatoria del meteorito
        self.velocidad_x = random.randrange(5, 15)

    def refrescarAster(self):
        '''Este metodo refresca los asteroides que salen 
        por un lado de la pantalla para generar otros, dando 
        la sensacion de continuidad'''
        self.rect.x -= self.velocidad_x
        if self.rect.right < 0:
            self.rect.y = random.randrange(self.margen_asteroide)
            self.rect.x = +self.rect.width
            self.velocidad_x = random.randrange(5, 15)

    def blitAster(self):
        self.pantalla.blit(self.aster_imagen, self.rect)
    
