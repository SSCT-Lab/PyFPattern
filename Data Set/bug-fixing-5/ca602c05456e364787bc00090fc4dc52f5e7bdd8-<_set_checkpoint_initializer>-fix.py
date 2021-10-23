def _set_checkpoint_initializer(variable, file_pattern, tensor_name, slice_spec, name='checkpoint_initializer'):
    "Sets variable initializer to assign op form value in checkpoint's tensor.\n\n  Args:\n    variable: `Variable` object.\n    file_pattern: string, where to load checkpoints from.\n    tensor_name: Name of the `Tensor` to load from checkpoint reader.\n    slice_spec: Slice specification for loading partitioned variables.\n    name: Name of the operation.\n  "
    base_type = variable.dtype.base_dtype
    with ops.device(variable.device), ops.device('/cpu:0'):
        restore_op = io_ops.restore_v2(file_pattern, [tensor_name], [slice_spec], [base_type], name=name)[0]
        variable._initializer_op = state_ops.assign(variable, restore_op)