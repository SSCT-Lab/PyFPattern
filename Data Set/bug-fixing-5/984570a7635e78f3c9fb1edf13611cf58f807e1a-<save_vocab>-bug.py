def save_vocab(self):
    'Save the vocabulary to a file so the model can be reloaded.'
    opts = self._options
    with open(os.path.join(opts.save_path, 'vocab.txt'), 'w') as f:
        for i in xrange(opts.vocab_size):
            f.write(('%s %d\n' % (tf.compat.as_text(opts.vocab_words[i]), opts.vocab_counts[i])))