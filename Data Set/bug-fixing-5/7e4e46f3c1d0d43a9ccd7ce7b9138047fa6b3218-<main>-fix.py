def main(model_dir=None):
    if (model_dir is not None):
        model_dir = pathlib.Path(model_dir)
        if (not model_dir.exists()):
            model_dir.mkdir()
        assert model_dir.is_dir()
    nlp = spacy.load('en', parser=False, entity=False, vectors=False)
    train_data = [('Who is Shaka Khan?', [(len('Who is '), len('Who is Shaka Khan'), 'PERSON')]), ('I like London and Berlin.', [(len('I like '), len('I like London'), 'LOC'), (len('I like London and '), len('I like London and Berlin'), 'LOC')])]
    ner = train_ner(nlp, train_data, ['PERSON', 'LOC'])
    doc = nlp.make_doc('Who is Shaka Khan?')
    nlp.tagger(doc)
    ner(doc)
    for word in doc:
        print(word.text, word.tag_, word.ent_type_, word.ent_iob)
    if (model_dir is not None):
        with (model_dir / 'config.json').open('w') as file_:
            json.dump(ner.cfg, file_)
        ner.model.dump(str((model_dir / 'model')))