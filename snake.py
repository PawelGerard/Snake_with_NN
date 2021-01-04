import pygame as pg
import random
import math


class Snake:

    def __init__(self, board_size, snake_size):
        self.unit_size = 16
        self.board_size = board_size
        self.screen_size = (board_size + 2) * 16
        self.border_coordinates = self.define_border_coordiantes()
        self.snake_coordinates = self.set_snake_size(snake_size)
        self.score = snake_size * 10
        self.apple_coordinates = self.set_apple_coordinates()
        self.dict_val = {"north": {0: [0, -self.unit_size], -1: [-self.unit_size, 0], 1: [self.unit_size, 0]},
                         "east": {0: [self.unit_size, 0], -1: [0, -self.unit_size], 1: [0, +self.unit_size]},
                         "west": {0: [-self.unit_size, 0], -1: [0, +self.unit_size], 1: [0, -self.unit_size]},
                         "south": {0: [0, +self.unit_size], -1: [self.unit_size, 0], 1: [-self.unit_size, 0]}}
        self.dict_dir = {"north": {0: "north", -1: "west", 1: "east"},
                         "east": {0: "east", -1: "north", 1: "south"},
                         "west": {0: "west", -1: "south", 1: "north"},
                         "south": {0: "south", -1: "east", 1: "west"}}
        self.last_direction = "north"

    def set_snake_size(self, snake_size):
        snake = []
        for i in range(snake_size):
            snake.append((self.screen_size / 2, self.screen_size / 2 + self.unit_size * i))
        return snake

    def define_border_coordiantes(self):
        border_coordinates = []
        for i in range(self.board_size + 2):
            for j in range(self.board_size + 2):
                if (i == 0 or j == 0) or (i == self.board_size + 1 or j == self.board_size + 1):
                    border_coordinates.append((i * self.unit_size, j * self.unit_size))
        return border_coordinates

    def update_snake(self, move, is_apple_eaten):
        self.snake_coordinates.insert(0, (self.snake_coordinates[0][0] + self.dict_val[self.last_direction][move][0],
                                          self.snake_coordinates[0][1] + self.dict_val[self.last_direction][move][1]))
        if not is_apple_eaten:
            self.snake_coordinates.pop(-1)
        return self.dict_dir[self.last_direction][move]

    def is_snake_dead(self):
        snake_body = self.snake_coordinates[1:]
        head = self.snake_coordinates[0]
        if (head in self.border_coordinates) or (head in snake_body):
            return True
        return False

    def check_status(self):
        result = []
        head_x = self.snake_coordinates[0][0]
        head_y = self.snake_coordinates[0][1]
        apple_x = self.apple_coordinates[0]
        apple_y = self.apple_coordinates[1]
        snake_body = self.snake_coordinates[1:-1]
        for i in range(-1, 2):
            if ((head_x + self.dict_val[self.last_direction][i][0],
                 head_y + self.dict_val[self.last_direction][i][1]) in self.border_coordinates) or (
                    (head_x + self.dict_val[self.last_direction][i][0],
                     head_y + self.dict_val[self.last_direction][i][1]) in snake_body):
                result.append(True)
            else:
                result.append(False)
        direction_north = True if self.last_direction == "north" else False
        direction_east = True if self.last_direction == "east" else False
        direction_south = True if self.last_direction == "south" else False
        direction_west = True if self.last_direction == "west" else False
        apple_north = True if apple_y < head_y else False
        apple_east = True if apple_x > head_x else False
        apple_south = True if apple_y > head_y else False
        apple_west = True if apple_x < head_x else False
        return [result[0], result[1], result[2], direction_north, direction_east, direction_south, direction_west,
                apple_north, apple_east, apple_south, apple_west]

    def set_apple_coordinates(self):
        search_for_coordinates = True
        while search_for_coordinates:
            apple_x = random.randint(1, self.board_size) * self.unit_size
            apple_y = random.randint(1, self.board_size) * self.unit_size
            if (apple_x, apple_y) not in self.snake_coordinates:
                search_for_coordinates = False
        return (apple_x, apple_y)

    def is_apple_eaten(self):
        head = self.snake_coordinates[0]
        if head == self.apple_coordinates:
            return True
        else:
            return False

    def get_distance_to_apple(self):
        head_x = self.snake_coordinates[0][0]
        head_y = self.snake_coordinates[0][1]
        apple_x = self.apple_coordinates[0]
        apple_y = self.apple_coordinates[1]
        distance = math.sqrt(math.pow(apple_x - head_x, 2) + math.pow(apple_y - head_y, 2))
        max_distance = math.sqrt(math.pow(self.board_size * 16, 2) + math.pow(self.board_size * 16, 2))
        return distance / max_distance

    def draw_board(self, screen):
        screen.fill((255, 255, 255))
        for x, y in self.border_coordinates:
            pg.draw.rect(screen, (0, 100, 0), [x, y, self.unit_size, self.unit_size])

    def draw_snake(self, screen):
        screen.blit(pg.image.load("head.png"), (self.snake_coordinates[0][0], self.snake_coordinates[0][1]))
        for coordinate in self.snake_coordinates[1:]:
            screen.blit(pg.image.load("body.png"), (coordinate[0], coordinate[1]))

    def draw_apple(self, screen):
        screen.blit(pg.image.load("apple.png"), self.apple_coordinates)

    def game_step(self, visualization, move):
        if visualization:
            pg.init()
            screen = pg.display.set_mode((self.screen_size, self.screen_size))
            fps_clock = pg.time.Clock()
            self.draw_board(screen)
            self.draw_apple(screen)
            self.draw_snake(screen)
            pg.display.update()
            fps_clock.tick(2)
        if self.is_apple_eaten():
            self.last_direction = self.update_snake(move, True)
            self.apple_coordinates = self.set_apple_coordinates()
            self.score += 10
        else:
            self.last_direction = self.update_snake(move, False)