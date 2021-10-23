def _get_expected_entrypoint(self):
    self.log('_get_expected_entrypoint')
    if (not self.parameters.entrypoint):
        return None
    return shlex.split(self.parameters.entrypoint)