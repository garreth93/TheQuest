
class Config:

    def __init__(self):
        '''Inicializa las estadisticas estaticas del juego'''
        # Vidas del jugador

        self.VIDAS = 3

        # Velocidad asteroides standard

        self.velocidad_asteroides = (5, 10)       

        # Colision con nave Puntos

        self.aster_colision = 100