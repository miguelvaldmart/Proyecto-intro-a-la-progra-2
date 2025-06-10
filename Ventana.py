import pygame
import sys
from Logica import Tablero
from jugador import Jugador
from PIL import Image
import os
class Ventana:
    def __init__(self, ancho, alto, filas, columnas):
        pygame.init()
        
        #Parametros de la ventana y los cuadros de las matrices
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
        self.negro = (0,0,0)

        # Ventana
        self.pantalla = pygame.display.set_mode((1300, 800))
        pygame.display.set_caption("Juego de Lógica")

        # Lógica
        self.tablero = Tablero(self.FILAS, self.COLUMNAS)
        self.tablero1 = Tablero(self.FILAS, self.COLUMNAS)
        self.rectangulos = self.crear_rectangulos(0)
        self.rectangulos1 = self.crear_rectangulos(7)
        self.clock = pygame.time.Clock()
        self.lista_coordenadas = []
        self.lista_seleccionados = []
        
        # Jugador 1
        self.seleccionados_j1 = []
        self.coordenadas_j1 = []
        self.intentos_j1 = -1
        self.escontrados_j1 = 0


        # Jugador 2
        self.seleccionados_j2 = []
        self.coordenadas_j2 = []
        self.intentos_j2 = 0
        self.escontrados_j2 = 0

        self.contador_turno = 0

        self.jugadores = Jugador()

        self.corriendo = True
        

        #Mensajes en pantalla
        self.mensaje = ""
        self.tiempo_mensaje = 0
        self.fuente_mensaje = pygame.font.SysFont(None, 28)
        self.fuente_mensaje2 = pygame.font.SysFont(None, 35)
        self.fuente_mensaje3 = pygame.font.SysFont(None, 45)
        

        #Tiempo
        self.inicio_tiempo = 0
        self.tiempo_limite = 0
        self.tiempo_transcurrido = 10000



        #Imagenes
        self.imagenes = self.carga_imagenes()


    #Muestra los mensajes en la panatlla
    def mostrar_mensaje(self, texto):
        self.mensaje = texto
        self.tiempo_mensaje = pygame.time.get_ticks()

    #Crea los rectangulos que el usuario apreta
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

    #Logica del juego de memoria de dos jugadores
    def Juego_memoria(self):
        for evento in pygame.event.get():
            #Verifica si se cierra el juego
            if evento.type == pygame.QUIT:
                self.corriendo = False
            #Verifica si se dio un click izquierdo
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                x, y = evento.pos
                #Verifica en cual de las dos matrices se dio el click y se verifica de quien es el turno
                turno_actual = self.jugadores.get_turno() 
                if x < 600 and y < 600:
                    if not turno_actual:  # Si el turno es False, significa que va el jugador uno
                        fila = y // self.TAM_CASILLA
                        columna = x // self.TAM_CASILLA           #Se pasa el tablero correspondiente a cada jugador
                        self.verifica_casillas(fila, columna, self.tablero, jugador=1)
                    else:
                        self.mostrar_mensaje("Turno de Jugador 2. No toques la izquierda.") # en caso de que el jugador 2, precione dentro de las coordenadas de la matriz 1, salta este mensaje

                elif x > 700 and y < 600:
                    if turno_actual:  # Solo Jugador 2 puede tocar esta área
                        fila = y // self.TAM_CASILLA
                        columna = x // self.TAM_CASILLA - 7
                        self.verifica_casillas(fila, columna, self.tablero1, jugador=2)
                    else:
                        self.mostrar_mensaje("Turno de Jugador 1. No toques la derecha.")
                
            if self.escontrados_j1 == 18:
                self.victoria("Jugador 1 ha ganado!")
                return
            elif self.escontrados_j2 == 18:
                self.victoria("Jugador 2 ha ganado!")
                return

    def victoria(self, mensaje):
        fuente_grande = pygame.font.SysFont(None, 72)
        fuente_botones = pygame.font.SysFont(None, 36)
        volver_jugar = pygame.Rect(400, 500, 200, 50)
        volver_menu = pygame.Rect(700, 500, 200, 50)

        while True:
            self.pantalla.fill(self.BLANCO)

            # Mensaje de victoria
            texto = fuente_grande.render(mensaje, True, self.VERDE)
            texto_rect = texto.get_rect(center=(self.ANCHO + 100, 200))
            self.pantalla.blit(texto, texto_rect)

            # Botón volver a jugar
            pygame.draw.rect(self.pantalla, self.AZUL, volver_jugar)
            texto_volver = fuente_botones.render("Volver a jugar", True, self.BLANCO)
            rect_volver = texto_volver.get_rect(center=volver_jugar.center)
            self.pantalla.blit(texto_volver, rect_volver)

            # Botón volver al menú
            pygame.draw.rect(self.pantalla, self.ROJO, volver_menu)
            texto_menu = fuente_botones.render("Menú principal", True, self.BLANCO)
            rect_menu = texto_menu.get_rect(center=volver_menu.center)
            self.pantalla.blit(texto_menu, rect_menu)

            pygame.display.flip()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if volver_jugar.collidepoint(evento.pos):
                        self.__init__(self.ANCHO, self.ALTO, self.FILAS, self.COLUMNAS)
                        self.ejecutar()
                        return
                    elif volver_menu.collidepoint(evento.pos):
                        from Menu import MenuPrincipal  # Asegurate que esto exista
                        menu = MenuPrincipal()
                        menu.ejecutar()
                        return



    
    #Esta funcion activa y desactiva las casillas del juego de memoria y verifica si son iguales o diferentes
    def verifica_casillas(self, fila, columna, tablero, jugador):
        # Seleccionar listas según el jugador
        if jugador == 1: 
            self.lista_seleccionados = self.seleccionados_j1  # Cada jugador tiene sus listas de casillas seleccionadas y sus cordenadas
            self.lista_coordenadas = self.coordenadas_j1      #Y dependiendo del turno que a esta funcion sea pasado, accede a una lista u otra
        else:
            self.lista_seleccionados = self.seleccionados_j2
            self.lista_coordenadas = self.coordenadas_j2

        #Verificar si la casilla ya fue seleccionada o descubierta
        if tablero.esta_activo(fila, columna) or tablero.esta_descubierto(fila, columna):
            self.mostrar_mensaje("Casilla ya seleccionada, escoge otra.")
            return

        #Activar casilla y guardar el valor
        tablero.alternar_boton(fila, columna)
        valor = tablero.Id_cuadro(fila, columna)
        self.lista_seleccionados.append(valor)
        self.lista_coordenadas.append((fila, columna))
        #Comparar si hay dos seleccionadas
        if len(self.lista_seleccionados) == 2:
            f1, c1 = self.lista_coordenadas[0]
            f2, c2 = self.lista_coordenadas[1]

            if self.lista_seleccionados[0] == self.lista_seleccionados[1]:
                self.tiempo_limite += 7000
                self.mostrar_mensaje("¡Pareja encontrada!")
                tablero.marcar_descubierto(f1, c1, f2, c2)
                if not self.jugadores.get_turno():
                    self.escontrados_j1 += 1
                else:
                    self.escontrados_j2 += 1
            else:
                if not self.jugadores.get_turno():
                    self.intentos_j1 += 1
                else:
                    self.intentos_j2 += 1
                self.tiempo_limite += (11 - self.tiempo_transcurrido) * 1000
                self.mostrar_mensaje("No son iguales")
                self.inicio_tiempo = 0
                self.dibujar_juego_memoria()
                pygame.display.flip()
                pygame.time.delay(1000)
                tablero.alternar_boton(f1, c1)
                tablero.alternar_boton(f2, c2)
                self.jugadores.set_turno()
            # Limpiar listas
            self.lista_seleccionados.clear()
            self.lista_coordenadas.clear()

    #Dibuja dos matrices del juego de memoria
    def dibujar_juego_memoria(self):
        self.pantalla.fill(self.BLANCO)

        # Dibujar primera matriz
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                rect = self.rectangulos[fila][columna]
                activo = self.tablero.esta_activo(fila, columna)
                color = self.VERDE if activo else self.GRIS

                pygame.draw.rect(self.pantalla, color, rect, 0, 4)
                pygame.draw.rect(self.pantalla, self.AZUL, rect, 2)

                #Revisa si algun cuadro en la primera matriz esta activo
                if activo:
                    imagen = self.imagenes[self.tablero.get_respuesta()[fila][columna]]
                    imagen_rect = imagen.get_rect(center=rect.center)
                    self.pantalla.blit(imagen, imagen_rect)

        # Dibujar segunda matriz
        for fila in range(self.FILAS):
            for columna in range(self.COLUMNAS):
                rect = self.rectangulos1[fila][columna]
                activo = self.tablero1.esta_activo(fila, columna)
                color = self.VERDE if activo else self.GRIS

                pygame.draw.rect(self.pantalla, color, rect)
                pygame.draw.rect(self.pantalla, self.AZUL, rect, 2)

                #Revisa si algun cuadro en la segunda matriz esta activo
                if activo:
                    imagen = self.imagenes[self.tablero1.get_respuesta()[fila][columna]]
                    imagen_rect = imagen.get_rect(center=rect.center)
                    self.pantalla.blit(imagen, imagen_rect)

        # Mostrar mensaje si existe
        if self.mensaje:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_mensaje < 1000:
                rect_mensaje = pygame.Rect(320, 620, 620, 50)
                pygame.draw.rect(self.pantalla, self.BLANCO, rect_mensaje)
                pygame.draw.rect(self.pantalla, self.ROJO, rect_mensaje, 2)

                texto_render = self.fuente_mensaje.render(self.mensaje, True, self.negro)
                texto_rect = texto_render.get_rect(center=rect_mensaje.center)
                self.pantalla.blit(texto_render, texto_rect)
            else:
                self.mensaje = ""

    #Dibuja las matrices del juego de secuencias
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
    
    #Esta funcion coloca un temporizador en la parte inferior de la pantalla
    def temporizador_en_pantalla(self):
        if self.tiempo_transcurrido > 0:
            self.inicio_tiempo = pygame.time.get_ticks()
        else:
            if not self.jugadores.get_turno():
                self.intentos_j1 += 1
            else:
                self.intentos_j2 += 1
            self.mostrar_mensaje("Cambio de turno")
            self.tiempo_limite += 10000
        self.tiempo_transcurrido = (self.tiempo_limite-self.inicio_tiempo) // 1000
        tiempo_texto1 = self.fuente_mensaje3.render("Tiempo:",True, self.negro)
        tiempo_texto = self.fuente_mensaje3.render(str(self.tiempo_transcurrido),True, self.negro)
        self.pantalla.blit(tiempo_texto1,(595,707))
        self.pantalla.blit(tiempo_texto,(640,750))


    def intentosJugador1(self):
        
        intentos_mjs = pygame.Rect(25, 615, 145, 35)
        pygame.draw.rect(self.pantalla, self.ROJO, intentos_mjs, 5, 10)
        intentos_texto = self.fuente_mensaje2.render(f"Intentos: {self.intentos_j1}",True, self.ROJO)
        self.pantalla.blit(intentos_texto,(35, 620))
        
         
        
        
        parejas_msj = pygame.Rect(25, 655, 145, 35)
        pygame.draw.rect(self.pantalla, self.VERDE, parejas_msj, 5, 10)
        parejas_texto = self.fuente_mensaje2.render(f"Parejas: {self.escontrados_j1}",True, self.VERDE)
        self.pantalla.blit(parejas_texto,(35, 660))



    def intentosJugador2(self):
        
        intentos_mjs = pygame.Rect(1000, 615, 145, 35)
        pygame.draw.rect(self.pantalla, self.ROJO, intentos_mjs, 5, 10)
        intentos_texto = self.fuente_mensaje2.render(f"Intentos: {self.intentos_j2}",True, self.ROJO)
        self.pantalla.blit(intentos_texto,(1010, 620))
        
         
       
        parejas_msj = pygame.Rect(1000, 655, 145, 35)
        pygame.draw.rect(self.pantalla, self.VERDE, parejas_msj, 5, 10)
        parejas_texto = self.fuente_mensaje2.render(f"Parejas: {self.escontrados_j2}",True, self.VERDE)
        self.pantalla.blit(parejas_texto,(1010, 660))

        



    def carga_imagenes(self):
        carpeta_base = os.path.dirname(os.path.abspath(__file__))
        carpeta_imagenes = os.path.join(carpeta_base, "imagenes_proyecto")
        lista = []
        for i in range(18):
            nombre_archivo = f'im{i}.jpg'
            ruta = os.path.join(carpeta_imagenes, nombre_archivo)

            # Abrir la imagen con PIL
            try:
                img_pil = Image.open(ruta)
            except FileNotFoundError:
                print(f'No se encontró la imagen: {ruta}')
                continue

            # Redimensiona la imagen
            img_pil = img_pil.resize((90,90))

            # Convertir a formato compatible con pygame
            modo = img_pil.mode
            tamaño = img_pil.size
            datos = img_pil.tobytes()

            imagen_pygame = pygame.image.fromstring(datos, tamaño, modo)

            lista.append(imagen_pygame)
        return lista


    #Ejecuta el juego de memoria
    def ejecutar(self):
        while self.corriendo:
            if self.tiempo_transcurrido == 0:
                self.jugadores.set_turno()
                print(self.lista_coordenadas,self.coordenadas_j1,self.coordenadas_j2,self.lista_seleccionados)
                if self.coordenadas_j1 != [] and self.tiempo_transcurrido == 0:
                    self.tablero.alternar_boton(self.lista_coordenadas[0][0],self.lista_coordenadas[0][1])
                    self.lista_coordenadas.clear()
                    self.coordenadas_j1.clear()
                    self.lista_seleccionados.clear()
                if self.coordenadas_j2 != [] and self.tiempo_transcurrido == 0:
                    self.tablero1.alternar_boton(self.lista_coordenadas[0][0],self.lista_coordenadas[0][1])
                    self.lista_coordenadas.clear()
                    self.coordenadas_j2.clear()
                    self.lista_seleccionados.clear()
                print(self.lista_coordenadas,self.coordenadas_j1,self.coordenadas_j2,self.lista_seleccionados)
            self.Juego_memoria()
            self.dibujar_juego_memoria()
            self.temporizador_en_pantalla()
            self.intentosJugador1()
            self.intentosJugador2()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

# Para ejecutar el juego:
if __name__ == "__main__":
    juego = Ventana(600,600,6,6)
    juego.ejecutar()