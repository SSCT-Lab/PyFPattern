def _make_on_batch_function(model, mode):
    'Creates a function of Model.*_on_batch methods.'
    if (mode == ModeKeys.TRAIN):
        func = training_eager.train_on_batch
    elif (mode == ModeKeys.TEST):
        func = training_eager.test_on_batch
    else:
        func = model
    if (not model.run_eagerly):
        func = def_function.function(func)
    return func