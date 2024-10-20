import pygame
import sys
import random

# THANKS FOR WATCHING, WHAT KIND OF GAMES U WANT TO SEE NEXT TIME? PLEASE STATE IT IN THE COMMENTS
# CHEERS

speed = 15

# window sizes
frame_size_x = 1380
frame_size_y = 840

check_errors = pygame.init()

if check_errors[1] > 0:
    print("Error " + check_errors[1])
else:
    print("Game Successfully initialized")

# initialize game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
violet = pygame.Color(148, 0, 211)
yellow = pygame.Color(255, 255, 0)
celeste = pygame.Color(0, 255, 255)
gray = pygame.Color(128, 128, 128)

# initial snake color
snake_color = green

fps_controller = pygame.time.Clock()
# one snake square size
square_size = 60


def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, score, direction, last_food_pos
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    last_food_pos = None
    spawn_food()
    score = 0


def spawn_food():
    global food_pos, food_spawn, last_food_pos
    while True:
        new_food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                        random.randrange(1, (frame_size_y // square_size)) * square_size]
        if new_food_pos != last_food_pos:
            food_pos = new_food_pos
            food_spawn = True
            break


init_vars()


def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render("Score: " + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)

    game_window.blit(score_surface, score_rect)


def main_menu():
    global snake_color
    while True:
        game_window.fill(black)
        menu_font = pygame.font.SysFont('consolas', 50)
        play_surface = menu_font.render('Press ENTER to Play', True, white)
        color_surface = menu_font.render(
            'Press C to Change Color', True, white)
        exit_surface = menu_font.render('Press ESC to Exit', True, white)
        game_window.blit(play_surface, (frame_size_x / 3, frame_size_y / 3))
        game_window.blit(color_surface, (frame_size_x / 3, frame_size_y / 2.5))
        game_window.blit(exit_surface, (frame_size_x / 3, frame_size_y / 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_c:
                    change_color_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


def change_color_menu():
    global snake_color
    colors = {
        "V": violet,
        "R": red,
        "B": blue,
        "G": green,
        "Y": yellow,
        "C": celeste,
        "A": gray
    }
    color_names = {
        "V": "Violet",
        "R": "Red",
        "B": "Blue",
        "G": "Green",
        "Y": "Yellow",
        "C": "Celeste",
        "A": "Gray"
    }

    while True:
        game_window.fill(black)
        menu_font = pygame.font.SysFont('consolas', 50)
        y_pos = frame_size_y / 6
        for key in colors.keys():
            color_surface = menu_font.render(
                f'Press {key} for {color_names[key]}', True, colors[key])
            game_window.blit(color_surface, (frame_size_x / 4, y_pos))
            y_pos += 70
        back_surface = menu_font.render(
            'Press BACKSPACE to go back', True, white)
        game_window.blit(back_surface, (frame_size_x / 4, y_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    return
                elif chr(event.key).upper() in colors:
                    snake_color = colors[chr(event.key).upper()]


main_menu()

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP or event.key == ord("w") and direction != "DOWN"):
                direction = "UP"
            elif (event.key == pygame.K_DOWN or event.key == ord("s") and direction != "UP"):
                direction = "DOWN"
            elif (event.key == pygame.K_LEFT or event.key == ord("a") and direction != "RIGHT"):
                direction = "LEFT"
            elif (event.key == pygame.K_RIGHT or event.key == ord("d") and direction != "LEFT"):
                direction = "RIGHT"

    if direction == "UP":
        head_pos[1] -= square_size
    elif direction == "DOWN":
        head_pos[1] += square_size
    elif direction == "LEFT":
        head_pos[0] -= square_size
    else:
        head_pos[0] += square_size

    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] > frame_size_x - square_size:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] > frame_size_y - square_size:
        head_pos[1] = 0

    # eating apple
    snake_body.insert(0, list(head_pos))
    if head_pos[0] == food_pos[0] and head_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
        last_food_pos = food_pos[:]
    else:
        snake_body.pop()

    # spawn food
    if not food_spawn:
        spawn_food()

    # GFX
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, snake_color, pygame.Rect(
            pos[0] + 2, pos[1] + 2,
            square_size - 2, square_size - 2))

    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0],
                                                   food_pos[1], square_size, square_size))

    # game over conditions
    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            init_vars()

    show_score(1, white, 'consolas', 20)
    pygame.display.update()
    fps_controller.tick(speed)
