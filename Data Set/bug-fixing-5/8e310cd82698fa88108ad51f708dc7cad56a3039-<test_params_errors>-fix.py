@pytest.mark.parametrize('args', [{
    'hidden_layer_sizes': (- 1),
}, {
    'max_iter': (- 1),
}, {
    'shuffle': 'true',
}, {
    'alpha': (- 1),
}, {
    'learning_rate_init': (- 1),
}, {
    'momentum': 2,
}, {
    'momentum': (- 0.5),
}, {
    'nesterovs_momentum': 'invalid',
}, {
    'early_stopping': 'invalid',
}, {
    'validation_fraction': 1,
}, {
    'validation_fraction': (- 0.5),
}, {
    'beta_1': 1,
}, {
    'beta_1': (- 0.5),
}, {
    'beta_2': 1,
}, {
    'beta_2': (- 0.5),
}, {
    'epsilon': (- 0.5),
}, {
    'n_iter_no_change': (- 1),
}, {
    'solver': 'hadoken',
}, {
    'learning_rate': 'converge',
}, {
    'activation': 'cloak',
}])
def test_params_errors(args):
    X = [[3, 2], [1, 6]]
    y = [1, 0]
    clf = MLPClassifier
    with pytest.raises(ValueError):
        clf(**args).fit(X, y)