import random

class LogicaMemoria:
    def __init__(self):
        self.nivel = 3
        self.secuencia = []
        self.respuesta = []

    def nueva_secuencia(self, cantidad):
        self.secuencia = [random.randint(0, cantidad - 1) for _ in range(self.nivel)]
        self.respuesta = []

    def verificar_click(self, indice):
        self.respuesta.append(indice)
        # Si se equivoca
        if self.respuesta[-1] != self.secuencia[len(self.respuesta) - 1]:
            return "error"
        # Si acierta la secuencia completa
        elif len(self.respuesta) == len(self.secuencia):
            self.nivel += 1
            return "completo"
        return "parcial"

    def get_secuencia(self):
        return self.secuencia

    def get_nivel(self):
        return self.nivel
    
    def reiniciar(self):
        self.nivel = 3