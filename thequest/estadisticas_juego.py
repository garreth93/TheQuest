import pygame

class GameStats():
    '''Sigue las estadisticas de Alien Invasion'''
    
    def __init__(self, tq_game):
        super().__init__()
        self.configuracion = tq_game.configuracion
        self.reiniciar_stats()

    def reiniciar_stats(self):
        '''Inicializa las estadisticas que pueden cambiar durante el juego'''
        