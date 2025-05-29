class jugador:
    def __init__(self):

        self.turno = False
        self.puntaje = 0

    #Esta funcion alterna el turno entre los jugadores
    def set_turno(self):
        self.turno = not self.turno

    #Esta funcion da cual es el turno actual
    def get_turno(self):
        return self.turno

    #Esta funcion cambia el puntaje del jugador
    def set_puntaje(self, puntos):
        self.puntaje += puntos
    
    #Esta funcion da el puntaje del jugador
    def get_puntaje(self):
        return self.puntaje