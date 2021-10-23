def toggleAutorun(self):
    if self.isAutorunEnabled():
        os.unlink(self.getAutorunPath())
    else:
        open(self.getAutorunPath(), 'w').write(self.formatAutorun())