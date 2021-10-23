

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
    x3 = np.random.random((1, 1, 1))
    nb_layers = 4
    x_i = layers.Input(shape=(None, None))
    x_list = [x_i]
    x = x_i
    for i in range(nb_layers):
        x_list.append(x)
        x = layers.concatenate(x_list, axis=1)
    concat_model = models.Model(x_i, x)
    concat_out = concat_model.predict([x3])
    x3 = np.repeat(x3, 16, axis=1)
    assert (concat_out.shape == (1, 16, 1))
    assert_allclose(concat_out, x3)
