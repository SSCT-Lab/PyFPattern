

def maybe_download():
    'May be downloads training data and returns train and test file names.'
    if FLAGS.train_data:
        train_file_name = FLAGS.train_data
    else:
        train_file = tempfile.NamedTemporaryFile(delete=False)
        urllib.urlretrieve('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data', train_file.name)
        train_file_name = train_file.name
        train_file.close()
        print(('Training data is downloaded to %s' % train_file_name))
    if FLAGS.test_data:
        test_file_name = FLAGS.test_data
    else:
        test_file = tempfile.NamedTemporaryFile(delete=False)
        urllib.urlretrieve('https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test', test_file.name)
        test_file_name = test_file.name
        test_file.close()
        print(('Test data is downloaded to %s' % test_file_name))
    return (train_file_name, test_file_name)
