import pygame
import sys
from Logica import Tablero, Boton

class Ventana:
    def __init__(self, ancho, alto, filas, columnas):
        pygame.init()

        self.ANCHO = ancho
        self.ALTO = alto
        self.FILAS = filas
        self.COLUMNAS = columnas
        self.TAM_CASILLA = ancho // columnas

        # Colores
        self.BLANCO = (255, 255, 255)
        self.GRIS = (180, 180, 180)
        self.VERDE = (0, 200, 0)
        self.AZUL = (50, 50, 255)

        # Ventana
        self.pantalla = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("Juego de Lógica")

        # Lógica
        self.tablero = Tablero(self.FILAS, self.COLUMNAS)
        self.rectangulos = self.crear_rectangulos()
        self.clock = pygame.time.Clock()
        self.seleccionados = []

    def crear_rectangulos(self):
        rectangulos = []
        for fila in range(self.FILAS):
            fila_rect = []
            for columna in range(self.COLUMNAS):
                rect = pygame.Rect(
                    columna * self.TAM_CASILLA,
                    fila * self.TAM_CASILLA,
                    self.TAM_CASILLA,
                    self.TAM_CASILLA
                )
                fila_rect.append(rect)
            rectangulos.append(fila_rect)
        return rectangulos

    def manejar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos
                fila = y // self.TAM_CASILLA
                columna = x // self.TAM_CASILLA
                self.tablero.alternar_boton(fila, columna)

                if self.tablero.esta_activo(fila, columna):
                    self.seleccionados.append(self.tablero.Id_cuadro(fila, columna))

                if len(self.seleccionados) == 2:
                    if self.seleccionados[0] == self.seleccionados[1]:
                        print("iguales")
                    else:
                        print("diferentes")
                        for i in range(len(self.tablero.get_respuesta())):
                            for j in range(len(self.tablero.get_respuesta()[0])):
                                if (self.tablero.get_respuesta()[i][j] in self.seleccionados and 
                                        not self.tablero.esta_activo(i, j)):
                                    self.tablero.alternar_boton(fila, columna)
                    self.seleccionados = []
                
        return True

    def dibujar(self):
        self.pantalla.fill(self.BLANCO)
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                color = self.VERDE if self.tablero.esta_activo(fila, columna) else self.GRIS
                pygame.draw.rect(self.pantalla, color, self.rectangulos[fila][columna])
                pygame.draw.rect(self.pantalla, self.AZUL, self.rectangulos[fila][columna], 2)
        pygame.display.flip()

    def ejecutar(self):
        corriendo = True
        while corriendo:
            corriendo = self.manejar_eventos()
            self.dibujar()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

# Para ejecutar el juego:
if __name__ == "__main__":
    juego = Ventana(600,600,6,6)
    juego.ejecutar()