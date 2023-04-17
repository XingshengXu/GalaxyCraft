import os
from sys import exit
import pygame

# Initialization
pygame.init()  # Pygame

# Define Variables
WIDTH, HEIGHT = 900, 500  # Game window display
FPS = 60  # Game FPS
GAME_BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))
GAME_TITLE_SCREEN = pygame.transform.scale(pygame.image.load(
    os.path.join('assets', 'galaxy.png')), (WIDTH, HEIGHT))
GAME_DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GalaxyCraft')

# Game Setting
SPACESHIP_VEL = 5
BULLET_VEL = 15
MAX_BULLETS = 3
WINNER_FONT = pygame.font.SysFont('arial', 100)
TITLE_FONT = pygame.font.SysFont('arial', 50)
GUILD_FONT = pygame.font.SysFont('arial', 20)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)  # Define the middle border

# Game Sound
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_HIT_SOUND.set_volume(0.3)
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join('assets', 'Gun+Silencer.mp3'))
BULLET_FIRE_SOUND.set_volume(0.3)
pygame.mixer.music.load(os.path.join('assets', 'fight.wav'))

# Game Events
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Spaceship Image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_yellow.png'))
RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_red.png'))

# Spaceship Image Rotation and Rescale
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), angle=270)

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), angle=90)

# Game Message:
GAME_MESSAGE = TITLE_FONT.render('Press SPACE to play', False, 'white')
GAME_NAME = TITLE_FONT.render('GalaxyCraft', False, 'white')
GAME_GUIDE1 = GUILD_FONT.render(
    'Game Move: W A S D, Shoot: Left Ctrl', False, 'white')
GAME_GUIDE2 = GUILD_FONT.render(
    'Game Move: ^ < v >, Shoot: Right Ctrl', True, 'white')


