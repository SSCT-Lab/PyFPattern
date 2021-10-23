def setup_module():
    'Test fixture run once and common to all tests of this module'
    if (not pillow_installed):
        raise SkipTest('PIL not installed.')
    if (not os.path.exists(LFW_HOME)):
        os.makedirs(LFW_HOME)
    random_state = random.Random(42)
    np_rng = np.random.RandomState(42)
    counts = {
        
    }
    for name in FAKE_NAMES:
        folder_name = os.path.join(LFW_HOME, 'lfw_funneled', name)
        if (not os.path.exists(folder_name)):
            os.makedirs(folder_name)
        n_faces = np_rng.randint(1, 5)
        counts[name] = n_faces
        for i in range(n_faces):
            file_path = os.path.join(folder_name, (name + ('_%04d.jpg' % i)))
            uniface = np_rng.randint(0, 255, size=(250, 250, 3))
            try:
                imsave(file_path, uniface)
            except ImportError:
                raise SkipTest('PIL not installed')
    with open(os.path.join(LFW_HOME, 'lfw_funneled', '.test.swp'), 'wb') as f:
        f.write(b'Text file to be ignored by the dataset loader.')
    with open(os.path.join(LFW_HOME, 'pairsDevTrain.txt'), 'wb') as f:
        f.write(b'10\n')
        more_than_two = [name for (name, count) in counts.items() if (count >= 2)]
        for i in range(5):
            name = random_state.choice(more_than_two)
            (first, second) = random_state.sample(range(counts[name]), 2)
            f.write(('%s\t%d\t%d\n' % (name, first, second)).encode())
        for i in range(5):
            (first_name, second_name) = random_state.sample(FAKE_NAMES, 2)
            first_index = random_state.choice(np.arange(counts[first_name]))
            second_index = random_state.choice(np.arange(counts[second_name]))
            f.write(('%s\t%d\t%s\t%d\n' % (first_name, first_index, second_name, second_index)).encode())
    with open(os.path.join(LFW_HOME, 'pairsDevTest.txt'), 'wb') as f:
        f.write(b"Fake place holder that won't be tested")
    with open(os.path.join(LFW_HOME, 'pairs.txt'), 'wb') as f:
        f.write(b"Fake place holder that won't be tested")