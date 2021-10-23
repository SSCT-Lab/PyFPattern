def isAutorunEnabled(self):
    path = self.getAutorunPath()
    return (os.path.isfile(path) and (open(path).read().decode('utf8') == self.formatAutorun()))