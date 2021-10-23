

def commit(self, *args, **kwargs):
    'Execute commit command on remote device.\n        :kwargs:\n            comment: Optional commit description.\n        '
    comment = kwargs.get('comment', None)
    command = b'commit'
    if comment:
        command += b' comment {0}'.format(comment)
    command += b' and-quit'
    return self.send_command(command)
