"""
The screen on which the L{Board} is displayed.
"""

from kivy.properties import BooleanProperty
from kivy.uix.screenmanager import Screen

class BoardScreen(Screen):
    """
    Extension of the kivy Screen class to support disabling of user input.

    This is needed to prevent the user from making a move while the server is
    processing its next move.
    """

    mouse_enabled = BooleanProperty()

    def __init__(self, *args, **kwargs):
        super(BoardScreen, self).__init__(*args, **kwargs)
        # Store the original definition of the event dispatching function so
        # that it can be patched back in when the mouse should be reenabled.
        self.real_on_touch_down = self.on_touch_down

    def on_mouse_enabled(self, caller, enabled):
        """
        Toggles whether user input events are ignored.
        """

        # Patch the event dispatching method 'on_touch_down()' with a stub
        # function that signals that the event has been handled and no
        # additional dispatching need take place.
        self.on_touch_down =\
            self.real_on_touch_down if enabled else lambda touch: True
