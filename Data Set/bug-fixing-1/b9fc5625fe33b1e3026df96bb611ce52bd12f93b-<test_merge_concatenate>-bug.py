

@keras_test
def test_merge_concatenate():
    i1 = layers.Input(shape=(4, 5))
    i2 = layers.Input(shape=(4, 5))
    o = layers.concatenate([i1, i2], axis=1)
    assert (o._keras_shape == (None, 8, 5))
    model = models.Model([i1, i2], o)
    concat_layer = layers.Concatenate(axis=1)
    o2 = concat_layer([i1, i2])
    assert (concat_layer.output_shape == (None, 8, 5))
    x1 = np.random.random((2, 4, 5))
    x2 = np.random.random((2, 4, 5))
    out = model.predict([x1, x2])
    assert (out.shape == (2, 8, 5))
    assert_allclose(out, np.concatenate([x1, x2], axis=1), atol=0.0001)
