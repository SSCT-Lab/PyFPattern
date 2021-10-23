def _set_column_width(self):
    if os.isatty(0):
        tty_size = unpack('HHHH', fcntl.ioctl(0, TIOCGWINSZ, pack('HHHH', 0, 0, 0, 0)))[1]
    else:
        tty_size = 0
    self.columns = max(79, (tty_size - 1))