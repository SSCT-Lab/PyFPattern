@skip_generators
def test_multiprocessing_training_from_file(in_tmpdir):
    arr_data = np.random.randint(0, 256, (50, 2))
    arr_labels = np.random.randint(0, 2, 50)
    np.savez('data.npz', **{
        'data': arr_data,
        'labels': arr_labels,
    })

    @threadsafe_generator
    def custom_generator():
        batch_size = 10
        n_samples = 50
        with np.load('data.npz') as arr:
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
    if (os.name is 'nt'):
        with pytest.raises(ValueError):
            model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    else:
        model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    if (os.name is 'nt'):
        with pytest.raises(ValueError):
            model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=1, use_multiprocessing=True)
    else:
        model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=1, use_multiprocessing=True)
    model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=0, use_multiprocessing=True)
    os.remove('data.npz')