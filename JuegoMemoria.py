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

        # Secuencia y estados
        self.mostrando = True
        self.index_mostrando = 0
        self.tiempo_mostrado = 0
        self.tiempo_espera = 700

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
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for idx, rect in enumerate(self.Lista_Cuadros):
                            if rect.collidepoint(event.pos):
                                resultado = self.logica.verificar_click(idx)
                                if resultado == "error":
                                    print("Orden incorrecto")
                                    
                                    
                                elif resultado == "completo":
                                    pygame.time.delay(1000)
                                    self.nueva_secuencia()

            pygame.display.flip()
            self.timer.tick(self.fps)

    def ejecutar(self):
        self.iniciarVentana()


if __name__ == "__main__":
    juego = MemoryGame(600, 600, 6, 6)
    juego.ejecutar()