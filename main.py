import pygame
import sys
import random
from pygame.locals import *
from pygame.math import Vector2

# pip install pygame
# pip install pygame upgrade

class Snake:
    def __init__(self):
        self.body = [Vector2(3, 0), Vector2(2, 0), Vector2(1, 0)]
        self.direction = RIGHT
        self.rect = None
        self.movement = None
        self.food = Fruit()

    def check_collision(self, objeto):
        if self.body[0] == objeto.pos:
            if self.direction == RIGHT:
                self.body.insert(0, self.body[0] + Vector2(1, 0))
            elif self.direction == LEFT:
                self.body.insert(0, self.body[0] + Vector2(-1, 0))
            elif self.direction == UP:
                self.body.insert(0, self.body[0] + Vector2(0, -1))
            elif self.direction == DOWN:
                self.body.insert(0, self.body[0] + Vector2(0, 1))
            objeto.new_pos()
            print(self.body)

    def check_direction(self):
        if self.direction == RIGHT:
            self.movement = Vector2(1, 0)
        elif self.direction == LEFT:
            self.movement = Vector2(-1, 0)
        elif self.direction == UP:
            self.movement = Vector2(0, -1)
        elif self.direction == DOWN:
            self.movement = Vector2(0, +1)

    def move(self):
        self.check_direction()
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.movement)
        self.body = body_copy[:]

    def draw(self, screen):
        for bd in self.body:
            posx = int(bd.x * CELL_SIZE)
            posy = int(bd.y * CELL_SIZE)
            self.rect = (posx, posy, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, self.rect)


class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE)).convert()
        self.image.fill(RED)
        x_random = random.randint(0, CELL_NUMBER - 1)
        y_random = random.randint(0, CELL_NUMBER - 1)
        self.pos = self.pos = Vector2(x_random, y_random)


    def new_pos(self):
        x_random = random.randint(0, CELL_NUMBER - 1)
        y_random = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(x_random, y_random)

    def draw(self, screen):
        screen.blit(self.image, (self.pos.x * CELL_NUMBER, self.pos.y * CELL_NUMBER))


def terminate():
    pygame.quit()
    sys.exit()


CELL_SIZE = 20
CELL_NUMBER = 20
WIDTH = int(CELL_SIZE * CELL_NUMBER)
HEIGHT = int(CELL_SIZE * CELL_NUMBER)

WHITE = pygame.Color('white')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')
FPS = 30

RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'


def main():
    pygame.init()

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')
    BG_SCREEN = pygame.Surface(SCREEN.get_size()).convert()
    BG_SCREEN.fill(WHITE)
    SCREEN.blit(BG_SCREEN, (0, 0))

    snake = Snake()
    fruit = Fruit()

    USER_EVENT = pygame.USEREVENT
    pygame.time.set_timer(USER_EVENT, 200)
    CLOCK = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == USER_EVENT:
                snake.move()
            elif event.type == KEYDOWN:
                if event.key == K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT

        SCREEN.blit(BG_SCREEN, (0, 0))

        snake.check_collision(fruit)

        snake.draw(SCREEN)
        fruit.draw(SCREEN)

        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()