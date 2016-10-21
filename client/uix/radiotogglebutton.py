"""
Toggle button that can only be untoggled by pressing another member of its
button group. Acts like a radio button.

This is used in the setup screen to select the board size.
"""

from kivy.uix.togglebutton import ToggleButton

class RadioToggleButton(ToggleButton):
    """
    Radio toggle button.
    """
    def _do_press(self):
        self._release_group(self)
        if self.state == 'normal':
            self.state = 'down'
