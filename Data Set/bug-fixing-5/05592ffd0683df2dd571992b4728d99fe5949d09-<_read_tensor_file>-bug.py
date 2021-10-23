def _read_tensor_file(fpath):
    with file_io.FileIO(fpath, 'r') as f:
        tensor = []
        for line in f:
            if line:
                tensor.append(map(float, line.rstrip('\n').split('\t')))
    return np.array(tensor, dtype='float32')