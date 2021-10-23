def cli(self, command):
    reply = command(self.module, command)
    output = reply.find('.//output')
    if (not output):
        self.module.fail_json(msg=('failed to retrieve facts for command %s' % command))
    return str(output.text).strip()