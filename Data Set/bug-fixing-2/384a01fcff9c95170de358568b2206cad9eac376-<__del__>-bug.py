

def __del__(self):
    self.filehandle.close()
    os.unlink(self.tmplfile)
