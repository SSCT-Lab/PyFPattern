def __call__(self, embeddings, labels):
    '\n        :param embeddings:\n            predicted embedding vectors             (batch size, max embedding dimensions, height, width)\n        :param labels:\n            instance segmentation ground truth\n            each unique value has to be denoting one instance             (batch size, height, width)\n        :return:\n        tuple of chainer.Variable:\n            Variance loss : Variance loss multiplied by alpha\n            Distance loss : Distance loss multiplied by beta\n            Regularization loss : Regularization loss multiplied by gamma\n        '
    assert (self.max_embedding_dim == embeddings.shape[1])
    l_dist = 0.0
    count = 0
    xp = cuda.get_array_module(embeddings)
    emb = embeddings[None, :]
    emb = broadcast_to(emb, (emb.shape[1], emb.shape[1], emb.shape[2], emb.shape[3], emb.shape[4]))
    ms = []
    for c in range(self.max_embedding_dim):
        mask = xp.expand_dims((labels == (c + 1)), 1)
        ms.append(mask)
    if hasattr(xp, 'stack'):
        ms = xp.stack(ms, 0)
    else:
        ms = xp.concatenate([xp.expand_dims(x, 0) for x in ms], 0)
    mns = c_sum((emb * ms), axis=(3, 4))
    mns = (mns / xp.maximum(xp.sum(ms, (2, 3, 4))[:, :, None], 1))
    mns_exp = mns[:, :, :, None, None]
    l_reg = c_sum(self.norm(mns, (1, 2)))
    l_reg = (l_reg / (self.max_embedding_dim * embeddings.shape[0]))
    l_var = self.norm(((mns_exp - emb) * ms), 2)
    l_var = (relu((l_var - self.delta_v)) ** 2)
    l_var = c_sum(l_var, (1, 2, 3))
    l_var = (l_var / xp.maximum(xp.sum(ms, (1, 2, 3, 4)), 1))
    l_var = (c_sum(l_var) / self.max_embedding_dim)
    for c_a in range(len(mns)):
        for c_b in range((c_a + 1), len(mns)):
            m_a = mns[c_a]
            m_b = mns[c_b]
            dist = self.norm((m_a - m_b), 1)
            l_dist += c_sum((relu(((2 * self.delta_d) - dist)) ** 2))
            count += 1
    l_dist /= max((count * embeddings.shape[0]), 1)
    rtn = ((self.alpha * l_var), (self.beta * l_dist), (self.gamma * l_reg))
    return rtn