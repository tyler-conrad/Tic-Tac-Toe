"""
Graphical widget representing the board in Tic-Tac-Toe.
"""
from kivy.uix.gridlayout import GridLayout

from client.uix.cellwidget import CellWidget

class BoardWidget(GridLayout):
    """
    Board widget.

    Responsible for constructing a graphical board given a L{Board} model.
    """
    def __init__(self, board, **kw):
        """
        Add a L{CellWidget} for each L{Cell} in the given L{Board}s state.

        @ivar board: the L{Board} model to represent.
        @type board: L{Board}
        """
        super(BoardWidget, self).__init__(**kw)
        self.board = board

        size = board.side_len()
        self.rows = size
        self.cols = size
        for cell in board.state:
            self.add_widget(CellWidget(cell))
