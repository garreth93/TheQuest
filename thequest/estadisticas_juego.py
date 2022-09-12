class GameStats():
    '''Sigue las estadisticas de Alien Invasion'''
    
    def __init__(self, tq_game):
        self.config = tq_game.config
        self.reiniciar_stats()
        self.puntuacion = 0        

    def reiniciar_stats(self):
        '''Inicializa las estadisticas que pueden cambiar durante el juego'''

        self.vidas_restantes = self.config.VIDAS
        self.velocidad_aster = self.config.velocidad_asteroides
        self.puntuacion = 0    
        