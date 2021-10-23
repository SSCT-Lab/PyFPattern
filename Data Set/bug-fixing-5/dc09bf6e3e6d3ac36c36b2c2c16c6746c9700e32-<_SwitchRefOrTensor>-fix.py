def _SwitchRefOrTensor(data, pred, name='Switch'):
    'Forwards `data` to an output determined by `pred`.\n\n  If `pred` is false, the `data` input is forwared to the first output.\n  Otherwise, the data goes to the second output.\n\n  This op handles `Tensor`s and `IndexedSlices`.\n\n  Args:\n    data: The tensor to be forwarded to the appropriate output.\n    pred: A scalar that specifies which output port will receive data.\n    name: A name for this operation (optional).\n\n  Returns:\n    `(output_false, output_false)`: If `pred` is true, data will be forwarded to\n    `output_true`, otherwise it goes to `output_false`.\n\n  Raises:\n    TypeError: if data is not a Tensor or IndexedSlices\n  '
    data = ops.convert_to_tensor_or_indexed_slices(data, name='data')
    with ops.colocate_with(data, ignore_existing=True):
        if isinstance(data, ops.Tensor):
            if data.dtype._is_ref_dtype:
                return ref_switch(data, pred, name=name)
        return switch(data, pred, name=name)