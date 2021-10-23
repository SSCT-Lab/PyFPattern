def pipe(self, texts, as_tuples=False, n_threads=(- 1), batch_size=1000, disable=[], cleanup=False, component_cfg=None, n_process=1):
    'Process texts as a stream, and yield `Doc` objects in order.\n\n        texts (iterator): A sequence of texts to process.\n        as_tuples (bool): If set to True, inputs should be a sequence of\n            (text, context) tuples. Output will then be a sequence of\n            (doc, context) tuples. Defaults to False.\n        batch_size (int): The number of texts to buffer.\n        disable (list): Names of the pipeline components to disable.\n        cleanup (bool): If True, unneeded strings are freed to control memory\n            use. Experimental.\n        component_cfg (dict): An optional dictionary with extra keyword\n            arguments for specific components.\n        n_process (int): Number of processors to process texts, only supported\n            in Python3. If -1, set `multiprocessing.cpu_count()`.\n        YIELDS (Doc): Documents in the order of the original text.\n\n        DOCS: https://spacy.io/api/language#pipe\n        '
    (texts, raw_texts) = itertools.tee(texts)
    if (is_python2 and (n_process != 1)):
        user_warning(Warnings.W023)
        n_process = 1
    if (n_threads != (- 1)):
        deprecation_warning(Warnings.W016)
    if (n_process == (- 1)):
        n_process = mp.cpu_count()
    if as_tuples:
        (text_context1, text_context2) = itertools.tee(texts)
        texts = (tc[0] for tc in text_context1)
        contexts = (tc[1] for tc in text_context2)
        docs = self.pipe(texts, batch_size=batch_size, disable=disable, n_process=n_process, component_cfg=component_cfg)
        for (doc, context) in izip(docs, contexts):
            (yield (doc, context))
        return
    if (component_cfg is None):
        component_cfg = {
            
        }
    pipes = []
    for (name, proc) in self.pipeline:
        if (name in disable):
            continue
        kwargs = component_cfg.get(name, {
            
        })
        kwargs.setdefault('batch_size', batch_size)
        if hasattr(proc, 'pipe'):
            f = functools.partial(proc.pipe, **kwargs)
        else:
            f = functools.partial(_pipe, proc=proc, kwargs=kwargs)
        pipes.append(f)
    if (n_process != 1):
        docs = self._multiprocessing_pipe(texts, pipes, n_process, batch_size)
    else:
        docs = (self.make_doc(text) for text in texts)
        for pipe in pipes:
            docs = pipe(docs)
    recent_refs = weakref.WeakSet()
    old_refs = weakref.WeakSet()
    original_strings_data = None
    nr_seen = 0
    for doc in docs:
        (yield doc)
        if cleanup:
            recent_refs.add(doc)
            if (nr_seen < 10000):
                old_refs.add(doc)
                nr_seen += 1
            elif (len(old_refs) == 0):
                (old_refs, recent_refs) = (recent_refs, old_refs)
                if (original_strings_data is None):
                    original_strings_data = list(self.vocab.strings)
                else:
                    (keys, strings) = self.vocab.strings._cleanup_stale_strings(original_strings_data)
                    self.vocab._reset_cache(keys, strings)
                    self.tokenizer._reset_cache(keys)
                nr_seen = 0