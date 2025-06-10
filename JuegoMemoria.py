import pygame
from logica_memoria import LogicaMemoria

class MemoryGame:
    def __init__(self, ancho, alto, filas, columnas):
        pygame.init()

        # Datos de la ventana
        self.ANCHO = ancho
        self.ALTO = alto
        self.FILAS = filas
        self.COLUMNAS = columnas

        # Colores
        self.BLANCO = (255, 255, 255)
        self.GRIS = (50, 50, 54)
        self.NEGRO = (0, 0, 0)
        self.VERDE = (19, 105, 16)
        self.VERDE_CLARO = (50, 200, 50)
        self.amarillodorado = (255, 221, 2) 
        self.AZUL = (50, 50, 255)
        self.ROJO = (255, 0, 0)

        # Pygame setup
        self.ventana = pygame.display.set_mode((700, 700))
        pygame.display.set_caption("Juego de Memoria")
        self.running = True
        self.fps = 60
        self.timer = pygame.time.Clock()

        # Cuadros
        self.Lista_Cuadros = []

        # Lógica del juego
        self.logica = LogicaMemoria()

        self.fuente_mensaje2 = pygame.font.SysFont(None, 35)

        # Secuencia y estados
        self.mostrando = True
        self.index_mostrando = 0
        self.tiempo_mostrado = 0
        self.tiempo_espera = 700

        self.tiempototal = 10
        self.tiempocuadros = 2

        self.mostrar_espera = False
        self.tiempo_pausa = 500  # Tiempo entre cuadros (milisegundos)

    #Esta funcion se encarga de dibujar los cuadros verdes
    def dibujar_fondo(self):
        self.Lista_Cuadros = []
        mouse_pos = pygame.mouse.get_pos() #Posicion del mouse en tiempo real

        for i in range(self.COLUMNAS):
            for j in range(self.FILAS):
                x = i * 115 + 28
                y = j * 90 + 20 # Posiciones de los cuadros, el "+35" es para que haya espacio entre estos
                ancho = 70
                alto = 70

                rect = pygame.Rect(x, y, ancho, alto)
                self.Lista_Cuadros.append(rect)

                # Dibujar en color claro si el mouse está encima
                color = self.VERDE_CLARO if rect.collidepoint(mouse_pos) else  self.VERDE
                    

                pygame.draw.rect(self.ventana, color, rect, 0, 15)

    def mostrar_secuencia(self):
        ahora = pygame.time.get_ticks()

        # ¿Estamos mostrando un cuadro de la secuencia?
        if self.index_mostrando < len(self.logica.get_secuencia()):
            if not self.mostrar_espera:
                # Mostrar cuadro por tiempo_espera
                if ahora - self.tiempo_mostrado >= self.tiempo_espera:
                    self.mostrar_espera = True
                    self.tiempo_mostrado = ahora
            else:
                # Esperar pausa y luego avanzar al siguiente
                if ahora - self.tiempo_mostrado >= self.tiempo_pausa:
                    self.index_mostrando += 1
                    self.mostrar_espera = False
                    self.tiempo_mostrado = ahora
        else:
            # ¡Ya se mostró toda la secuencia!
            self.mostrando = False  # Fin de animación

        # Dibujar los cuadros
        for i, rect in enumerate(self.Lista_Cuadros):
            # Solo iluminar si estamos mostrando, y es el cuadro actual
            if (not self.mostrar_espera and 
                self.index_mostrando < len(self.logica.get_secuencia()) and 
                i == self.logica.get_secuencia()[self.index_mostrando]):
                pygame.draw.rect(self.ventana, self.VERDE_CLARO, rect, 0, 15)
            else:
                pygame.draw.rect(self.ventana, self.VERDE, rect, 0, 15)

    def nueva_secuencia(self):
        self.logica.nueva_secuencia(len(self.Lista_Cuadros))
        self.mostrando = True
        self.index_mostrando = 0
        self.tiempo_mostrado = pygame.time.get_ticks()

    def iniciarVentana(self):
        self.dibujar_fondo()
        self.nueva_secuencia()

        while self.running:
            self.ventana.fill(self.GRIS)

            if self.mostrando:
                self.mostrar_secuencia()
            else:
                self.dibujar_fondo()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        return
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for idx, rect in enumerate(self.Lista_Cuadros):
                            if rect.collidepoint(event.pos):
                                resultado = self.logica.verificar_click(idx)
                                if resultado == "error":
                                    self.Fallo("Orden Incorrecto! :(")
                                    
                                    
                                elif resultado == "completo":
                                    pygame.time.delay(1000)
                                    self.nueva_secuencia()
            self.ShowLevel()

            pygame.display.flip()
            self.timer.tick(self.fps)


    def ShowLevel(self):
        
        nivel_mjs = pygame.Rect(50, 600, 145, 35)
        pygame.draw.rect(self.ventana, self.amarillodorado, nivel_mjs, 5, 10)
        nivel = self.logica.get_nivel()
        nivel_texto = self.fuente_mensaje2.render(f"Nivel: {nivel}",True, self.amarillodorado)
        self.ventana.blit(nivel_texto,(60, 605))

    def Fallo(self, mensaje): # Esta funcion se llama al momento de que el jugador falla en el patron
        fuente_grande = pygame.font.SysFont(None, 72)
        fuente_botones = pygame.font.SysFont(None, 36)
        volver_jugar = pygame.Rect(400, 500, 200, 50)
        volver_menu = pygame.Rect(100, 500, 200, 50)

        while True: #Se crea un nuevo bucle
            self.ventana.fill(self.BLANCO) #Con fondo blanco (Todo lo demas se borra)

            # Mensaje de que fallo
            texto = fuente_grande.render(mensaje, True, self.VERDE)
            texto_rect = texto.get_rect(center=(350, 200))
            self.ventana.blit(texto, texto_rect)

            # Botón volver a jugar
            pygame.draw.rect(self.ventana, self.AZUL, volver_jugar)
            texto_volver = fuente_botones.render("Volver a jugar", True, self.BLANCO)
            rect_volver = texto_volver.get_rect(center=volver_jugar.center)
            self.ventana.blit(texto_volver, rect_volver)

            # Botón volver al menú
            pygame.draw.rect(self.ventana, self.ROJO, volver_menu)
            texto_menu = fuente_botones.render("Menú principal", True, self.BLANCO)
            rect_menu = texto_menu.get_rect(center=volver_menu.center)
            self.ventana.blit(texto_menu, rect_menu)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if volver_jugar.collidepoint(evento.pos): # Se dectecta la posicion de los clicks
                        self.__init__(self.ANCHO, self.ALTO, self.FILAS, self.COLUMNAS)
                        
                        return
                    elif volver_menu.collidepoint(evento.pos):
                        from Menu import MenuPrincipal  # Asegurate que esto exista
                        menu = MenuPrincipal()
                        menu.ejecutar()
                        return
        
         
       
    def ejecutar(self):
        self.iniciarVentana()


if __name__ == "__main__":
    juego = MemoryGame(600, 600, 6, 6)
    juego.ejecutar()