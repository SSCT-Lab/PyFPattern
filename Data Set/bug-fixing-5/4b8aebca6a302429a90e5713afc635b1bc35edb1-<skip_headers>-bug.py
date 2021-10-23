def skip_headers(self, input_file):
    '\n        Skip file headers that appear before the first document.\n        '
    for line in input_file:
        if line.startswith(b'%'):
            continue
        break