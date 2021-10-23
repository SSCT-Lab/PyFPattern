def fetch_var(name, scope=None, return_numpy=True):
    '\n    Fetch the value of the variable with the given name from the given scope\n    Args:\n        name(str): name of the variable. Typically, only persistable variables\n            can be found in the scope used for running the program.\n        scope(core.Scope|None): scope object. It should be the scope where\n            you pass to Executor.run() when running your program.\n            If None, global_scope() will be used.\n        return_numpy(bool): whether convert the tensor to numpy.ndarray\n    Returns:\n       LodTensor|numpy.ndarray\n    '
    assert isinstance(name, str)
    if (scope is None):
        scope = global_scope()
    assert isinstance(scope, core.Scope)
    var = global_scope().find_var(name)
    assert (var is not None), (('Cannot find ' + name) + ' in scope. Perhaps you need to make the variable persistable by using var.persistable = True in your program.')
    tensor = var.get_tensor()
    if return_numpy:
        tensor = as_numpy(tensor)
    return tensor