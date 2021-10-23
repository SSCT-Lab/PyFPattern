def get(self, command=None, prompt=None, answer=None, sendonly=False, output=None, check_all=False):
    if (not command):
        raise ValueError('must provide value of command to execute')
    if output:
        raise ValueError(("'output' value %s is not supported for get" % output))
    return self.send_command(command=command, prompt=prompt, answer=answer, sendonly=sendonly, check_all=check_all)