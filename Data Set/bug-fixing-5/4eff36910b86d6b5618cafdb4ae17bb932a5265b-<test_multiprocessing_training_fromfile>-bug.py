@keras_test
def test_multiprocessing_training_fromfile():
    arr_data = np.random.randint(0, 256, (50, 2))
    arr_labels = np.random.randint(0, 2, 50)
    np.savez('data.npz', **{
        'data': arr_data,
        'labels': arr_labels,
    })

    def custom_generator():
        batch_size = 10
        n_samples = 50
        arr = np.load('data.npz')
        while True:
            batch_index = np.random.randint(0, (n_samples - batch_size))
            start = batch_index
            end = (start + batch_size)
            X = arr['data'][start:end]
            y = arr['labels'][start:end]
            (yield (X, y))
    model = Sequential()
    model.add(Dense(1, input_shape=(2,)))
    model.compile(loss='mse', optimizer='adadelta')
    model.fit_generator(custom_generator(), steps_per_epoch=5, epochs=1, verbose=1, max_q_size=10, workers=2, pickle_safe=True)
    model.fit_generator(custom_generator(), steps_per_epoch=5, epochs=1, verbose=1, max_q_size=10, pickle_safe=False)