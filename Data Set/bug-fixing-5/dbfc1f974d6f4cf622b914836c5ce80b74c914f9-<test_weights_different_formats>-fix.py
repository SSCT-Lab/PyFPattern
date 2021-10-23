@nose.tools.nottest
@pytest.mark.parametrize('formatted', [weights, np.asarray(weights), pd.Series(weights)], ids=['list', 'ndarray', 'Series'])
def test_weights_different_formats(formatted):
    check_weights_as_formats(formatted)