

def gradient(self, target, sources, output_gradients=None, unconnected_gradients=UnconnectedGradients.NONE):
    "Computes the gradient using operations recorded in context of this tape.\n\n    Args:\n      target: Tensor (or list of tensors) to be differentiated.\n      sources: a list or nested structure of Tensors or Variables. `target`\n        will be differentiated against elements in `sources`.\n      output_gradients: a list of gradients, one for each element of\n        target. Defaults to None.\n      unconnected_gradients: a value which can either hold 'none' or 'zero' and\n        alters the value which will be returned if the target and sources are\n        unconnected. The possible values and effects are detailed in\n        'UnconnectedGradients' and it defaults to 'none'.\n\n    Returns:\n      a list or nested structure of Tensors (or IndexedSlices, or None),\n      one for each element in `sources`. Returned structure is the same as\n      the structure of `sources`.\n\n    Raises:\n      RuntimeError: if called inside the context of the tape, or if called more\n       than once on a non-persistent tape.\n      ValueError: if the target is a variable or if unconnected gradients is\n       called with an unknown value.\n    "
    if (self._tape is None):
        raise RuntimeError('GradientTape.gradient can only be called once on non-persistent tapes.')
    if self._recording:
        if (not self._persistent):
            self._pop_tape()
        else:
            logging.log_first_n(logging.WARN, "Calling GradientTape.gradient on a persistent tape inside it's context is significantly less efficient than calling it outside the context (it causes the gradient ops to be recorded on the tape, leading to increased CPU and memory usage). Only call GradientTape.gradient inside the context if you actually want to trace the gradient in order to compute higher order derrivatives.", 1)
    flat_targets = []
    for t in nest.flatten(target):
        if resource_variable_ops.is_resource_variable(t):
            with self:
                t = ops.convert_to_tensor(t)
        flat_targets.append(t)
    flat_sources = nest.flatten(sources)
    flat_sources = [_handle_or_self(x) for x in flat_sources]
    if (output_gradients is not None):
        output_gradients = [(None if (x is None) else ops.convert_to_tensor(x)) for x in nest.flatten(output_gradients)]
    flat_grad = imperative_grad.imperative_grad(self._tape, flat_targets, flat_sources, output_gradients=output_gradients, unconnected_gradients=unconnected_gradients)
    if (not self._persistent):
        self._tape = None
    grad = nest.pack_sequence_as(sources, flat_grad)
    return grad
