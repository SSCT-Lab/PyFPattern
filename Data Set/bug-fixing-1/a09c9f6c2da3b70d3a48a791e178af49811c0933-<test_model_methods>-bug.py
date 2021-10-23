

@keras_test
def test_model_methods():
    a = Input(shape=(3,), name='input_a')
    b = Input(shape=(3,), name='input_b')
    a_2 = Dense(4, name='dense_1')(a)
    dp = Dropout(0.5, name='dropout')
    b_2 = dp(b)
    model = Model([a, b], [a_2, b_2])
    optimizer = 'rmsprop'
    loss = 'mse'
    loss_weights = [1.0, 0.5]
    input_a_np = np.random.random((10, 3))
    input_b_np = np.random.random((10, 3))
    output_a_np = np.random.random((10, 4))
    output_b_np = np.random.random((10, 3))
    with pytest.raises(RuntimeError):
        model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    model.compile(optimizer, loss, metrics=[], loss_weights=loss_weights, sample_weight_mode=None)
    out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    out = model.train_on_batch({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, [output_a_np, output_b_np])
    out = model.train_on_batch({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, {
        'dense_1': output_a_np,
        'dropout': output_b_np,
    })
    out = model.fit([input_a_np, input_b_np], [output_a_np, output_b_np], epochs=1, batch_size=4)
    out = model.fit({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, [output_a_np, output_b_np], epochs=1, batch_size=4)
    out = model.fit({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, {
        'dense_1': output_a_np,
        'dropout': output_b_np,
    }, epochs=1, batch_size=4)
    out = model.fit([input_a_np, input_b_np], [output_a_np, output_b_np], epochs=1, batch_size=4, validation_split=0.5)
    out = model.fit({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, [output_a_np, output_b_np], epochs=1, batch_size=4, validation_split=0.5)
    out = model.fit({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, {
        'dense_1': output_a_np,
        'dropout': output_b_np,
    }, epochs=1, batch_size=4, validation_split=0.5)
    out = model.fit([input_a_np, input_b_np], [output_a_np, output_b_np], epochs=1, batch_size=4, validation_data=([input_a_np, input_b_np], [output_a_np, output_b_np]))
    out = model.fit({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, [output_a_np, output_b_np], epochs=1, batch_size=4, validation_split=0.5, validation_data=({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, [output_a_np, output_b_np]))
    out = model.fit({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, {
        'dense_1': output_a_np,
        'dropout': output_b_np,
    }, epochs=1, batch_size=4, validation_split=0.5, validation_data=({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, {
        'dense_1': output_a_np,
        'dropout': output_b_np,
    }))
    out = model.test_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    out = model.test_on_batch({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, [output_a_np, output_b_np])
    out = model.test_on_batch({
        'input_a': input_a_np,
        'input_b': input_b_np,
    }, {
        'dense_1': output_a_np,
        'dropout': output_b_np,
    })
    out = model.predict_on_batch([input_a_np, input_b_np])
    out = model.predict_on_batch({
        'input_a': input_a_np,
        'input_b': input_b_np,
    })
    input_a_np = np.random.random((10, 3))
    input_b_np = np.random.random((10, 3))
    output_a_np = np.random.random((10, 4))
    output_b_np = np.random.random((10, 3))
    out = model.evaluate([input_a_np, input_b_np], [output_a_np, output_b_np], batch_size=4)
    out = model.predict([input_a_np, input_b_np], batch_size=4)
    input_a_np = np.random.random((10, 3))
    input_b_np = np.random.random((10, 3))
    output_a_np = np.random.random((10, 4))
    output_b_np = np.random.random((10, 3))
    sample_weight = [None, np.random.random((10,))]
    out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np], sample_weight=sample_weight)
    out = model.test_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np], sample_weight=sample_weight)
    model.compile(optimizer, loss, metrics=['acc'], sample_weight_mode=None)
    out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    assert (len(out) == 5)
    out = model.test_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    assert (len(out) == 5)
    model.compile(optimizer, loss, metrics={
        'dense_1': 'acc',
    }, sample_weight_mode=None)
    out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    assert (len(out) == 4)
    out = model.test_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    assert (len(out) == 4)
    model.compile(optimizer, loss, metrics={
        'dense_1': ['acc'],
    }, sample_weight_mode=None)
    out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    assert (len(out) == 4)
    out = model.test_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    assert (len(out) == 4)
    trained_epochs = []

    def on_epoch_begin(epoch, logs):
        trained_epochs.append(epoch)
    tracker_cb = LambdaCallback(on_epoch_begin=on_epoch_begin)
    out = model.fit([input_a_np, input_b_np], [output_a_np, output_b_np], epochs=5, batch_size=4, initial_epoch=2, callbacks=[tracker_cb])
    assert (trained_epochs == [2, 3, 4])
    trained_epochs = []

    def gen_data(batch_sz):
        while True:
            (yield ([np.random.random((batch_sz, 3)), np.random.random((batch_sz, 3))], [np.random.random((batch_sz, 4)), np.random.random((batch_sz, 3))]))
    out = model.fit_generator(gen_data(4), steps_per_epoch=3, epochs=5, initial_epoch=2, callbacks=[tracker_cb])
    assert (trained_epochs == [2, 3, 4])

    def mse(y_true, y_pred):
        return K.mean(K.pow((y_true - y_pred), 2))
    model.compile(optimizer, loss, metrics=[mse], sample_weight_mode=None)
    out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    out_len = (1 + (2 * (1 + 1)))
    assert (len(out) == out_len)
    out = model.test_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np])
    assert (len(out) == out_len)
    input_a_np = np.random.random((10, 3))
    input_b_np = np.random.random((10, 3))
    output_a_np = np.random.random((10, 4))
    output_b_np = np.random.random((10, 3))
    out = model.fit([input_a_np, input_b_np], [output_a_np, output_b_np], batch_size=4, epochs=1)
    out = model.evaluate([input_a_np, input_b_np], [output_a_np, output_b_np], batch_size=4)
    out = model.predict([input_a_np, input_b_np], batch_size=4)
    with pytest.raises(StopIteration):

        def gen_data():
            (yield (np.asarray([]), np.asarray([])))
        out = model.evaluate_generator(gen_data(), steps=1)
    with pytest.raises(ValueError):
        out = model.predict([None])
    with pytest.raises(ValueError):
        out = model.predict([input_a_np, None, input_b_np])
    with pytest.raises(ValueError):
        out = model.predict([None, input_a_np, input_b_np])
    with pytest.raises(ValueError):
        out = model.train_on_batch([input_a_np, input_b_np[:2]], [output_a_np, output_b_np], sample_weight=sample_weight)
    with pytest.raises(ValueError):
        out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np[:2]], sample_weight=sample_weight)
    with pytest.raises(ValueError):
        out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np], sample_weight=[sample_weight[1], sample_weight[1][:2]])
    with pytest.raises(TypeError):
        out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np], sample_weight=tuple(sample_weight))
    with pytest.raises(ValueError):
        out = model.fit([input_a_np, input_b_np], [output_a_np, output_b_np], epochs=1, batch_size=4, validation_data=([input_a_np, input_b_np],))
    with pytest.raises(ValueError):
        model.compile(optimizer, loss=['mse', 'mae', 'mape'])
    with pytest.raises(ValueError):
        model.compile(optimizer, loss='mse', loss_weights={
            'lstm': 0.5,
        })
    with pytest.raises(ValueError):
        model.compile(optimizer, loss='mse', loss_weights=[0.5])
    with pytest.raises(TypeError):
        model.compile(optimizer, loss='mse', loss_weights=(0.5, 0.5))
    with pytest.raises(ValueError):
        model.compile(optimizer, loss='mse', sample_weight_mode={
            'lstm': 'temporal',
        })
    with pytest.raises(ValueError):
        model.compile(optimizer, loss='mse', sample_weight_mode=['temporal'])
    with pytest.raises(ValueError):
        model.compile(optimizer, loss='mse', sample_weight_mode={
            'dense_1': 'temporal',
        })
    with pytest.raises(RuntimeError):
        model.compile(optimizer, loss=[])
    model.compile(optimizer, loss=['mse', 'mae'])
    model.compile(optimizer, loss='mse', loss_weights={
        'dense_1': 0.2,
        'dropout': 0.8,
    })
    model.compile(optimizer, loss='mse', loss_weights=[0.2, 0.8])
    with pytest.raises(ValueError):
        out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np], sample_weight=[None, np.random.random((10, 20, 30))])
    model.compile(optimizer, loss='mse', sample_weight_mode={
        'dense_1': None,
        'dropout': 'temporal',
    })
    model.compile(optimizer, loss='mse', sample_weight_mode=[None, 'temporal'])
    with pytest.raises(ValueError):
        out = model.train_on_batch([input_a_np, input_b_np], [output_a_np, output_b_np], sample_weight=sample_weight)
    model.compile(optimizer, loss, metrics=[], loss_weights=loss_weights, sample_weight_mode=None)
    trained_epochs = []
    out = model.fit_generator(generator=RandomSequence(3), steps_per_epoch=4, epochs=5, initial_epoch=0, validation_data=RandomSequence(4), validation_steps=3, callbacks=[tracker_cb])
    assert (trained_epochs == [0, 1, 2, 3, 4])
