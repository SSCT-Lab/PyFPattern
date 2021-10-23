

def update_play_context(self, pc_data):
    'Updates the play context information for the connection'
    pc_data = to_bytes(pc_data)
    if PY3:
        pc_data = cPickle.loads(pc_data, encoding='bytes')
    else:
        pc_data = cPickle.loads(pc_data)
    play_context = PlayContext()
    play_context.deserialize(pc_data)
    messages = ['updating play_context for connection']
    if (self._play_context.become ^ play_context.become):
        if (play_context.become is True):
            auth_pass = play_context.become_pass
            self._terminal.on_become(passwd=auth_pass)
            messages.append('authorizing connection')
        else:
            self._terminal.on_unbecome()
            messages.append('deauthorizing connection')
    self._play_context = play_context
    self.reset_history()
    self.disable_response_logging()
    return messages
