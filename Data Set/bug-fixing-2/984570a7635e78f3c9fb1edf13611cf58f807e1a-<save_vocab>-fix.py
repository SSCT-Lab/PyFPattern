

def save_vocab(self):
    'Save the vocabulary to a file so the model can be reloaded.'
    opts = self._options
    with open(os.path.join(opts.save_path, 'vocab.txt'), 'w') as f:
        for i in xrange(opts.vocab_size):
            vocab_word = tf.compat.as_text(opts.vocab_words[i]).encode('utf-8')
            f.write(('%s %d\n' % (vocab_word, opts.vocab_counts[i])))
