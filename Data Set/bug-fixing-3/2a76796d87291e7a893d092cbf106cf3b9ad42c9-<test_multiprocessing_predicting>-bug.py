@skip_generators
def test_multiprocessing_predicting():
    arr_data = np.random.randint(0, 256, (50, 2))

    @threadsafe_generator
    def custom_generator():
        batch_size = 10
        n_samples = 50
        while True:
            batch_index = np.random.randint(0, (n_samples - batch_size))
            start = batch_index
            end = (start + batch_size)
            X = arr_data[start:end]
            (yield X)
    model = Sequential()
    model.add(Dense(1, input_shape=(2,)))
    model.compile(loss='mse', optimizer='adadelta')
    if (os.name is 'nt'):
        with pytest.raises(ValueError):
            model.predict_generator(custom_generator(), steps=STEPS, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    else:
        model.predict_generator(custom_generator(), steps=STEPS, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    if (os.name is 'nt'):
        with pytest.raises(ValueError):
            model.predict_generator(custom_generator(), steps=STEPS, max_queue_size=10, workers=1, use_multiprocessing=True)
    else:
        model.predict_generator(custom_generator(), steps=STEPS, max_queue_size=10, workers=1, use_multiprocessing=True)
    model.predict_generator(custom_generator(), steps=STEPS, max_queue_size=10, workers=0, use_multiprocessing=True)