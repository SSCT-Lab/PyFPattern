def _get_expected_entrypoint(self):
    if (not self.parameters.entrypoint):
        return None
    return shlex.split(self.parameters.entrypoint)