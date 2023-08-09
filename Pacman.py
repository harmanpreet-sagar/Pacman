# Harmanpreet Singh Sagar
# Pacman Game

import pygame

# Set base colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)

# Set game icon
pacman = pygame.image.load('images_Pacman/pacman.png')
pygame.display.set_icon(pacman)

# Set game music
pygame.mixer.init()
pygame.mixer.music.load('pacman.ogg')
pygame.mixer.music.play(-1, 0.0)


# This is our wall class
class Wall(pygame.sprite.Sprite):

    # Constructor function
    def __init__(self, x, y, width, height, color):
        # Call parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make the top-left corner the passed-in location
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x


def setupRoomOne(all_sprites_list):
    # Make the walls
    wall_list = pygame.sprite.RenderPlain()

    # This is our list of walls
    walls = [[0, 0, 6, 600],
             [0, 0, 600, 6],
             [0, 600, 606, 6],
             [600, 0, 6, 606],
             [300, 0, 6, 66],
             [60, 60, 186, 6],
             [360, 60, 186, 6],
             [60, 120, 66, 6],
             [60, 120, 6, 126],
             [180, 120, 246, 6],
             [300, 120, 6, 66],
             [480, 120, 66, 6],
             [540, 120, 6, 126],
             [120, 180, 126, 6],
             [120, 180, 6, 126],
             [360, 180, 126, 6],
             [480, 180, 6, 126],
             [180, 240, 6, 126],
             [180, 360, 246, 6],
             [420, 240, 6, 126],
             [240, 240, 42, 6],
             [324, 240, 42, 6],
             [240, 240, 6, 66],
             [240, 300, 126, 6],
             [360, 240, 6, 66],
             [0, 300, 66, 6],
             [540, 300, 66, 6],
             [60, 360, 66, 6],
             [60, 360, 6, 186],
             [480, 360, 66, 6],
             [540, 360, 6, 186],
             [120, 420, 366, 6],
             [120, 420, 6, 66],
             [480, 420, 6, 66],
             [180, 480, 246, 6],
             [300, 480, 6, 66],
             [120, 540, 126, 6],
             [360, 540, 126, 6]
             ]

    # Loop through the list. Create a wall, and add it to the list
    for item in walls:
        wall = Wall(item[0], item[1], item[2], item[3], BLUE)
        wall_list.add(wall)
        all_sprites_list.add(wall)

    # Return wall list
    return wall_list


# Setup the ghost gate
def setupGate(all_sprites_list):
    gate = pygame.sprite.RenderPlain()
    gate.add(Wall(282, 242, 42, 2, WHITE))
    all_sprites_list.add(gate)
    return gate


# This class is for the ball
class Block(pygame.sprite.Sprite):

    # Constructor. Pass in color of block and x and y coordinate
    def __init__(self, color, width, height):
        # Call parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block and fill with color
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()


# This is the main PacMan player class
class Player(pygame.sprite.Sprite):
    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, x, y, filename):
        # Call parent constructor
        pygame.sprite.Sprite.__init__(self)

        # Set height, width
        self.image = pygame.image.load(filename).convert()

        # Make top left corner passed-in location
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    # Clear speed of player
    def prevDirection(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    # Change speed of player
    def changeSpeed(self, x, y):
        self.change_x += x
        self.change_y += y

    # Find new position for player
    def update(self, walls, gate):

        # Get old position
        old_x = self.rect.left
        new_x = old_x + self.change_x
        prev_x = old_x + self.prev_x
        self.rect.left = new_x

        old_y = self.rect.top
        new_y = old_y + self.change_y
        prev_y = old_y + self.prev_y

        # Did we hit a wall?
        x_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_collide:
            # We hit a wall, go back to old position
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            # Did the update cause us to hit a wall?
            y_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_collide:
                # We hit a wall, go back to old position
                self.rect.top = old_y

        if gate:
            gate_hit = pygame.sprite.spritecollide(self, gate, False)
            if gate_hit:
                self.rect.left = old_x
                self.rect.top = old_y


class Ghost(Player):
    # Change speed of the ghost
    def changeSpeed(self, list, ghost, turn, steps, l):
        try:
            z = list[turn][2]
            if steps < z:
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps += 1
            else:
                if turn < l:
                    turn += 1
                elif ghost == "clyde":
                    turn = 2
                else:
                    turn = 0
                self.change_x = list[turn][0]
                self.change_y = list[turn][1]
                steps = 0
            return [turn, steps]
        except IndexError:
            return [0, 0]


Pinky_directions = [
    [0, -30, 4],
    [15, 0, 9],
    [0, 15, 11],
    [-15, 0, 23],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 19],
    [0, 15, 3],
    [15, 0, 3],
    [0, 15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 7],
    [0, 15, 3],
    [-15, 0, 19],
    [0, -15, 11],
    [15, 0, 9]
]

