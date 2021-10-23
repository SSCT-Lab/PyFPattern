def test_classification_report_dictionary_output():
    iris = datasets.load_iris()
    (y_true, y_pred, _) = make_prediction(dataset=iris, binary=False)
    expected_report = {
        'setosa': {
            'precision': 0.8260869565217391,
            'recall': 0.7916666666666666,
            'f1-score': 0.8085106382978724,
            'support': 24,
        },
        'versicolor': {
            'precision': 0.3333333333333333,
            'recall': 0.0967741935483871,
            'f1-score': 0.15000000000000002,
            'support': 31,
        },
        'virginica': {
            'precision': 0.4186046511627907,
            'recall': 0.9,
            'f1-score': 0.5714285714285715,
            'support': 20,
        },
        'macro avg': {
            'f1-score': 0.5099797365754813,
            'precision': 0.5260083136726211,
            'recall': 0.596146953405018,
            'support': 75,
        },
        'micro avg': {
            'f1-score': 0.5333333333333333,
            'precision': 0.5333333333333333,
            'recall': 0.5333333333333333,
            'support': 75,
        },
        'weighted avg': {
            'f1-score': 0.47310435663627154,
            'precision': 0.5137535108414785,
            'recall': 0.5333333333333333,
            'support': 75,
        },
    }
    report = classification_report(y_true, y_pred, labels=np.arange(len(iris.target_names)), target_names=iris.target_names, output_dict=True)
    assert (report.keys() == expected_report.keys())
    for key in expected_report:
        assert (report[key].keys() == expected_report[key].keys())
        for metric in expected_report[key]:
            assert_almost_equal(expected_report[key][metric], report[key][metric])
    assert (type(expected_report['setosa']['precision']) == float)
    assert (type(expected_report['macro avg']['precision']) == float)
    assert (type(expected_report['setosa']['support']) == int)
    assert (type(expected_report['macro avg']['support']) == int)