"""
Various attributes representing the game state.
"""

# Using a module here to act as a Singleton.  Having these in an independent
# module also prevents issues with circular dependecies.

# Whether the user decided to play the first move.
user_goes_first = None

# The users selected board size.
board_side_len = None

# Total wins.
wins = 0

# Total draws.
draws = 0

# Total losses.
losses = 0
