import os
import pygame as pg

from thequest.escenas import Historia, Portada, Instrucciones, Partida
from thequest import ALTO, ANCHO

class Thequest:
    def __init__(self):
        pg.init()
        self.display = pg.display.set_mode((ANCHO, ALTO))
        pg.display.set_caption("The Quest")

        icon = pg.image.load(os.path.join("resources", "images", "game-icon.png"))
        pg.display.set_icon(icon)

        self.escenas = [
            Portada(self.display),
            Instrucciones(self.display),
            Historia(self.display),
            Partida(self.display)
        ]

    def jugar(self):
        for escena in self.escenas:
            escena.bucle_principal()
        