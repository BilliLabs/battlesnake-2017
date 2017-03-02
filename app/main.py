import bottle
import os
import random
from random import shuffle
import logging
logging.basicConfig(level=logging.DEBUG)


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    logging.info("Request %s", data)
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    food = data['food']
    snakes = data['snakes']
    turn = data['turn']
    my_id = data['you']

    # TODO: Do things with data
    directions = ['right', 'down', 'left', 'up']

    if turn%5:
        shuffle(directions)

    my_snake = get_snake(my_id, snakes)
    my_head_pos = my_snake['coords'][0]

    for dir in directions:
        move = dir
        move_coord = get_move_coord(move, my_head_pos)
        if not is_boundary(move_coord, board_width, board_height) and not is_any_tail(move_coord, snakes):
            break

    return {
        'move': move,
        'taunt': 'why you you!'
    }


def get_snake(snake_uuid, snakes):
    for snake in snakes:
        if snake['id'] == snake_uuid:
            return snake


def is_boundary(coord, board_width, board_height):
    if (board_width <= coord[0]) or (board_height <= coord[1]) or (coord[0] < 0) or (coord[1] < 0):
        return True
    else:
        return False

def is_tail(coord, snake):
    for pos in snake['coords']:
        if pos[0] == coord[0] and pos[1] == coord[1]:
            return True

    return False

def is_any_tail(coord, snakes):
    for snake in snakes:
        if is_tail(coord, snake):
            return True



def get_move_coord(move, current_pos):
    x = current_pos[0]
    y = current_pos[1]

    if move == "up":
        y -= 1
    elif move == "down":
        y += 1
    elif move == "left":
        x -= 1
    else: # move == "right":
        x += 1

    logging.info("Calculated move coordinates for %s as %s, %s", move, x, y)
    return (x, y)

#todo check health -- go for food when health is less than distance to food

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))
