def banner(self, msg, color=None, cows=True):
    '\n        Prints a header-looking line with cowsay or stars wit hlength depending on terminal width (3 minimum)\n        '
    if (self.b_cowsay and cows):
        try:
            self.banner_cowsay(msg)
            return
        except OSError:
            self.warning('somebody cleverly deleted cowsay or something during the PB run.  heh.')
    msg = msg.strip()
    star_len = (self.columns - len(msg))
    if (star_len <= 3):
        star_len = 3
    stars = ('*' * star_len)
    self.display(('\n%s %s' % (msg, stars)), color=color)