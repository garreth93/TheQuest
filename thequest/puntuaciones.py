import os
import pygame.font
from . import COLOR_TEXTO

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

        # Renderizamos la imagen de la puntuacion
        self.iniciar_puntuacion()

    def iniciar_puntuacion(self):
        '''Renderiza la fuente en imagen'''
        puntuacionStr = str(self.stats.puntuacion)
        