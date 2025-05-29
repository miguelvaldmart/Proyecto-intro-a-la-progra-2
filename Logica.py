from random import randint
class Boton:
    #Esta clase se encarga de darle un valor de False a cada boton y de cambiar su valor dependiende si ha sido tocado o no
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.activo = False  # Estado lógico del botón

    #Alterna el estado del boton
    def alternar(self):
        self.activo = not self.activo

    #Retorna si el boton esta activo o no
    def esta_activo(self):
        return self.activo


class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.botones = []  #Matriz para saber si el boton fue presionado o no, para cambiar su color
        self.respuesta = self.crea_juego(filas,columnas)
        self.revelado = [[False for _ in range(columnas)] for _ in range(filas)] #Crea un matriz de Falses del tamaño del tablero (6x6) donde cada false representa un cuadrado
        print(self.respuesta)                                                    #Esta matriz es para saber si el numero del cuadrado esta siendo mostrado en pantalla o no
        for fila in range(filas): #Aqui se crea la matriz de self.botones
            fila_actual = []  # Lista para esta fila
            for columna in range(columnas):
                nuevo_boton = Boton(fila, columna)
                fila_actual.append(nuevo_boton)
            self.botones.append(fila_actual) 
        self.descubiertos = [[False for _ in range(columnas)] for _ in range(filas)]
    
    #Alterna el estado del boton
    def alternar_boton(self, fila, columna):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.botones[fila][columna].alternar()
            self.revelado[fila][columna] = not self.revelado[fila][columna]

    #Retorna si el boton esta activo o no
    def esta_activo(self, fila, columna):
        return self.botones[fila][columna].esta_activo()
    
    #Esta funcion crea una matriz con numeros del 0 al 17 en posiciones aleatorias, hay solo dos instancias del mismo numero en la matriz
    def crea_juego(self,filas, columnas):
        identificador1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        identificador2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        turno = 1
        respuesta = []
        for _ in range(filas):
            fila_actual = []
            for _ in range(columnas):
                if turno == 1:
                    valor = randint(0,len(identificador1)-1)
                    fila_actual.append(identificador1[valor])
                    identificador1.remove(identificador1[valor])
                    turno = 2
                else:
                    valor = randint(0,len(identificador2)-1)
                    fila_actual.append(identificador2[valor])
                    identificador2.remove(identificador2[valor])
                    turno = 1
            respuesta.append(fila_actual)
        return respuesta
    
    #Esta funcion da la variable que contiene la matriz con las respuestas(valor del cuadrado)
    def get_respuesta(self):
        return self.respuesta
    
    #Retorna True si el numero esta siendo mostrado en pantalla y False en caso contrario
    def esta_revelado(self, fila, columna): 
        return self.revelado[fila][columna]

    #Retorna el valor del cuadro especificado por su fila y su columna
    def Id_cuadro (self, fila, columna):
        return self.respuesta[fila][columna]
    
    #Marca de manera permanente dos casillas en el juego
    def marcar_descubierto(self, fila1, col1, fila2, col2):
        self.descubiertos[fila1][col1] = True
        self.descubiertos[fila2][col2] = True

    #Retorna si el cuadro esta descubierto o no
    def esta_descubierto(self, fila, columna):
        return self.descubiertos[fila][columna]