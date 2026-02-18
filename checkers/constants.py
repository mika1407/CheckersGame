import pygame

pygame.mixer.init()

MOVE_SOUND = pygame.mixer.Sound('assets/click.wav')

WIDTH, HEIGHT = 700, 700
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# rgb
RED = (181, 8, 25) # Fire Engine Red
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (218, 165, 32) # Goldenrod
BROWN = (137, 81, 41)
LBROWN = (196, 164, 132) 

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))