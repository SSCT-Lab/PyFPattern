@configure
def compare_configuration(self, rollback_id=None):
    command = 'show | compare'
    if (rollback_id is not None):
        command += (' rollback %s' % int(rollback_id))
    resp = self.send_command(command)
    return resp