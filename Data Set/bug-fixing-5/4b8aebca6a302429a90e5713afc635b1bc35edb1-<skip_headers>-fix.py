def skip_headers(self, input_file):
    'Skip file headers that appear before the first document.\n\n        Parameters\n        ----------\n        input_file : file-like object\n            Opened file.\n\n        '
    for line in input_file:
        if line.startswith(b'%'):
            continue
        break