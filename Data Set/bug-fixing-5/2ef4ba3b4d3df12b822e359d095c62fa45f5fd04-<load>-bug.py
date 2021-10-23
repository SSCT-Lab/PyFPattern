def load(self, config):
    '\n        :type config: dict[str, str]\n        :rtype: bool\n        '
    self.instance_id = config['instance_id']
    self.endpoint = config['endpoint']
    self.started = True
    display.sensitive.add(self.instance_id)
    return True