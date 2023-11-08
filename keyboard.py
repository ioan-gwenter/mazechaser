# Keyboard Listener - Handles Keyboard Events

class KeyboardListener:
    """
    Class to handle multiple keyboard inputs simultaneously
    """
    def __init__(self, game):
        self.keys_pressed = []
        self.last_pressed = []
        self.game = game

    def listener(self, event):
        """
        Appends any pressed keys to the keys_pressed list
        """
        key = event.keysym
        if key not in self.keys_pressed:
            self.keys_pressed.append(key)

    def clear_pressed(self, event):
        """
        Clears all the keys from the keys pressed list, and appends them to the last_pressed list
        """
        key = event.keysym
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
            self.last_pressed.append(key)

    def get_pressed(self):
        """
        Getter for the keys_pressed list
        :return: list of pressed keys
        """
        return self.keys_pressed
    
    def get_last_pressed(self):
        """
        Getter for the last_pressed list
        :return: list of previously pressed keys
        """
        return self.last_pressed

    def check_key(self, key):
        """
        Checks whether a certain key has been presesed by comparing to the list of currently pressed keys
        :param key: a key string eg. "a", "Escape"
        :return: True/False
        """
        return bool(key in self.keys_pressed)
