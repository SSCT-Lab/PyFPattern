

def download_mnist_data():
    print('Downloading {:s}...'.format(train_images))
    request.urlretrieve('{:s}/{:s}'.format(parent, train_images), train_images)
    print('Done')
    print('Downloading {:s}...'.format(train_labels))
    request.urlretrieve('{:s}/{:s}'.format(parent, train_labels), train_labels)
    print('Done')
    print('Downloading {:s}...'.format(test_images))
    request.urlretrieve('{:s}/{:s}'.format(parent, test_images), test_images)
    print('Done')
    print('Downloading {:s}...'.format(test_labels))
    request.urlretrieve('{:s}/{:s}'.format(parent, test_labels), test_labels)
    print('Done')
    print('Converting training data...')
    (data_train, target_train) = load_mnist(train_images, train_labels, num_train)
    print('Done')
    print('Converting test data...')
    (data_test, target_test) = load_mnist(test_images, test_labels, num_test)
    mnist = {
        
    }
    mnist['data'] = np.append(data_train, data_test, axis=0)
    mnist['target'] = np.append(target_train, target_test, axis=0)
    print('Done')
    print('Save output...')
    with open('mnist.pkl', 'wb') as output:
        six.moves.cPickle.dump(mnist, output, (- 1))
    print('Done')
    print('Convert completed')
