import tkinter as tk
from tkinter import messagebox
from face import FaceApp
from Menu import MenuPrincipal

class SimpleApp:
    def __init__(self, archivo = "users_pass.txt"):
        self.root = tk.Tk()
        self.root.title("Ejemplo con Tkinter")
        self.root.geometry("400x300")
        self.archivo = archivo

        # Etiquetas y cajas de texto
        tk.Label(self.root, text="Usuario:").pack(pady=5)
        self.entry_user = tk.Entry(self.root, width=30)
        self.entry_user.pack(pady=5)

        tk.Label(self.root, text="Contraseña:").pack(pady=5)
        self.entry_contra = tk.Entry(self.root, width=30)
        self.entry_contra.pack(pady=5)

        # Botones
        tk.Button(self.root, text="Registro", command=self.guardar_datos).pack(pady=10)
        tk.Button(self.root, text="Login", command= lambda: self.Verificar_registro(self.entry_user.get(), self.entry_contra.get())).pack(pady=10)
        tk.Button(self.root, text="Reconocimiento facial", command=lambda: FaceApp().run()).pack(pady=10)

        self.root.mainloop()

    def guardar_datos(self):
        user = self.entry_user.get()
        contra = self.entry_contra.get()
        with open(self.archivo, "a") as archivo:
            archivo.write(user + " " + contra + "\n")   
              
    def Verificar_registro(self, user, password):
        with open(self.archivo, "r") as archivo:
            lista = archivo.readlines()
            for i in range(len(lista)):
                elementos = lista[i].rstrip()
                elementos = elementos.split()
                if elementos[0] == user and elementos[1] == password:
                    MenuPrincipal().ejecutar()
                else:
                    print("Incorrectos")

if __name__ == "__main__":
    app = SimpleApp()

