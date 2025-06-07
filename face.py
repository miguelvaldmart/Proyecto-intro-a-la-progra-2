import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import os
import numpy as np
import threading
import time

USERS_DIR = "users_lbph"

class FaceRegistrar:
    def __init__(self, users_dir=USERS_DIR):
        self.users_dir = users_dir
        self.face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.face_cascade_path)
        self.capture_count = 10
        self.face_size = (100, 100)

        if not os.path.exists(self.users_dir):
            os.makedirs(self.users_dir)

    def register(self):
        name = simpledialog.askstring("Registro", "Ingresa tu nombre de usuario:")
        if not name:
            messagebox.showerror("Error", "Nombre inválido.")
            return

        name = name.strip().lower()
        cap = cv2.VideoCapture(0)
        count = 0
        faces_data = []

        messagebox.showinfo("Instrucción", f"Mira a la cámara. Se capturarán {self.capture_count} imágenes automáticamente.")

        while True:
            ret, frame = cap.read()
            if not ret:
                messagebox.showerror("Error", "No se pudo acceder a la cámara.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face = gray[y:y+h, x:x+w]
                face_resized = cv2.resize(face, self.face_size)
                faces_data.append(face_resized)
                count += 1

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Captura {count}/{self.capture_count}", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            cv2.imshow("Registrando rostro", frame)

            if count >= self.capture_count or cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if faces_data:
            mean_face = np.mean(faces_data, axis=0)
            filepath = os.path.join(self.users_dir, f"{name}.npy")
            np.save(filepath, mean_face)
            messagebox.showinfo("Éxito", f"Rostro guardado correctamente como '{filepath}'")
        else:
            messagebox.showwarning("Sin capturas", "No se capturó ningún rostro.")


class FaceLogin:
    def __init__(self, users_dir=USERS_DIR):
        self.users_dir = users_dir
        self.face_cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(self.face_cascade_path)
        self.face_size = (100, 100)
        self.threshold = 2000
        self.timeout = 15

    def load_known_faces(self):
        encodings = []
        names = []

        for file in os.listdir(self.users_dir):
            if file.endswith(".npy"):
                path = os.path.join(self.users_dir, file)
                encoding = np.load(path).flatten()
                encodings.append(encoding)
                names.append(os.path.splitext(file)[0])

        return encodings, names

    def login(self):
        threading.Thread(target=self._login_thread).start()

    def _login_thread(self):
        try:
            known_encodings, known_names = self.load_known_faces()
            if not known_encodings:
                messagebox.showerror("Error", "No hay rostros registrados.")
                return

            cap = cv2.VideoCapture(0)
            start_time = time.time()
            recognized = False

            while True:
                ret, frame = cap.read()
                if not ret:
                    messagebox.showerror("Error", "No se pudo acceder a la cámara.")
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    face = cv2.resize(gray[y:y+h, x:x+w], self.face_size).flatten()
                    distances = [np.linalg.norm(face - enc) for enc in known_encodings]
                    min_distance = min(distances)
                    best_match_index = np.argmin(distances)

                    if min_distance < self.threshold:
                        name = known_names[best_match_index]
                        label = f"Reconocido: {name}"
                        color = (0, 255, 0)
                        recognized = True
                    else:
                        label = "Desconocido"
                        color = (0, 0, 255)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, label, (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

                    if recognized:
                        cv2.imshow("Login con rostro", frame)
                        cv2.waitKey(1000)
                        messagebox.showinfo("Login exitoso", f"Bienvenido, {name}!")
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                cv2.imshow("Login con rostro", frame)

                if time.time() - start_time > self.timeout or cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
            messagebox.showinfo("Login fallido", "No se reconoció ningún rostro o se canceló el login.")
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))


class FaceApp:
    def __init__(self):
        self.registrar = FaceRegistrar()
        self.login = FaceLogin()

    def run(self):
        root = tk.Tk()
        root.title("Sistema de Reconocimiento Facial (LBPH)")
        root.geometry("400x250")

        tk.Label(root, text="Reconocimiento Facial (OpenCV + LBPH)", font=("Arial", 14)).pack(pady=10)
        tk.Button(root, text="Registrar nuevo rostro", command=self.registrar.register, width=30, height=2).pack(pady=10)
        tk.Button(root, text="Iniciar sesión con rostro", command=self.login.login, width=30, height=2).pack(pady=10)
        tk.Button(root, text="Salir", command=root.destroy, width=30, height=2).pack(pady=10)

        root.mainloop()


if __name__ == "__main__":
    app = FaceApp()
    app.run()
