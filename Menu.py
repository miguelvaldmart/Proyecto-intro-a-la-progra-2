import pygame
import sys
from Ventana import Ventana
from JuegoMemoria import MemoryGame
from APIBCCR import TipoCambioBCCR
import requests


class MenuPrincipal:
    def __init__(self):
        pygame.init()
        self.ANCHO, self.ALTO = 600, 400
        self.pantalla = pygame.display.set_mode((self.ANCHO, self.ALTO))
        pygame.display.set_caption("Menú Principal")
        self.clock = pygame.time.Clock()

        # Colores
        self.AZUL = (70, 130, 180)
        self.AZUL_OSCURO = (40, 90, 140)
        self.GRIS_CLARO = (230, 230, 230)
        self.GRIS_OSCURO = (180, 180, 180)
        self.NEGRO = (0, 0, 0)
        self.BLANCO = (255, 255, 255)
        self.VERDE = (0, 200, 25)
        self.VERDE_CLARO = (50, 220, 70)


        # Fuente
        self.fuente = pygame.font.SysFont("arial", 32, bold=True)

        # Botones
        self.boton1 = pygame.Rect(200, 100, 220, 60)
        self.boton2 = pygame.Rect(200, 200, 220, 60)
        self.boton3 = pygame.Rect(200, 0, 220, 60)

    def dibujar_boton(self, rect, texto, color_texto, activo):
        color = self.AZUL_OSCURO if activo else self.AZUL
        pygame.draw.rect(self.pantalla, color, rect, border_radius=12)
        texto_render = self.fuente.render(texto, True, color_texto)
        self.pantalla.blit(texto_render, texto_render.get_rect(center=rect.center))

    def BotonTipoCambio(self, rect, texto, color_texto, activo):
        color = self.VERDE_CLARO if activo else self.VERDE
        pygame.draw.rect(self.pantalla, color, rect, border_radius=12)
        texto_render = self.fuente.render(texto, True, color_texto)
        self.pantalla.blit(texto_render, texto_render.get_rect(center=rect.center))


    def ejecutar(self):
        corriendo = True
        while corriendo:
            self.pantalla.fill(self.GRIS_OSCURO)
            mouse_pos = pygame.mouse.get_pos()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if self.boton1.collidepoint(evento.pos):
                        juego = Ventana(600, 600, 6, 6)
                        juego.ejecutar()
                    if self.boton2.collidepoint(evento.pos):
                        memoria = MemoryGame(600, 600, 6, 6)
                        memoria.ejecutar()
                    if self.boton3.collidepoint(evento.pos):
                        correo = "cuentacoc1er@gmail.com"
                        token = "AAAOLNP5CM"
                        cambio = TipoCambioBCCR(correo, token)
                        try: # El try es por si hay un error al consultar el servicio
                            compra = cambio.obtener_compra()
                            venta = cambio.obtener_venta()

                            print(f"Tipo de cambio de compra: {compra}")
                            print(f"Tipo de cambio de venta: {venta}")
                        except requests.RequestException as e: # si hay un error al hacer la petición cae aquí
                            print(f"Error al consultar el servicio del BCCR: {e}")

            # Dibujar botones
            self.dibujar_boton(self.boton1, "Hallar parejas", self.BLANCO, self.boton1.collidepoint(mouse_pos))
            self.dibujar_boton(self.boton2, "Memoria", self.NEGRO, self.boton2.collidepoint(mouse_pos))
            self.BotonTipoCambio(self.boton3, "Tipo cambio", self.GRIS_CLARO, self.boton3.collidepoint(mouse_pos))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

# Ejecutar el menú si este archivo es el principal
if __name__ == "__main__":
    menu = MenuPrincipal()
    menu.ejecutar()


