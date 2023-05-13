import numpy as np
import pygame
import sys
import math

# Game rules, instructions, etc.
DESCRIPTION = ("Connect Four (also known as Connect 4, Four Up, Plot Four, Find Four, "
               "Captain's Mistress, Four in a Row, Drop Four, and Gravitrips) is a"
               " two-player connection rack game, in which the "
               "players choose a color and then take turns dropping colored tokens "
               "into a seven-column, six-row vertically suspended grid. "
               "The pieces fall straight down, occupying the lowest available "
               "space within the column. The objective of the game is to be the "
               "first to form a horizontal, vertical, or diagonal line of four "
               "of one's own tokens.")
# Color identification and assignment
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100

buttons = []

# Player class with ID and color attributes
class Player:
    def __init__(self, id, color):
        self.id = id
        self.color = color

# Disc class with a player attribute
class Disc:
    def __init__(self, player):
        self.player = player

# Button class for GUI buttons
class Button:
    def __init__(self, text, width, height, pos, elevation):
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text = text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)
        buttons.append(self)

    def change_text(self, newtext):
        self.text_surf = gui_font.render(newtext, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color,
                         self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color,
                         self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.change_text(f"{self.text}")
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.change_text(self.text)
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

# Board class for game board operations
class Board:
    def __init__(self, row_count, column_count):
        self.row_count = row_count
        self.column_count = column_count
        self.height = (row_count + 1) * SQUARESIZE
        self.RADIUS = int(SQUARESIZE / 2 - 5)
        self.board = np.zeros((row_count, column_count))

    def create_board(self):
        return np.zeros((self.row_count, self.column_count))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, col):
        return self.board[self.row_count - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.row_count):
            if self.board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self.board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.column_count - 3):
            for r in range(self.row_count):
                if self.board[r][c] == piece and self.board[r][c + 1] == piece and self.board[r][c + 2] == piece and \
                        self.board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.column_count):
            for r in range(self.row_count - 3):
                if self.board[r][c] == piece and self.board[r + 1][c] == piece and self.board[r + 2][c] == piece and \
                        self.board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(self.row_count - 3):
                if self.board[r][c] == piece and self.board[r + 1][c + 1] == piece and self.board[r + 2][
                    c + 2] == piece and self.board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self.column_count - 3):
            for r in range(3, self.row_count):
                if self.board[r][c] == piece and self.board[r - 1][c + 1] == piece and self.board[r - 2][
                    c + 2] == piece and self.board[r - 3][c + 3] == piece:
                    return True

    def draw_board(self, screen):
        for c in range(self.column_count):
            for r in range(self.row_count):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r *
                                                SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(
                    r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), self.RADIUS)

        for c in range(self.column_count):
            for r in range(self.row_count):
                if self.board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2),
                                                     self.height - int(r * SQUARESIZE + SQUARESIZE / 2)), self.RADIUS)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(screen, YELLOW, (int(
                        c * SQUARESIZE + SQUARESIZE / 2), self.height - int(r * SQUARESIZE + SQUARESIZE / 2)),
                                       self.RADIUS)
        pygame.display.update()

# Initialize Pygame
pygame.init()

# Set up game elements
myfont = pygame.font.SysFont("monospace", 75)

game_board = Board(ROW_COUNT, COLUMN_COUNT)
player1 = Player(1, RED)
player2 = Player(2, YELLOW)
width = COLUMN_COUNT * SQUARESIZE
size = (width, game_board.height)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None, 30)
details_font = pygame.font.Font(None, 30)
game_over = False
turn = 0

# Set up GUI buttons
startButton = Button('Game Start', 200, 40, (250, 300), 5)
quitButton = Button('Quit', 200, 40, (250, 350), 5)
# detailsButton = Button('Details', 200, 40, (250, 450), 5)
# cancelButton = Button('Cancel', 200, 40, (250, 450), 5)

# Draw initial game board
game_board.draw_board(screen)
pygame.display.update()

# Function to draw GUI buttons
def buttons_draw():
    for button in buttons:
        button.draw()

# Function to display text on screen
def text_on_screen(content, font, w, h):
    ''' Renders content with font '''
    fps_surface = font.render(content, 1, pygame.Color("#f78f19"))
    text_width = fps_surface.get_width()
    # the control to go to the next line when is going out of the screen
    if w + text_width > screen.get_width():
        start = 0
        for word in content.split():
            wr = font.render(word + " ", 1, pygame.Color("#f78f19"))
            if w + start + wr.get_width() < screen.get_width():
                screen.blit(wr, (w + start, h))
                start += wr.get_width()
            else:
                start = 0
                h = h + wr.get_height()
                screen.blit(wr, (w + start, h))
                start += wr.get_width()
    else:
        screen.blit(fps_surface, (w, h))

# Main game loop
while not game_over:
    for event in pygame.event.get():
        # Exit the game if the user quits
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Process start button press
        if startButton.pressed:
            game_board.draw_board(screen)
            pygame.display.update()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, player1.color, (posx, int(
                        SQUARESIZE / 2)), game_board.RADIUS)  # Use game_board.RADIUS
                else:
                    pygame.draw.circle(screen, player2.color, (posx, int(
                        SQUARESIZE / 2)), game_board.RADIUS)  # Use game_board.RADIUS
                pygame.display.update()
            # Handle mouse motion for token placement          
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                col = int(math.floor(event.pos[0] / SQUARESIZE))

                if game_board.is_valid_location(col):
                    row = game_board.get_next_open_row(col)
                    if turn == 0:
                        game_board.drop_piece(row, col, player1.id)
                        if game_board.winning_move(player1.id):
                            label = myfont.render(
                                "Player 1 wins!!", 1, player1.color)
                            screen.blit(label, (40, 10))
                            game_over = True
                    else:
                        game_board.drop_piece(row, col, player2.id)
                        if game_board.winning_move(player2.id):
                            label = myfont.render(
                                "Player 2 wins!!", 1, player2.color)
                            screen.blit(label, (40, 10))
                            game_over = True

                    game_board.print_board()
                    game_board.draw_board(screen)

                    turn += 1
                    turn %= 2

                if game_over:
                    pygame.time.wait(2000)
                    del game_board
                    screen.fill('#DCDDD8')
                    buttons_draw()
                    startButton.pressed = False

                    pygame.display.update()
                    game_board = Board(ROW_COUNT, COLUMN_COUNT)
                    game_over = False
                    clock.tick(60)

        if not startButton.pressed:
            screen.fill('#DCDDD8')
            text_on_screen(DESCRIPTION, details_font, 30, 40)
            buttons_draw()

            pygame.display.update()
            clock.tick(60)

        if quitButton.pressed:
            pygame.quit()
            sys.exit()
