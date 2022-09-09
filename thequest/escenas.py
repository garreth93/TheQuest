# Importaciones necesarias para el funcionamiento del juego
from multiprocessing.synchronize import Event
import sys
import os
import time
import pygame as pg

from . import ANCHO, ALTO, COLOR_TEXTO, FPS
from .entidades import Nave, Asteroide

# Creacion de la clase padre de todas
class Escena:
    def __init__(self, pantalla: pg.Surface):
        self.pantalla = pantalla

        # Instanciamiento de la clase Clock, para definir los FPS
        self.reloj = pg.time.Clock()

        # Metodo del bucle principal, para que las demas escenas lo hereden
    def bucle_principal(self):
        pass


class Portada(Escena):
    '''Clase para el menú principal, 
    hereda directamente de la clase Escena'''
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)

        # Carga de recursos, titulo, fondo, fuentes...
        self.fondo_portada = pg.image.load(os.path.join("resources", "images", "fondo.png"))
        fuente_titulo = os.path.join("resources", "fonts", "Arcadia.ttf")
        self.titulo = pg.font.Font(fuente_titulo, 90)
        fuente_texto = os.path.join("resources", "fonts", "Plaguard-ZVnjx.otf")
        self.texto = pg.font.Font(fuente_texto, 40)        
        
        # Musica del menú principal
        pg.mixer.music.load(os.path.join("resources", "sounds", "mainmenu.ogg"))
        pg.mixer.music.play(-1)

    def bucle_principal(self):
        '''Este es el bucle principal'''
        
        salir = False
        while not salir:
            # Definimos las teclas para navegar por el juego y salir del mismo
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    salir = True            

                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit()

                if event.type == pg.QUIT:
                    sys.exit()

            # Pintar el fondo de la portada, con titulo y opciones
            self.pantalla.blit(self.fondo_portada, (0,0))
            self.pintar_titulo()
            self.pintar_opciones()
                              
            pg.display.flip()

    def pintar_titulo(self):
        # Metodo para mostrar el titulo del juego en pantalla
        nombre_titulo = "The Quest"
        texto = pg.font.Font.render(self.titulo, nombre_titulo, True, COLOR_TEXTO)
        ancho_texto = texto.get_width()
        # Posicionamiento 
        pos_x = (ANCHO - ancho_texto)/2
        pos_y = ALTO - 650
        self.pantalla.blit(texto, (pos_x, pos_y))

    def pintar_opciones(self):
        # Metodo para mostrar las opciones del menú de juego
        opcion_comenzar = "COMENZAR PARTIDA - (SPACE)"        
        opcion_salir = "SALIR - (ESC)"

        render_comenzar = pg.font.Font.render(self.texto, opcion_comenzar, True, COLOR_TEXTO)        
        render_salir = pg.font.Font.render(self.texto, opcion_salir, True, COLOR_TEXTO)
        
        # Posicionamiento de las opciones
        posx_comenzar = (ANCHO - render_comenzar.get_width()) / 2        
        posx_salir = (ANCHO - render_salir.get_width()) / 2

        self.pantalla.blits(
            [(render_comenzar, (posx_comenzar, ALTO - 300)),
               (render_salir, (posx_salir, ALTO - 250))])
    


class Instrucciones(Escena):
    '''Clase para las instrucciones del juego, funcionamiento de
    teclas y una breve explicación del juego '''
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.instrucciones_img = pg.image.load(os.path.join("resources", "images", "instrucciones_image.png"))
    
    def bucle_principal(self):
        '''Este es el bucle principal'''

        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    salir = True
                
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit()

                if event.type == pg.QUIT:
                    sys.exit()

            self.pantalla.blit(self.instrucciones_img, (0,0))                 
            pg.display.flip()


class Historia(Escena):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)                
        self.historia_imagen = pg.image.load(os.path.join("resources", "images", "historiatexto.png"))

    def bucle_principal(self):
        '''Este es el bucle principal'''

        salir = False
        while not salir:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    salir = True
                
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit()

                if event.type == pg.QUIT:
                    sys.exit()

            self.pantalla.blit(self.historia_imagen, (0,0))                 
            pg.display.flip()

