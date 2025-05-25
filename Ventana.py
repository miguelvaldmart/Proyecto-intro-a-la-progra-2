import pygame
import sys
from Logica import Tablero

#Este archivo se encarga de la parte grafica, donde se muestra un tablero de 6x6 cuadrados, que pueden variar entre gris o verde si se tocan
# Inicialización
pygame.init()

# Configuración
ANCHO, ALTO = 600, 600
FILAS, COLUMNAS = 6, 6
TAM_CASILLA = ANCHO // COLUMNAS

# Colores
BLANCO = (255, 255, 255)
GRIS = (180, 180, 180)
VERDE = (0, 200, 0)
AZUL = (50, 50, 255)

# Ventana
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Lógica")

# Crear tablero lógico
tablero = Tablero(FILAS, COLUMNAS)

# Crear rectángulos de cada celda
rectangulos = []
for fila in range(FILAS):
    fila_rectangulos = []
    for columna in range(COLUMNAS):
        rect = pygame.Rect(columna * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
        fila_rectangulos.append(rect)
    rectangulos.append(fila_rectangulos)

# Bucle principal
clock = pygame.time.Clock()
corriendo = True
seleccionados = []
while corriendo:
    pantalla.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            fila = y // TAM_CASILLA
            columna = x // TAM_CASILLA
            tablero.alternar_boton(fila, columna)
            seleccionados += [tablero.Id_cuadro(fila,columna)]
            if len(seleccionados) == 2:
                if seleccionados[0] == seleccionados[1]:
                    print("iguales")
                    seleccionados = []
                else:
                    print("diferentes")
                    seleccionados = []
            
    
    # Dibujar los botones
    for fila in range(FILAS):
        for columna in range(COLUMNAS):
            color = VERDE if tablero.esta_activo(fila, columna) else GRIS
            pygame.draw.rect(pantalla, color, rectangulos[fila][columna])
            pygame.draw.rect(pantalla, AZUL, rectangulos[fila][columna], 2)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()