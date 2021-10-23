def to_string(self, metadata):
    return '{}: {}'.format(metadata['type'], truncatechars(metadata['value'].splitlines()[0], 100))