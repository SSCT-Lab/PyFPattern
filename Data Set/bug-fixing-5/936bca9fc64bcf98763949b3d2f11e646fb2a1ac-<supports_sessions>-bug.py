def supports_sessions(self):
    try:
        if isinstance(self, Eapi):
            self.execute('show configuration sessions', output='text')
        else:
            self.execute('show configuration sessions')
        return True
    except NetworkError:
        return False