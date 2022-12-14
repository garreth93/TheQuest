import os
import pygame as pg

from . import ALTO, ANCHO, COLOR_TEXTO

class Config:

    def __init__(self):
        '''Inicializa las estadisticas estaticas del juego'''
        # Vidas del jugador

        self.VIDAS = 3

        # Velocidad asteroides standard

        self.velocidad_asteroides = (5, 10)       

        # Colision con nave Puntos

        self.aster_colision = 100

       


class InputBox:
    '''Clase para gestionar un cuadro emergente que pide texto'''
    def __init__(self, pantalla: pg.Surface, color_texto="white", color_fondo="Blue", title=""):
        font_file = os.path.join(
            "resources", "fonts", "Arcadia.ttf")
        self.tipografia = pg.font.Font(font_file, 20)
        self.texto = ""
        self.color_fondo = color_fondo
        self.color_texto = color_texto
        self.pantalla = pantalla
        self.margen = 30
        self.crear_elementos_fijos()
        self.maxima_longidtud = 3        

    def get_text(self):
        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE and len(self.texto) > 0:
                        self.texto = self.texto[:-1]
                    elif event.key == pg.K_RETURN:
                        salir = True
                    else: 
                        if len(self.texto) < self.maxima_longidtud:                   
                            self.texto += event.unicode
            self.pintar()
            pg.display.flip()
        return self.texto

    def pintar(self):
        pg.draw.rect(self.pantalla, self.color_fondo, self.fondo)
        self.pantalla.blit(self.titulo, (self.x_titulo, self.y_titulo))

        superficie_texto = self.tipografia.render(
            self.texto, True, self.color_texto, self.color_fondo)
        pos_x = self.x_titulo
        pos_y = self.y_titulo + self.titulo.get_height()
        self.pantalla.blit(superficie_texto, (pos_x, pos_y))

    def crear_elementos_fijos(self):
        # el t??tulo
        self.titulo = self.tipografia.render(
            "Nuevo Record! Pon tus iniciales y pulsa intro:", True, self.color_texto, self.color_fondo)
        self.x_titulo = (ANCHO-self.titulo.get_width())//2 - 200
        self.y_titulo = (ALTO-self.titulo.get_height())//2

        # el rect??ngulo de fondo
        x_fondo = self.x_titulo - self.margen
        y_fondo = self.y_titulo - self.margen
        w_fondo = self.titulo.get_width() + self.margen * 2
        h_fondo = self.titulo.get_height() * 2 + self.margen * 2
        self.fondo = pg.Rect(x_fondo, y_fondo, w_fondo, h_fondo)