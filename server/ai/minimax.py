"""
Implemetations of the minimax algorithm.
"""

from common.model.board import to_string

# The transition point between large and small boards.
# Used to limit the search depth for large boards.
SMALL_BOARD_CUTOFF = 3

# The maximum depth to search to for small boards.
MAX_DEPTH_SMALL_BOARD = 9

# The maximum depth to search to for large boards.
MAX_DEPTH_LARGE_BOARD = 1

def max_depth(board):
    """
    Return the depth to search to for the given L{Board}.

    L{Board}s less than 3x3 are searched completely.  Larger L{Boards} are only
    searched to MAX_DEPTH_LARGE_BOARD

    @param board: The L{Board} to determine the max depth for.
    @type board: L{Board}

    @return: The maximum depth to search to.
    @rtype: C{int}
    """
    return (MAX_DEPTH_LARGE_BOARD
        if board.side_len() > SMALL_BOARD_CUTOFF
        else MAX_DEPTH_SMALL_BOARD)

def pluck_score(state_tup):
    """
    Pull the score from the tuple returned from the minimax algorithm.

    @return: the score in the tuple returned by the minmax function.
    @rtype: C{float}
    """
    return state_tup[0][0]

def cached(func):
    """
    Decorator for a minimax implementation that memoizes results from calls to
    the wrapped function.

    @param func: The function to memoize.
    @type func: C{function}
    """
    cache = {}
    def wrapper(board, *args):
        key = to_string(board), args
        if key in cache:
            return cache[key]
        val = func(board, *args)
        cache[key] = val
        return val
    return wrapper

@cached
def minimax(board, is_min_turn):
    """
    A minimal implementation of the minimax alogorithm.

    Does not implement alpha-beta pruning or limit search depth. This
    implementation is not used but it works.

    When recursing on a leaf board instead of returning C{None}
    for the best sub-L{Board} instead return the current L{Board}.  This means
    that if we attempt to start the minimax function on a L{Board} that is a
    leaf L{Board} it will simply return that L{Board} as the best move.  This
    has the effect of simplifying the client code as we only need to check for
    a 'Game Over' state in one place - the response from the server.  For
    example if the user plays a winning move, that winning L{Board} is passed to
    the server which then returns the L{Board} unchanged. Once returned the
    client checks whether the L{Board} is a 'Game Over' L{Board}.

    @param board: the L{Board} for which to determine the best move.
    @type board: L{Board}

    @param is_min_turn: whether this is the minimizing players turn.
    @type is_min_turn: C{bool}

    @return: this L{Board}s score, the best sub-L{Board} and the current
        L{Board}
    @rtype: a C{tuple} containing a C{tuple} of a C{float} and L{Board} and
        L{Board}
    """
    is_leaf, score = board.is_leaf_and_score()
    if is_leaf:
        return ((1 if is_min_turn else -1) * score, board), board

    (score, sub_sub_board), sub_board = sorted([
            minimax(child, not is_min_turn)
            for child in board.children()],
        key=pluck_score)[0 if is_min_turn else -1]

    return (score, sub_board), board

@cached
def alpha_beta(board, is_min_turn=True, alpha=1, beta=-1, depth=0):
    """
    Implementation of the minimax algorithm with alpha-beta pruning and support
    for limiting the search depth.

    L{Board}s of size 3x3 or less are searched completely.  Larger L{Board}s are
    assigned a heuristic score once MAX_DEPTH_LARGE_BOARD has been reached.

    For details about the handling of leaf boards see L{minimax}.

    @param board: the L{Board} for which to the determine the best move.
    @type board: L{Board}

    @param is_min_turn: whether this is the minimizing players turn.
    @type is_min_turn: C{bool}

    @return: this L{Board}s score, the best sub-L{Board} and the current
        L{Board}
    @rtype: a C{tuple} containing a C{tuple} of a C{float} and L{Board} and
        L{Board}
    """
    is_leaf, score = board.is_leaf_and_score()
    if is_leaf:
        return ((1 if is_min_turn else -1) * score, board), board

    if depth > max_depth(board):
        return ((1 if is_min_turn else -1) * board.heur_score(), board), board

    score_list = []
    for child in board.children():
        (score, sub_sub_board), sub_board\
            = alpha_beta(child, not is_min_turn, alpha, beta, depth + 1)

        if is_min_turn:
            if score < alpha:
                alpha = score
        else:
            if score > beta:
                beta = score

        if alpha <= beta:
            return ((alpha if is_min_turn else beta), sub_board), board

        score_list.append(((score, sub_board), board))

    return sorted(score_list, key=pluck_score)[0 if is_min_turn else -1]

