import pygame
from .constants import BLACK, BLUE, ROWS, RED, SQUARE_SIZE, COLS, WHITE, BROWN, LBROWN
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win

    def update(self):
        self.board.draw(self.win)
        self.highlight_mandatory_moves() # Uusi lisäys: korostetaan pakolliset nappulat
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def highlight_mandatory_moves(self):
        # Haetaan kaikki nappulat, joilla on pakko hypätä
        mandatory = self._get_all_mandatory_jumps()
        for piece in mandatory:
            # Piirretään valkoinen kehä nappulan ympärille
            pygame.draw.circle(self.win, WHITE, (piece.x, piece.y), SQUARE_SIZE//2 - 5, 5)

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
            return result
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            # Tarkista onko koko laudalla pakollisia hyppyjä
            all_mandatory = self._get_all_mandatory_jumps()
            
            if all_mandatory:
                if piece in all_mandatory:
                    self.selected = piece
                    self.valid_moves = all_mandatory[piece]
                    return True
                return False # Ei saa valita tätä nappulaa, koska on hypättävä toisella
            
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _get_all_mandatory_jumps(self):
        mandatory = {}
        for r in range(ROWS):
            for c in range(COLS):
                p = self.board.get_piece(r, c)
                if p != 0 and p.color == self.turn:
                    moves = self.board.get_valid_moves(p)
                    # Jos nappulalla on siirtoja joissa skipped > 0
                    jumps = {m: s for m, s in moves.items() if len(s) > 0}
                    if jumps:
                        mandatory[p] = jumps
        return mandatory

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            skipped = self.valid_moves[(row, col)]
            self.board.move(self.selected, row, col)
            
            if skipped:
                self.board.remove(skipped)
                # TUPLAHYPPY: Tarkista voiko samalla nappulalla jatkaa
                new_moves = self.board.get_valid_moves(self.selected)
                # Koska Board.get_valid_moves suodattaa jo, tarkistetaan vain onko hyppyjä
                if any(len(s) > 0 for s in new_moves.values()):
                    self.valid_moves = new_moves
                    return True # Pysytään samassa nappulassa
            
            self.change_turn()
            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        self.selected = None
        self.turn = BLACK if self.turn == RED else RED

    # Uusi metodi: Piirretään ilmoitus voittajasta
    def draw_winner(self, winner_color):
        # Luodaan fontti-olio (koko 100)
        font = pygame.font.SysFont("arial", 50, bold=True)
        
        # Määritetään teksti ja väri
        if winner_color == RED:
            text = "PUNAINEN VOITTI!"
            color = RED
        else:
            text = "MUSTA VOITTI!"
            color = BLACK

        # Luodaan tekstipinta (Surface)
        winner_text = font.render(text, True, color)
        
        # Piirretään valkoinen taustalaatikko tekstille, jotta se erottuu
        bg_rect = winner_text.get_rect(center=(COLS * SQUARE_SIZE // 2, ROWS * SQUARE_SIZE // 2))
        pygame.draw.rect(self.win, WHITE, bg_rect.inflate(20, 20))
        pygame.draw.rect(self.win, BLACK, bg_rect.inflate(20, 20), 2) # Reunukset
        
        # Piirretään teksti keskelle ruutua
        self.win.blit(winner_text, bg_rect)
        pygame.display.update()