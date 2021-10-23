def get_failed_hosts(self):
    return dict(((host, True) for (host, state) in iteritems(self._host_states) if self._check_failed_state(state)))