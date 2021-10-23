def _c_or_a(self, stdin):
    while True:
        key_pressed = stdin.read(1)
        if (key_pressed.lower() == b'a'):
            return False
        elif (key_pressed.lower() == b'c'):
            return True