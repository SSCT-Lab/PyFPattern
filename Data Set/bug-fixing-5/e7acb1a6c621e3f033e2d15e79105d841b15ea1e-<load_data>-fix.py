@keras_export('keras.datasets.boston_housing.load_data')
def load_data(path='boston_housing.npz', test_split=0.2, seed=113):
    'Loads the Boston Housing dataset.\n\n  Arguments:\n      path: path where to cache the dataset locally\n          (relative to ~/.keras/datasets).\n      test_split: fraction of the data to reserve as test set.\n      seed: Random seed for shuffling the data\n          before computing the test split.\n\n  Returns:\n      Tuple of Numpy arrays: `(x_train, y_train), (x_test, y_test)`.\n  '
    assert (0 <= test_split < 1)
    origin_folder = 'https://storage.googleapis.com/tensorflow/tf-keras-datasets/'
    path = get_file(path, origin=(origin_folder + 'boston_housing.npz'), file_hash='f553886a1f8d56431e820c5b82552d9d95cfcb96d1e678153f8839538947dff5')
    with np.load(path, allow_pickle=True) as f:
        x = f['x']
        y = f['y']
    np.random.seed(seed)
    indices = np.arange(len(x))
    np.random.shuffle(indices)
    x = x[indices]
    y = y[indices]
    x_train = np.array(x[:int((len(x) * (1 - test_split)))])
    y_train = np.array(y[:int((len(x) * (1 - test_split)))])
    x_test = np.array(x[int((len(x) * (1 - test_split))):])
    y_test = np.array(y[int((len(x) * (1 - test_split))):])
    return ((x_train, y_train), (x_test, y_test))