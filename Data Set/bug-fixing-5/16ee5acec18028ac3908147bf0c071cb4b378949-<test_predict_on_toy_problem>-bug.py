def test_predict_on_toy_problem():
    'Manually check predicted class labels for toy dataset.'
    clf1 = LogisticRegression(random_state=123)
    clf2 = RandomForestClassifier(random_state=123)
    clf3 = GaussianNB()
    X = np.array([[(- 1.1), (- 1.5)], [(- 1.2), (- 1.4)], [(- 3.4), (- 2.2)], [1.1, 1.2], [2.1, 1.4], [3.1, 2.3]])
    y = np.array([1, 1, 1, 2, 2, 2])
    assert (all(clf1.fit(X, y).predict(X)) == all([1, 1, 1, 2, 2, 2]))
    assert (all(clf2.fit(X, y).predict(X)) == all([1, 1, 1, 2, 2, 2]))
    assert (all(clf3.fit(X, y).predict(X)) == all([1, 1, 1, 2, 2, 2]))
    eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='hard', weights=[1, 1, 1])
    assert (all(eclf.fit(X, y).predict(X)) == all([1, 1, 1, 2, 2, 2]))
    eclf = VotingClassifier(estimators=[('lr', clf1), ('rf', clf2), ('gnb', clf3)], voting='soft', weights=[1, 1, 1])
    assert (all(eclf.fit(X, y).predict(X)) == all([1, 1, 1, 2, 2, 2]))