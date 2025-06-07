"""
Snake Eater
Made with PyGame
Last modification in January 2024 by José Carlos Pulido
Machine Learning Classes - University Carlos III of Madrid
"""
from wekaI import Weka
import pygame, sys, time, random
import os
# DIFFICULTY settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
DIFFICULTY = 10

# Window size
FRAME_SIZE_X = 480
FRAME_SIZE_Y = 480

# Colors (R, G, B)
BLACK = pygame.Color(51, 51, 51)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(204, 51, 0)
GREEN = pygame.Color(204, 255, 153)
BLUE = pygame.Color(0, 51, 102)

# GAME STATE CLASS
class GameState:
    def __init__(self, FRAME_SIZE):
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]
        self.food_pos = [random.randrange(1, (FRAME_SIZE[0]//10)) * 10, random.randrange(1, (FRAME_SIZE[1]//10)) * 10]
        self.food_spawn = True
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0


# Game Over
def game_over(game):
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, WHITE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/4)
    game_window.fill(BLUE)
    game_window.blit(game_over_surface, game_over_rect)
    show_score(game, 0, WHITE, 'times', 20)
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

# Score
def show_score(game, choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(game.score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (FRAME_SIZE_X/8, 15)
    else:
        score_rect.midtop = (FRAME_SIZE_X/2, FRAME_SIZE_Y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()

# Move the snake
def move_keyboard(game, event):
    # Whenever a key is pressed down
    change_to = game.direction
    if event.type == pygame.KEYDOWN:
        # W -> Up; S -> Down; A -> Left; D -> Right
        if (event.key == pygame.K_UP or event.key == ord('w')) and game.direction != 'DOWN':
            change_to = 'UP'
        if (event.key == pygame.K_DOWN or event.key == ord('s')) and game.direction != 'UP':
            change_to = 'DOWN'
        if (event.key == pygame.K_LEFT or event.key == ord('a')) and game.direction != 'RIGHT':
            change_to = 'LEFT'
        if (event.key == pygame.K_RIGHT or event.key == ord('d')) and game.direction != 'LEFT':
            change_to = 'RIGHT'
    game.change_to = change_to
    return change_to

# TODO: IMPLEMENT HERE THE NEW INTELLIGENT METHOD

def add_lists(list1, list2):
    result = []
    for x, y in zip(list1, list2):
        result.append(x + y)
    return result

def compute_next_state(direction, game):
    if direction == 'RIGHT':
        vdir = [10, 0]
    if direction == 'LEFT':
        vdir = [-10, 0]
    if direction == 'UP':
        vdir = [0, -10]
    if direction == 'DOWN':
        vdir = [0, 10]

    # summing the vector of movement to all the coordinates of the snake's body position
    new_head = add_lists(game.snake_pos, vdir)
    new_body = game.snake_body[:-1]
    result_body = [new_head] + new_body

    next_game = GameState((FRAME_SIZE_X,FRAME_SIZE_Y))
    next_game.snake_pos = new_head
    next_game.food_pos = game.food_pos
    next_game.direction = game.direction
    next_game.snake_body = result_body
    next_game.food_spawn = game.food_spawn
    next_game.change_to = game.change_to
    if check_end(next_game) == False:
        next_game.score = game.score - 1 #esto significaria que te mueres
    else:
        if new_head == game.food_pos:
            next_game.score = game.score + 100
        else:
            next_game.score = game.score - 1
    return next_game

def check_end(game):
    result_body = game.snake_body
    new_head = game.snake_pos

    for block in result_body[1:]:
        if new_head[0] == block[0] and new_head[1] == block[1]:
            return False
    if result_body[0][0] >= 480 or result_body[0][1] >= 480 or result_body[0][0] <=0 or result_body[0][1] <=0:
        return False
    return True

# PRINTING DATA FROM GAME STATE
def print_state(game):
    print("--------GAME STATE--------")
    print("FrameSize:", FRAME_SIZE_X, FRAME_SIZE_Y)
    print("Direction:", game.direction)
    print("Snake X:", game.snake_pos[0], ", Snake Y:", game.snake_pos[1])
    print("Snake Body:", game.snake_body)
    print("Food X:", game.food_pos[0], ", Food Y:", game.food_pos[1])
    print("Score:", game.score)

# TODO: IMPLEMENT HERE THE NEW INTELLIGENT METHOD
def compute_next_score(game): #*DOUBT: Como escribir la score si te mueres?
    new_game = compute_next_state(game.direction, game)
    return new_game.score

def compute_next_food_x(game):
    new_game = compute_next_state(game.direction, game)
    return new_game.snake_pos[0] - new_game.food_pos[0]

def compute_next_food_y(game):
    new_game = compute_next_state(game.direction, game)
    return new_game.snake_pos[1] - new_game.food_pos[1]

def compute_next_w_down(game):
    new_game = compute_next_state(game.direction, game)
    return FRAME_SIZE_Y - new_game.snake_pos[1]

def compute_next_w_right(game):
    new_game = compute_next_state(game.direction, game)
    return FRAME_SIZE_X - new_game.snake_pos[0]


def write_direction(direction):
    if direction == 'UP':
        return "1"
    if direction == 'DOWN':
        return "2"
    if direction == 'LEFT':
        return "3"
    if direction == 'RIGHT':
        return "4"

def create_line(game, last_direction):
    x = []
    r = 30  # the radius of the close up
    snake_body_pos = ""
    for j in range(game.snake_pos[1] - r, game.snake_pos[1] + r + 10, 10):
        for i in range(game.snake_pos[0] - r, game.snake_pos[0] + r + 10, 10):
            if i < 0 or j < 0 or i > FRAME_SIZE_X or j > FRAME_SIZE_Y:
                snake_body_pos += "1"
            else:
                if [i, j] == game.snake_pos:
                    snake_body_pos += "2"
                else:
                    if [i, j] in game.snake_body:
                        snake_body_pos += "1"
                    else:
                        snake_body_pos += "0"
    snake_body_dis_h = []  # distance to the body horizontally
    snake_body_dis_v = []  # distance to the body vertically
    g = 30  # number of positions of the body taken into account
    for i in range(1, len(game.snake_body)):
        dis_x = game.snake_pos[0] - game.snake_body[i][0]
        dis_y = game.snake_pos[1] - game.snake_body[i][1]
        snake_body_dis_h.append(dis_x)
        snake_body_dis_v.append(dis_y)
    for j in range(i, g):
        dis_x = 480
        dis_y = 480
        snake_body_dis_h.append(dis_x)
        snake_body_dis_v.append(dis_y)
    food_pos_x, food_pos_y = game.food_pos
    head_pos_x, head_pos_y = game.snake_pos
    score = game.score
    actual_direction = write_direction(game.direction)
    distance_food_x = head_pos_x - food_pos_x
    distance_food_y = head_pos_y - food_pos_y
    dis_food_x_abs = abs(distance_food_x)
    dis_food_y_abs = abs(distance_food_y)
    distance_wall_down = FRAME_SIZE_Y - head_pos_y
    distance_wall_right = FRAME_SIZE_X - head_pos_x
    last_dir = write_direction(last_direction)

    # Create the vector
    #x = [str(i) for i in snake_body_pos]
    #x.extend([head_pos_x,head_pos_y,food_pos_x,food_pos_y,score,dis_food_x_abs,dis_food_y_abs,distance_wall_down, distance_wall_right])
    x.extend([head_pos_x,head_pos_y,food_pos_x,food_pos_y,score,distance_food_x,distance_food_y,dis_food_x_abs,dis_food_y_abs,distance_wall_down, distance_wall_right])
    #x.extend([i for i in snake_body_dis_h])
    #x.extend([i for i in snake_body_dis_v])
    #x.extend([str(actual_direction)])
    x.extend([str(last_dir),str(actual_direction)])
    return x


def print_line_data(game, last_direction):
    if not os.path.exists("test_keyboard_v4_final.arff"):
        with open("test_keyboard_v4_final.arff", 'a') as result_file:
            result_file.write("@relation Snake_Game\n\n")
            # Write snake body attributes
            r = 30
            for j in range(game.snake_pos[1] - r, game.snake_pos[1] + r + 10, 10):
                for i in range(game.snake_pos[0] - r, game.snake_pos[0] + r + 10, 10):
                    result_file.write(f"@attribute snake_body_pos{i - game.snake_pos[0]}_{j - game.snake_pos[1]} {{0, 1, 2}}\n")

            result_file.write("@attribute head_pos_x numeric\n")
            result_file.write("@attribute head_pos_y numeric\n")
            result_file.write("@attribute food_pos_x numeric\n")
            result_file.write("@attribute food_pos_y numeric\n")
            result_file.write("@attribute score numeric\n")
            result_file.write("@attribute distance_food_x numeric\n\n")
            result_file.write("@attribute distance_food_y numeric\n\n")
            result_file.write("@attribute distance_food_x_abs numeric\n\n")
            result_file.write("@attribute distance_food_y_abs numeric\n\n")
            result_file.write("@attribute distance_wall_down numeric\n\n")
            result_file.write("@attribute distance_wall_right numeric\n\n")
            for j in range(0,30):
                result_file.write(f"@attribute snake_body_dis_h{j+1} numeric\n")
            for j in range(0,30):
                result_file.write(f"@attribute snake_body_dis_v{j+1} numeric\n")
            result_file.write("@attribute last_direction {1, 2, 3, 4}\n")
            result_file.write("@attribute next_score numeric\n\n")
            result_file.write("@attribute next_food_x numeric\n\n")
            result_file.write("@attribute next_food_y numeric\n\n")
            result_file.write("@attribute next_head_x numeric\n\n")
            result_file.write("@attribute next_head_y numeric\n\n")
            result_file.write("@attribute next_dis_wall_down numeric\n\n")
            result_file.write("@attribute next_dis_wall_right numeric\n\n")
            result_file.write("@attribute actual_direction {1, 2, 3, 4}\n")

            result_file.write("@data\n")

    with open("test_keyboard_v4_final.arff", 'a') as result_file:
        # Write game state, action, and next score for each instance
        #snake_body = ''.join([f"{x:03d}{y:03d}" for x, y in game.snake_body])
        r = 30 #the radius of the close up
        snake_body_pos = ""
        for j in range(game.snake_pos[1] - r, game.snake_pos[1] + r + 10, 10):
            for i in range(game.snake_pos[0] - r, game.snake_pos[0] + r + 10, 10):
                if i < 0 or j < 0 or i > FRAME_SIZE_X or j > FRAME_SIZE_Y:
                    snake_body_pos += "1,"
                else:
                    if [i,j] == game.snake_pos:
                        snake_body_pos += "2,"
                    else:
                        if [i, j] in game.snake_body:
                            snake_body_pos += "1,"
                        else:
                            snake_body_pos += "0,"
        snake_body_dis_h = "" #distance to the body horizontally
        snake_body_dis_v = "" #distance to the body vertically
        g = 30 #number of positions of the body taken into account
        for i in range(1, len(game.snake_body)):
            dis_x = game.snake_pos[0] - game.snake_body[i][0]
            dis_y = game.snake_pos[1] - game.snake_body[i][1]
            snake_body_dis_h += f'{dis_x},'
            snake_body_dis_v += f'{dis_y},'
        for j in range(i, g):
            dis_x = 480
            dis_y = 480
            snake_body_dis_h += f'{dis_x},'
            snake_body_dis_v += f'{dis_y},'

        food_pos_x, food_pos_y = game.food_pos
        head_pos_x, head_pos_y = game.snake_pos
        score = game.score
        actual_direction = write_direction(game.direction)
        distance_food_x = head_pos_x - food_pos_x
        distance_food_y = head_pos_y - food_pos_y
        dis_food_x_abs = abs(distance_food_x)
        dis_food_y_abs = abs(distance_food_y)
        distance_wall_down = FRAME_SIZE_Y - head_pos_y
        distance_wall_right = FRAME_SIZE_X - head_pos_x
        last_dir = write_direction(last_direction)
        next_score = compute_next_score(game)
        next_food_x = compute_next_food_x(game)
        next_food_y = compute_next_food_y(game)
        next_dis_wall_down = compute_next_w_down(game)
        next_dis_wall_right =compute_next_w_right(game)
        next_head_x = compute_next_state(game.direction, game).snake_pos[0]
        next_head_y = compute_next_state(game.direction, game).snake_pos[1]

        # Write data instance
        result_file.write(f'{snake_body_pos}{head_pos_x},{head_pos_y},{food_pos_x},{food_pos_y},{score},{distance_food_x},{distance_food_y},{dis_food_x_abs},{dis_food_y_abs},{distance_wall_down},{distance_wall_right},{snake_body_dis_h}{snake_body_dis_v}{last_dir},{next_score},{next_food_x},{next_food_y},{next_head_x},{next_head_y},{next_dis_wall_down},{next_dis_wall_right},{actual_direction}\n')

# Checks for errors encounteRED
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption('Snake Eater - Machine Learning (UC3M)')
game_window = pygame.display.set_mode((FRAME_SIZE_X, FRAME_SIZE_Y))

weka=Weka()
weka.start_jvm()
direction_vector = []


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()
v_direction = []
# Main logic
game = GameState((FRAME_SIZE_X,FRAME_SIZE_Y))
v_direction.append(game.direction)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            # Esc -> Create event to quit the game
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
        # CALLING MOVE METHOD
        v_direction.append(game.direction)
        #game.direction = move_keyboard(game, event)

    # UNCOMMENT WHEN METHOD IS IMPLEMENTED

    #game.direction = move_tutorial_1(game)
    last_direction = v_direction[-1]
    
    
    print_line_data(game, last_direction)
    print_state(game)
    x = create_line(game, last_direction)
    print(x)
    a = weka.predict("./RandomTree_v5_anybody.model", x, "./training_keyboard_v5_anybody.arff")
    print(a)
    # Moving the snake
    if a == '1' and game.direction != 'DOWN':
        game.direction = 'UP'
    elif a == '2' and game.direction != 'UP':
        game.direction = 'DOWN'
    elif a == '3' and game.direction != 'RIGHT':
        game.direction = 'LEFT'
    elif a == '4' and game.direction != 'LEFT':
        game.direction = 'RIGHT'
    
    # Moving the snake
    if game.direction == 'UP':
        game.snake_pos[1] -= 10
    if game.direction == 'DOWN':
        game.snake_pos[1] += 10
    if game.direction == 'LEFT':
        game.snake_pos[0] -= 10
    if game.direction == 'RIGHT':
        game.snake_pos[0] += 10
    # Snake body growing mechanism
    game.snake_body.insert(0, list(game.snake_pos))

    if game.snake_pos[0] == game.food_pos[0] and game.snake_pos[1] == game.food_pos[1]:
        game.score += 100
        game.food_spawn = False
    else:
        game.snake_body.pop()
        game.score -= 1

    # Spawning food on the screen
    if not game.food_spawn:
        game.food_pos = [random.randrange(1, (FRAME_SIZE_X//10)) * 10, random.randrange(1, (FRAME_SIZE_Y//10)) * 10]
    game.food_spawn = True

    # GFX
    game_window.fill(BLUE)
    for pos in game.snake_body:
        # Snake body
        # .draw.rect(play_surface, color, xy-coordinate)
        # xy-coordinate -> .Rect(x, y, size_x, size_y)
        pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

    # Snake food
    pygame.draw.rect(game_window, RED, pygame.Rect(game.food_pos[0], game.food_pos[1], 10, 10))

    # Game Over conditions
    # Getting out of bounds
    if game.snake_pos[0] < 0 or game.snake_pos[0] > FRAME_SIZE_X-10:
        game_over(game)
    if game.snake_pos[1] < 0 or game.snake_pos[1] > FRAME_SIZE_Y-10:
        game_over(game)
    # Touching the snake body
    for block in game.snake_body[1:]:
        if game.snake_pos[0] == block[0] and game.snake_pos[1] == block[1]:
            game_over(game)

    show_score(game, 1, WHITE, 'consolas', 15)
    # Refresh game screen
    pygame.display.update()
    # Refresh rate
    fps_controller.tick(DIFFICULTY)
    # PRINTING STATE (we decided to move this)
    #print_state(game)
    #print_line_data(game, last_direction)
