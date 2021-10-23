def switch(data, pred, dtype=None, name=None):
    'Forwards `data` to an output determined by `pred`.\n\n  If `pred` is true, the `data` input is forwared to the first output.\n  Otherwise, the data goes to the second output.\n\n  This op handles `Tensor`s and `IndexedSlices`.\n\n  Args:\n    data: The tensor to be forwarded to the appropriate output.\n    pred: A scalar that specifies which output port will receive data.\n    dtype: Optional element type for the returned tensor. If missing,\n           the type is inferred from the type of `value`.\n    name: A name for this operation (optional).\n\n  Returns:\n    `(output_false, output_true)`: If `pred` is true, data will be forwarded\n    to `output_true`, otherwise it goes to `output_false`.\n  '
    with ops.name_scope(name, 'Switch', [data, pred]) as name:
        data = ops.internal_convert_to_tensor_or_indexed_slices(data, dtype=dtype, name='data', as_ref=True)
        pred = ops.convert_to_tensor(pred, name='pred')
        if isinstance(data, ops.Tensor):
            return gen_control_flow_ops._switch(data, pred, name=name)
        else:
            if (not isinstance(data, (ops.IndexedSlices, sparse_tensor.SparseTensor))):
                raise TypeError(('Type %s not supported' % type(data)))
            (val, ind) = (data.values, data.indices)
            (val_f, val_t) = gen_control_flow_ops._switch(val, pred, name=name)
            (ind_f, ind_t) = gen_control_flow_ops._switch(ind, pred, name='indices')
            if isinstance(data, ops.IndexedSlices):
                dense_shape = data.dense_shape
                if (dense_shape is not None):
                    (dense_shape_f, dense_shape_t) = gen_control_flow_ops._switch(dense_shape, pred, name='dense_shape')
                else:
                    (dense_shape_f, dense_shape_t) = (None, None)
                return (ops.IndexedSlices(val_f, ind_f, dense_shape_f), ops.IndexedSlices(val_t, ind_t, dense_shape_t))
            else:
                dense_shape = data.dense_shape
                (dense_shape_f, dense_shape_t) = gen_control_flow_ops._switch(data.dense_shape, pred, name='dense_shape')
                return (sparse_tensor.SparseTensor(ind_f, val_f, dense_shape_f), sparse_tensor.SparseTensor(ind_t, val_t, dense_shape_t))