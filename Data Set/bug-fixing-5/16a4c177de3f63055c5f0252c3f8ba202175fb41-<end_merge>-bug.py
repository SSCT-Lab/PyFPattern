def end_merge(self, state):
    state = state.copy()
    state['datetime'] = datetime.now(tz=pytz.utc)
    self._send(state['project_id'], 'merge', extra_data=(state,), asynchronous=False)