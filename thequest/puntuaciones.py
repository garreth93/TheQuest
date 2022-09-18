import os
import pygame.font
from . import COLOR_TEXTO, COLOR_FONDO

class Puntuaciones:
    '''Clase para informar de la puntuacion obtenida'''
    
    def __init__(self, tq_game):
        '''Inicializa los atributos de puntuacion'''
        self.pantalla = tq_game.pantalla
        self.pantalla_rect = self.pantalla.get_rect()
        self.config = tq_game.config
        self.stats = tq_game.estadisticas

        # Configuramos la fuente
        self.fuente = pygame.font.SysFont(None, 48)

        # Contador de asteroides
        self.contador_aster = 0
        # Flag para activar ultimos asteroides
        self.recta_final_flag = False

        # Renderizamos la imagen de la puntuacion
        self.iniciar_puntuacion()

    def iniciar_puntuacion(self):
        '''Renderiza la fuente en imagen'''        
        self.puntuacion_render = self.fuente.render(str(self.stats.puntuacion), True, COLOR_TEXTO, COLOR_FONDO)

        # Mostrar puntuacion en la parte superior derecha
        self.puntuacion_rect = self.puntuacion_render.get_rect()
        self.puntuacion_rect.right = self.pantalla_rect.right - 20
        self.puntuacion_rect.top = 20
    
    def mostrar_puntuacion(self):
        '''Pinta la puntuacion'''
        self.pantalla.blit(self.puntuacion_render, self.puntuacion_rect)
