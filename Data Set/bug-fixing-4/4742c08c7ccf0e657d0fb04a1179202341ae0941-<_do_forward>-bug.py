def _do_forward(self, *input):
    unpacked_input = tuple((arg.data for arg in input))
    is_volatile = any((arg.volatile for arg in input))
    self.input = input
    if (not is_volatile):
        self.needs_input_grad = tuple((arg.requires_grad for arg in input))
        self.requires_grad = any(self.needs_input_grad)
        self.previous_functions = [((arg.creator or arg), id(arg)) for arg in input]
    raw_output = self.forward(*unpacked_input)
    if (not isinstance(raw_output, tuple)):
        raw_output = (raw_output,)
    if is_volatile:
        output = tuple((Variable(tensor, volatile=True) for tensor in raw_output))
    else:
        output = tuple((Variable(tensor, self, requires_grad=self.requires_grad) for tensor in raw_output))
        self.output_ids = {id(var): i for (i, var) in enumerate(output)}
        if self.to_save:
            t2var = {var._data: var for var in chain(input, output)}
            self.saved_variables = tuple((t2var[t] for t in self.to_save))
            del self.to_save
        if (self.non_differentiable is not None):
            for var in output:
                if (var.data in self.non_differentiable):
                    var.requires_grad = False
    del self.input
    del self.non_differentiable
    if (len(output) == 1):
        output = output[0]
    return output