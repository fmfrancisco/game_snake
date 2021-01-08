import pygame
import random
import sys
from pygame.locals import *
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.body = [Vector2(3, 0), Vector2(2, 0), Vector2(1, 0)]
        self.direction = Vector2(1, 0)
        self.rect = None

    def draw(self, screen):
        for blk in self.body:
            self.rect = (blk.x * CELL_SIZE, blk.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, self.rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy[:]

    def check_collision(self, obj):
        if self.body[0] == obj.pos:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            obj.reset_pos()

    def check_fail(self):
        if not 0 <= self.body[0].x < CELL_NUMBER or not 0 <= self.body[0].y < CELL_NUMBER:
            self.game_over()
        for blk in self.body[1:]:
            if blk == self.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()


class Fruit:
    def __init__(self):
        self.reset_pos()

    def draw(self, screen):
        fruit = pygame.Rect(self.pos.x * CELL_NUMBER,self.pos.y * CELL_NUMBER, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, fruit)

    def reset_pos(self):
        pos_x = random.randint(0, CELL_NUMBER - 1)
        pos_y = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(pos_x, pos_y)


def terminate():
    pygame.quit()
    sys.exit()


CELL_SIZE = 20
CELL_NUMBER = 20
SCREEN_WIDTH = CELL_SIZE * CELL_NUMBER
SCREEN_HEIGHT = CELL_SIZE * CELL_NUMBER

RED = pygame.Color('red')
BLUE = pygame.Color('blue')
WHITE = pygame.Color('white')
FPS = 60


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake')

    SCREEN_UPDATE = USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    snake = Snake()
    fruit = Fruit()

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == SCREEN_UPDATE:
                snake.move_snake()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                elif event.key == K_UP:
                    snake.direction = Vector2(0, -1)
                elif event.key == K_DOWN:
                    snake.direction = Vector2(0, 1)
                elif event.key == K_RIGHT:
                    snake.direction = Vector2(1, 0)
                elif event.key == K_LEFT:
                    snake.direction = Vector2(-1, 0)

        screen.fill(WHITE)

        snake.check_collision(fruit)
        snake.check_fail()

        snake.draw(screen)
        fruit.draw(screen)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()