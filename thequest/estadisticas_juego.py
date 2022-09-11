from .configuracion import VIDAS, velocidad_asteroides

class GameStats():
    '''Sigue las estadisticas de Alien Invasion'''
    
    def __init__(self, tq_game):
        self.configuracion = tq_game.configuracion
        self.reiniciar_stats()        

    def reiniciar_stats(self):
        '''Inicializa las estadisticas que pueden cambiar durante el juego'''

        self.vidas_restantes = self.configuracion.VIDAS
        self.velocidad_aster = self.configuracion.velocidad_asteroides
            
        