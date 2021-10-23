

def _make_function_class_criterion(class_name, update_output, update_grad_input, acc_grad_parameters):
    weight_arg_idx = (- 1)
    for (i, arg) in enumerate(update_output.arguments):
        if arg.name.startswith('weight'):
            weight_arg_idx = i
            break
    buffers_idx = []
    additional_arg_idx = 0
    for arg in update_output.arguments[4:]:
        if ((not arg.name.startswith('weight')) and (arg.type == 'THTensor*')):
            buffers_idx.append(additional_arg_idx)
        additional_arg_idx += 1

    def __init__(self, *args, **kwargs):
        Function.__init__(self)
        self.weight = kwargs.get('weight')
        self.additional_args = list(args)

    def forward(self, input, target):
        self._backend = type2backend[type(input)]
        self.save_for_backward(input, target)
        if (weight_arg_idx >= 0):
            insert_idx = (weight_arg_idx - 4)
            self.additional_args.insert(insert_idx, self.weight)
        for idx in buffers_idx:
            self.additional_args.insert(idx, input.new(1))
        output = input.new(1)
        getattr(self._backend, update_output.name)(self._backend.library_state, input, target, output, *self.additional_args)
        return output

    def backward(self, grad_output):
        (input, target) = self.saved_tensors
        grad_input = grad_output.new().resize_as_(input).zero_()
        getattr(self._backend, update_grad_input.name)(self._backend.library_state, input, target, grad_input, *self.additional_args)
        grad_output_expanded = grad_output.resize_(*repeat(1, grad_input.dim()))
        grad_input.mul_(grad_output.expand_as(grad_input))
        return (grad_input, None)
    return type(class_name, (Function,), dict(__init__=__init__, forward=forward, backward=backward))
