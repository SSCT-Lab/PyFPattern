def clear(self):
    '\n        Reset the styler, removing any previously applied styles.\n\n        Returns None.\n        '
    self.ctx.clear()
    self._todo = []