class Game:
    def __init__(self):
        self.yellow_ship = pygame.Rect(
            100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.red_ship = pygame.Rect(
            700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

        self.yellow_bullets = []
        self.red_bullets = []

        self.yellow_health = 10
        self.red_health = 10

        self.winner_text = ''
        self.game_active = False
        self.flash_counter = 0

        # Play BGM
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(loops=-1)

    def draw_window(self, yellow_ship, red_ship, yellow_bullets, red_bullets, yellow_health, red_health):
        '''Draws the game window with the specified background, ships, bullets, and health.'''
        # Draw the game background
        GAME_DISPLAY.blit(GAME_BACKGROUND, (0, 0))

        # Draw the border
        pygame.draw.rect(GAME_DISPLAY, 'black', BORDER)

        # Draw the yellow health bar
        yellow_health_bar = pygame.Rect(
            yellow_ship.x - 10, yellow_ship.y - 20, 10, 100)
        yellow_current_health_bar = pygame.Rect(
            yellow_ship.x - 10, yellow_ship.y - 20, 10, yellow_health * 10)
        pygame.draw.rect(GAME_DISPLAY, (255, 255, 255), yellow_health_bar, 1)
        pygame.draw.rect(GAME_DISPLAY, 'green', yellow_current_health_bar)

        # Draw the red health bar
        red_health_bar = pygame.Rect(red_ship.x + 40, red_ship.y - 20, 10, 100)
        red_current_health_bar = pygame.Rect(
            red_ship.x + 40, red_ship.y - 20, 10, red_health * 10)
        pygame.draw.rect(GAME_DISPLAY, (255, 255, 255), red_health_bar, 1)
        pygame.draw.rect(GAME_DISPLAY, 'green', red_current_health_bar)

        # Draw the yellow spaceship
        GAME_DISPLAY.blit(YELLOW_SPACESHIP, (yellow_ship.x, yellow_ship.y))

        # Draw the red spaceship
        GAME_DISPLAY.blit(RED_SPACESHIP, (red_ship.x, red_ship.y))

        for bullet in yellow_bullets:
            pygame.draw.rect(GAME_DISPLAY, 'yellow', bullet)

        for bullet in red_bullets:
            pygame.draw.rect(GAME_DISPLAY, 'red', bullet)

        pygame.display.update()

    def yellow_handle_movememnt(self, keys_pressed, yellow_ship):
        '''Handle the movement of the yellow spaceship based on the keys pressed.'''

        if keys_pressed[pygame.K_a] and yellow_ship.x - SPACESHIP_VEL > 0:  # Left Key
            yellow_ship.x -= SPACESHIP_VEL
        if keys_pressed[pygame.K_d] and yellow_ship.x + yellow_ship.w // 1.3 + SPACESHIP_VEL < BORDER.x:  # right Key
            yellow_ship.x += SPACESHIP_VEL
        if keys_pressed[pygame.K_w] and yellow_ship.y - SPACESHIP_VEL > 0:  # up Key
            yellow_ship.y -= SPACESHIP_VEL
        if keys_pressed[pygame.K_s] and yellow_ship.y + yellow_ship.h + SPACESHIP_VEL < HEIGHT - 15:  # down Key
            yellow_ship.y += SPACESHIP_VEL

    def red_handle_movememnt(self, keys_pressed, red_ship):
        '''Handle the movement of the red spaceship based on the keys pressed.'''

        if keys_pressed[pygame.K_LEFT] and red_ship.x - SPACESHIP_VEL > BORDER.x + BORDER.w:  # Left Key
            red_ship.x -= SPACESHIP_VEL
        if keys_pressed[pygame.K_RIGHT] and red_ship.x + red_ship.w + SPACESHIP_VEL < WIDTH:  # right Key
            red_ship.x += SPACESHIP_VEL
        if keys_pressed[pygame.K_UP] and red_ship.y - SPACESHIP_VEL > 0:  # up Key
            red_ship.y -= SPACESHIP_VEL
        if keys_pressed[pygame.K_DOWN] and red_ship.y + red_ship.h + SPACESHIP_VEL < HEIGHT - 15:  # down Key
            red_ship.y += SPACESHIP_VEL

    def handle_bullets(self, yellow_bullets, red_bullets, yellow_ship, red_ship):
        '''Updates the positions of the bullets and checks for collisions with the spaceships. 
        If a collision is detected, a hit event is posted to the Pygame event queue. 
        If a bullet goes out of bounds, it is removed from the bullet list.'''

        for bullet in yellow_bullets:
            bullet.x += BULLET_VEL
            if red_ship.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > WIDTH:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x -= BULLET_VEL
            if yellow_ship.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0:
                red_bullets.remove(bullet)

    def draw_winner(self, text):
        '''Draws the winner message on the game display.'''

        draw_text = WINNER_FONT.render(text, True, 'white')
        GAME_DISPLAY.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
                          2, HEIGHT//2 - draw_text.get_height()//2))
        pygame.display.update()

    def draw_title_screen(self):
        '''Draw the title page of the game, including the game message, guide text, game name, and spaceship images.'''
        def blit_centered(surface, x_factor, y_factor):
            x = (WIDTH * x_factor - surface.get_width() // 2)
            y = (HEIGHT * y_factor - surface.get_height() // 2)
            GAME_DISPLAY.blit(surface, (x, y))

        GAME_DISPLAY.blit(GAME_TITLE_SCREEN, (0, 0))

        if self.flash_counter % FPS < 30:
            blit_centered(GAME_MESSAGE, 1/2, 1/1.2)

        blit_centered(GAME_GUIDE1, 1/4, 1/1.5)
        blit_centered(GAME_GUIDE2, 1/1.35, 1/1.5)
        blit_centered(GAME_NAME, 1/2, 1/7)
        blit_centered(YELLOW_SPACESHIP, 1/4, 1/2)
        blit_centered(RED_SPACESHIP, 1/1.35, 1/2)

        pygame.display.update()

    def main_loop(self):
        clock = pygame.time.Clock()  # Set in-game clock
        while True:
            clock.tick(FPS)  # Set game FPS
            self.flash_counter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # User quit
                    pygame.quit()
                    exit()

                if self.game_active:
                    if event.type == pygame.KEYDOWN:  # Shoot bullets
                        if event.key == pygame.K_LCTRL and len(self.yellow_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(
                                self.yellow_ship.x + self.yellow_ship.w // 2, self.yellow_ship.y + self.yellow_ship.h//2 + 4, 10, 5)
                            self.yellow_bullets.append(bullet)
                            BULLET_FIRE_SOUND.play()

                        if event.key == pygame.K_RCTRL and len(self.red_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(
                                self.red_ship.x, self.red_ship.y + self.red_ship.h//2 + 4, 10, 5)
                            self.red_bullets.append(bullet)
                            BULLET_FIRE_SOUND.play()

                    if event.type == YELLOW_HIT:  # Yellow ship is hit event
                        self.yellow_health -= 1
                        BULLET_HIT_SOUND.play()

                    if event.type == RED_HIT:  # Red ship is hit event
                        self.red_health -= 1
                        BULLET_HIT_SOUND.play()
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.game_active = True
                        self.flash_counter = 0
                        self.yellow_health = 10
                        self.red_health = 10
                        self.yellow_bullets.clear()
                        self.red_bullets.clear()
                        self.winner_text = ''

            if self.game_active:
                # Generate Game Result
                if self.red_health <= 0 and self.yellow_health <= 0:
                    self.winner_text = "It's a tie!"
                elif self.red_health <= 0:
                    self.winner_text = 'Yellow Wins!'
                elif self.yellow_health <= 0:
                    self.winner_text = 'Red Wins!'
                if self.winner_text != '':
                    self.draw_winner(self.winner_text)
                    pygame.time.delay(2000)
                    self.game_active = False

                # Battle Ship's Movement
                keys_pressed = pygame.key.get_pressed()
                self.yellow_handle_movememnt(keys_pressed, self.yellow_ship)
                self.red_handle_movememnt(keys_pressed, self.red_ship)

                # Handle Bullets
                self.handle_bullets(self.yellow_bullets, self.red_bullets,
                                    self.yellow_ship, self.red_ship)
                self.draw_window(self.yellow_ship, self.red_ship, self.yellow_bullets,
                                 self.red_bullets, self.yellow_health, self.red_health)

            else:
                # Generate Title Screen
                self.draw_title_screen()

        # Quit The Game
        pygame.quit()
        exit()


# Run Main Loop
game = Game()
game.main_loop()
