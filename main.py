import pygame
from pygame.locals import *
import time
import random

size = 40


class Apple:
    def __init__(self, main_screen):
        self.apple = pygame.image.load("Resources/apple.jpg").convert()
        self.main_screen = main_screen
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.main_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 22) * size
        self.y = random.randint(0, 17) * size


class Snake:
    def __init__(self, main_screen, length):
        self.length = length
        self.main_screen = main_screen
        self.block = pygame.image.load("Resources/block.jpg").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = "down"

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        for i in range(self.length):
            self.main_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "right":
            self.x[0] += size
        if self.direction == "left":
            self.x[0] -= size
        if self.direction == "up":
            self.y[0] -= size
        if self.direction == "down":
            self.y[0] += size

        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("SLANG!")
        pygame.mixer.init()
        self.play_bg_music()
        # BG
        self.surface = pygame.display.set_mode((920, 720))
        self.surface.fill((23, 43, 7))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True

        return False

    def play_bg_music(self):
        pygame.mixer.music.load("Resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1,0)

    def play_sound(self, sound):
        if sound == "crash":
            sound = pygame.mixer.Sound("Resources/1_snake_game_resources_crash.mp3")
        elif sound == 'ding':
            sound = pygame.mixer.Sound("Resources/1_snake_game_resources_ding.mp3")
        pygame.mixer.Sound.play(sound)

    def render_bg(self):
        bg = pygame.image.load("Resources/bg2.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_bg()
        self.snake.walk()
        self.apple.draw()
        self.define_score()
        pygame.display.flip()
        # snake eating apple
        for i in range(self.snake.length):
            if self.is_collision(self.snake.x[i], self.snake.y[i], self.apple.x, self.apple.y):
                self.play_sound("ding")
                self.snake.increase_length()
                self.apple.move()
        # snake hitting itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "GAME OVER"
        # snake hitting the boundaries.
        if not (0 <= self.snake.x[0] <= 920 and 0 <= self.snake.y[0] <= 720):
            self.play_sound('crash')
            raise "Hit the boundary error"

    def define_score(self):
        font = pygame.font.SysFont("Times new roman", 40)
        score = font.render(f"Score:{self.snake.length}", True, (135, 145, 38))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_bg()
        font = pygame.font.SysFont("Times new roman", 40)
        line1 = font.render("Game over!!", True, (135, 145, 38))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"Your score is: {self.snake.length}", True, (135, 145, 38))
        self.surface.blit(line2, (200, 350))
        line3 = font.render("Press Enter To Try Again", True, (135, 145, 38))
        self.surface.blit(line3, (200, 400))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()


                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.1)


if __name__ == "__main__":
    game = Game()
    game.run()
