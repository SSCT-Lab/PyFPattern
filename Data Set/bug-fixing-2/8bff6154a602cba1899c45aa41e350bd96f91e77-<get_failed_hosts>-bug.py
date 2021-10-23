

def get_failed_hosts(self):
    return dict(((host, True) for (host, state) in iteritems(self._host_states) if ((state.run_state == self.ITERATING_COMPLETE) and (state.fail_state != self.FAILED_NONE))))
