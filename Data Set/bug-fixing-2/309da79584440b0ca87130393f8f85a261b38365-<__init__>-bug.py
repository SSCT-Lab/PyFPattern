

def __init__(self, fname, processes=None, lemmatize=utils.has_pattern(), dictionary=None, filter_namespaces=('0',), tokenizer_func=tokenize, article_min_tokens=ARTICLE_MIN_WORDS, token_min_len=TOKEN_MIN_LEN, token_max_len=TOKEN_MAX_LEN, lower=True):
    'Initialize the corpus.\n\n        Unless a dictionary is provided, this scans the corpus once,\n        to determine its vocabulary.\n\n        Parameters\n        ----------\n        fname : str\n            Path to file with wikipedia dump.\n        processes : int, optional\n            Number of processes to run, defaults to **number of cpu - 1**.\n        lemmatize : bool\n            Whether to use lemmatization instead of simple regexp tokenization.\n            Defaults to `True` if *pattern* package installed.\n        dictionary : :class:`~gensim.corpora.dictionary.Dictionary`, optional\n            Dictionary, if not provided,  this scans the corpus once, to determine its vocabulary\n            (this needs **really long time**).\n        filter_namespaces : tuple of str\n            Namespaces to consider.\n        tokenizer_func : function, optional\n            Function that will be used for tokenization. By default, use :func:`~gensim.corpora.wikicorpus.tokenize`.\n            Need to support interface:\n            tokenizer_func(text: str, token_min_len: int, token_max_len: int, lower: bool) -> list of str.\n        article_min_tokens : int, optional\n            Minimum tokens in article. Article will be ignored if number of tokens is less.\n        token_min_len : int, optional\n            Minimal token length.\n        token_max_len : int, optional\n            Maximal token length.\n        lower : bool, optional\n             If True - convert all text to lower case.\n\n        '
    self.fname = fname
    self.filter_namespaces = filter_namespaces
    self.metadata = False
    if (processes is None):
        processes = max(1, (multiprocessing.cpu_count() - 1))
    self.processes = processes
    self.lemmatize = lemmatize
    self.tokenizer_func = tokenizer_func
    self.article_min_tokens = article_min_tokens
    self.token_min_len = token_min_len
    self.token_max_len = token_max_len
    self.lower = lower
    self.dictionary = (dictionary or Dictionary(self.get_texts()))
