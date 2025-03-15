import pygame
import sys
import random

pygame.init()
pygame.font.init()

from game.board import Board
from game.tetrimino import Tetrimino
from game.ui import UI
from game.constants import *
from game.local_db import LocalData
from game.firebase_db import FirebaseTetrisDB
class Game:

#Para que funcione sin errores debe tener internet para que funcione la
#conexion a la base de datos.

    UI_STATE = {'Main Menu':0, 'Game':1, 'Leaderboard':2}

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.font = pygame.font.Font(None,48)
        self.clock = pygame.time.Clock()
        self.board = Board()
        self.ui = UI(self.screen)
        self.current_piece = None
        self.next_piece = None
        self.last_drop_time = pygame.time.get_ticks()
        self.local_data = LocalData()
        # TODO TASK 4: Implement game over tracking
        #   Add a game_over attribute
        #   Hint: Make the a boolean and defined them as False
        self.game_over = False
        # TODO TASK 5: Implement pause state tracking
        #   Add a paused attribute
        #   # Hint: Make the a boolean and defined them as False
        self.is_paused = False

        #para el main menu
        self.state = self.UI_STATE['Main Menu']
        self.is_playing = False
        self.selected_option = 0
        self.leaderboard = {}
        self.firebaes_db = FirebaseTetrisDB()
        self.username = {}

    def new_piece(self):
        if self.game_over:
            return
        self.current_piece = self.next_piece or Tetrimino(random.choice(list(SHAPES.keys())))
        self.next_piece = Tetrimino(random.choice(list(SHAPES.keys())))
        # TODO TASK 4: Implement game over logic when a new piece cannot be placed at the top
        #   If the current piece is not a valid position modify the game_over attribute to True
        if not self.board.is_valid_position(self.current_piece,0,0):
            self.game_over = True

    def handle_input(self):
        if self.state == self.UI_STATE['Game']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        if self.board.is_valid_position(self.current_piece, -1, 0):
                            self.current_piece.x -= 1
                            MOVE_SOUND.play()
                    elif event.key == pygame.K_RIGHT:
                        if self.board.is_valid_position(self.current_piece, 1, 0):
                            self.current_piece.x += 1
                            MOVE_SOUND.play()
                    elif event.key == pygame.K_DOWN:
                        if self.board.is_valid_position(self.current_piece, 0, 1):
                            self.current_piece.y += 1
                    elif event.key == pygame.K_UP:
                        rotated = self.current_piece.rotation
                        self.current_piece.rotate()
                        if not self.board.is_valid_position(self.current_piece, 0, 0):
                            self.current_piece.rotation = rotated
                    elif event.key == pygame.K_SPACE:
                        self.drop_piece()
                    elif event.key == pygame.K_r:
                        if self.game_over:
                            self.restart_game()
                    elif event.key == pygame.K_p:
                        if self.is_paused:
                            self.is_paused = False
                        else:
                            self.is_paused = True
                    elif event.key == pygame.K_m:
                        self.state=self.UI_STATE['Main Menu']
                    # TODO TASK 5: Implement pause game functionality (toggle the paused state)
                    #   If the key is k_p toggle the paused attribute
                    # TODO TASK 4: Implement game_over  functionality
                    #   If the key is k_r and game_over is True called restart_game()
        elif self.state == self.UI_STATE['Main Menu']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % 3
                    elif event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % 3
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            self.state = self.UI_STATE['Game']
                            self.is_playing = True
                        elif self.selected_option == 1:
                            self.state = self.UI_STATE['Leaderboard']
                            self.ui.draw_leaderboard(self.leaderboard)

                        elif self.selected_option ==2:
                            pygame.quit()
                            sys.exit()
                        print(self.state)
            self.restart_game()

            menu_options, menu_rects = self.ui.draw_main_menu(self.selected_option)
        elif self.state == self.UI_STATE['Leaderboard']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.state = self.UI_STATE['Main Menu']


    def drop_piece(self):
        # TODO TASK 3: Implement the logic to drop the piece.
        #   Move the current piece downwards while it remains in a valid position.
        #   Once it can no longer move down, lock the piece in place on the board.
        #   Play a sound effect when the piece is successfully placed.
        #   Generate a new piece after the current piece is locked.
        while self.board.is_valid_position(self.current_piece, 0, 1):
            self.current_piece.y += 1
            self.ui.draw_board(self.board, self.current_piece, self.next_piece)

            pygame.display.update()
            pygame.time.delay(20)

        self.board.lock_piece(self.current_piece)
        PLACE_SOUND.play()
        self.new_piece()

    def update(self):
        if pygame.time.get_ticks() - self.last_drop_time >= PIECE_DROP_TIME:
            if self.board.is_valid_position(self.current_piece, 0, 1):
                self.current_piece.y += 1
            else:
                self.board.lock_piece(self.current_piece)
                PLACE_SOUND.play()
                self.new_piece()
            self.last_drop_time = pygame.time.get_ticks()

    def run(self):
        self.new_piece()
        while True:
            self.handle_input()

            # TODO TASK 4: Implement the logic to display game over screen
            #   If game_over is true call draw_game_over()
            # TODO TASK 5: Implement the logic to display pause screen
            #   If paused is true call draw_pause()
            if self.game_over:
                self.local_data.update_best_score(self.board.score)
                self.firebaes_db.update_high_record(self.username, self.board.score)
                self.ui.draw_game_over(self.board.score, self.local_data.get_best_score())
                pygame.display.update()
                continue
            if self.is_paused:
                self.ui.draw_pause()
                pygame.display.update()
                continue

            if self.state == self.UI_STATE['Leaderboard']:
                self.leaderboard = self.firebaes_db.update_leaderboard()
                print(self.leaderboard)
                self.ui.draw_leaderboard(self.leaderboard)
                pygame.display.update()
                continue

            # Pantalla principal del juego
            if self.state == self.UI_STATE['Game']:
                self.update()
                ghost_piece = self.get_ghost_position()
                self.ui.draw_board(self.board, self.current_piece, self.next_piece, ghost_piece)

            # Pantalla del menú principal
            elif self.state == self.UI_STATE['Main Menu']:
                menu_options, menu_rects = self.ui.draw_main_menu(self.selected_option)

            self.clock.tick(FPS)

    def restart_game(self):
        self.board = Board()  # Reset board and score
        self.game_over = False
        self.paused = False
        self.new_piece()

    def get_ghost_position(self):
        ghost_piece = Tetrimino(self.current_piece.shape_key)  # Crear una copia de la pieza actual
        ghost_piece.x = self.current_piece.x
        ghost_piece.y = self.current_piece.y
        ghost_piece.rotation = self.current_piece.rotation

        #caída de la pieza hasta la posición más baja válida
        while self.board.is_valid_position(ghost_piece, 0, 1):
            ghost_piece.y += 1
        return ghost_piece

    def load_username(self):
        user_data = self.local_data.load_user_data()

        if user_data is not None and user_data is not "":
            self.username = user_data
            print(f"Nombre de usuario cargado automáticamente: {self.username}")
        else:
            self.username = self.ui.username_screen()

            if self.username:
                self.local_data.save_user_data(self.username)
                self.firebaes_db.create_user(self.username)
                print(f"Nombre de usuario ingresado y guardado: {self.username}")
            else:
                print("No se ingresó un nombre de usuario.")


if __name__ == "__main__":
    game = Game()
    game.load_username()
    game.run()

