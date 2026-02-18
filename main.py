import pygame
from checkers.game import Game
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK
from minimax.algorithm import minimax  # Tuodaan tekoälyalgoritmi

# Alustetaan pygame ja fontit
pygame.init()

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)

        # 1. TEKOÄLYN VUORO (musta pelaa)
        if game.turn == BLACK:
            game.update()  # Piirretään lauta ennen AI:n siirtoa, jotta pelaaja näkee nykyisen tilanteen
            # depth=3 on hyvä tasapaino nopeuden ja älykkyyden välillä
            _, new_board = minimax(game.get_board(), 3, float('-inf'), float('inf'), BLACK, game)

            if new_board is not None:
                pygame.time.delay(500)  # Pieni viive, jotta pelaaja näkee AI:n valinnan
                game.ai_move(new_board)
            else:
                # Jos AI ei voi liikkua, se häviää pelin
                print("AI ei voi liikkua!")

        # TARKISTUS: Onko joku voittanut?
        winner = game.winner()
        if winner != None:
            game.update()       # Piirretään lauta viimeisen kerran
            game.draw_winner(winner) # Kutsutaan game.py:hyn lisättyä ilmoitusta       
            pygame.time.delay(4000)  # Odotetaan 4 sekuntia, jotta voittaja näkyy
            game.reset()             # Aloitetaan peli alusta

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game.turn == RED:  # Vain punainen pelaaja voi klikata
                    pos = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(pos)
                    game.select(row, col)

        game.update()

    pygame.quit()

if __name__ == "__main__":
    main()