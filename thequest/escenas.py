# Importaciones necesarias para el funcionamiento del juego

import random
import sys
import os
from time import sleep
from random import randrange

import pygame as pg

from . import ANCHO, ALTO, COLOR_TEXTO, FPS
from .configuracion import Config
from .entidades import Nave, Asteroide, Planeta, NaveVictoriosa, TextoNivel2
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
        self.texto_level2 = TextoNivel2(self)
        # Banderilla para victoria
        self.victoria = False

        # Fondo del juego
        self.fondo = pg.image.load(os.path.join("resources", "images", "fondo_juego.png"))        
        self.x = 0
        self.y = 0
    
        # Fuente para las vidas, marcador y game over
        fuente = os.path.join("resources", "fonts", "Arcadia.ttf")
        self.fuente_vidas_final = pg.font.Font(fuente, 20)
        self.fuente_game_over_win = pg.font.Font(fuente, 50)
        

        # Instanciamos la clase Nave
        self.jugador = Nave(self) 
        # Instancio Imagen de misma nave, pero para animacion de victoria      
        self.nave_ganadora = NaveVictoriosa(self)
        # Instancia de grupos de asteroides, generamos 10
        self.asteroides = pg.sprite.Group()

        for i in range(10):
            self.asteroide = Asteroide(self)
            self.asteroides.add(self.asteroide)
        
        # Instancia de la clase planeta
        self.planeta = Planeta(self)

        # Creo variables para hacer contadores necesarios
        self.momento_colision = 0
        self.momento_victoria = 0

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
                    # Genera asteroides y cuenta puntos
                    self.asteroides.update()
                    # Pintar jugador
                    self.jugador.blitNave()

                # Esta parte permite a la nave volver a su estado normal en medio segundo
                self.refresca_colision()                

                # Pinta los asteroides del grupo
                self.asteroides.draw(self.pantalla)

                # Pinta la puntuacion
                self.puntuacion.mostrar_puntuacion()                      
                                
                # Comprueba y ejecuta nivel 2
                self.nivel2()

                # Comprueba y ejecuta la victoria
                self.ganar_partida()  

                # Emerge un texto despues de unos segundos de haber ganado
                self.textoVictoria()        

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
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        sys.exit()                
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.salir = True

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
        '''Este metodo detecta las colisones que 
        se producen en la nave con los asteroides y resta vidas'''       
        self.colision_nave = pg.sprite.spritecollide(self.jugador, self.asteroides, False, pg.sprite.collide_circle)
        # Captura de los ticks en la colision y cambio del estado de la nave a explosion
        if self.colision_nave:
            self.momento_colision = pg.time.get_ticks()//1000
            self.jugador.nave_imagen = pg.image.load(os.path.join("resources", "images", "explosion.png"))
           
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
    
    def refresca_colision(self):
        '''Cuenta medio segundo y vuelve la imagen de la nave'''
        if self.tiempo_actual - self.momento_colision > 0.5:
            self.jugador.nave_imagen = pg.image.load(os.path.join("resources", "images", "Main_Ship.png"))
            self.jugador.nave_imagen = pg.transform.rotate(self.jugador.nave_imagen, -90)
            self.jugador.nave_imagen = pg.transform.scale(self.jugador.nave_imagen, self.jugador.TAMAÑO_NAVE)

    def contador_vidas(self):
        '''Metodo para cargar y mostrar el contador de vidas'''
        render_fuente = self.fuente_vidas_final.render("VIDAS:", True, COLOR_TEXTO)
        rectangulo = render_fuente.get_rect()
        x = 50
        y = 20
        rectangulo.center = (x, y)
        self.pantalla.blit(render_fuente, rectangulo)

        # Esta parte hace funcional el numero de vidas
        render_num = self.fuente_vidas_final.render(str(self.estadisticas.vidas_restantes), True, COLOR_TEXTO)
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
            render_msg1 = pg.font.Font.render(self.fuente_game_over_win, mensaje1, True, COLOR_TEXTO)
            render_msg2 = pg.font.Font.render(self.fuente_game_over_win, mensaje2, True, COLOR_TEXTO)
            
            msg1_width = render_msg1.get_width()
            msg2_width = render_msg2.get_width()

            msg1_x = (ANCHO - msg1_width)/2
            msg2_x = (ANCHO - msg2_width)/2

            self.pantalla.blits(
            [(render_msg1, (msg1_x, ALTO - 600)),
               (render_msg2, (msg2_x, ALTO - 500))])
    
    def nivel2(self):
        '''Crea un texto emergente que avisa de nivel 2 alcanzado, y
        aumenta la velocidad con la que son generados los asteroides'''
        if self.estadisticas.puntuacion > 1000:                       
            self.asteroide.velocidad_x = random.randrange(10, 15)
            self.texto_level2.blitNivel2Text()
            self.texto_level2.rect_textlevel.y += self.texto_level2.velocidad_y
            if self.texto_level2.rect_textlevel.top > ALTO - 550:
                self.texto_level2.velocidad_y = 0
                if self.texto_level2.velocidad_y == 0:
                    self.texto_level2.rect_textlevel.x -= self.texto_level2.velocidad_x
                
            
    
    def ganar_partida(self): #FIXME Terminar la animacion de victoria
        if self.estadisticas.puntuacion > 200:                                 
            self.victoria = True            
            self.planeta.blit_planeta()            
            self.planeta.planeta_rect.x -= self.planeta.velocidad_x
            if self.planeta.planeta_rect.left < ANCHO - 300:
                self.planeta.velocidad_x = 0

            self.nave_ganadora.blitNaveWin()
            self.nave_ganadora.rect.x += self.nave_ganadora.velocidad_x
            if self.nave_ganadora.rect.right == ANCHO - 300:
                self.nave_ganadora.velocidad_x = 0
                if self.nave_ganadora.velocidad_x == 0:
                    """ for grados in range(0, 180): # Esto peta el juego
                        self.nave_ganadora.angulo += grados                    
                        self.nave_ganadora.nave_imagen = (pg.transform.rotate(self.nave_ganadora.nave_imagen, self.nave_ganadora.angulo))
                        print(grados) """


    def textoVictoria(self):
        print(f'Tiempo actual: {self.tiempo_actual} Momento Victoria: {self.momento_victoria}')
        if self.nave_ganadora.rect.right == ANCHO - 300:
            mensaje = "HAS GANADO LA PARTIDA"
            texto_render = pg.font.Font.render(self.fuente_game_over_win, mensaje, True, COLOR_TEXTO)
            texto_ancho = texto_render.get_width()                    
            pos_x = (ANCHO - texto_ancho)/2
            pos_y = ALTO - 650
            self.pantalla.blit(texto_render, (pos_x, pos_y))

            mensaje2 = "Pulsa (Space) para continuar"
            texto_render2 = pg.font.Font.render(self.fuente_vidas_final, mensaje2, True, COLOR_TEXTO)
            texto_ancho2 = texto_render2.get_width()                    
            pos_x2 = (ANCHO - texto_ancho2)/2
            pos_y2 = ALTO - 550
            self.pantalla.blit(texto_render2, (pos_x2, pos_y2))
   
class HallOfFame(Escena):
    def __init__(self, pantalla: pg.Surface):
        super().__init__(pantalla)
        self.fondo_portada = pg.image.load(os.path.join("resources", "images", "fondo.png"))
        self.fuente_direccion = os.path.join("resources", "fonts", "Arcadia.ttf")
        self.fuente_puntuacion = pg.font.Font(self.fuente_direccion, 50)

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
            self.textoSuperior()
                                
            pg.display.flip()
    
    def textoSuperior(self):
        '''Pinta el texto superior de la pantalla Score'''
        mensaje = "PUNTUACION GLOBAL"
        texto_render = pg.font.Font.render(self.fuente_puntuacion, mensaje, True, COLOR_TEXTO)
        texto_ancho = texto_render.get_width()
        pos_x = (ANCHO - texto_ancho)/2
        pos_y = ALTO - 650
        self.pantalla.blit(texto_render, (pos_x, pos_y))

    def textoInferior(self):
        pass