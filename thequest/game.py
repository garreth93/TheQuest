# Importaciones necesarias para el funcionamiento correcto
import os
import pygame as pg

from thequest.escenas import Historia, Portada, Instrucciones, Partida
from thequest import ALTO, ANCHO


# Clase principal del juego para gestionar escenas y que el juego se ejecute
class Thequest:
    # Metodo init para inicializar la ventana de juego y otras funcionalidades
    def __init__(self):
        pg.init()
        # Generacion de la ventana
        self.display = pg.display.set_mode((ANCHO, ALTO))

        # Añadir titulo a la ventana
        pg.display.set_caption("The Quest")
        
        # Carga y añadida imagen para icono de ventana
        icon = pg.image.load(os.path.join("resources", "images", "game-icon.png"))
        pg.display.set_icon(icon)

        # Lista para gestionar la continuidad de pantallas del juego
        self.escenas = [
            Portada(self.display),
            Instrucciones(self.display),
            Historia(self.display),
            Partida(self.display)
        ]
    
    # Metodo para ejecucion del juego en archivo main
    def jugar(self):
        for escena in self.escenas:
            escena.bucle_principal()
        