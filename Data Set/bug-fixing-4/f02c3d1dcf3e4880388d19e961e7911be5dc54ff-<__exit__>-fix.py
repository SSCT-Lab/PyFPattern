def __exit__(self, exc_type, exc_value, traceback):
    self.proc.kill()
    self.proc.communicate()