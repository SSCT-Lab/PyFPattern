def debug_data(lang: ('Model language', 'positional', None, str), train_path: ('Location of JSON-formatted training data', 'positional', None, Path), dev_path: ('Location of JSON-formatted development data', 'positional', None, Path), tag_map_path: ('Location of JSON-formatted tag map', 'option', 'tm', Path)=None, base_model: ('Name of model to update (optional)', 'option', 'b', str)=None, pipeline: ('Comma-separated names of pipeline components to train', 'option', 'p', str)='tagger,parser,ner', ignore_warnings: ('Ignore warnings, only show stats and errors', 'flag', 'IW', bool)=False, verbose: ('Print additional information and explanations', 'flag', 'V', bool)=False, no_format: ("Don't pretty-print the results", 'flag', 'NF', bool)=False):
    '\n    Analyze, debug and validate your training and development data, get useful\n    stats, and find problems like invalid entity annotations, cyclic\n    dependencies, low data labels and more.\n    '
    msg = Printer(pretty=(not no_format), ignore_warnings=ignore_warnings)
    if (not train_path.exists()):
        msg.fail('Training data not found', train_path, exits=1)
    if (not dev_path.exists()):
        msg.fail('Development data not found', dev_path, exits=1)
    tag_map = {
        
    }
    if (tag_map_path is not None):
        tag_map = srsly.read_json(tag_map_path)
    pipeline = [p.strip() for p in pipeline.split(',')]
    if base_model:
        nlp = load_model(base_model)
    else:
        lang_cls = get_lang_class(lang)
        nlp = lang_cls()
    nlp.vocab.morphology.tag_map.update(tag_map)
    msg.divider('Data format validation')
    loading_train_error_message = ''
    loading_dev_error_message = ''
    with msg.loading('Loading corpus...'):
        corpus = GoldCorpus(train_path, dev_path)
        try:
            train_dataset = list(corpus.train_dataset(nlp))
            train_dataset_unpreprocessed = list(corpus.train_dataset_without_preprocessing(nlp))
        except ValueError as e:
            loading_train_error_message = f'Training data cannot be loaded: {e}'
        try:
            dev_dataset = list(corpus.dev_dataset(nlp))
        except ValueError as e:
            loading_dev_error_message = f'Development data cannot be loaded: {e}'
    if (loading_train_error_message or loading_dev_error_message):
        if loading_train_error_message:
            msg.fail(loading_train_error_message)
        if loading_dev_error_message:
            msg.fail(loading_dev_error_message)
        sys.exit(1)
    msg.good('Corpus is loadable')
    gold_train_data = _compile_gold(train_dataset, pipeline)
    gold_train_unpreprocessed_data = _compile_gold(train_dataset_unpreprocessed, pipeline)
    gold_dev_data = _compile_gold(dev_dataset, pipeline)
    train_texts = gold_train_data['texts']
    dev_texts = gold_dev_data['texts']
    msg.divider('Training stats')
    msg.text(f"Training pipeline: {', '.join(pipeline)}")
    for pipe in [p for p in pipeline if (p not in nlp.factories)]:
        msg.fail(f"Pipeline component '{pipe}' not available in factories")
    if base_model:
        msg.text(f"Starting with base model '{base_model}'")
    else:
        msg.text(f"Starting with blank model '{lang}'")
    msg.text(f'{len(train_dataset)} training docs')
    msg.text(f'{len(gold_dev_data)} evaluation docs')
    if (not len(gold_dev_data)):
        msg.fail('No evaluation docs')
    overlap = len(train_texts.intersection(dev_texts))
    if overlap:
        msg.warn(f'{overlap} training examples also in evaluation data')
    else:
        msg.good('No overlap between training and evaluation data')
    if ((not base_model) and (len(train_dataset) < BLANK_MODEL_THRESHOLD)):
        text = f'Low number of examples to train from a blank model ({len(train_dataset)})'
        if (len(train_dataset) < BLANK_MODEL_MIN_THRESHOLD):
            msg.fail(text)
        else:
            msg.warn(text)
        msg.text(f"It's recommended to use at least {BLANK_MODEL_THRESHOLD} examples (minimum {BLANK_MODEL_MIN_THRESHOLD})", show=verbose)
    msg.divider('Vocab & Vectors')
    n_words = gold_train_data['n_words']
    msg.info(f"{n_words} total word(s) in the data ({len(gold_train_data['words'])} unique)")
    if (gold_train_data['n_misaligned_words'] > 0):
        n_misaligned = gold_train_data['n_misaligned_words']
        msg.warn(f'{n_misaligned} misaligned tokens in the training data')
    if (gold_dev_data['n_misaligned_words'] > 0):
        n_misaligned = gold_dev_data['n_misaligned_words']
        msg.warn(f'{n_misaligned} misaligned tokens in the dev data')
    most_common_words = gold_train_data['words'].most_common(10)
    msg.text(f'10 most common words: {_format_labels(most_common_words, counts=True)}', show=verbose)
    if len(nlp.vocab.vectors):
        msg.info(f'{len(nlp.vocab.vectors)} vectors ({nlp.vocab.vectors.n_keys} unique keys, {nlp.vocab.vectors_length} dimensions)')
    else:
        msg.info('No word vectors present in the model')
    if ('ner' in pipeline):
        labels = set((label for label in gold_train_data['ner'] if (label not in ('O', '-', None))))
        label_counts = gold_train_data['ner']
        model_labels = _get_labels_from_model(nlp, 'ner')
        new_labels = [l for l in labels if (l not in model_labels)]
        existing_labels = [l for l in labels if (l in model_labels)]
        has_low_data_warning = False
        has_no_neg_warning = False
        has_ws_ents_error = False
        msg.divider('Named Entity Recognition')
        msg.info(f'{len(new_labels)} new label(s), {len(existing_labels)} existing label(s)')
        missing_values = label_counts['-']
        msg.text(f"{missing_values} missing value(s) (tokens with '-' label)")
        for label in new_labels:
            if (len(label) == 0):
                msg.fail('Empty label found in new labels')
        if new_labels:
            labels_with_counts = [(label, count) for (label, count) in label_counts.most_common() if (label != '-')]
            labels_with_counts = _format_labels(labels_with_counts, counts=True)
            msg.text(f'New: {labels_with_counts}', show=verbose)
        if existing_labels:
            msg.text(f'Existing: {_format_labels(existing_labels)}', show=verbose)
        if gold_train_data['ws_ents']:
            msg.fail(f"{gold_train_data['ws_ents']} invalid whitespace entity spans")
            has_ws_ents_error = True
        for label in new_labels:
            if (label_counts[label] <= NEW_LABEL_THRESHOLD):
                msg.warn(f"Low number of examples for new label '{label}' ({label_counts[label]})")
                has_low_data_warning = True
                with msg.loading('Analyzing label distribution...'):
                    neg_docs = _get_examples_without_label(train_dataset, label)
                if (neg_docs == 0):
                    msg.warn(f"No examples for texts WITHOUT new label '{label}'")
                    has_no_neg_warning = True
        if (not has_low_data_warning):
            msg.good('Good amount of examples for all labels')
        if (not has_no_neg_warning):
            msg.good('Examples without occurrences available for all labels')
        if (not has_ws_ents_error):
            msg.good('No entities consisting of or starting/ending with whitespace')
        if has_low_data_warning:
            msg.text(f'To train a new entity type, your data should include at least {NEW_LABEL_THRESHOLD} instances of the new label', show=verbose)
        if has_no_neg_warning:
            msg.text('Training data should always include examples of entities in context, as well as examples without a given entity type.', show=verbose)
        if has_ws_ents_error:
            msg.text('As of spaCy v2.1.0, entity spans consisting of or starting/ending with whitespace characters are considered invalid.')
    if ('textcat' in pipeline):
        msg.divider('Text Classification')
        labels = [label for label in gold_train_data['cats']]
        model_labels = _get_labels_from_model(nlp, 'textcat')
        new_labels = [l for l in labels if (l not in model_labels)]
        existing_labels = [l for l in labels if (l in model_labels)]
        msg.info(f'Text Classification: {len(new_labels)} new label(s), {len(existing_labels)} existing label(s)')
        if new_labels:
            labels_with_counts = _format_labels(gold_train_data['cats'].most_common(), counts=True)
            msg.text(f'New: {labels_with_counts}', show=verbose)
        if existing_labels:
            msg.text(f'Existing: {_format_labels(existing_labels)}', show=verbose)
        if (set(gold_train_data['cats']) != set(gold_dev_data['cats'])):
            msg.fail(f"The train and dev labels are not the same. Train labels: {_format_labels(gold_train_data['cats'])}. Dev labels: {_format_labels(gold_dev_data['cats'])}.")
        if (gold_train_data['n_cats_multilabel'] > 0):
            msg.info("The train data contains instances without mutually-exclusive classes. Use '--textcat-multilabel' when training.")
            if (gold_dev_data['n_cats_multilabel'] == 0):
                msg.warn('Potential train/dev mismatch: the train data contains instances without mutually-exclusive classes while the dev data does not.')
        else:
            msg.info('The train data contains only instances with mutually-exclusive classes.')
            if (gold_dev_data['n_cats_multilabel'] > 0):
                msg.fail('Train/dev mismatch: the dev data contains instances without mutually-exclusive classes while the train data contains only instances with mutually-exclusive classes.')
    if ('tagger' in pipeline):
        msg.divider('Part-of-speech Tagging')
        labels = [label for label in gold_train_data['tags']]
        tag_map = nlp.vocab.morphology.tag_map
        msg.info(f'{len(labels)} label(s) in data ({len(tag_map)} label(s) in tag map)')
        labels_with_counts = _format_labels(gold_train_data['tags'].most_common(), counts=True)
        msg.text(labels_with_counts, show=verbose)
        non_tagmap = [l for l in labels if (l not in tag_map)]
        if (not non_tagmap):
            msg.good(f"All labels present in tag map for language '{nlp.lang}'")
        for label in non_tagmap:
            msg.fail(f"Label '{label}' not found in tag map for language '{nlp.lang}'")
    if ('parser' in pipeline):
        has_low_data_warning = False
        msg.divider('Dependency Parsing')
        msg.info(f"Found {gold_train_data['n_sents']} sentence(s) with an average length of {(gold_train_data['n_words'] / gold_train_data['n_sents']):.1f} words.")
        sents_per_doc = (gold_train_data['n_sents'] / len(gold_train_data['texts']))
        if (sents_per_doc < 1.1):
            msg.warn(f'The training data contains {sents_per_doc:.2f} sentences per document. When there are very few documents containing more than one sentence, the parser will not learn how to segment longer texts into sentences.')
        labels_train = [label for label in gold_train_data['deps']]
        labels_train_unpreprocessed = [label for label in gold_train_unpreprocessed_data['deps']]
        labels_dev = [label for label in gold_dev_data['deps']]
        if (gold_train_unpreprocessed_data['n_nonproj'] > 0):
            n_nonproj = gold_train_unpreprocessed_data['n_nonproj']
            msg.info(f'Found {n_nonproj} nonprojective train sentence(s)')
        if (gold_dev_data['n_nonproj'] > 0):
            n_nonproj = gold_dev_data['n_nonproj']
            msg.info(f'Found {n_nonproj} nonprojective dev sentence(s)')
        msg.info(f'{labels_train_unpreprocessed} label(s) in train data')
        msg.info(f'{len(labels_train)} label(s) in projectivized train data')
        labels_with_counts = _format_labels(gold_train_unpreprocessed_data['deps'].most_common(), counts=True)
        msg.text(labels_with_counts, show=verbose)
        for label in gold_train_unpreprocessed_data['deps']:
            if (gold_train_unpreprocessed_data['deps'][label] <= DEP_LABEL_THRESHOLD):
                msg.warn(f"Low number of examples for label '{label}' ({gold_train_unpreprocessed_data['deps'][label]})")
                has_low_data_warning = True
        rare_projectivized_labels = []
        for label in gold_train_data['deps']:
            if ((gold_train_data['deps'][label] <= DEP_LABEL_THRESHOLD) and ('||' in label)):
                rare_projectivized_labels.append(f"{label}: {gold_train_data['deps'][label]}")
        if (len(rare_projectivized_labels) > 0):
            msg.warn(f'Low number of examples for {len(rare_projectivized_labels)} label(s) in the projectivized dependency trees used for training. You may want to projectivize labels such as punct before training in order to improve parser performance.')
            msg.warn(f'Projectivized labels with low numbers of examples: ', ', '.join(rare_projectivized_labels), show=verbose)
            has_low_data_warning = True
        if (set(labels_train) - set(labels_dev)):
            msg.warn('The following labels were found only in the train data:', ', '.join((set(labels_train) - set(labels_dev))), show=verbose)
        if (set(labels_dev) - set(labels_train)):
            msg.warn('The following labels were found only in the dev data:', ', '.join((set(labels_dev) - set(labels_train))), show=verbose)
        if has_low_data_warning:
            msg.text(f'To train a parser, your data should include at least {DEP_LABEL_THRESHOLD} instances of each label.', show=verbose)
        if (len(gold_train_unpreprocessed_data['roots']) > 1):
            msg.warn(f"Multiple root labels ({', '.join(gold_train_unpreprocessed_data['roots'])}) found in training data. spaCy's parser uses a single root label ROOT so this distinction will not be available.")
        if (gold_train_data['n_nonproj'] > 0):
            msg.fail(f"Found {gold_train_data['n_nonproj']} nonprojective projectivized train sentence(s)")
        if (gold_train_data['n_cycles'] > 0):
            msg.fail(f"Found {gold_train_data['n_cycles']} projectivized train sentence(s) with cycles")
    msg.divider('Summary')
    good_counts = msg.counts[MESSAGES.GOOD]
    warn_counts = msg.counts[MESSAGES.WARN]
    fail_counts = msg.counts[MESSAGES.FAIL]
    if good_counts:
        msg.good(f"{good_counts} {('check' if (good_counts == 1) else 'checks')} passed")
    if warn_counts:
        msg.warn(f"{warn_counts} {('warning' if (warn_counts == 1) else 'warnings')}")
    if fail_counts:
        msg.fail(f"{fail_counts} {('error' if (fail_counts == 1) else 'errors')}")
        sys.exit(1)