

def embed_sequence(ids, vocab_size=None, embed_dim=None, unique=False, initializer=None, regularizer=None, trainable=True, scope=None, reuse=None):
    'Maps a sequence of symbols to a sequence of embeddings.\n\n  Typical use case would be reusing embeddings between an encoder and decoder.\n\n  Args:\n    ids: `[batch_size, doc_length]` `Tensor` of type `int32` or `int64`\n      with symbol ids.\n    vocab_size: Integer number of symbols in vocabulary.\n    embed_dim: Integer number of dimensions for embedding matrix.\n    unique: If `True`, will first compute the unique set of indices, and then\n         lookup each embedding once, repeating them in the output as needed.\n    initializer: An initializer for the embeddings, if `None` default for\n        current scope is used.\n    regularizer: Optional regularizer for the embeddings.\n    trainable: If `True` also add variables to the graph collection\n      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).\n    scope: Optional string specifying the variable scope for the op, required\n        if `reuse=True`.\n    reuse: If `True`, variables inside the op will be reused.\n\n  Returns:\n    `Tensor` of `[batch_size, doc_length, embed_dim]` with embedded sequences.\n\n  Raises:\n    ValueError: if `embed_dim` or `vocab_size` are not specified when \n      `reuse` is `None` or `False`.\n  '
    if (not (reuse or (vocab_size and embed_dim))):
        raise ValueError(('Must specify vocab size and embedding dimension when notreusing. Got vocab_size=%s and embed_dim=%s' % (vocab_size, embed_dim)))
    with variable_scope.variable_scope(scope, 'EmbedSequence', [ids], reuse=reuse):
        shape = [vocab_size, embed_dim]
        if ((reuse and (vocab_size is None)) or (embed_dim is None)):
            shape = None
        embeddings = variables.model_variable('embeddings', shape=shape, initializer=initializer, regularizer=regularizer, trainable=trainable)
        if unique:
            return contrib_embedding_ops.embedding_lookup_unique(embeddings, ids)
        return embedding_ops.embedding_lookup(embeddings, ids)
