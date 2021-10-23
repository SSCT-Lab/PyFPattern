@plac.annotations(model=('Model name or path', 'positional', None, str), data_path=('Location of JSON-formatted evaluation data', 'positional', None, str), gold_preproc=('Use gold preprocessing', 'flag', 'G', bool), gpu_id=('Use GPU', 'option', 'g', int), displacy_path=('Directory to output rendered parses as HTML', 'option', 'dp', str), displacy_limit=('Limit of parses to render as HTML', 'option', 'dl', int))
def evaluate(model, data_path, gpu_id=(- 1), gold_preproc=False, displacy_path=None, displacy_limit=25):
    '\n    Evaluate a model. To render a sample of parses in a HTML file, set an\n    output directory as the displacy_path argument.\n    '
    msg = Printer()
    util.fix_random_seed()
    if (gpu_id >= 0):
        util.use_gpu(gpu_id)
    util.set_env_log(False)
    data_path = util.ensure_path(data_path)
    displacy_path = util.ensure_path(displacy_path)
    if (not data_path.exists()):
        msg.fail('Evaluation data not found', data_path, exits=1)
    if (displacy_path and (not displacy_path.exists())):
        msg.fail('Visualization output directory not found', displacy_path, exits=1)
    corpus = GoldCorpus(data_path, data_path)
    nlp = util.load_model(model)
    dev_docs = list(corpus.dev_docs(nlp, gold_preproc=gold_preproc))
    begin = timer()
    scorer = nlp.evaluate(dev_docs, verbose=False)
    end = timer()
    nwords = sum((len(doc_gold[0]) for doc_gold in dev_docs))
    results = {
        'Time': ('%.2f s' % (end - begin)),
        'Words': nwords,
        'Words/s': ('%.0f' % (nwords / (end - begin))),
        'TOK': ('%.2f' % scorer.token_acc),
        'POS': ('%.2f' % scorer.tags_acc),
        'UAS': ('%.2f' % scorer.uas),
        'LAS': ('%.2f' % scorer.las),
        'NER P': ('%.2f' % scorer.ents_p),
        'NER R': ('%.2f' % scorer.ents_r),
        'NER F': ('%.2f' % scorer.ents_f),
    }
    msg.table(results, title='Results')
    if displacy_path:
        (docs, golds) = zip(*dev_docs)
        render_deps = ('parser' in nlp.meta.get('pipeline', []))
        render_ents = ('ner' in nlp.meta.get('pipeline', []))
        render_parses(docs, displacy_path, model_name=model, limit=displacy_limit, deps=render_deps, ents=render_ents)
        msg.good('Generated {} parses as HTML'.format(displacy_limit), displacy_path)