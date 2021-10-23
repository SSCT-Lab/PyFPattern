def exists(self):
    'Check if the namespace already exists'
    (rtc, out, err) = self._netns(['exec', self.name, 'ls'])
    if (rtc != 0):
        self.module.fail_json(msg=err)