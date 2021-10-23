

def commit(self, comment=None):
    command = b'commit'
    if comment:
        command += b' comment {0}'.format(comment)
    command += b' and-quit'
    return self.send_command(command)
