def set_color(self, color):
    '\n        Change the color of the secondary axes and all decorators.\n\n        Parameters\n        ----------\n        color : Matplotlib color\n        '
    if (self._orientation == 'x'):
        self.tick_params(axis='x', colors=color)
        self.spines['bottom'].set_color(color)
        self.spines['top'].set_color(color)
        self.xaxis.label.set_color(color)
    else:
        self.tick_params(axis='y', colors=color)
        self.spines['left'].set_color(color)
        self.spines['right'].set_color(color)
        self.yaxis.label.set_color(color)