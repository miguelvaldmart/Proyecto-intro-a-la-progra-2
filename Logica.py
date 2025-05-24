from random import randint
class Boton:
    #esta clase se encarga de darle un valor de False a cada boton y de cambiar su valor dependiende si ha sido tocado o no
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.activo = False  # Estado lógico del botón

    def alternar(self):
        self.activo = not self.activo

    def esta_activo(self):
        return self.activo


class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        self.botones = []  # Aquí se guardará la matriz
        self.respuesta = self.crea_juego(filas,columnas)
        print(self.respuesta)
        for fila in range(filas):
            fila_actual = []  # Lista para esta fila
            for columna in range(columnas):
                nuevo_boton = Boton(fila, columna)
                fila_actual.append(nuevo_boton)
            self.botones.append(fila_actual)
        
    def alternar_boton(self, fila, columna):
        if 0 <= fila < self.filas and 0 <= columna < self.columnas:
            self.botones[fila][columna].alternar()

    def esta_activo(self, fila, columna):
        return self.botones[fila][columna].esta_activo()
    
    #Esta funcion crea una matriz con numeros del 0 al 17 en posiciones aleatorias, hay solo dos instancias del mismo numero en la matriz
    def crea_juego(self,filas, columnas):
        identificador1 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        identificador2 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17]
        turno = 1
        respuesta = []
        for fila in range(filas):
            fila_actual = []
            for columna in range(columnas):
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
    
    #Esta funcion da la variable que contiene la matriz con las respuestas
    def get_respuesta(self):
        return self.respuesta