Blinky_directions = [
    [0, -15, 4],
    [15, 0, 9],
    [0, 15, 11],
    [15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [15, 0, 15],
    [0, -15, 15],
    [15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 11],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 7],
    [0, -15, 3],
    [15, 0, 15],
    [0, 15, 15],
    [-15, 0, 3],
    [0, 15, 3],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 5]
]

Inky_directions = [
    [30, 0, 2],
    [0, -15, 4],
    [15, 0, 10],
    [0, 15, 7],
    [15, 0, 3],
    [0, -15, 3],
    [15, 0, 3],
    [0, -15, 15],
    [-15, 0, 15],
    [0, 15, 3],
    [15, 0, 15],
    [0, 15, 11],
    [-15, 0, 3],
    [0, -15, 7],
    [-15, 0, 11],
    [0, 15, 3],
    [-15, 0, 11],
    [0, 15, 7],
    [-15, 0, 3],
    [0, -15, 3],
    [-15, 0, 3],
    [0, -15, 15],
    [15, 0, 15],
    [0, 15, 3],
    [-15, 0, 15],
    [0, 15, 11],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 11],
    [0, 15, 3],
    [15, 0, 1],
]

Clyde_directions = [
    [-30, 0, 2],
    [0, -15, 4],
    [15, 0, 5],
    [0, 15, 7],
    [-15, 0, 11],
    [0, -15, 7],
    [-15, 0, 3],
    [0, 15, 7],
    [-15, 0, 7],
    [0, 15, 15],
    [15, 0, 15],
    [0, -15, 3],
    [-15, 0, 11],
    [0, -15, 7],
    [15, 0, 3],
    [0, -15, 11],
    [15, 0, 9],
]

pl = len(Pinky_directions) - 1
bl = len(Blinky_directions) - 1
il = len(Inky_directions) - 1
cl = len(Clyde_directions) - 1

# Initialize pygame
pygame.init()

# Create window
screen = pygame.display.set_mode([606, 606])

pygame.display.set_caption('Pac-Man')

background = pygame.Surface(screen.get_size())

background = background.convert()

background.fill(BLACK)

clock = pygame.time.Clock()

pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 24)

# Default location for Pac-Man and monsters
w = 303 - 16
p_h = (7 * 60) + 19
m_h = (4 * 60) + 19
b_h = (3 * 60) + 19
i_w = 303 - 13 - 32
c_w = 303 + (32 - 16)


