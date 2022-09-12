
class Config:

    def __init__(self):
        '''Inicializa las estadisticas estaticas del juego'''
        # Vidas del jugador

        self.VIDAS = 3

        # Velocidad asteroides standard

        self.velocidad_asteroides = (5, 10)

        # Puntuacion asteroides

        self.aster_small_puntos = 20
        self.aster_medium_puntos = 50
        self.aster_big_puntos = 80

        # Colision con nave Puntos

        self.aster_colision = 100