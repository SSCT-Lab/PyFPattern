def _c_or_a(self):
    while True:
        key_pressed = self._connection._new_stdin.read(1)
        if (key_pressed.lower() == 'a'):
            return False
        elif (key_pressed.lower() == 'c'):
            return True