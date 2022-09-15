# Importaciones necesarias para el funcionamiento del juego

import random
import sys
import os
from time import sleep
from random import randrange

import pygame as pg

from . import ANCHO, ALTO, COLOR_TEXTO, FPS
from .configuracion import Config
from .entidades import Nave, Asteroide, Planeta, NaveVictoriosa
from .estadisticas_juego import GameStats
from .puntuaciones import Puntuaciones

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
        self.config = Config()
        # Instancia para guardar las estadisticas del juego y crear un marcador
        self.estadisticas = GameStats(self)
        self.puntuacion = Puntuaciones(self)
        
        # Banderilla para victoria
        self.victoria = False

        # Fondo del juego
        self.fondo = pg.image.load(os.path.join("resources", "images", "fondo_juego.png"))        
        self.x = 0
        self.y = 0

        # Fuente para las vidas, marcador y game over
        fuente = os.path.join("resources", "fonts", "Arcadia.ttf")
        self.fuente_vidas = pg.font.Font(fuente, 20)
        self.fuente_game_over = pg.font.Font(fuente, 50)
        self.fuente_nivel2 = pg.font.Font(fuente, 50)

        # Instanciamos la clase Nave
        self.jugador = Nave(self) 
        # Instancio Imagen de misma nave, pero para animacion de victoria      
        self.nave_ganadora = NaveVictoriosa(self)
        # Instancia de grupos de asteroides, generamos 10
        self.asteroides = pg.sprite.Group()

        for i in range(5):
            self.asteroide = Asteroide(self)
            self.asteroides.add(self.asteroide)
        
        # Instancia de la clase planeta
        self.planeta = Planeta(self)

        
    def bucle_principal(self):
        '''Este es el bucle principal'''
        # Frena la música del menú
        pg.mixer.music.stop()

        # Empieza la música ingame
        pg.mixer.music.load(os.path.join("resources", "sounds", "musica_ingame.ogg"))
        pg.mixer.music.play(-1)

        # Medidor de tiempo
        tiempo_juego = pg.time.get_ticks()

        self.salir = False
        while not self.salir:                                       

            # Revisor de eventos
            self.revisa_eventos()
            self.control_juego_ganado()

            if self.estadisticas.juego_activo:
                # Control de FPS
                self.reloj.tick(FPS)                  
                # Contador de ticks
                self.tiempo_actual = (pg.time.get_ticks() - tiempo_juego)//1000

                # Refrescar posicion del jugador
                self.jugador.actualizaNave()


                # Movimiento del fondo
                x_relativa = self.x % self.fondo.get_rect().width
                self.pantalla.blit(self.fondo, (x_relativa - self.fondo.get_rect().width,self.y))
                if x_relativa < ANCHO:
                    self.pantalla.blit(self.fondo, (x_relativa, 0))
                self.x -= 1           
                if self.victoria == False:
                    # Colisiones con asteroides
                    self.colision()
                    # Genera asteroides y los pinta y cuenta puntos
                    self.asteroides.update()
                    # Pintar jugador
                    self.jugador.blitNave()
                
                self.asteroides.draw(self.pantalla)

                # Pinta la puntuacion
                self.puntuacion.mostrar_puntuacion()                      
                                
                # Comprueba y ejecuta nivel 2
                self.nivel2()

                # Comprueba y ejecuta la victoria
                self.ganar_partida()                

                # Texto Vidas
                self.contador_vidas()   

                # Metodo para comprobar el game over
                self.game_over()

                # Actualizacion de la ventana
                pg.display.update()   

    def revisa_eventos(self):
        '''Aqui se revisara si hay eventos en el bucle principal'''
        if self.victoria == False:
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

    def control_juego_ganado(self):
        '''Estas teclas solo se habilitaran cuando el juego se haya ganado'''
        if self.victoria == True:
            for event in pg.event.get():
                # Opciones para salir del juego
                if event.type == pg.QUIT:
                        sys.exit()            
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        sys.exit()

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
            
    def colision(self): #FIXME Añadir tiempo de colision
        '''Este metodo detecta las colisones que 
        se producen en la nave con los asteroides y resta vidas'''       
        self.colision_nave = pg.sprite.spritecollide(self.jugador, self.asteroides, False, pg.sprite.collide_circle)
        if self.colision_nave:
            self.momento_colision = pg.time.get_ticks()//1000
            self.jugador.nave_imagen = pg.image.load(os.path.join("resources", "images", "explosion.png"))
            print(f'Tiempo actual: {self.tiempo_actual} Momento de colision: {self.momento_colision}')
            if self.tiempo_actual - self.momento_colision < 2000:
                self.nave_imagen = pg.image.load(os.path.join("resources", "images", "Main_Ship.png"))
            # Sonido de la colision
            impacto = pg.mixer.Sound(os.path.join("resources", "sounds" ,"impact.ogg"))
            pg.mixer.Sound.set_volume(impacto, 1)
            pg.mixer.Sound.play(impacto)
            # Disminuye las vidas
            self.estadisticas.vidas_restantes -= 1
            # Comprueba si las vidas llegan a 0 para activar el game over
            if self.estadisticas.vidas_restantes == 0:
                self.estadisticas.juego_activo = False
            # Se deshace de los meteoritos en pantalla
            self.asteroides.empty()
            # Crea de nuevo los meteoritos
            for i in range(10):
                self.asteroide = Asteroide(self)               
                self.asteroides.add(self.asteroide)
            # Una pausa para volver retomar el juego
            #sleep(1)
    def refresca_colison(self):        
        if self.tiempo_actual - self.momento_colision < 2000:
            self.nave_imagen = pg.image.load(os.path.join("resources", "images", "Main_Ship.png"))
    
    def contador_vidas(self):
        '''Metodo para cargar y mostrar el contador de vidas'''
        render_fuente = self.fuente_vidas.render("VIDAS:", True, COLOR_TEXTO)
        rectangulo = render_fuente.get_rect()
        x = 50
        y = 20
        rectangulo.center = (x, y)
        self.pantalla.blit(render_fuente, rectangulo)

        # Esta parte hace funcional el numero de vidas
        render_num = self.fuente_vidas.render(str(self.estadisticas.vidas_restantes), True, COLOR_TEXTO)
        num_rect = render_num.get_rect()
        num_x = 100
        num_y = 20
        num_rect.center = (num_x, num_y)
        self.pantalla.blit(render_num, num_rect)   

    def game_over(self):
        '''En este metodo habilitamos la comprobacion del game over
        con lo que se genera un mensaje y detiene el juego'''

        mensaje1 = "HAS PERDIDO"
        mensaje2 = "Pulsa (ESC) para salir del juego"
        if self.estadisticas.juego_activo == False:
            render_msg1 = pg.font.Font.render(self.fuente_game_over, mensaje1, True, COLOR_TEXTO)
            render_msg2 = pg.font.Font.render(self.fuente_game_over, mensaje2, True, COLOR_TEXTO)
            
            msg1_width = render_msg1.get_width()
            msg2_width = render_msg2.get_width()

            msg1_x = (ANCHO - msg1_width)/2
            msg2_x = (ANCHO - msg2_width)/2

            self.pantalla.blits(
            [(render_msg1, (msg1_x, ALTO - 600)),
               (render_msg2, (msg2_x, ALTO - 500))])
    
    def nivel2(self): #FIXME Reparar texto emergente del nivel 2
        if self.estadisticas.puntuacion > 50:                       
            msg_leve2 = "NIVEL 2"
            self.render_msg = pg.font.Font.render(self.fuente_nivel2, msg_leve2, True, COLOR_TEXTO)                        
            self.rect_textlevel = self.render_msg.get_rect()
            self.rect_textlevel.y = ALTO - 600
            self.rect_textlevel.x = (ANCHO - self.rect_textlevel.width)/2
            self.rect_textlevel.y += 10

            self.pantalla.blit(self.render_msg, self.rect_textlevel)
            self.asteroide.velocidad_x = random.randrange(10, 15)
    
    def ganar_partida(self): #TODO Crear la condicion de victoria, hacer aparecer el planeta
        if self.estadisticas.puntuacion > 100:
            self.victoria = True
            self.planeta.blit_planeta()            
            self.planeta.planeta_rect.x -= self.planeta.velocidad_x
            if self.planeta.planeta_rect.left < ANCHO - 300:
                self.planeta.velocidad_x = 0

            self.nave_ganadora.blitNaveWin()
            self.nave_ganadora.rect.x += self.nave_ganadora.velocidad_x
            if self.nave_ganadora.rect.right == ANCHO - 300:
                self.nave_ganadora.velocidad_x = 0
            
           
   
           



