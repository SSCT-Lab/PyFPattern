@keras_test
def test_saving_without_compilation():
    'Test saving model without compiling.\n    '
    model = Sequential()
    model.add(Dense(2, input_shape=(3,)))
    model.add(Dense(3))
    (_, fname) = tempfile.mkstemp('.h5')
    save_model(model, fname)
    model = load_model(fname)
    os.remove(fname)