

@keras_test
def test_multiprocessing_predict_error():
    batch_size = 10
    good_batches = 3

    def custom_generator():
        'Raises an exception after a few good batches'
        for i in range(good_batches):
            (yield (np.random.randint(batch_size, 256, (50, 2)), np.random.randint(batch_size, 2, 50)))
        raise RuntimeError
    model = Sequential()
    model.add(Dense(1, input_shape=(2,)))
    model.compile(loss='mse', optimizer='adadelta')
    with pytest.raises(ValueError):
        model.predict_generator(custom_generator(), (good_batches + 1), 1, workers=4, pickle_safe=True)
    with pytest.raises(ValueError):
        model.predict_generator(custom_generator(), (good_batches + 1), 1, pickle_safe=False)
