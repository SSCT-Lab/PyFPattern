

def _retrieve_cifar(name):
    root = download.get_dataset_directory('pfnet/chainer/cifar')
    path = os.path.join(root, '{}.npz'.format(name))
    url = 'https://www.cs.toronto.edu/~kriz/{}-python.tar.gz'.format(name)

    def creator(path):
        archive_path = download.cached_download(url)
        train_x = numpy.empty((5, 10000, 3072), dtype=numpy.uint8)
        train_y = numpy.empty((5, 10000), dtype=numpy.uint8)
        test_y = numpy.empty(10000, dtype=numpy.uint8)
        dir_name = '{}-batches-py/'.format(name)
        with tarfile.open(archive_path, 'r:gz') as archive:
            for i in range(5):
                file_name = '{}/data_batch_{}'.format(dir_name, (i + 1))
                d = pickle.load(archive.extractfile(file_name))
                train_x[i] = d['data']
                train_y[i] = d['labels']
            file_name = '{}/test_batch'.format(dir_name)
            d = pickle.load(archive.extractfile(file_name))
            test_x = d['data']
            test_y[...] = d['labels']
        train_x = train_x.reshape(50000, 3072)
        train_y = train_y.reshape(50000)
        numpy.savez_compressed(path, x=train_x, y=train_y)
        return {
            'train_x': train_x,
            'train_y': train_y,
            'test_x': test_x,
            'test_y': test_y,
        }
    return download.cache_or_load_file(path, creator, numpy.load)
