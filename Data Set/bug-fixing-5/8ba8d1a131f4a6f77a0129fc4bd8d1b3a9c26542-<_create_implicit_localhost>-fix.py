def _create_implicit_localhost(self, pattern):
    if self.localhost:
        new_host = self.localhost
    else:
        new_host = Host(pattern)
        new_host.address = '127.0.0.1'
        new_host.implicit = True
        py_interp = sys.executable
        if (not py_interp):
            py_interp = '/usr/bin/python'
            display.warning('Unable to determine python interpreter from sys.executable. Using /usr/bin/python default. You can correct this by setting ansible_python_interpreter for localhost')
        new_host.set_variable('ansible_python_interpreter', py_interp)
        new_host.set_variable('ansible_connection', 'local')
        self.localhost = new_host
    return new_host