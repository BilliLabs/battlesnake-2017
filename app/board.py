import logging

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

HEAD = 'head'
FOOD = 'food'
BODY = 'body'
EMPTY = 'empty'
BOUNDARY = 'boundary'
COLLISION = 'collision'

MY_HEAD = 'myhead'
MY_BODY = 'mybody'



class Board(object):
    def __init__(self, width, height, snakes, food, my_id):
        self.width = width
        self.height = height
        self.snakes = snakes
        self.my_snake = self.get_snake(my_id)
        self.my_head = self.my_snake['coords'][0]
        self.board = self.fill_board(width, height, snakes, food, my_id)
        self.corners = [[0,0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]]
        return

    def fill_board(self, width, height, snakes, food, my_id):
        board = {}
        #todo add a buffer of 1 around other snake's heads to prevent head on collisions
        for snake in snakes:
            head_pos = snake['coords'][0]
            board[(head_pos[0], head_pos[1])] = HEAD if snake['id'] != my_id else MY_HEAD
            for pos in snake['coords'][1:]:
                board[(pos[0], pos[1])] = BODY if snake['id'] != my_id else MY_BODY

        for apple in food:
            board[(apple[0], apple[1])] = FOOD
        return board

    def get_square_state(self, x, y):
        if self.is_boundary(x,y):
            return BOUNDARY
        elif (x, y) not in self.board:
            return EMPTY
        else:
            return self.board[(x, y)]

    def get_snake(self, snake_uuid):
        for snake in self.snakes:
            if snake['id'] == snake_uuid:
                return snake

    def is_boundary(self, x, y):
        if (self.width <= x) or (self.height <= y) or (x < 0) or (y < 0):
            return True
        else:
            return False

    def get_move_coord(self, move, start_pos):
        x = start_pos[0]
        y = start_pos[1]

        if move == "up":
            y -= 1
        elif move == "down":
            y += 1
        elif move == "left":
            x -= 1
        else:  # move == "right":
            x += 1

        logging.debug("Calculated move coordinates for %s as %s, %s", move, x, y)
        return (x, y)

    def adjacent(self, pos_a, pos_b):
        return self.manhattan_dist(pos_a, pos_b) == 1

    def manhattan_dist(self, pos_a, pos_b):
        return (abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1]))

    def closest_square_in_list(self, squares, current_pos):
        closest_square = sorted(squares, key=lambda square:
            data.manhattan_dist(current_pos, square))[0]
        return closest_square

    def get_move_towards(self, pos, safe = DIRECTIONS):
        x, y = self.my_head
        cx, cy = pos
        for direction in safe:
            if direction == data.LEFT and cx < x:
                return direction
            if direction == data.RIGHT and cx > x:
                return direction
            if direction == data.UP and cy < y:
                return direction
            if direction == data.DOWN and cy > y:
                return direction

    def is_move_safe(self, move, n = 0, allowed_tiles = [EMPTY, FOOD]):
        pos = self.get_move_coord(move, self.my_head)
        if self.get_square_state(pos[0], pos[1]) not in allowed_tiles:
            return False

        safe = True
        for i in range(n):
            safe = False
            for direction in DIRECTIONS:
                step_pos = self.get_move_coord(move, pos)
                if self.get_square_state(step_pos[0], step_pos[1]) in allowed_tiles:
                    pos = step_pos
                    safe = True
                    break
        return safe
