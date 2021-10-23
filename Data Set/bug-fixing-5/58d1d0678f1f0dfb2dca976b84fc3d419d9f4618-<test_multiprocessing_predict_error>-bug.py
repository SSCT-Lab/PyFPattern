@keras_test
def test_multiprocessing_predict_error():
    good_batches = 3

    def custom_generator():
        'Raises an exception after a few good batches'
        for i in range(good_batches):
            (yield (np.random.randint(1, 256, size=(2, 5)), np.random.randint(1, 256, size=(2, 5))))
        raise RuntimeError
    model = Sequential()
    model.add(Dense(1, input_shape=(5,)))
    model.compile(loss='mse', optimizer='adadelta')
    with pytest.raises(StopIteration):
        model.predict_generator(custom_generator(), (good_batches + 1), 1, use_multiprocessing=False)