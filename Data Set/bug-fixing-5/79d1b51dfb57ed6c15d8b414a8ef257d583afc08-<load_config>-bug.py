def load_config(self, config):
    checkpoint = ('ansible_%s' % int(time.time()))
    self.execute([('checkpoint %s' % checkpoint)], output='text')
    try:
        self.configure(config)
    except NetworkError:
        self.load_checkpoint(checkpoint)
        raise
    self.execute([('no checkpoint %s' % checkpoint)], output='text')