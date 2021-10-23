def update(self):
    self.im.set_data(self.X[:, :, self.ind])
    ax.set_ylabel(('slice %s' % self.ind))
    self.im.axes.figure.canvas.draw()