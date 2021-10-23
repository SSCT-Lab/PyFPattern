def main(unused_argv):
    global n_words
    dbpedia = learn.datasets.load_dataset('dbpedia', test_with_fake_data=FLAGS.test_with_fake_data)
    x_train = pandas.DataFrame(dbpedia.train.data)[1]
    y_train = pandas.Series(dbpedia.train.target)
    x_test = pandas.DataFrame(dbpedia.test.data)[1]
    y_test = pandas.Series(dbpedia.test.target)
    vocab_processor = learn.preprocessing.VocabularyProcessor(MAX_DOCUMENT_LENGTH)
    x_train = np.array(list(vocab_processor.fit_transform(x_train)))
    x_test = np.array(list(vocab_processor.transform(x_test)))
    n_words = len(vocab_processor.vocabulary_)
    print(('Total words: %d' % n_words))
    classifier = learn.Estimator(model_fn=cnn_model)
    classifier.fit(x_train, y_train, steps=100)
    y_predicted = [p['class'] for p in classifier.predict(x_test, as_iterable=True)]
    score = metrics.accuracy_score(y_test, y_predicted)
    print('Accuracy: {0:f}'.format(score))