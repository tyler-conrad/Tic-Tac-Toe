"""
Main game controller.
"""
from urllib import urlencode
from kivy.app import App
from kivy.network.urlrequest import UrlRequest

from common import config
from common.model import board
from client.model import game
from client.uix.popup import GameOverPopup
from client.util.query import find
from client.util.query import kvquery
from client.util.query import root
from client.uix.boardwidget import BoardWidget


def add_new_board(board_model):
    """
    Add a L{BoardWidget} to the L{BoardScreen}.

    @param board_model: the L{Board} representing the current game state.
    """
    board_screen = find('board_screen')
    board_screen.clear_widgets()
    board_screen.add_widget(BoardWidget(
        board_model,
        cls=['board_widget']))

def new_game():
    """
    Start a new game.

    Gathers user parameters from the setup screen and switches to the
    L{BoardScreen}.
    """
    game.user_goes_first = find('play_first_toggle').state == 'down'

    # Get the board size from the int representation of the text of the selected
    # RadioToggleButton
    game.board_side_len = int(filter(
        lambda button: button.state == 'down',
        kvquery(root(), group='board_size'))[0].text)

    find('screen_manager').current = 'board_screen'

def init_board():
    """
    Start the game by presenting the user with a blank L{Board} or passing a
    blank L{Board} to the server.
    """
    board_model = board.blank(int(game.board_side_len))
    if game.user_goes_first:
        add_new_board(board_model)
    else:
        get_move(board_model)

def on_new_board(req, resp):
    """
    Handle the response move from the server.

    @param req: The GET request object.

    @param resp: The GET response text.
    """
    new_board = board.from_string(resp)
    add_new_board(new_board)
    find('board_screen').mouse_enabled = True

    is_leaf, score = new_board.is_leaf_and_score()
    if is_leaf:
        if score == 0: # draw
            game.draws += 1
            GameOverPopup(title='Draw').open()
            return

        # otherwise loss
        game.losses += 1
        GameOverPopup(title='You Lose').open()

def get_move(old_board):
    """
    Get the servers next move.

    @param old_board: the board for which to calculate the best move from.
    @type old_board: L{Board}
    """
    find('board_screen').mouse_enabled = False

    def build_url():
        """
        Build a URI with the string representation of the current board as a
        query parameter.

        The URI host and port are configured in config.py.
        """
        return 'http://' + config.host + ':' + str(config.port) + '/?' + \
            urlencode({'board': board.to_string(old_board)})

    UrlRequest(url=build_url(), on_success=on_new_board)

def quit_game():
    """
    Exit the application.
    """
    App.get_running_app().stop()
