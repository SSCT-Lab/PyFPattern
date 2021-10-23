@pytest.mark.parametrize('vectorizer_dtype, output_dtype, warning_expected', [(np.int32, np.float64, True), (np.int64, np.float64, True), (np.float32, np.float32, False), (np.float64, np.float64, False)])
def test_tfidf_vectorizer_type(vectorizer_dtype, output_dtype, warning_expected):
    X = np.array(['numpy', 'scipy', 'sklearn'])
    vectorizer = TfidfVectorizer(dtype=vectorizer_dtype)
    warning_msg_match = "'dtype' should be used."
    warning_cls = UserWarning
    expected_warning_cls = (warning_cls if warning_expected else None)
    with pytest.warns(expected_warning_cls, match=warning_msg_match) as record:
        X_idf = vectorizer.fit_transform(X)
    if (expected_warning_cls is None):
        relevant_warnings = [w for w in record if isinstance(w, warning_cls)]
        assert (len(relevant_warnings) == 0)
    assert (X_idf.dtype == output_dtype)