# Start Game function
def startGame():
    all_sprites_list = pygame.sprite.RenderPlain()

    block_list = pygame.sprite.RenderPlain()

    monster_list = pygame.sprite.RenderPlain()

    pacman_collide = pygame.sprite.RenderPlain()

    wall_list = setupRoomOne(all_sprites_list)

    gate = setupGate(all_sprites_list)

    p_turn = 0
    p_steps = 0

    b_turn = 0
    b_steps = 0

    i_turn = 0
    i_steps = 0

    c_turn = 0
    c_steps = 0

    # Create player and ghost
    Pacman = Player(w, p_h, "images_Pacman/pacman.png")
    all_sprites_list.add(Pacman)
    pacman_collide.add(Pacman)

    Blinky = Ghost(w, b_h, "images_Pacman/blinky.png")
    all_sprites_list.add(Blinky)
    monster_list.add(Blinky)

    Pinky = Ghost(w, m_h, "images_Pacman/pinky.png")
    all_sprites_list.add(Pinky)
    monster_list.add(Pinky)

    Inky = Ghost(i_w, m_h, "images_Pacman/inky.png")
    all_sprites_list.add(Inky)
    monster_list.add(Inky)

    Clyde = Ghost(i_w, m_h, "images_Pacman/clyde.png")
    all_sprites_list.add(Clyde)
    monster_list.add(Clyde)

    # Draw grid
    for row in range(19):
        for column in range(19):
            if (row == 7 or row == 8) and (column == 8 or column == 9 or column == 10):
                continue
            else:
                block = Block(YELLOW, 4, 4)

            # Set a random location for Block
            block.rect.x = (30 * column + 6) + 26
            block.rect.y = (30 * row + 6) + 26

            b_collide = pygame.sprite.spritecollide(block, wall_list, False)
            p_collide = pygame.sprite.spritecollide(block, pacman_collide, False)

            if b_collide:
                continue
            elif p_collide:
                continue
            else:
                block_list.add(block)
                all_sprites_list.add(block)

    bll = len(block_list)

    score = 0

    done = False

    i = 0

    # Main Game Loop
    while done == False:
        # Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    Pacman.changeSpeed(-30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changeSpeed(30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changeSpeed(0, -30)
                if event.key == pygame.K_DOWN:
                    Pacman.changeSpeed(0, 30)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    Pacman.changeSpeed(30, 0)
                if event.key == pygame.K_RIGHT:
                    Pacman.changeSpeed(-30, 0)
                if event.key == pygame.K_UP:
                    Pacman.changeSpeed(0, 30)
                if event.key == pygame.K_DOWN:
                    Pacman.changeSpeed(0, -30)

        # Event processing goes above this line

        # Game logic goes below this code
        Pacman.update(wall_list, gate)

        returned = Pinky.changeSpeed(Pinky_directions, False, p_turn, p_steps, pl)
        p_turn = returned[0]
        p_steps = returned[1]
        Pinky.changeSpeed(Pinky_directions, False, p_turn, p_steps, pl)
        Pinky.update(wall_list, False)

        returned = Blinky.changeSpeed(Blinky_directions, False, b_turn, b_steps, bl)
        b_turn = returned[0]
        b_steps = returned[1]
        Blinky.changeSpeed(Blinky_directions, False, b_turn, b_steps, bl)
        Blinky.update(wall_list, False)

        returned = Inky.changeSpeed(Inky_directions, False, i_turn, i_steps, il)
        i_turn = returned[0]
        i_steps = returned[1]
        Inky.changeSpeed(Inky_directions, False, i_turn, i_steps, il)
        Inky.update(wall_list, False)

        returned = Clyde.changeSpeed(Clyde_directions, False, c_turn, c_steps, cl)
        c_turn = returned[0]
        c_steps = returned[1]
        Clyde.changeSpeed(Clyde_directions, False, c_turn, c_steps, cl)
        Clyde.update(wall_list, False)

        # See if Pac-Man has collided
        block_hit_list = pygame.sprite.spritecollide(Pacman, block_list, True)

        # Check list of collisions
        if len(block_hit_list) > 0:
            score += len(block_hit_list)

        # All game logic goes above this

        # All code to draw should go below this line
        screen.fill(BLACK)

        wall_list.draw(screen)
        gate.draw(screen)
        all_sprites_list.draw(screen)
        monster_list.draw(screen)

        text = font.render("Score: " + str(score) + "/" + str(bll), True, RED)
        screen.blit(text, [10, 10])

        if score == bll:
            doNext("Congratulations, you won!", 145, all_sprites_list, block_list, monster_list, pacman_collide,
                   wall_list, gate)

        monster_hit_list = pygame.sprite.spritecollide(Pacman, monster_list, False)

        if monster_hit_list:
            doNext("Game Over!", 235, all_sprites_list, block_list, monster_list, pacman_collide, wall_list, gate)

        # All code to draw goes above this line

        pygame.display.flip()

        clock.tick(10)


def doNext(message, left, all_sprites_list, block_list, monster_list, pacman_collide, wall_list, gate):
    while True:
        # Event processing goes below this line
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.key == pygame.K_RETURN:
                del all_sprites_list
                del block_list
                del monster_list
                del pacman_collide
                del wall_list
                del gate
                startGame()

        # Grey background
        w = pygame.Surface((400, 200))
        w.set_alpha(10)
        w.fill((128, 128, 128))
        screen.blit(w, (100, 200))

        # Won or lost
        text1 = font.render(message, True, WHITE)
        screen.blit(text1, [left, 233])

        text2 = font.render("To play again, press ENTER.", True, WHITE)
        screen.blit(text2, [135, 303])

        text3 = font.render("To quit, press ESCAPE.", True, WHITE)
        screen.blit(text3, [165, 333])

        pygame.display.flip()

        clock.tick(10)


startGame()

pygame.quit()

# END OF THE CODE
