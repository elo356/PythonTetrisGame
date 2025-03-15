import pygame
from game.constants import background_image, ROWS, COLUMNS, CELL_SIZE, GRID_X, GRID_Y, NEXT_PIECE_X, NEXT_PIECE_Y, \
    SCORE_X, SCORE_Y, TEXT_COLOR, SCREEN_WIDTH, FONT, SCREEN_HEIGHT, GHOST_COLOR, TITLE_FONT
from game.local_db import LocalData

class UI:
    def __init__(self, screen):
        self.screen = screen

    def draw_board(self, board, current_piece, next_piece,ghost_piece=None):
        self.screen.blit(background_image, (0, 0))
        for y in range(ROWS):
            for x in range(COLUMNS):
                if board.grid[y][x]:
                    pygame.draw.rect(self.screen,
                                     board.grid[y][x],
                                     (GRID_X + x * CELL_SIZE, GRID_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for y, row in enumerate(current_piece.get_current_shape()):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen,
                                     current_piece.color,
                                     (GRID_X + (current_piece.x + x) * CELL_SIZE,
                                      GRID_Y + (current_piece.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # TODO TASK 2 Draw the nex_piece
        #   To draw the next piece the code is similar to the draw of the current_piece (previous code)
        #   but using next_piece instead of current_piece.
        #   HINT: The rectangle X is NEXT_PIECE_X + 50 + x * CELL_SIZE
        #         The rectangle Y is NEXT_PIECE_Y + 40 + y * CELL_SIZE
        for y, row in enumerate(next_piece.get_current_shape()):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen,
                                     next_piece.color,
                                     (NEXT_PIECE_X + 45 + x * CELL_SIZE,
                                      NEXT_PIECE_Y + 60 + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Dibujar grid
        for y in range(ROWS):
            for x in range(COLUMNS):
                pygame.draw.rect(self.screen,(200, 200, 200), (GRID_X + x * CELL_SIZE, GRID_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE),1)

        # Dibujar la pieza fantasma
        if ghost_piece:
            for y, row in enumerate(ghost_piece.get_current_shape()):
                for x, cell in enumerate(row):
                    if cell:
                        pygame.draw.rect(self.screen, GHOST_COLOR,(GRID_X + (ghost_piece.x + x) * CELL_SIZE, GRID_Y + (ghost_piece.y + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE),2)

        score_text = FONT.render(f"{board.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCORE_X, SCORE_Y))
        pygame.display.flip()

    def draw_game_over(self, score,best_score):
        self.screen.fill((0, 0, 0))

        game_over_text = FONT.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))

        score_text = FONT.render(f"Score: {score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 60))

        high_score_text = FONT.render(f"High Score: {best_score}", True, (255, 215, 0))  # Color dorado
        self.screen.blit(high_score_text,
                         (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 3 + 120))

        restart_text = FONT.render("Press R to Restart", True, TEXT_COLOR)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 3 + 180))

        main_menu_text = FONT.render("Press M to Main Menu", True, TEXT_COLOR)
        self.screen.blit(main_menu_text,
                         (SCREEN_WIDTH // 2 - main_menu_text.get_width() // 2, SCREEN_HEIGHT // 3 + 220))

        pygame.display.flip()

    def draw_pause(self):
        pause_text = FONT.render("PAUSED", True, TEXT_COLOR)
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3))
        pause_text = FONT.render("Press P to Resume", True, TEXT_COLOR)
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3 + 50))
        pygame.display.flip()


    def draw_main_menu(self, selected_option=0):
        self.screen.fill((0, 0, 0))
        menu_options = ['Jugar','Leaderboard','Salir']
        color_active = (0, 255, 0)
        color_inactive = (255, 255, 255)
        menu_rects = []

        title_text = TITLE_FONT.render("TETRIS", True, TEXT_COLOR)
        title_x = SCREEN_WIDTH // 2 - title_text.get_width() // 2
        title_y = 50
        self.screen.blit(title_text, (title_x, title_y))

        for i, option in enumerate(menu_options):
            color = color_active if selected_option == i else color_inactive
            text = FONT.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 200 + i * 60))
            menu_rects.append(text_rect)
            self.screen.blit(text, text_rect)

        instructions_text = pygame.font.Font(None, 20).render("Para mover usa las flechas y para entrar presiona Enter", True, TEXT_COLOR)
        instructions_x = 10
        instructions_y = SCREEN_HEIGHT - 30
        self.screen.blit(instructions_text, (instructions_x, instructions_y))
        pygame.display.flip()

        return menu_options, menu_rects

    def draw_leaderboard(self, leaderboard_dict):
        self.screen.fill((0, 0, 0))

        title_text = FONT.render("Leaderboard", True, (255, 215, 0))  # Título
        self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

        for i, (name, score) in enumerate(leaderboard_dict.items()):
            rank_text = FONT.render(f"{i + 1}. {name}: {score}", True, TEXT_COLOR)
            self.screen.blit(rank_text, (SCREEN_WIDTH // 2 - rank_text.get_width() // 2, 120 + i * 50))

        main_menu_text = FONT.render("Press M to Main Menu", True, TEXT_COLOR)
        self.screen.blit(main_menu_text, (SCREEN_WIDTH // 2 - main_menu_text.get_width() // 2, SCREEN_HEIGHT - 50))

        pygame.display.flip()

    def username_screen(self):
        font = pygame.font.Font(None, 32)
        title_font = pygame.font.Font(None, 48)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (200, 200, 200)
        BLUE = (0, 120, 215)
        RED = (255, 0, 0)

        # Caja de texto
        input_box = pygame.Rect(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20, 300, 40)
        username = ""
        active = False

        # Botón
        button = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 100, 40)

        # Mensajes informativos
        max_length = 8
        message_font = pygame.font.Font(None, 24)
        instructions = "El nombre debe tener máximo 8 caracteres."
        explanation = "Pon un username. Será usado en el leaderboard."

        running = True
        while running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None  # Salir si se cierra la ventana
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Activar o desactivar la caja de texto
                    active = input_box.collidepoint(event.pos)
                    # Verificar si se hace clic en el botón
                    if button.collidepoint(event.pos):
                        if username.strip() and len(
                                username.strip()) <= max_length:
                            return username.strip()
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif len(username) < max_length:
                            username += event.unicode

            # Título de la pantalla
            title_text = title_font.render("Bienvenido a Tetris Game", True, WHITE)
            self.screen.blit(title_text,
                             (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 200))

            # Explicación del nombre
            explanation_text = message_font.render(explanation, True, WHITE)
            self.screen.blit(explanation_text,
                             (SCREEN_WIDTH // 2 - explanation_text.get_width() // 2, SCREEN_HEIGHT // 2 - 120))

            # Mensaje de restricción de caracteres
            message_text = message_font.render(f"{instructions}", True, RED)
            self.screen.blit(message_text,
                             (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2 - 80))

            # Dibujar la caja de texto
            pygame.draw.rect(self.screen, BLUE if active else GRAY, input_box, 2)  # Borde
            text_surface = font.render(username, True, WHITE)
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, BLACK, (input_box.x + 5 + text_surface.get_width(), input_box.y + 5,
                                                  input_box.width - 10 - text_surface.get_width(),
                                                  input_box.height - 10))  # Ocultar texto sobrante

            # Dibujar el botón
            pygame.draw.rect(self.screen, BLUE, button)
            button_text = font.render("Confirmar", True, WHITE)
            self.screen.blit(button_text, (button.x + button.width // 2 - button_text.get_width() // 2,
                                           button.y + button.height // 2 - button_text.get_height() // 2))

            pygame.display.flip()

