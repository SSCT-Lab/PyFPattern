@plac.annotations(model=("Model name. Defaults to blank 'en' model.", 'option', 'm', str), output_dir=('Optional output directory', 'option', 'o', Path), n_texts=('Number of texts to train from', 'option', 't', int), n_iter=('Number of training iterations', 'option', 'n', int))
def main(model=None, output_dir=None, n_iter=20, n_texts=2000):
    if (model is not None):
        nlp = spacy.load(model)
        print(("Loaded model '%s'" % model))
    else:
        nlp = spacy.blank('en')
        print("Created blank 'en' model")
    if ('textcat' not in nlp.pipe_names):
        textcat = nlp.create_pipe('textcat')
        nlp.add_pipe(textcat, last=True)
    else:
        textcat = nlp.get_pipe('textcat')
    textcat.add_label('POSITIVE')
    print('Loading IMDB data...')
    ((train_texts, train_cats), (dev_texts, dev_cats)) = load_data(limit=n_texts)
    print('Using {} examples ({} training, {} evaluation)'.format(n_texts, len(train_texts), len(dev_texts)))
    train_data = list(zip(train_texts, [{
        'cats': cats,
    } for cats in train_cats]))
    other_pipes = [pipe for pipe in nlp.pipe_names if (pipe != 'textcat')]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        print('Training the model...')
        print('{:^5}\t{:^5}\t{:^5}\t{:^5}'.format('LOSS', 'P', 'R', 'F'))
        for i in range(n_iter):
            losses = {
                
            }
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                (texts, annotations) = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.2, losses=losses)
            with textcat.model.use_params(optimizer.averages):
                scores = evaluate(nlp.tokenizer, textcat, dev_texts, dev_cats)
            print('{0:.3f}\t{1:.3f}\t{2:.3f}\t{3:.3f}'.format(losses['textcat'], scores['textcat_p'], scores['textcat_r'], scores['textcat_f']))
    test_text = 'This movie sucked'
    doc = nlp(test_text)
    print(test_text, doc.cats)
    if (output_dir is not None):
        output_dir = Path(output_dir)
        if (not output_dir.exists()):
            output_dir.mkdir()
        with nlp.use_params(optimizer.averages):
            nlp.to_disk(output_dir)
        print('Saved model to', output_dir)
        print('Loading from', output_dir)
        nlp2 = spacy.load(output_dir)
        doc2 = nlp2(test_text)
        print(test_text, doc2.cats)