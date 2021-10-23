def load_config(self, config):
    checkpoint = ('ansible_%s' % int(time.time()))
    try:
        self.execute([('checkpoint %s' % checkpoint)], output='text')
    except TypeError:
        self.execute([('checkpoint %s' % checkpoint)])
    try:
        self.configure(config)
    except NetworkError:
        self.load_checkpoint(checkpoint)
        raise
    try:
        self.execute([('no checkpoint %s' % checkpoint)], output='text')
    except TypeError:
        self.execute([('no checkpoint %s' % checkpoint)])