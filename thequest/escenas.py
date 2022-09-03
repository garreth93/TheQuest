import sys
import os
import pygame as pg

from . import ANCHO, ALTO, COLOR_FONDO, COLOR_TEXTO


class Escena:
    def __init__(self, pantalla: pg.Surface):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        pass


class Portada(Escena):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.fondo_portada = pg.image.load(os.path.join("resources", "images", "fondo.png"))
        fuente_titulo = os.path.join("resources", "fonts", "Arcadia.ttf")
        self.titulo = pg.font.Font(fuente_titulo, 90)
        fuente_texto = os.path.join("resources", "fonts", "Plaguard-ZVnjx.otf")
        self.texto = pg.font.Font(fuente_texto, 40)

        pg.mixer.music.load(os.path.join("resources", "sounds", "mainmenu.ogg"))
        pg.mixer.music.play(-1)

    def bucle_principal(self):
        '''Este es el bucle principal'''

        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    salir = True
                
                if event.type == pg.KEYDOWN and event.key == pg.K_h:
                    salir = True

                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit()

            self.pantalla.blit(self.fondo_portada, (0,0))
            self.pintar_titulo()
            self.pintar_opciones()                   
            pg.display.flip()

    def pintar_titulo(self):
        nombre_titulo = "The Quest"
        texto = pg.font.Font.render(self.titulo, nombre_titulo, True, COLOR_TEXTO)
        ancho_texto = texto.get_width()
        pos_x = (ANCHO - ancho_texto)/2
        pos_y = ALTO - 650
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_opciones(self):
        opcion_comenzar = "COMENZAR PARTIDA - (SPACE)"
        opcion_historia = "HISTORIA - (H)"
        opcion_instrucciones = "INSTRUCCIONES - (I)"
        opcion_salir = "SALIR - (ESC)"

        render_comenzar = pg.font.Font.render(self.texto, opcion_comenzar, True, COLOR_TEXTO)
        render_historia = pg.font.Font.render(self.texto, opcion_historia, True, COLOR_TEXTO)
        render_instrucciones = pg.font.Font.render(self.texto, opcion_instrucciones, True, COLOR_TEXTO)
        render_salir = pg.font.Font.render(self.texto, opcion_salir, True, COLOR_TEXTO)
        
        posx_comenzar = (ANCHO - render_comenzar.get_width()) / 2
        posx_historia = (ANCHO - render_historia.get_width()) / 2
        posx_instrucciones = (ANCHO - render_instrucciones.get_width()) / 2
        posx_salir = (ANCHO - render_salir.get_width()) / 2

        self.pantalla.blits(
            [(render_comenzar, (posx_comenzar, ALTO - 300)),
             (render_historia, (posx_historia, ALTO - 250)),
              (render_instrucciones, (posx_instrucciones, ALTO - 200)),
               (render_salir, (posx_salir, ALTO - 150))])
    
class Historia(Escena):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)


    def bucle_principal(self):
        '''Este es el bucle principal'''

        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    salir = True
                
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit()

            self.pantalla.fill(COLOR_FONDO)     
                            
            pg.display.flip()

    def textoHistoria(self):
        fuente_historia = os.path.join("resources", "fonts", "gomarice_no_continue.ttf")
        self.historia = pg.font.Font(fuente_historia, 20)
        