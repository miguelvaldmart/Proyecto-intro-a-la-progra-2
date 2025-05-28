import pygame
import sys
from Ventana import Ventana

pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Menú Principal")

# Colores 
AZUL = (70, 130, 180)          
AZUL_OSCURO = (40, 90, 140)   
GRIS_CLARO = (230, 230, 230)
GRIS_OSCURO = (180, 180, 180)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)

# Fuente estilizada
fuente = pygame.font.SysFont("arial", 32, bold=True)

# Botones como rectángulos
boton1 = pygame.Rect(200, 100, 220, 60)
boton2 = pygame.Rect(200, 200, 220, 60)

# Bucle principal del menú
clock = pygame.time.Clock()
corriendo = True
while corriendo:
    pantalla.fill(GRIS_OSCURO)
    mouse_pos = pygame.mouse.get_pos()

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if boton1.collidepoint(evento.pos):
                juego = Ventana(600, 600, 6, 6)
                juego.ejecutar()
            elif boton2.collidepoint(evento.pos):
                print("Siguiente Juego que Vamos que hay que Crear")


    # Botón 1 - Juego 2 contra 2
    if boton1.collidepoint(mouse_pos):
        color_boton1 = AZUL_OSCURO 
    else:
        color_boton1 = AZUL
    pygame.draw.rect(pantalla, color_boton1, boton1, border_radius=12)
    texto1 = fuente.render("Hallar parejas", True, BLANCO)
    pantalla.blit(texto1, texto1.get_rect(center=boton1.center))

    # Botón 2 - Juego de memoria (a futuro)
    if boton2.collidepoint(mouse_pos):
        color_boton2 = AZUL_OSCURO 
    else:
        color_boton2 = AZUL
    pygame.draw.rect(pantalla, color_boton2, boton2, border_radius=12)
    texto2 = fuente.render("Memoria", True, NEGRO)
    pantalla.blit(texto2, texto2.get_rect(center=boton2.center))

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()