from email.mime import image
import os
import random

import pygame as pg
from . import ALTO, ANCHO, NEGRO, COLOR_TEXTO
from pygame.sprite import Sprite


class Nave(Sprite):

    MARGEN_LATERAL = 20
    VELOCIDAD = 8
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

        # Velocidad para animacion X
        self.velocidad_x = 1

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
    SIZE_SMALL_ASTER = (50, 50)
    SIZE_MEDIUM_ASTER = (75, 75)
    SIZE_BIG_ASTER = (100, 100)    
    
    def __init__(self, tq_game):
        super().__init__()
        self.stats = tq_game.estadisticas
        self.puntuaciones = tq_game.puntuacion
        # Cargar imagen de asteroide
        self.image = pg.image.load(os.path.join("resources", "images", "asteroide.png"))
        
        '''Esta parte sirve para aleatorizar la 
        aparicion de asteroides en pantalla de manera que por
        cada vuelta de ciclo se instancie una imagen con un escalado
        diferente'''
        self.aster_random = random.randrange(0, 3)
        if self.aster_random == 0:
            self.image = pg.transform.scale(self.image, self.SIZE_SMALL_ASTER)
            self.aster_small_puntos = 5
            self.radius = 10
        elif self.aster_random == 1:
            self.image = pg.transform.scale(self.image, self.SIZE_MEDIUM_ASTER)
            self.aster_medium_puntos = 10
            self.radius = 10
        elif self.aster_random == 2:
            self.image = pg.transform.scale(self.image, self.SIZE_BIG_ASTER)
            self.radius = 10
            self.aster_big_puntos = 15

                       
        
        '''
        Con esta parte se generan aleatoriamente 
        los asteroides por todo la pantalla y desde 
        fuera del ancho'''        
        self.rect = self.image.get_rect()
        self.margen_asteroide = (ALTO - self.rect.height)
        self.rect.y = random.randrange(0, self.margen_asteroide)
        self.rect.x = ANCHO + self.rect.width
        
        # Velocidad aleatoria del meteorito
        self.velocidad_x = random.randrange(5, 10)        

    def update(self):
        '''Esta parte sirve para ir contado los puntos que nos dan
        los diferentes tamaños de los asteroides'''
        if self.aster_random == 0: 
            if self.rect.right < 0:
                self.stats.puntuacion += self.aster_small_puntos
        elif self.aster_random == 1: 
            if self.rect.right < 0:
                self.stats.puntuacion += self.aster_medium_puntos
        elif self.aster_random == 2:
            if self.rect.right < 0: 
                self.stats.puntuacion += self.aster_big_puntos
        
        self.puntuaciones.iniciar_puntuacion()

        '''Este metodo refresca los asteroides que salen 
        por un lado de la pantalla para generar otros, dando 
        la sensacion de continuidad'''                
        self.rect.x -= self.velocidad_x
        if self.rect.right < -10:
            self.rect.y = random.randrange(0, self.margen_asteroide)
            self.rect.x = ANCHO + self.rect.width
            self.velocidad_x = random.randrange(5, 10)
            if self.puntuaciones.recta_final_flag == True:
               self.puntuaciones.contador_aster += 1
               

class Planeta(Sprite):
    def __init__(self, tq_game):
        super().__init__()
        self.pantalla = tq_game.pantalla
        self.pantalla_rect = tq_game.pantalla.get_rect()
        self.planeta_imagen = pg.image.load(os.path.join("resources", "images", "planeta.png"))
        self.planeta_rect = self.planeta_imagen.get_rect(midleft=(ANCHO + 5, ALTO/2))
        self.velocidad_x = 1
    def blit_planeta(self):
     self.pantalla.blit(self.planeta_imagen, self.planeta_rect)

class NaveVictoriosa(Sprite):

    MARGEN_LATERAL = 20    
    TAMAÑO_NAVE = (80, 80)   

    def __init__(self, tq_game):
        super().__init__()
        self.pantalla = tq_game.pantalla
        self.pantalla_rect = tq_game.pantalla.get_rect()
        self.velocidad_x = 1
        self.rotacion = 0        
        # Cargar imagen de nave
        self.nave_imagen = pg.image.load(os.path.join("resources", "images", "Main_Ship.png"))

        # Rotacion de la imagen
        self.nave_imagen = pg.transform.rotate(self.nave_imagen, -90)

        # Escalar imagen de la nave
        self.nave_imagen = pg.transform.scale(self.nave_imagen, self.TAMAÑO_NAVE)

        # Posicion inicial de la nave
        self.rect = self.nave_imagen.get_rect(midleft=(self.MARGEN_LATERAL, ALTO/2))
    
    def blitNaveWin(self):
        # Pintar imagen de la nave
        self.pantalla.blit(self.nave_imagen, self.rect)

    def tick(self):
        self.rotacion += 1
        if self.rotacion < 180:
            self.rotar_nave(self.nave_imagen, ANCHO - 400, 350, self.rotacion)
            if self.rotacion == 180:
                self.velocidad_x = 1
                self.rect.x += self.velocidad_x

    def rotar_nave(self, imagen, x, y, angulo):
        '''Rota la nave en su eje central'''
        self.imagen_rotada = pg.transform.rotate(imagen, angulo)
        self.pantalla.blit(self.imagen_rotada, self.imagen_rotada.get_rect(center=imagen.get_rect(topleft=(x,y)).center).topleft)       
        

class TextoNivel2():
    def __init__(self, tq_game):
        super().__init__()
        self.pantalla = tq_game.pantalla
        self.pantalla_rect = tq_game.pantalla.get_rect()
        self.velocidad_y = 1
        self.velocidad_x = 2
        fuente = os.path.join("resources", "fonts", "Arcadia.ttf")
        self.fuente_nivel2 = pg.font.Font(fuente, 50)
        msg_leve2 = "NIVEL 2"
        self.render_msg = pg.font.Font.render(self.fuente_nivel2, msg_leve2, True, COLOR_TEXTO)
        self.text_ancho = self.render_msg.get_width()
        self.text_alto = self.render_msg.get_height()       
        self.rect_textlevel = self.render_msg.get_rect(center=((ANCHO)/2, 0 - self.text_alto))
              

    def blitNivel2Text(self):
        self.pantalla.blit(self.render_msg, self.rect_textlevel)