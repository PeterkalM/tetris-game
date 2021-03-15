import sys

import pygame
import pygame.locals

import data.ai as ai
import data.game as game
import data.main as main
import data.text as text

PLAY_AI = True

# Initialize pygame and window
pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode((600, 800))  # , pygame.FULLSCREEN)
width, height = pygame.display.get_surface().get_size()

# Load fonts
rock_font_40 = main.load_font("rockb.ttf", 40)
rock_font_50 = main.load_font("rockb.ttf", 50)

# Load sounds
music = main.load_music("tetris.ogg")
click = main.load_sfx("click.ogg")

# Key press event for AI handler
event_space = pygame.event.Event(
    pygame.locals.KEYDOWN, unicode=" ", key=pygame.locals.K_SPACE, mod=pygame.locals.KMOD_NONE)
event_right = pygame.event.Event(
    pygame.locals.KEYDOWN, unicode="d", key=pygame.locals.K_d, mod=pygame.locals.KMOD_NONE)
event_left = pygame.event.Event(
    pygame.locals.KEYDOWN, unicode="a", key=pygame.locals.K_a, mod=pygame.locals.KMOD_NONE)
event_rotate = pygame.event.Event(
    pygame.locals.KEYDOWN, unicode="r", key=pygame.locals.K_r, mod=pygame.locals.KMOD_NONE)
event_down = pygame.event.Event(
    pygame.locals.KEYDOWN, unicode="", key=pygame.locals.K_DOWN, mod=pygame.locals.KMOD_NONE)


def singleplayer():
    main_game = game.Game(width / 2, height / 2)

    # Clock to check game running speed
    clock = pygame.time.Clock()
    count = 4
    countdown_text = text.Text(3, rock_font_50, [width / 2, height / 2 - 120], color=(255, 255, 255))

    # Music settings
    music.set_volume(0.25)
    music.play(-1)
    faster = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    music.stop()
                    return
                if main_game.running:
                    if event.key == pygame.K_SPACE:
                        while main_game.move_down():
                            main_game.score += 1
                    if PLAY_AI:
                        if event.key == pygame.K_a:
                            main_game.move_x_axis(-1)
                        elif event.key == pygame.K_d:
                            main_game.move_x_axis(1)
                        elif event.key == pygame.K_r:
                            main_game.rotate_current_piece()

        if not main_game.game_over:
            screen.fill((0, 0, 0))

            main_game.draw_time()
            main_game.draw_score()

            dt = clock.tick()

            # Countdown function
            # TODO: Make it more compact
            if countdown_text:
                if countdown_text.text > 1:
                    count -= 1
                    countdown_text.text = count

                    countdown_text.draw()
                    main_game.draw_background()
                    pygame.display.flip()

                    pygame.time.delay(900)
                else:
                    countdown_text.text = "GO!"
                    countdown_text.recenter()

                    countdown_text.draw()
                    main_game.draw_background()
                    pygame.display.flip()

                    pygame.time.delay(1000)
                    screen.fill((0, 0, 0))
                    main_game.draw_time()
                    main_game.draw_score()

                    countdown_text = None
                    main_game.running = True
                    main_game.start_time = pygame.time.get_ticks()

            if main_game.running:
                main_game.check_full_row()

                count += dt
                speed = 1000

                if PLAY_AI:
                    faster = True

                # Get all key presses
                # TODO: Maybe move it up
                pressed = pygame.key.get_pressed()

                # Rotate piece on R key press or W key press
                if pressed[pygame.K_r] or pressed[pygame.K_w] or pressed[pygame.K_UP]:
                    main_game.rotate_current_piece()

                # Move piece to left on A key press
                if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                    main_game.move_x_axis(-1)

                # Move piece to right on D key press
                if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                    main_game.move_x_axis(1)

                if faster or pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                    speed = 1
                    main_game.score += 1

                if PLAY_AI:
                    if main_game.pos_x == 3 and main_game.pos_y == 1:
                        loc, shape = ai.play_ai(main_game.static_arena, main_game.current_piece)
                        for _ in range(shape):
                            pygame.event.post(event_rotate)
                        c = loc[0] - main_game.pos_x
                        for _ in range(abs(c)):
                            if loc[0] > main_game.pos_x:
                                pygame.event.post(event_right)
                            else:
                                pygame.event.post(event_left)
                pygame.event.post(event_down)

                if count > speed:
                    main_game.move_down()
                    count = 0

                main_game.draw_arena()

            main_game.draw_background()

            pygame.time.delay(100)
        else:
            main_game.game_over_text.draw()

        pygame.display.flip()


def load_menu():
    options = [text.Text("PLAY GAME", rock_font_50, (width / 2, height / 2 - 100)),
               text.Text("EXIT", rock_font_50, (width / 2, height / 2))]

    while True:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            # Nice quit on quit
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            # If player is clicked on button then to what progam needs to do
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for option in options:
                    if option.rect.collidepoint(mouse_pos):
                        # Start game
                        if option.text == "PLAY GAME":
                            click.play()
                            singleplayer()
                        # Exit game
                        elif option.text == "EXIT":
                            click.play()
                            pygame.quit()
                            return

        screen.fill((0, 0, 0))

        # Loop through option buttons, and if mouse is
        # hovering over it then change colors
        for option in options:
            if option.rect.collidepoint(mouse_pos):
                option.hovered = True
            else:
                option.hovered = False
            option.draw()

        pygame.display.update()


if __name__ == "__main__":
    load_menu()