class Partida(Escena):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.fondo = pg.image.load(os.path.join("resources", "images", "fondo_juego.png"))        
        self.x = 0
        self.y = 0
        fuente = os.path.join("resources", "fonts", "Arcadia.ttf")
        self.fuente_vidas = pg.font.Font(fuente, 20)

        #Variable para numero de vidas
        self.vidas = 3

        # Instanciamos la clase Nave
        self.jugador = Nave(self)       

        # Instancia de grupos de asteroides, generamos 10
        self.asteroides = pg.sprite.Group()

        for i in range(15):
            self.asteroide = Asteroide()
            self.asteroides.add(self.asteroide)

    def bucle_principal(self):
        '''Este es el bucle principal'''
        # Frena la música del menú
        pg.mixer.music.stop()

        # Empieza la música ingame
        pg.mixer.music.load(os.path.join("resources", "sounds", "musica_ingame.ogg"))
        pg.mixer.music.play(-1)

        self.salir = False
        while not self.salir: 
            # Control de FPS
            self.reloj.tick(FPS)                       

            # Revisor de eventos
            self.revisa_eventos()

            # Refrescar posicion del jugador
            self.jugador.actualizaNave()
            # Colisiones con asteroides
            self.colision()
            
            # Movimiento del fondo
            x_relativa = self.x % self.fondo.get_rect().width
            self.pantalla.blit(self.fondo, (x_relativa - self.fondo.get_rect().width,self.y))
            if x_relativa < ANCHO:
                self.pantalla.blit(self.fondo, (x_relativa, 0))
            self.x -= 1           
            
            # Genera asteroides y los pinta
            self.asteroides.update()
            self.asteroides.draw(self.pantalla)            

            # Pintar jugador
            self.jugador.blitNave()
            #Texto Vidas
            self.contador_vidas()               
            # Actualizacion de la ventana
            pg.display.update()   

    def revisa_eventos(self):
        '''Aqui se revisara si hay eventos en el bucle principal'''
        for event in pg.event.get():
            # Opciones para salir del juego
            if event.type == pg.QUIT:
                    sys.exit()            
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    sys.exit()

            # Controles de la nave
            elif event.type == pg.KEYDOWN:
                self.revisa_keydown(event)
            elif event.type == pg.KEYUP:
                self.revisa_keyup(event)
    
    def revisa_keydown(self, event):
        '''Responde a las PULSACIONES de las teclas'''
        if event.key == pg.K_UP:
            self.jugador.mueve_arriba = True
        elif event.key == pg.K_DOWN:
            self.jugador.mueve_abajo = True

    def revisa_keyup(self, event):
        '''Responde a las LIBERACIONES de las teclas'''
        if event.key == pg.K_UP:
            self.jugador.mueve_arriba = False
        elif event.key == pg.K_DOWN:
            self.jugador.mueve_abajo = False
    
    def colision(self):
        colision_nave = pg.sprite.spritecollide(self.jugador, self.asteroides, True, pg.sprite.collide_circle)
        if colision_nave:
            self.vidas -= 1
            if self.vidas == 2:                
                self.asteroides.add(self.asteroide)
            elif self.vidas == 1:
                self.asteroides.add(self.asteroide)
            self.jugador.nave_imagen = pg.image.load(os.path.join("resources", "images", "explosion.png"))
            
        if self.jugador.mueve_abajo == True or self.jugador.mueve_arriba == True:
            self.jugador.nave_imagen = pg.image.load(os.path.join("resources", "images", "Main_Ship.png"))
            self.jugador.nave_imagen = pg.transform.rotate(self.jugador.nave_imagen, -90)
            self.jugador.nave_imagen = pg.transform.scale(self.jugador.nave_imagen, self.jugador.TAMAÑO_NAVE)
        if self.vidas == 0:
            pass
    
    def contador_vidas(self):
        render_fuente = self.fuente_vidas.render("VIDAS:", True, COLOR_TEXTO)
        rectangulo = render_fuente.get_rect()
        x = 50
        y = 20
        rectangulo.center = (x, y)
        self.pantalla.blit(render_fuente, rectangulo)

        render_num = self.fuente_vidas.render(str(self.vidas), True, COLOR_TEXTO)
        num_rect = render_num.get_rect()
        num_x = 100
        num_y = 20
        num_rect.center = (num_x, num_y)
        self.pantalla.blit(render_num, num_rect)