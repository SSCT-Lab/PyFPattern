def __init__(self, loader):
    self._entries = []
    self._basedir = os.getcwd()
    self._loader = loader
    self._file_name = None