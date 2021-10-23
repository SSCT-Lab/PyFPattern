def close(self):
    logger.debug('closing %s', self.fname)
    if hasattr(self, 'fout'):
        self.fout.close()