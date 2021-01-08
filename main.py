# Importando módulos
import pygame
import sys
import random
from pygame.locals import *
from pygame.math import Vector2

# pip install pygame
# pip install pygame upgrade

# Classe snake
class Snake:
    def __init__(self):
        self.body = [Vector2(3, 0), Vector2(2, 0), Vector2(1, 0)]
        self.direction = RIGHT
        self.rect = None
        self.movement = None
        self.food = Fruit()
        self.score = 0
        self.score_text = score_font.render(f'Score: {str(self.score):>2}', True, BLACK)

    # Método para verificar se houve colisão com o objeto
    def check_collision(self, objeto):
        # Se houver colisão será adicionado +1 Vector ao corpo da "snake" de acordo com direção
        if self.body[0] == objeto.pos:
            self.score += 1
            self.score_text = score_font.render(f'Score: {str(self.score):>2}', True, BLACK)
            if self.direction == RIGHT:
                self.body.insert(0, self.body[0] + Vector2(1, 0))
            elif self.direction == LEFT:
                self.body.insert(0, self.body[0] + Vector2(-1, 0))
            elif self.direction == UP:
                self.body.insert(0, self.body[0] + Vector2(0, -1))
            elif self.direction == DOWN:
                self.body.insert(0, self.body[0] + Vector2(0, 1))
            # Gera nova posição para o objeto Fruit()
            objeto.new_pos()
        # Se a "cabeça" da snake colidir com seu corpo a função game_over() é chamada
        for bd in self.body[1:]:
            if self.body[0] == bd or self.body[0].x == -1 or self.body[0].y == -1 or self.body[0].x == CELL_NUMBER or self.body[0].y == CELL_NUMBER:
                game_over()

    # Adiciona novo Vector ao corpo da snake de acordo com a direção
    def check_direction(self):
        if self.direction == RIGHT:
            self.movement = Vector2(1, 0)
        elif self.direction == LEFT:
            self.movement = Vector2(-1, 0)
        elif self.direction == UP:
            self.movement = Vector2(0, -1)
        elif self.direction == DOWN:
            self.movement = Vector2(0, +1)

    # Move a snake
    def move(self):
        self.check_direction()
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.movement)
        self.body = body_copy[:]

    # Desenha o objeto na tela de acordo com as posições de cada Vector em seu corpo
    def draw(self, screen):
        for bd in self.body:
            posx = int(bd.x * CELL_SIZE)
            posy = int(bd.y * CELL_SIZE)
            self.rect = (posx, posy, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLUE, self.rect)
        screen.blit(self.score_text, (5, 5))


# CLasse Fruit - Será o alimento da snake
class Fruit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE)).convert()
        self.image.fill(RED)
        x_random = random.randint(0, CELL_NUMBER - 1)
        y_random = random.randint(0, CELL_NUMBER - 1)
        self.pos = self.pos = Vector2(x_random, y_random)

    # Método para definir nova posição
    def new_pos(self):
        x_random = random.randint(0, CELL_NUMBER - 1)
        y_random = random.randint(0, CELL_NUMBER - 1)
        self.pos = Vector2(x_random, y_random)

    # Desenha o objeto na tela
    def draw(self, screen):
        screen.blit(self.image, (self.pos.x * CELL_NUMBER, self.pos.y * CELL_NUMBER))


class EventUser:
    def __init__(self):
        self.event = pygame.USEREVENT
        pygame.time.set_timer(self.event, 200)

    def new_event(self, speed):
        if speed == 1:
            self.event = pygame.USEREVENT
            pygame.time.set_timer(self.event, 150)
        elif speed == 2:
            self.event = pygame.USEREVENT
            pygame.time.set_timer(self.event, 100)
        elif speed == 3:
            self.event = pygame.USEREVENT
            pygame.time.set_timer(self.event, 80)
        elif speed == 4:
            self.event = pygame.USEREVENT
            pygame.time.set_timer(self.event, 60)
        elif speed == 5:
            self.event = pygame.USEREVENT
            pygame.time.set_timer(self.event, 40)


