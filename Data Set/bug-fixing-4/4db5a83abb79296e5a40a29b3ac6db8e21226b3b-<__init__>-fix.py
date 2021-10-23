def __init__(self, vocab_size, tag2idx, embedding_dim, hidden_dim):
    super(BiLSTM_CRF, self).__init__()
    with self.name_scope():
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        self.vocab_size = vocab_size
        self.tag2idx = tag2idx
        self.tagset_size = len(tag2idx)
        self.word_embeds = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = rnn.LSTM((hidden_dim // 2), num_layers=1, bidirectional=True)
        self.hidden2tag = nn.Dense(self.tagset_size)
        self.transitions = self.params.get('crf_transition_matrix', shape=(self.tagset_size, self.tagset_size))
        self.hidden = self.init_hidden()