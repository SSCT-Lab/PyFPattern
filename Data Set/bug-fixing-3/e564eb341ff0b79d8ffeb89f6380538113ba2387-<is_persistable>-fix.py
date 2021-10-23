def is_persistable(var):
    "\n    Check whether the given variable is persistable.\n\n    Args:\n        var(Variable): The variable to be checked.\n\n    Returns:\n        bool: True if the given `var` is persistable\n        False if not.\n\n    Examples:\n        .. code-block:: python\n\n            param = fluid.default_main_program().global_block().var('fc.b')\n            res = fluid.io.is_persistable(param)\n    "
    if ((var.desc.type() == core.VarDesc.VarType.FEED_MINIBATCH) or (var.desc.type() == core.VarDesc.VarType.FETCH_LIST) or (var.desc.type() == core.VarDesc.VarType.READER)):
        return False
    return var.persistable