# Método para fechar o jogo
def terminate():
    pygame.quit()
    sys.exit()


def game_over():
    SCREEN.blit(text, rect_text)
    pygame.display.update()
    pygame.time.wait(1000)
    terminate()


# Define o tamanho do bloco  da snake
CELL_SIZE = 20
# Define a quantidade de blocos da tela
CELL_NUMBER = 20
# Largura e Altura da tela
WIDTH = int(CELL_SIZE * CELL_NUMBER)
HEIGHT = int(CELL_SIZE * CELL_NUMBER)

# Cores
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
BLUE = pygame.Color('blue')
RED = pygame.Color('red')
# Controla a velocidade de atualizaçaõ da tela
FPS = 30
# Iniciando variáveis constantes para defenir a direção do objeto
RIGHT = 'right'
LEFT = 'left'
UP = 'up'
DOWN = 'down'

pygame.font.init()
FONT = pygame.font.SysFont('dejavuserif', 60)
score_font = pygame.font.SysFont('dejavuserif', 15)
text = FONT.render('Game Over', True, RED)
rect_text = text.get_rect()
rect_text.centerx = int(WIDTH / 2)
rect_text.centery = int(HEIGHT / 2)

max_speed = pygame.font.SysFont('dejavuserif', 20)


# Função principal
def main():
    global SCREEN
    # Iniciando o pygame e criando a tela
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')
    BG_SCREEN = pygame.Surface(SCREEN.get_size()).convert()
    BG_SCREEN.fill(WHITE)
    SCREEN.blit(BG_SCREEN, (0, 0))

    # Instanciando os objetos snake e fruit
    snake = Snake()
    fruit = Fruit()
    speed = 0
    event_user = EventUser()
    # Gerando evento para controlar a velocidade de movimento do objeto snake

    game_time = 0
    game_time_seconds = 0
    game_time_minutes = 0

    # Instanciando objeto para controlar o FPS
    CLOCK = pygame.time.Clock()

    # Laço principal do jogo
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            # Chamando o método move() para mover o objeto
            elif event.type == event_user.event:
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
                elif event.key == K_x and speed == 5:
                    speed = 2
                    event_user.new_event(speed)
                    snake.score = 0

        # Desenhando a tela
        SCREEN.blit(BG_SCREEN, (0, 0))

        game_time += 1
        if game_time == 30:
            game_time_seconds += 1
            game_time = 0
            if game_time_seconds == 60:
                game_time_minutes += 1
                game_time_seconds = 0

        if snake.score == 2 and speed == 0:
            speed += 1
            event_user.new_event(speed)
        elif snake.score == 4 and speed == 1:
            speed += 1
            event_user.new_event(speed)
        elif snake.score == 6 and speed == 2:
            speed += 1
            event_user.new_event(speed)
        elif snake.score == 8 and speed == 3:
            speed += 1
            event_user.new_event(speed)
            tex_max_speed = max_speed.render('Velocidade máxima', True, BLACK)
            tex_max_speed_rect = tex_max_speed.get_rect()
        elif snake.score == 10 and speed == 4:
            speed += 1
            event_user.new_event(speed)
            tex_max_speed = max_speed.render('Eu menti', True, BLACK)
            tex_max_speed_rect = tex_max_speed.get_rect()

        if speed == 4:
            SCREEN.blit(tex_max_speed, (WIDTH - tex_max_speed_rect.width - 5, 10))
        elif speed == 5:
            SCREEN.blit(tex_max_speed, (WIDTH - tex_max_speed_rect.width - 5, 10))

        render_game_time = score_font.render(f'Time: {str(game_time_minutes):>2}:{str(game_time_seconds):>2}', True, BLACK)

        # Verificando se houve colição dos objetos
        snake.check_collision(fruit)
        # Desenhnado os objetos na tela
        snake.draw(SCREEN)
        fruit.draw(SCREEN)
        SCREEN.blit(render_game_time, (5, 20))
        # Atualizando tudo
        pygame.display.update()
        CLOCK.tick(FPS)


if __name__ == '__main__':
    main()