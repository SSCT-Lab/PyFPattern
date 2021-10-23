def create_slot(primary, val, name, colocate_with_primary=True):
    'Create a slot initialized to the given value.\n\n  The type of the slot is determined by the given value.\n\n  Args:\n    primary: The primary `Variable` or `Tensor`.\n    val: A `Tensor` specifying the initial value of the slot.\n    name: Name to use for the slot variable.\n    colocate_with_primary: Boolean.  If True the slot is located\n      on the same device as `primary`.\n\n  Returns:\n    A `Variable` object.\n  '
    with ops.name_scope(((primary.op.name + '/') + name)) as scope:
        if colocate_with_primary:
            with ops.colocate_with(primary):
                return _create_slot_var(primary, val, scope)
        else:
            return _create_slot_var(primary, val, scope)