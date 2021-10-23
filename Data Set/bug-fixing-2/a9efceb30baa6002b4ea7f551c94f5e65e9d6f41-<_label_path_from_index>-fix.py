

def _label_path_from_index(self, index):
    '\n        given image index, find out annotation path\n\n        Parameters:\n        ----------\n        index: int\n            index of a specific image\n\n        Returns:\n        ----------\n        full path of annotation file\n        '
    label_file = os.path.join(self.data_path, 'Annotations', (index + '.xml'))
    assert os.path.exists(label_file), 'Path does not exist: {}'.format(label_file)
    return label_file
