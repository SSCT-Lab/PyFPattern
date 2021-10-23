@skip_generators
def test_multiprocessing_training():
    arr_data = np.random.randint(0, 256, (50, 2))
    arr_labels = np.random.randint(0, 2, 50)
    arr_weights = np.random.random(50)

    @threadsafe_generator
    def custom_generator(use_weights=False):
        batch_size = 10
        n_samples = 50
        while True:
            batch_index = np.random.randint(0, (n_samples - batch_size))
            start = batch_index
            end = (start + batch_size)
            X = arr_data[start:end]
            y = arr_labels[start:end]
            if use_weights:
                w = arr_weights[start:end]
                (yield (X, y, w))
            else:
                (yield (X, y))
    model = Sequential()
    model.add(Dense(1, input_shape=(2,)))
    model.compile(loss='mse', optimizer='adadelta')
    if (os.name is 'nt'):
        with pytest.raises(ValueError):
            model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    else:
        model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=WORKERS, use_multiprocessing=True)
    model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, epochs=1, verbose=1, validation_steps=None, max_queue_size=10, workers=WORKERS, use_multiprocessing=False)
    if (os.name is 'nt'):
        with pytest.raises(ValueError):
            model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=(arr_data[:10], arr_labels[:10], arr_weights[:10]), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=True)
    else:
        model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=(arr_data[:10], arr_labels[:10], arr_weights[:10]), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=True)
    model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=(arr_data[:10], arr_labels[:10], arr_weights[:10]), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=False)
    if (os.name is 'nt'):
        with pytest.raises(ValueError):
            model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=custom_generator(True), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=True)
    else:
        model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=custom_generator(True), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=True)
    model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=custom_generator(True), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=False)
    model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=custom_generator(True), validation_steps=1, max_queue_size=10, workers=0, use_multiprocessing=True)
    model.fit_generator(custom_generator(True), steps_per_epoch=STEPS_PER_EPOCH, validation_data=custom_generator(True), validation_steps=1, max_queue_size=10, workers=0, use_multiprocessing=False)

    @threadsafe_generator
    def invalid_generator():
        while True:
            (yield (arr_data[:10], arr_data[:10], arr_labels[:10], arr_labels[:10]))
    with pytest.raises(ValueError):
        model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, validation_data=custom_generator(), validation_steps=None, max_queue_size=10, workers=1, use_multiprocessing=False)
    with pytest.raises(ValueError):
        model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, validation_data=(arr_data[:10], arr_data[:10], arr_labels[:10], arr_weights[:10]), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=False)
    with pytest.raises(ValueError):
        model.fit_generator(custom_generator(), steps_per_epoch=STEPS_PER_EPOCH, validation_data=invalid_generator(), validation_steps=1, max_queue_size=10, workers=1, use_multiprocessing=False)
    model.fit_generator(DummySequence(), steps_per_epoch=STEPS_PER_EPOCH, validation_data=DummySequence(), validation_steps=1, max_queue_size=10, workers=0, use_multiprocessing=True)
    model.fit_generator(DummySequence(), steps_per_epoch=STEPS_PER_EPOCH, validation_data=DummySequence(), validation_steps=1, max_queue_size=10, workers=0, use_multiprocessing=False)