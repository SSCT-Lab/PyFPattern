def update(self):
    if os.path.exists(self.want.dest):
        if (not self.want.force):
            raise F5ModuleError("File '{0}' already exists".format(self.want.fulldest))
    self.execute()