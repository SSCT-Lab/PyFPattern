def __init__(self, loader):
    self._entries = []
    self._basedir = to_text(os.getcwd(), errors='surrogate_or_strict')
    self._loader = loader
    self._file_name = None