"""
A representation of a cell of a Tic-Tac-Toe board.
"""

from common.log import Loggable

class InvalidMove(Exception):
    """
    Raised when the player attempts to make an invalid move.
    """
    pass

# This implementation uses a style of object composition inspired by the
# 'Cake Pattern': http://jonasboner.com/2008/10/06/real-world-scala-dependency-injection-di/
# It is similar to Mixins but the emphasis is on extending existing
# functionality.  It is especially useful for separating cross-cutting
# concerns like logging and error-checking from the essential functionality
# of an object.  Additionally it allows you to compose your objects
# as you desire from components that implement different 'aspects'.
class CellBase(object):
    """
    Minimal implementation of a cell.

    @ivar index: the index of the cell.  Cells are indexed from left-to-right
        top-to-bottom.
    @type index: C{int}

    @ivar state: a string representing the state of this cell.  One of 'X',
    'O', or ' '.
    @type state: C{str}
    """

    def __init__(self, index, state):
        """
        Construct a L{Cell} with the given index and state.

        @param index: the index for the new L{Cell}
        @type index: C{int}

        @param state: the state for the new L{Cell}
        @type state: C{str}
        """
        self.index = index
        self.state = state

    def set_state(self, state):
        """
        Set the state of this L{Cell}.

        @param state: the new state for this L{Cell}
        """
        self.state = state

class CellError(Loggable):
    """
    Extends the functionality of L{CellBase} with error checking.
    """

    def set_state(self, state):
        if not self.state == ' ':
            self.warn(
                'Cannot set state of non-blank cell {index}',
                index=self.index)
            raise InvalidMove
        super(CellError, self).set_state(state)

class CellLogger(Loggable):
    """
    Extends the functionality of L{CellBase} with logging.
    """

    def set_state(self, state):
        self.info(
            'Setting cell {index} to state {state}',
            index=self.index,
            state=state)
        super(CellLogger, self).set_state(state)

class Cell(CellLogger, CellError, CellBase):
    """
    Implementation of cell with error-checking and logging.
    """
    pass
