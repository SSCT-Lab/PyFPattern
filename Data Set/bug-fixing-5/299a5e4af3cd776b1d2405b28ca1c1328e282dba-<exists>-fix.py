def exists(self):
    'Check if the namespace already exists'
    (rc, out, err) = self.module.run_command('ip netns list')
    if (rc != 0):
        self.module.fail_json(msg=to_text(err))
    return (self.name in out)