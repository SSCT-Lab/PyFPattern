def banner(self, msg, color=None):
    '\n        Prints a header-looking line with stars taking up to 80 columns\n        of width (3 columns, minimum)\n        '
    if self.b_cowsay:
        try:
            self.banner_cowsay(msg)
            return
        except OSError:
            self.warning('somebody cleverly deleted cowsay or something during the PB run.  heh.')
    msg = msg.strip()
    star_len = (79 - len(msg))
    if (star_len < 0):
        star_len = 3
    stars = ('*' * star_len)
    self.display(('\n%s %s' % (msg, stars)), color=color)