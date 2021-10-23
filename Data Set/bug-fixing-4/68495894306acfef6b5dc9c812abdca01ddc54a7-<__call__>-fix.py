def __call__(self, inputs):
    assert (type(inputs) in {list, tuple})
    feed_dict = {
        
    }
    for (tensor, value) in zip(self.inputs, inputs):
        if is_sparse(tensor):
            sparse_coo = value.tocoo()
            indices = np.concatenate((np.expand_dims(sparse_coo.row, 1), np.expand_dims(sparse_coo.col, 1)), 1)
            value = (indices, sparse_coo.data, sparse_coo.shape)
        feed_dict[tensor] = value
    session = get_session()
    updated = session.run((self.outputs + [self.updates_op]), feed_dict=feed_dict)
    return updated[:len(self.outputs)]