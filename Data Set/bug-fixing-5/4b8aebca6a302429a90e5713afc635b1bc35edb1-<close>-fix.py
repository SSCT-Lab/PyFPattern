def close(self):
    'Close file.'
    logger.debug('closing %s', self.fname)
    if hasattr(self, 'fout'):
        self.fout.close()