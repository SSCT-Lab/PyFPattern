

def supports_sessions(self):
    if (not self.get_option('eos_use_sessions')):
        self._session_support = False
    else:
        if self._session_support:
            return self._session_support
        try:
            self.get('show configuration sessions')
            self._session_support = True
        except AnsibleConnectionFailure:
            self._session_support = False
    return self._session_support
