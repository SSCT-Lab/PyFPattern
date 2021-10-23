def load(self):
    if (self.backend is None):
        functions = self.load_header()
        self.backend = load_backend(self.t, self.lib, functions, self.mixins)
    return self.backend