@skip_generators
def test_multiprocessing_predict_error():
    arr_data = np.random.randint(0, 256, (50, 2))
    good_batches = 3

    @threadsafe_generator
    def custom_generator():
        'Raises an exception after a few good batches'
        batch_size = 10
        n_samples = 50
        for i in range(good_batches):
            batch_index = np.random.randint(0, (n_samples - batch_size))
            start = batch_index
            end = (start + batch_size)
            X = arr_data[start:end]
            (yield X)
        raise RuntimeError
    model = Sequential()
    model.add(Dense(1, input_shape=(2,)))
    model.compile(loss='mse', optimizer='adadelta')
    if (os.name is 'nt'):
        with pytest.raises(StopIteration):
            model.predict_generator(custom_generator(), steps=((good_batches * WORKERS) + 1), max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    else:
        with pytest.raises(RuntimeError):
            model.predict_generator(custom_generator(), steps=((good_batches * WORKERS) + 1), max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    if (os.name is 'nt'):
        with pytest.raises(RuntimeError):
            model.predict_generator(custom_generator(), steps=(good_batches + 1), max_queue_size=10, workers=1, use_multiprocessing=True)
    else:
        with pytest.raises(RuntimeError):
            model.predict_generator(custom_generator(), steps=(good_batches + 1), max_queue_size=10, workers=1, use_multiprocessing=True)
    with pytest.raises(RuntimeError):
        model.predict_generator(custom_generator(), steps=(good_batches + 1), max_queue_size=10, workers=0, use_multiprocessing=True)