"""
A representation of a Tic-Tac-Toe board of variable size.
"""

from math import sqrt

from common.model.cell import Cell

# Factory functions
def blank(side_len):
    """
    Create a blank L{Board} where the state of every cell is ' '.

    @param side_len: the side length of the board.
    @type side_len: C{int}

    @return: A blank L{Board}
    @rtype: L{Board}
    """
    return Board([Cell(i, ' ') for i in range(side_len ** 2)])

def from_string(string):
    """
    Construct a L{Board} from its string representation.

    @param string: a string representing the L{Board} state.  Composed of 'X', 'O'
        and ' ' characters only.  The length of the string should be a perfect
        square.
    @type string: C{str}

    @return: A L{Board} representation of the input string.
    @rtype: L{Board}
    """
    return Board([Cell(i, state) for i, state in enumerate(string)])

def to_string(board):
    """
    Construct the string representation of a L{Board}.

    @param board: the L{Board} model.
    @type board: L{Board}

    @return: A string representation of the given L{Board}
    @rtype: L{Board}
    """
    return ''.join([cell.state for cell in board.state])

class Board(object):
    """
    Board model class.

    Provides a representation for the current or computed states of the game.
    A L{Board}'s state attribute is a list of L{Cell}s.  A L{Board} provides
    methods that compute various properties of the game state.

    @ivar state: A list of L{Cell}s representing the current state of the board.
    @type state: C{list} of L{Cell}
    """

    def __init__(self, state):
        """
        Construct a L{Board} with the given state.

        @param state: a C{List} of L{Cell}s.
        @type state: C{List} of L{Cell}
        """
        self.state = state

    def size(self):
        """
        Return the total number of L{Cell}s that compose this L{Board}s state.

        @return: Cell count
        @rtype: C{int}
        """
        return len(self.state)

    def side_len(self):
        """
        Return the side length of the L{Board}.

        @return: side length
        @rtype: C{int}
        """
        # Implemeted as a method instead of an instance variable to maintain a
        # single canonical source (Board.state) for the state of the board.
        return int(sqrt(self.size()))

    def x_has_next_turn(self):
        """
        Whether it is 'X's turn to move.

        @return: Whether is is 'X's turn.
        @rtype: C{bool}
        """
        as_string = to_string(self)
        return as_string.count('X') <= as_string.count('O')

    def symbols_in_turn_order(self):
        """
        Return a tuple containing 'X' and 'O' ordered by who takes the next
        turn.

        @return: A tuple of 'X' and 'O' in turn order.
        @rtype: C{tuple} of C{str}
        """
        return ('X', 'O') if self.x_has_next_turn() else ('O', 'X')

    def children(self):
        """
        Calculate the child L{Board}s of this L{Board}.

        Given a L{Board} and the symbol representing the player that takes
        the next turn calculate the L{Board}s for all possible next moves.
        This is equivalent to yielding a L{Board} for each replacement of  ' '
        with the symbol ('X' or 'O') representing the player whose turn it is.
        This is used by the minimax algorithm to build the game state tree.

        @return: A list of L{Board}s representing possible next moves.
        @rtype: C{list} of L{Board}
        """
        as_string = to_string(self)
        symbol = self.symbols_in_turn_order()[0]

        def replace_cell(i):
            char_list = list(as_string)
            char_list[i] = symbol
            return ''.join(char_list)

        return [from_string(replace_cell(i))
            for i, char in enumerate(as_string)
            if char == ' ']

    def is_win(self):
        """
        Whether this L{Board} represents a win for any player.

        @return: Whether this board is a winning board.
        @rtype: C{bool}
        """
        return any(check_line(line) for line in self.all_lines())

    def is_draw(self):
        """
        Whether this L{Board} represents a tie game.

        This method needs to be qualified by is_win() to determine whether this
        board truly represents a draw game.
        'a true draw' == (not is_win()) and is_draw()

        @return: Whether this board is a tie board.
        @rtype: C{bool}
        """
        return all([cell.state != ' ' for cell in self.state])

    def is_leaf_and_score(self):
        """
        Whether this game represents a 'Game Over' (win or draw) along with
        the corresponding score.

        Winning boards get a score of 1.0.  Tie boards get as score of 0.0.
        Non-'Game Over' boards get a score of C{None}.

        This function is only ever called from the context of the active player
        so it does not need to calculate a loss e.g. a win for the active
        player is a loss for the unactive player.

        @return: Whether this board is a game state leaf, and its score.
        @rtype: C{tuple} of a C{bool} with C{float} or a C{bool} with C{None}
        """
        if self.is_win():
            return True, 1.0
        elif self.is_draw():
            return True, 0.0
        return False, None

    def row_lines(self):
        """
        Calculate the rows of this L{Board}.

        @return: A C{list} of the string representations of this L{Board}s rows.
        @rtype: C{list} of C{str}
        """
        as_string = to_string(self)
        side_len = self.side_len()
        return [
            as_string[i * side_len: (i + 1) * side_len]
            for i in range(side_len)]

    def col_lines(self):
        """
        Calculate the columns of this L{Board}.

        @return: A C{list} of the string representations of this L{Board}s
            columns.
        @rtype: C{list} of C{str}
        """
        as_string = to_string(self)
        side_len = self.side_len()
        return [
            as_string[i::side_len]
            for i in range(side_len)]

    def zig_line(self):
        """
        Calculate the diagonal line from the top-left to the bottom-right.

        The result is wrapped in a C{list} to conform to the return types of
        row_lines() and col_lines().

        @return: A list containing the single string representing the top-left
            to bottom-right diagonal of this L{Board}.
        @rtype: C{list} of C{str}
        """
        return [to_string(self)[::self.side_len() + 1]]

    def zag_line(self):
        """
        Calculate the diagonal line from the bottom-left to the top-right.

        The result is wrapped in a C{list} to conform to the return types of
        row_lines() and col_lines().

        @return: A list containing the single string representing the bottom-left
            to top-right diagonal of this L{Board}.
        @rtype: C{list} of C{str}
        """
        side_len = self.side_len()
        size = self.size()
        return [to_string(self)[-side_len:-size:-(side_len - 1)]]

    def all_lines(self):
        """
        Returns a list of all possible lines for this L{Board}.

        This is used by is_win() and heur_score() to determine whether the board
        represents a win and its preliminary score respectively.

        @return: A C{list} of all lines for this board.
        """
        return self.row_lines() +\
            self.col_lines() +\
            self.zig_line() +\
            self.zag_line()

    def score_line(self, line):
        """
        Provides a heuristic score for the given line.

        @param line: a string representing a line of the board.
        @type line: C{str}
        """
        active_symbol, unactive_symbol = self.symbols_in_turn_order()
        return (line.count(active_symbol) + line.count(unactive_symbol))\
            / (self.side_len() * 2.0)

    def heur_score(self):
        """
        Provides a heuristic score for this L{Board}.

        This is used by the minimax algorithm implemented by the server.  On
        L{Board} sizes greater than 3x3 the depth of the search is limitied and
        L{Board}s are assigned this preliminary score.
        """
        return max([self.score_line(line) for line in self.all_lines()])

def check_line(line):
    """
    Calculate whether the given line is a winning line. e.g. the line is
    of entirely 'X's or 'O's.

    @param line: a string representing a line of the L{Board}
    @type line: C{str}

    @return: Whether this line is a winning line.
    @rtype: C{bool}
    """
    def is_match(left, right):
        if left == right:
            return left
        return False
    match = reduce(is_match, line)
    return match and match != ' '
