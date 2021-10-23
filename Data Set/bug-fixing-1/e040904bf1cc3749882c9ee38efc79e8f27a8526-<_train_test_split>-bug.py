

def _train_test_split(*args, **options):
    test_size = options.pop('test_size', None)
    train_size = options.pop('train_size', None)
    random_state = options.pop('random_state', None)
    if ((test_size is None) and (train_size is None)):
        train_size = 0.75
    elif (train_size is None):
        train_size = (1 - test_size)
    train_size = int((train_size * args[0].shape[0]))
    np.random.seed(random_state)
    indices = np.random.permutation(args[0].shape[0])
    (train_idx, test_idx) = (indices[:train_size], indices[:train_size])
    result = []
    for x in args:
        result += [x.take(train_idx, axis=0), x.take(test_idx, axis=0)]
    return tuple(result)
