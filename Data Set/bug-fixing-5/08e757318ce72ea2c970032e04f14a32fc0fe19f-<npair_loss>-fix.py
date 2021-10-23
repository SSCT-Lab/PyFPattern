def npair_loss(anchor, positive, labels, l2_reg=0.002):
    "\n  **Npair Loss Layer**\n\n  Read `Improved Deep Metric Learning with Multi class N pair Loss Objective <http://www.nec-labs.com/uploads/images/Department-Images/MediaAnalytics/papers/nips16_npairmetriclearning.pdf>`_ .\n\n  Npair loss requires paired data. Npair loss has two parts: the first part is L2\n  regularizer on the embedding vector; the second part is cross entropy loss which\n  takes the similarity matrix of anchor and positive as logits.\n\n  Args:\n    anchor(Variable): embedding vector for the anchor image. shape=[batch_size, embedding_dims]\n    positive(Variable): embedding vector for the positive image. shape=[batch_size, embedding_dims]\n    labels(Variable): 1-D tensor. shape=[batch_size]\n    l2_reg(float32): L2 regularization term on embedding vector, default: 0.002\n\n  Returns:\n    npair loss(Variable): return npair loss, shape=[1]\n\n  Examples:\n    .. code-block:: python\n\n       anchor = fluid.layers.data(\n                     name = 'anchor', shape = [18, 6], dtype = 'float32', append_batch_size=False)\n       positive = fluid.layers.data(\n                     name = 'positive', shape = [18, 6], dtype = 'float32', append_batch_size=False)\n       labels = fluid.layers.data(\n                     name = 'labels', shape = [18], dtype = 'float32', append_batch_size=False)\n\n       npair_loss = fluid.layers.npair_loss(anchor, positive, labels, l2_reg = 0.002)\n  "
    Beta = 0.25
    batch_size = labels.shape[0]
    labels = reshape(labels, shape=[batch_size, 1], inplace=True)
    labels = expand(labels, expand_times=[1, batch_size])
    labels = equal(labels, transpose(labels, perm=[1, 0])).astype('float32')
    labels = (labels / reduce_sum(labels, dim=1, keep_dim=True))
    l2loss = (reduce_mean(reduce_sum(square(anchor), 1)) + reduce_mean(reduce_sum(square(positive), 1)))
    l2loss = ((l2loss * Beta) * l2_reg)
    similarity_matrix = matmul(anchor, positive, transpose_x=False, transpose_y=True)
    softmax_ce = softmax_with_cross_entropy(logits=similarity_matrix, label=labels, soft_label=True)
    cross_entropy = reduce_sum((labels * softmax_ce), 0)
    celoss = reduce_mean(cross_entropy)
    return (l2loss + celoss)