import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
GRID_X, GRID_Y = 34, 25
GRID_WIDTH, GRID_HEIGHT = 300, 550
CELL_SIZE = 25
COLUMNS, ROWS = GRID_WIDTH // CELL_SIZE, GRID_HEIGHT // CELL_SIZE
FPS = 30
PIECE_DROP_TIME = 500

NEXT_PIECE_X, NEXT_PIECE_Y = 370, 205
SCORE_X, SCORE_Y = 400, 140

# Load Background Image
BACKGROUND_IMAGE_PATH = "assets/images/background.png"
background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.init()
pygame.mixer.music.load("assets/music/tetris_theme.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)

# Load sound effects
MOVE_SOUND = pygame.mixer.Sound("assets/sounds/move.mp3")
PLACE_SOUND = pygame.mixer.Sound("assets/sounds/land.mp3")
LINE_CLEAR_SOUND = pygame.mixer.Sound("assets/sounds/clear_line.mp3")
MOVE_SOUND.set_volume(0.1)
PLACE_SOUND.set_volume(0.1)
LINE_CLEAR_SOUND.set_volume(0.1)
GHOST_COLOR = (255,165,0)  # color para la prediccion de la pieza

# Tetrimino definitions
SHAPES = {
    "I": [
            [
                [1],
                [1],
                [1],
                [1]
            ],
            [
                [1, 1, 1, 1]
            ]
    ],
    "O": [
            [
                [1, 1],
                [1, 1]
            ]
    ],
    "T": [
            [
                [0, 1, 0],
                [1, 1, 1]],
            [
                [1, 0],
                [1, 1],
                [1, 0]
            ],
            [
                [1, 1, 1],
                [0, 1, 0]
            ],
            [
                [0, 1],
                [1, 1],
                [0, 1]
            ]
    ],
    "L": [
            [
                [1, 0, 0],
                [1, 1, 1]
            ],
            [
                [1, 1],
                [1, 0],
                [1, 0]
            ],
            [
                [1, 1, 1],
                [0, 0, 1]
            ],
            [
                [0, 1],
                [0, 1],
                [1, 1]
            ]
    ],
    "J": [
            [
                [0, 0, 1],
                [1, 1, 1]
            ],
            [
                [1, 0],
                [1, 0],
                [1, 1]
            ],
            [
                [1, 1, 1],
                [1, 0, 0]
            ],
            [
                [1, 1],
                [0, 1],
                [0, 1]
            ]
    ],
    "S": [
            [
                [0, 1, 1],
                [1, 1, 0]
            ],
            [
                [1, 0],
                [1, 1],
                [0, 1]
            ]
    ],
    "Z": [
            [
                [1, 1, 0],
                [0, 1, 1]
            ],
            [
                [0, 1],
                [1, 1],
                [1, 0]
            ]
        ]
    }

COLORS = {
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "T": (128, 0, 128),
    "L": (255, 165, 0),
    "J": (0, 0, 255),
    "S": (0, 255, 0),
    "Z": (255, 0, 0)
}

TEXT_COLOR = (240, 240, 240)
TITLE_FONT = pygame.font.Font(None, 100)
FONT = pygame.font.Font("assets/fonts/tetris.ttf", 24)
