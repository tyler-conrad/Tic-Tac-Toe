from kivy.app import App
from kivy.factory import Factory

def register_widgets():
    """
    Register widgets that are not explicitly imported.
    """
    custom_widgets = [
        ('RadioToggleButton', 'client.uix.radiotogglebutton'),
        ('BoardScreen', 'client.uix.boardscreen')]

    for name, module in custom_widgets:
        Factory.register(name, module=module)

class TTT(App):
    """
    Main application class.
    """
    kv_directory = 'view'

if __name__ == '__main__':
    register_widgets()
    TTT().run()
