def sequences_to_matrix(self, sequences, mode='binary'):
    'Converts a list of sequences into a Numpy matrix,\n        according to some vectorization mode.\n\n        # Arguments:\n            sequences: list of sequences\n                (a sequence is a list of integer word indices).\n            modes: one of "binary", "count", "tfidf", "freq"\n        '
    if (not self.nb_words):
        if self.word_index:
            nb_words = (len(self.word_index) + 1)
        else:
            raise Exception('Specify a dimension (nb_words argument), or fit on some text data first.')
    else:
        nb_words = self.nb_words
    if ((mode == 'tfidf') and (not self.document_count)):
        raise Exception('Fit the Tokenizer on some data before using tfidf mode.')
    X = np.zeros((len(sequences), nb_words))
    for (i, seq) in enumerate(sequences):
        if (not seq):
            continue
        counts = {
            
        }
        for j in seq:
            if (j >= nb_words):
                continue
            if (j not in counts):
                counts[j] = 1.0
            else:
                counts[j] += 1
        for (j, c) in list(counts.items()):
            if (mode == 'count'):
                X[i][j] = c
            elif (mode == 'freq'):
                X[i][j] = (c / len(seq))
            elif (mode == 'binary'):
                X[i][j] = 1
            elif (mode == 'tfidf'):
                tf = (1 + np.log(c))
                idf = np.log((1 + (self.document_count / (1 + self.index_docs.get(j, 0)))))
                X[i][j] = (tf * idf)
            else:
                raise Exception(('Unknown vectorization mode: ' + str(mode)))
    return X