

def execute_command(self, *args, **kwargs):
    try:
        return super(self.__class__, self).execute_command(*args, **kwargs)
    except (ConnectionError, BusyLoadingError, KeyError):
        self.connection_pool.nodes.reset()
        return super(self.__class__, self).execute_command(*args, **kwargs)
