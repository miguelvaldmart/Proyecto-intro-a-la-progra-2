import pygame
import sys
from Logica import Tablero

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
        self.ROJO = (255, 0, 0)

        # Ventana
        self.pantalla = pygame.display.set_mode((1300, 800))
        pygame.display.set_caption("Juego de Lógica")

        # Lógica
        self.tablero = Tablero(self.FILAS, self.COLUMNAS)
        self.tablero1 = Tablero(self.FILAS, self.COLUMNAS)
        self.rectangulos = self.crear_rectangulos(0)
        self.rectangulos1 = self.crear_rectangulos(7)
        self.clock = pygame.time.Clock()
        self.seleccionados = []
        self.cordenadas_seleccionados = []
        self.corriendo = True

        #Mensajes en pantalla
        self.mensaje = ""
        self.tiempo_mensaje = 0
        self.fuente_mensaje = pygame.font.SysFont(None, 28)

    def mostrar_mensaje(self, texto):
        self.mensaje = texto
        self.tiempo_mensaje = pygame.time.get_ticks()

    def crear_rectangulos(self, offset_columna):
        rectangulos = []
        for fila in range(self.FILAS):
            fila_rect = []
            for columna in range(self.COLUMNAS):
                rect = pygame.Rect(
                    (columna + offset_columna) * self.TAM_CASILLA,
                    fila * self.TAM_CASILLA,
                    self.TAM_CASILLA,
                    self.TAM_CASILLA
                )
                fila_rect.append(rect)
            rectangulos.append(fila_rect)
        return rectangulos

    def Juego_memoria(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                fila = y // self.TAM_CASILLA
                columna = x // self.TAM_CASILLA

                # Verificamos si ya fue descubierta permanentemente
                if self.tablero.esta_descubierto(fila, columna) or self.tablero1.esta_descubierto(fila, columna):
                    self.mostrar_mensaje("Casilla ya encontrada, no se puede tocar.")
                    return

                # Verificamos si ya fue seleccionada en este turno
                if (fila, columna) in self.cordenadas_seleccionados:
                    self.mostrar_mensaje("Casilla ya seleccionada, escoge otra.")
                    return

                # Activar la casilla
                if columna<= 6:
                    self.tablero.alternar_boton(fila, columna)
                    valor = self.tablero.Id_cuadro(fila, columna)
                else:
                    self.tablero1.alternar_boton(fila, columna)
                    valor = self.tablero1.Id_cuadro(fila, columna)
                self.seleccionados.append(valor)
                self.cordenadas_seleccionados.append((fila, columna))

                # Comparar si hay dos seleccionadas
                if len(self.seleccionados) == 2:
                    f1, c1 = self.cordenadas_seleccionados[0]
                    f2, c2 = self.cordenadas_seleccionados[1]

                    if self.seleccionados[0] == self.seleccionados[1]:
                        print("iguales")
                        self.tablero.marcar_descubierto(f1, c1, f2, c2)
                    else:
                        print("diferentes")
                        self.dibujar_juego_memoria()
                        pygame.display.flip()
                        pygame.time.delay(1000)
                        self.tablero.alternar_boton(f1, c1)
                        self.tablero.alternar_boton(f2, c2)

                    # Limpiar listas al final
                    self.seleccionados = []
                    self.cordenadas_seleccionados = []

    #Dibuja dos matrices
    def dibujar_juego_memoria(self):
        self.pantalla.fill(self.BLANCO)
        fuente = pygame.font.SysFont(None, 36)  # Fuente por defecto, tamaño 36

        # Dibujar primera matriz
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                rect = self.rectangulos[fila][columna]
                activo = self.tablero.esta_activo(fila, columna)
                color = self.VERDE if activo else self.GRIS

                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, self.AZUL, rect, 2)

                if activo:
                    numero = self.tablero.get_respuesta()[fila][columna]
                    texto = fuente.render(str(numero), True, (0, 0, 0))
                    texto_rect = texto.get_rect(center=rect.center)
                    self.pantalla.blit(texto, texto_rect)

        # Dibujar segunda matriz
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                rect = self.rectangulos1[fila][columna]
                activo = self.tablero1.esta_activo(fila, columna)
                color = self.VERDE if activo else self.GRIS

                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, self.AZUL, rect, 2)

                if activo:
                    numero = self.tablero1.get_respuesta()[fila][columna]
                    texto = fuente.render(str(numero), True, (0, 0, 0))
                    texto_rect = texto.get_rect(center=rect.center)
                    self.pantalla.blit(texto, texto_rect)

        # Mostrar mensaje si existe
        if self.mensaje:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_mensaje < 1500:
                rect_mensaje = pygame.Rect(100, 20, 400, 50)
                pygame.draw.rect(self.pantalla, self.BLANCO, rect_mensaje)
                pygame.draw.rect(self.pantalla, self.ROJO, rect_mensaje, 2)

                texto_render = self.fuente_mensaje.render(self.mensaje, True, (0, 0, 0))
                texto_rect = texto_render.get_rect(center=rect_mensaje.center)
                self.pantalla.blit(texto_render, texto_rect)
            else:
                self.mensaje = ""

        pygame.display.flip()

    def dibujar_juego_secuencia(self):
        self.pantalla.fill(self.BLANCO)
        fuente = pygame.font.SysFont(None, 36)  # Fuente por defecto, tamaño 36

        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                rect = self.rectangulos[fila][columna]
                activo = self.tablero.esta_activo(fila, columna)
                color = self.VERDE if activo else self.GRIS

                # Dibujar el rectángulo
                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, self.AZUL, rect, 2)

                # Si está activo, mostrar el número
                if activo:
                    numero = self.tablero.get_respuesta()[fila][columna]
                    texto = fuente.render(str(numero), True, (0, 0, 0))  # Negro
                    texto_rect = texto.get_rect(center=rect.center)
                    self.pantalla.blit(texto, texto_rect)
                
                if self.mensaje:
                    tiempo_actual = pygame.time.get_ticks()
                    if tiempo_actual - self.tiempo_mensaje < 1500:  # Mostrar por 1 segundo

                        # Fondo blanco con borde azul
                        rect_mensaje = pygame.Rect(100, 20, 400, 50)
                        pygame.draw.rect(self.pantalla, self.BLANCO, rect_mensaje)
                        pygame.draw.rect(self.pantalla, self.ROJO, rect_mensaje, 2)

                        # Renderizar texto y centrarlo dentro de la caja
                        texto_render = self.fuente_mensaje.render(self.mensaje, True, (0, 0, 0))
                        texto_rect = texto_render.get_rect(center=rect_mensaje.center)
                        self.pantalla.blit(texto_render, texto_rect)
                    else:
                        self.mensaje = ""  # Ocultar mensaje
        pygame.display.flip()


    def ejecutar(self):
        while self.corriendo:
            self.Juego_memoria()
            self.dibujar_juego_memoria()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

# Para ejecutar el juego:
if __name__ == "__main__":
    juego = Ventana(600,600,6,6)
    juego.ejecutar()