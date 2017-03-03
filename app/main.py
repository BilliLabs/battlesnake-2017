import bottle
import os
import random
from random import shuffle
import logging
import board
logging.basicConfig(level=logging.DEBUG)


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')


@bottle.post('/<name>/start')
def start(name = 'random'):
    data = bottle.request.json
    logging.info("Request %s", data)
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
        'name': name.capitalize() + ' Snake'
    }


@bottle.post('/<name>/move')
def move(name = 'random'):
    data = bottle.request.json
    logging.info("Request %s", data)
    game_id = data['game_id']
    width = data['width']
    height = data['height']
    food = data['food']
    snakes = data['snakes']
    turn = data['turn']
    my_id = data['you']

    game_board = board.Board(width, height, snakes, food, my_id)

    logging.info("Current location %s", game_board.my_head)
    move = basic_strategy(game_board, turn)
    logging.info("Current location %s", game_board.my_head)

    return {
        'move': move,
        'taunt': 'why you you!'
    }





def is_tail(coord, snake):
    for pos in snake['coords']:
        if pos[0] == coord[0] and pos[1] == coord[1]:
            return True

    return False

def is_any_tail(coord, snakes):
    for snake in snakes:
        if is_tail(coord, snake):
            return True


def basic_strategy(game_board, turn):
    directions = board.DIRECTIONS
    if turn%5:
        shuffle(directions)

    for dir in directions:
        move = dir
        if game_board.is_move_safe(move):
            return move

    # no safe move found
    logging.info("No safe move found %s", move)
    return move

#todo check health -- go for food when health is less than distance to food

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))


#todo more sneks
#corner sneck
#wall sneck
#box sneck
#hungry sneck
#nascar sneck
#kamikazi snaek
#shanke'n snake
#cutoff snake
#avoidance snake