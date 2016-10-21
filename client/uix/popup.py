"""
A Graphical popup window displayed at the end of a game.
"""

from kivy.uix.popup import Popup

from client.util.query import find

class GameOverPopup(Popup):
    """
    Game over popup.
    """
    def close(self):
        """
        Reset the game to the setup screen and close the popup.
        """
        find('board_screen').clear_widgets()
        find('screen_manager').current = 'setup_screen'
        self.dismiss()


