

def __exit__(self, exec_type, exec_value, exec_tb):
    if (exec_type is errors.OpError):
        logging.error('Session closing due to OpError: %s', (exec_value,))
    self._default_session_context_manager.__exit__(exec_type, exec_value, exec_tb)
    self._default_graph_context_manager.__exit__(exec_type, exec_value, exec_tb)
    self._default_session_context_manager = None
    self._default_graph_context_manager = None
    self.close()
