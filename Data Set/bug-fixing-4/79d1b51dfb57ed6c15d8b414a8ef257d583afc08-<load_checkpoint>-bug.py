def load_checkpoint(self, checkpoint):
    self.execute([('rollback running-config checkpoint %s' % checkpoint), ('no checkpoint %s' % checkpoint)], output='text')