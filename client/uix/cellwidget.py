"""
Graphical widget representing a cell of a Tic-Tac-Toe board.
"""

from kivy.uix.button import Button

from client import controller
from client.model import game
from common.model.cell import InvalidMove

class CellWidget(Button):
    """
    Cell widget.

    Responible for toggling the state of the underlying L{Cell} model object and
    initiating the request for the computers next move.
    """
    def __init__(self, cell, **kw):
        """
        Construct a new L{CellWidget}.

        @param cell: the underlying L{Cell} model object.
        @type cell: L{Cell}
        """
        super(CellWidget, self).__init__(**kw)
        self.cell = cell
        self.update()

    def on_press(self):
        """
        Handle a mouse click by setting the cells state to the users symbol.
        """
        try:
            self.cell.set_state('X' if game.user_goes_first else 'O')
        except InvalidMove:
            return

        self.update()
        controller.game.get_move(self.parent.board)

    def update(self):
        """
        Set the widgets text the wrapped L{Cell} models state.
        """
        self.text = self.cell.state
