def load(self):
    if (self.backend is None):
        with self.loading_lock:
            if (self.backend is None):
                self.backend = load_backend(self.lib_prefix, self.lib_name, self.functions, self.mixins)
    return self.backend