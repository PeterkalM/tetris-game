import random
import copy
import pygame
import data.main as main
import data.text as text

# Default shapes for Tetris
# TODO: Add more shapes
o_shape = [
    [1, 1],
    [1, 1]
]

s_shape = [
    [0, 2, 2],
    [2, 2, 0],
    [0, 0, 0]
]

j_shape = [
    [3, 3, 3],
    [0, 0, 3],
    [0, 0, 0]
]

i_shape = [
    [0, 0, 0, 0],
    [4, 4, 4, 4],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]


def choose_random_piece():
    """ Select random piece from list """
    return random.choice([i_shape, j_shape, s_shape, o_shape])


class Game:
    def __init__(self, center_x, center_y):
        # Default variables for pygame and screen
        self.screen = pygame.display.get_surface()
        self.start_time = None
        self.center_x = center_x
        self.center_y = center_y

        # Loading fonts
        self.font = main.load_font("rockb.ttf", 30)
        self.game_over_font = main.load_font("rockb.ttf", 40)

        # Rendering texts
        self.time_text = self.font.render("TIME", False, (150, 150, 150))
        self.score_text = self.font.render("SCORE", False, (150, 150, 150))
        self.game_over_text = text.Text("GAME OVER", self.game_over_font,
                                        [self.center_x, self.center_y - 120], color=(255, 255, 255))

        # Loading images
        self.bg = main.load_image("bg.png")
        self.cubes = [
            main.load_image("y.png"),
            main.load_image("g.png"),
            main.load_image("b.png"),
            main.load_image("r.png"),
        ]

        # Default variables for game
        self.game_arena = [[0 for _ in range(10)] for _ in range(20)]
        self.static_arena = [[0 for _ in range(10)] for _ in range(20)]
        self.score = 0
        self.pos_x, self.pos_y = 3, 1
        self.game_over = False
        self.running = False

        # Generating pieces for starting game
        self.current_piece = choose_random_piece()
        self.next_piece = choose_random_piece()
        self.append_to_game_arena(self.current_piece)

    def move_down(self):
        """ Move current piece down by one cube

            Moves piece one cube down, but if it fails
            doing it then move piece up again, and
            add it to static arena, but if it also fails
            then it then means you just lost the game :(
        """
        self.pos_y += 1
        if not self.append_to_game_arena(self.current_piece):
            self.pos_y -= 1
            if self.append_to_game_arena(self.current_piece):
                self.static_arena = self.game_arena
                self.pos_x, self.pos_y = 3, 1
                self.current_piece = self.next_piece
                self.next_piece = choose_random_piece()
                if not self.append_to_game_arena(self.current_piece):
                    self.game_over = True
                    self.running = False
            else:
                self.game_over = True
                self.running = False
        else:
            return True

    def append_to_game_arena(self, piece):
        """ Append selected piece to game arena

            Try to add all cubes to current game arena,
            but if any cubes start overlapping then it
            marks process as failed, and outputs False.
            It also catches any outside of arena work.
        """
        test_arena = copy.deepcopy(self.static_arena)
        try:
            for y, row in enumerate(piece):
                for x, cube in enumerate(row):
                    # If there is a cube
                    if cube:
                        if self.pos_x + x < 0 or test_arena[self.pos_y + y][self.pos_x + x]:
                            return False
                        test_arena[self.pos_y + y][self.pos_x + x] = cube
            self.game_arena = test_arena
            return True
        except IndexError:
            return False

    def rotate_current_piece(self):
        """ Rotate current piece

            Tries to rotate piece, and restores
            original if it fails
        """
        rotated_piece = [list(y[::-1]) for y in zip(*self.current_piece)]
        if self.append_to_game_arena(rotated_piece):
            self.current_piece = rotated_piece

    def move_x_axis(self, move):
        """ Move piece left or right

            Again tries to move piece left or right,
            and if it fails then restore original pos.
        """
        old_pos = self.pos_x
        self.pos_x += move
        if not self.append_to_game_arena(self.current_piece):
            self.pos_x = old_pos

    def check_full_row(self):
        """ Checks if row if full, and later tries to delete it """
        delete = []
        for i in self.static_arena:
            if all(i):
                delete.append(i)

        for i in delete:
            self.score += 50
            self.static_arena.remove(i)
            self.static_arena.insert(0, [0 for _ in range(10)])

    def draw_arena(self, arena=None):
        """ Drawing all pieces to screen

            This also accepts arena argument so
            you could just generate arena yourself,
            and not rely on this class (e.g servers).
        """
        if arena is None:
            arena = self.game_arena

        for y, row in enumerate(arena[::-1]):
            for x, cube in enumerate(row):
                # Only draw when there is a cube (not 0)
                if cube:
                    self.screen.blit(self.cubes[cube - 1], [self.center_x - 160 + x * 32,
                                                            self.center_y + 280 - y * 32])

    def draw_background(self):
        """ Blit background to enclose arena """
        self.screen.blit(self.bg, [self.center_x - 165, self.center_y - 324])

    def draw_time(self):
        """ Drawing time text and current time onto screen

            It first computes current ongoing game time, and
            then blits time text and game time to screen.
        """
        time = self.font.render(self.get_time(), False, (255, 255, 255))
        self.screen.blit(self.time_text, [self.center_x + 175, self.center_y + 160])
        self.screen.blit(time, [self.center_x + 175, self.center_y + 190])

    def draw_score(self):
        """ Blits both current score, and score text that is above score text """
        score = self.font.render(str(self.score), False, (255, 255, 255))

        self.screen.blit(self.score_text, [self.center_x + 175, self.center_y + 235])
        self.screen.blit(score, [self.center_x + 175, self.center_y + 265])

    def get_time(self):
        """ Retrurns current running time

            If game is not running then returns 0:00
        """
        if self.start_time:
            time = (pygame.time.get_ticks() - self.start_time) // 1000
            return str(time // 60) + ":" + '{:02d}'.format(time % 60)
        else:
            return "0:00"
