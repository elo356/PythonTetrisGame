import os
import hashlib

class LocalData:
    def __init__(self, file_name="user_data.txt", score_file="highscore.txt"):
        self.file_name = file_name
        self.score_file = score_file
        self.username = ""
        self.best_score = self.load_best_score()

        self.load_user_data()

    def load_best_score(self):
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, 'r') as file:
                    score = int(file.read().strip())
                    return score
            except ValueError:
                return 0
        else:
            self.save_best_score(0)
            return 0

    def save_best_score(self, score):
        with open(self.score_file, 'w') as file:
            file.write(str(score))

    def update_best_score(self, score):
        if score > self.best_score:
            self.best_score = score
            self.save_best_score(self.best_score)

    def get_best_score(self):
        return self.best_score

    def load_user_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as file:
                    return file.readline().strip()  # Leer la primera línea y eliminar espacios en blanco
            except Exception as e:
                print(f"Error al cargar los datos del usuario: {e}")
                return None
        return None

    def save_user_data(self, username):
        with open(self.file_name, 'w') as file:
            file.write(f"{username}")
