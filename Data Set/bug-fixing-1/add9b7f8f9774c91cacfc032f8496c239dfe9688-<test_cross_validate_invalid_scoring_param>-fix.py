

def test_cross_validate_invalid_scoring_param():
    (X, y) = make_classification(random_state=0)
    estimator = MockClassifier()
    error_message_regexp = '.*must be unique strings.*'
    assert_raises_regex(ValueError, error_message_regexp, cross_validate, estimator, X, y, scoring=(make_scorer(precision_score), make_scorer(accuracy_score)))
    assert_raises_regex(ValueError, error_message_regexp, cross_validate, estimator, X, y, scoring=(make_scorer(precision_score),))
    assert_raises_regex(ValueError, (error_message_regexp + 'Empty list.*'), cross_validate, estimator, X, y, scoring=())
    assert_raises_regex(ValueError, (error_message_regexp + 'Duplicate.*'), cross_validate, estimator, X, y, scoring=('f1_micro', 'f1_micro'))
    assert_raises_regex(ValueError, error_message_regexp, cross_validate, estimator, X, y, scoring=[[make_scorer(precision_score)]])
    error_message_regexp = '.*should either be.*string or callable.*for single.*.*dict.*for multi.*'
    assert_raises_regex(ValueError, 'An empty dict', cross_validate, estimator, X, y, scoring=dict())
    assert_raises_regex(ValueError, error_message_regexp, cross_validate, estimator, X, y, scoring=5)
    multiclass_scorer = make_scorer(precision_recall_fscore_support)
    assert_raises_regex(ValueError, "Classification metrics can't handle a mix of binary and continuous targets", cross_validate, estimator, X, y, scoring=multiclass_scorer)
    assert_raises_regex(ValueError, "Classification metrics can't handle a mix of binary and continuous targets", cross_validate, estimator, X, y, scoring={
        'foo': multiclass_scorer,
    })
    multivalued_scorer = make_scorer(confusion_matrix)
    assert_raises_regex(ValueError, 'scoring must return a number, got', cross_validate, SVC(), X, y, scoring=multivalued_scorer)
    assert_raises_regex(ValueError, 'scoring must return a number, got', cross_validate, SVC(), X, y, scoring={
        'foo': multivalued_scorer,
    })
    assert_raises_regex(ValueError, "'mse' is not a valid scoring value.", cross_validate, SVC(), X, y, scoring='mse')
