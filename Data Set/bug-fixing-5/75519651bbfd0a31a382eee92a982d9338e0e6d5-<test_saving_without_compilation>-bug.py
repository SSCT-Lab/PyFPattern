@keras_test
def test_saving_without_compilation():
    model = Sequential()
    model.add(Dense(2, input_shape=(3,)))
    model.add(Dense(3))
    model.compile(loss='mse', optimizer='sgd', metrics=['acc'])
    (_, fname) = tempfile.mkstemp('.h5')
    save_model(model, fname)
    model = load_model(fname)
    os.remove(fname)