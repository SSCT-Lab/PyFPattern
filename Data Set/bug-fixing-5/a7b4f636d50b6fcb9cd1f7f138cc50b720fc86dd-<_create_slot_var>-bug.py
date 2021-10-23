def _create_slot_var(primary, val, scope):
    'Helper function for creating a slot variable.'
    slot = variables.Variable(val, name=scope, trainable=False)
    if (isinstance(primary, variables.Variable) and primary._save_slice_info):
        real_slot_name = scope[len((primary.op.name + '/')):(- 1)]
        slice_info = primary._save_slice_info
        slot._set_save_slice_info(variables.Variable.SaveSliceInfo(((slice_info.full_name + '/') + real_slot_name), slice_info.full_shape[:], slice_info.var_offset[:], slice_info.var_shape[:]))
    return slot