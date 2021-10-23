def train(self, sentences, total_examples=None, total_words=None, epochs=None, start_alpha=None, end_alpha=None, word_count=0, queue_factor=2, report_delay=1.0):
    'Update the model\'s neural weights from a sequence of sentences (can be a once-only generator stream).\n        For FastText, each sentence must be a list of unicode strings. (Subclasses may accept other examples.)\n\n        To support linear learning-rate decay from (initial) alpha to min_alpha, and accurate\n        progress-percentage logging, either total_examples (count of sentences) or total_words (count of\n        raw words in sentences) **MUST** be provided (if the corpus is the same as was provided to\n        :meth:`~gensim.models.fasttext.FastText.build_vocab()`, the count of examples in that corpus\n        will be available in the model\'s :attr:`corpus_count` property).\n\n        To avoid common mistakes around the model\'s ability to do multiple training passes itself, an\n        explicit `epochs` argument **MUST** be provided. In the common and recommended case,\n        where :meth:`~gensim.models.fasttext.FastText.train()` is only called once,\n        the model\'s cached `iter` value should be supplied as `epochs` value.\n\n        Parameters\n        ----------\n        sentences : iterable of iterables\n            The `sentences` iterable can be simply a list of lists of tokens, but for larger corpora,\n            consider an iterable that streams the sentences directly from disk/network.\n            See :class:`~gensim.models.word2vec.BrownCorpus`, :class:`~gensim.models.word2vec.Text8Corpus`\n            or :class:`~gensim.models.word2vec.LineSentence` in :mod:`~gensim.models.word2vec` module for such examples.\n        total_examples : int\n            Count of sentences.\n        total_words : int\n            Count of raw words in sentences.\n        epochs : int\n            Number of iterations (epochs) over the corpus.\n        start_alpha : float\n            Initial learning rate.\n        end_alpha : float\n            Final learning rate. Drops linearly from `start_alpha`.\n        word_count : int\n            Count of words already trained. Set this to 0 for the usual\n            case of training on all words in sentences.\n        queue_factor : int\n            Multiplier for size of queue (number of workers * queue_factor).\n        report_delay : float\n            Seconds to wait before reporting progress.\n\n        Examples\n        --------\n        >>> from gensim.models import FastText\n        >>> sentences = [["cat", "say", "meow"], ["dog", "say", "woof"]]\n        >>>\n        >>> model = FastText(min_count=1)\n        >>> model.build_vocab(sentences)\n        >>> model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)\n\n        '
    self.neg_labels = []
    if (self.negative > 0):
        self.neg_labels = zeros((self.negative + 1))
        self.neg_labels[0] = 1.0
    Word2Vec.train(self, sentences, total_examples=self.corpus_count, epochs=self.iter, start_alpha=self.alpha, end_alpha=self.min_alpha)
    self.get_vocab_word_vecs()