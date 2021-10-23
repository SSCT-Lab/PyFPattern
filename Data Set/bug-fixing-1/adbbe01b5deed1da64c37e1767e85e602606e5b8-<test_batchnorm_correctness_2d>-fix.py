

@keras_test
def test_batchnorm_correctness_2d():
    model = Sequential()
    norm = normalization.BatchNormalization(axis=1, input_shape=(10, 6), momentum=0.8)
    model.add(norm)
    model.compile(loss='mse', optimizer='sgd')
    x = np.random.normal(loc=5.0, scale=10.0, size=(1000, 10, 6))
    model.fit(x, x, epochs=4, verbose=0)
    out = model.predict(x)
    out -= np.reshape(K.eval(norm.beta), (1, 10, 1))
    out /= np.reshape(K.eval(norm.gamma), (1, 10, 1))
    assert_allclose(out.mean(axis=(0, 2)), 0.0, atol=0.11)
    assert_allclose(out.std(axis=(0, 2)), 1.0, atol=0.11)
