def load_checkpoint(self, checkpoint):
    try:
        self.execute([('rollback running-config checkpoint %s' % checkpoint), ('no checkpoint %s' % checkpoint)], output='text')
    except TypeError:
        self.execute([('rollback running-config checkpoint %s' % checkpoint), ('no checkpoint %s' % checkpoint)])