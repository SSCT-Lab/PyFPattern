def update_play_context(self, play_context):
    'Updates the play context information for the connection'
    if ((self._play_context.become is False) and (play_context.become is True)):
        auth_pass = play_context.become_pass
        self._terminal.on_authorize(passwd=auth_pass)
    elif ((self._play_context.become is True) and (not play_context.become)):
        self._terminal.on_deauthorize()
    self._play_context = play_context