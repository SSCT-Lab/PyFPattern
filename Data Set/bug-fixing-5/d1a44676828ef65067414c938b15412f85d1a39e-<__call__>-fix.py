def __call__(self, *input, **kwargs):
    result = self.forward(*input, **kwargs)
    for hook in self._forward_hooks.values():
        hook_result = hook(self, input, result)
        if (hook_result is not None):
            raise RuntimeError("forward hooks should never return any values, but '{}'didn't return None".format(hook))
    if (len(self._backward_hooks) > 0):
        var = result
        while (not isinstance(var, Variable)):
            var = var[0]
        grad_fn = var.grad_fn
        if (grad_fn is not None):
            for hook in self._backward_hooks.values():
                wrapper = functools.partial(hook, self)
                functools.update_wrapper(wrapper, hook)
                grad_fn.register_hook(wrapper)
    return result