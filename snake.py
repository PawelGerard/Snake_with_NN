import pygame as pg
import random
import math


class Snake:

    def __init__(self, board_size, snake_size):
        self._unit_size = 16
        self._board_size = board_size
        self._screen_size = (board_size + 2) * 16
        self._border_coordinates = self._define_border_coordiantes()
        self._snake_coordinates = self._set_snake_size(snake_size)
        self.score = snake_size * 10
        self._apple_coordinates = self._set_apple_coordinates()
        # dict describes snake's head coordinates due to direction change
        self._dict_val = {"north": {0: [0, -self._unit_size], -1: [-self._unit_size, 0], 1: [self._unit_size, 0]},
                         "east": {0: [self._unit_size, 0], -1: [0, -self._unit_size], 1: [0, +self._unit_size]},
                         "west": {0: [-self._unit_size, 0], -1: [0, +self._unit_size], 1: [0, -self._unit_size]},
                         "south": {0: [0, +self._unit_size], -1: [self._unit_size, 0], 1: [-self._unit_size, 0]}}
        # next direction after particular move
        # only 3 options: 0 same dir, 1 left, -1 right
        self._dict_dir = {"north": {0: "north", -1: "west", 1: "east"},
                         "east": {0: "east", -1: "north", 1: "south"},
                         "west": {0: "west", -1: "south", 1: "north"},
                         "south": {0: "south", -1: "east", 1: "west"}}
        self._last_direction = "north"

    def _set_snake_size(self, snake_size):
        snake = []
        for i in range(snake_size):
            snake.append((self._screen_size / 2, self._screen_size / 2 + self._unit_size * i))
        return snake

    def _define_border_coordiantes(self):
        border_coordinates = []
        for i in range(self._board_size + 2):
            for j in range(self._board_size + 2):
                # only first or last values for border
                if (i == 0 or j == 0) or (i == self._board_size + 1 or j == self._board_size + 1):
                    border_coordinates.append((i * self._unit_size, j * self._unit_size))
        return border_coordinates

    def _update_snake(self, move, is_apple_eaten):
        # dict tells what is next coordinate after particular move
        self._snake_coordinates.insert(0, (self._snake_coordinates[0][0] + self._dict_val[self._last_direction][move][0],
                                           self._snake_coordinates[0][1] + self._dict_val[self._last_direction][move][1]))
        # move = additional part of snake body
        # if apple is not eaten last part of snake body should be deleted
        if not is_apple_eaten:
            self._snake_coordinates.pop(-1)
        return self._dict_dir[self._last_direction][move]

    def is_snake_dead(self):
        snake_body = self._snake_coordinates[1:]
        head = self._snake_coordinates[0]
        if (head in self._border_coordinates) or (head in snake_body):
            return True
        return False

    # for NN 11 bool variables
    # first 3 describes is obstacles on right, forward or left
    # next 4: what snake direction is: north, east, south or west
    # last 4: is apple on north, east, south or west
    def check_status(self):
        obstacle = []
        head_x = self._snake_coordinates[0][0]
        head_y = self._snake_coordinates[0][1]
        apple_x = self._apple_coordinates[0]
        apple_y = self._apple_coordinates[1]
        snake_body = self._snake_coordinates[1:-1]
        # -1 right, 0 forward, 1 left
        for i in range(-1, 2):
            if ((head_x + self._dict_val[self._last_direction][i][0],
                 head_y + self._dict_val[self._last_direction][i][1]) in self._border_coordinates) or (
                    (head_x + self._dict_val[self._last_direction][i][0],
                     head_y + self._dict_val[self._last_direction][i][1]) in snake_body):
                obstacle.append(True)
            else:
                obstacle.append(False)
        direction_north = True if self._last_direction == "north" else False
        direction_east = True if self._last_direction == "east" else False
        direction_south = True if self._last_direction == "south" else False
        direction_west = True if self._last_direction == "west" else False
        apple_north = True if apple_y < head_y else False
        apple_east = True if apple_x > head_x else False
        apple_south = True if apple_y > head_y else False
        apple_west = True if apple_x < head_x else False
        return [obstacle[0], obstacle[1], obstacle[2], direction_north, direction_east, direction_south, direction_west,
                apple_north, apple_east, apple_south, apple_west]

    # random coodrinates for apple
    def _set_apple_coordinates(self):
        search_for_coordinates = True
        while search_for_coordinates:
            apple_x = random.randint(1, self._board_size) * self._unit_size
            apple_y = random.randint(1, self._board_size) * self._unit_size
            if (apple_x, apple_y) not in self._snake_coordinates:
                search_for_coordinates = False
        return (apple_x, apple_y)

    def _is_apple_eaten(self):
        head = self._snake_coordinates[0]
        if head == self._apple_coordinates:
            return True
        else:
            return False

    # distance cannot exceed 1 (feature for NN)
    def get_distance_to_apple(self):
        head_x = self._snake_coordinates[0][0]
        head_y = self._snake_coordinates[0][1]
        apple_x = self._apple_coordinates[0]
        apple_y = self._apple_coordinates[1]
        distance = math.sqrt(math.pow(apple_x - head_x, 2) + math.pow(apple_y - head_y, 2))
        max_distance = math.sqrt(math.pow(self._board_size * 16, 2) + math.pow(self._board_size * 16, 2))
        return distance / max_distance

    def _draw_board(self, screen):
        screen.fill((255, 255, 255))
        for x, y in self._border_coordinates:
            pg.draw.rect(screen, (0, 100, 0), [x, y, self._unit_size, self._unit_size])

    def _draw_snake(self, screen):
        screen.blit(pg.image.load("head.png"), (self._snake_coordinates[0][0], self._snake_coordinates[0][1]))
        for coordinate in self._snake_coordinates[1:]:
            screen.blit(pg.image.load("body.png"), (coordinate[0], coordinate[1]))

    def _draw_apple(self, screen):
        screen.blit(pg.image.load("apple.png"), self._apple_coordinates)

    # optional visualisation is feature for NN
    # it allows algorithm to learn faster
    def game_step(self, visualisation, move):
        if visualisation:
            pg.init()
            screen = pg.display.set_mode((self._screen_size, self._screen_size))
            fps_clock = pg.time.Clock()
            self._draw_board(screen)
            self._draw_apple(screen)
            self._draw_snake(screen)
            pg.display.update()
            fps_clock.tick(2)
        if self._is_apple_eaten():
            self._last_direction = self._update_snake(move, True)
            self._apple_coordinates = self._set_apple_coordinates()
            self.score += 10
        else:
            self._last_direction = self._update_snake(move, False)