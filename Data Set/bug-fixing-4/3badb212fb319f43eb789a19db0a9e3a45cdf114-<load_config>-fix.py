def load_config(self, config, commit=False, replace=False):
    if self.supports_sessions():
        return self.load_config_session(config, commit, replace)
    else:
        return self.configure(config)