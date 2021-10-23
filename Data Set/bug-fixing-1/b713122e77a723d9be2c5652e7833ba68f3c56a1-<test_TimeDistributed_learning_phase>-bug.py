

@keras_test
@pytest.mark.skipif((K.backend() == 'cntk'), reason='cntk does not support dropout yet')
def test_TimeDistributed_learning_phase():
    x = Input(shape=(3, 2))
    y = wrappers.TimeDistributed(core.Dropout(0.999))(x, training=True)
    model = Model(x, y)
    y = model.predict(np.random.random((10, 3, 2)))
    assert_allclose(0.0, y, atol=0.01)
