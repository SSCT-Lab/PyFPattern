def get_mnist(path, name):
    path = pathlib.Path(path)
    x_path = (path / '{}-images-idx3-ubyte.gz'.format(name))
    y_path = (path / '{}-labels-idx1-ubyte.gz'.format(name))
    with gzip.open(x_path, 'rb') as fx:
        fx.read(16)
        x = np.frombuffer(fx.read(), dtype=np.uint8).reshape((- 1), 784)
        x.flags.writeable = True
    with gzip.open(y_path, 'rb') as fy:
        fy.read(8)
        y = np.frombuffer(fy.read(), dtype=np.uint8)
        y.flags.writeable = True
    assert (x.shape[0] == y.shape[0])
    x = x.astype(np.float32)
    x /= 255
    y = y.astype(np.int32)
    return (chx.array(x), chx.array(y))