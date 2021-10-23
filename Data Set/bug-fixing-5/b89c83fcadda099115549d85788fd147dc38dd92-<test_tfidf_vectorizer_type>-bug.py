@pytest.mark.parametrize('vectorizer_dtype, output_dtype, expected_warning, msg_warning', [(np.int32, np.float64, UserWarning, "'dtype' should be used."), (np.int64, np.float64, UserWarning, "'dtype' should be used."), (np.float32, np.float32, None, None), (np.float64, np.float64, None, None)])
def test_tfidf_vectorizer_type(vectorizer_dtype, output_dtype, expected_warning, msg_warning):
    X = np.array(['numpy', 'scipy', 'sklearn'])
    vectorizer = TfidfVectorizer(dtype=vectorizer_dtype)
    with pytest.warns(expected_warning, match=msg_warning) as record:
        X_idf = vectorizer.fit_transform(X)
    if (expected_warning is None):
        assert (len(record) == 0)
    assert (X_idf.dtype == output_dtype)