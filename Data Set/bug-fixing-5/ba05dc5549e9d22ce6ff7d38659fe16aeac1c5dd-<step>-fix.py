def step(self, closure=None):
    'Performs a single optimization step.\n\n        Arguments:\n            closure (callable, optional): A closure that reevaluates the model\n                and returns the loss.\n        '
    loss = None
    if (closure is not None):
        loss = closure()
    for group in self.param_groups:
        weight_decay = group['weight_decay']
        momentum = group['momentum']
        dampening = group['dampening']
        nesterov = group['nesterov']
        for p in group['params']:
            if (p.grad is None):
                continue
            d_p = p.grad.data
            if (weight_decay != 0):
                d_p.add_(weight_decay, p.data)
            if (momentum != 0):
                param_state = self.state[p]
                if ('momentum_buffer' not in param_state):
                    buf = param_state['momentum_buffer'] = p.data.new().resize_as_(p.data).zero_()
                    buf.mul_(momentum).add_(d_p)
                else:
                    buf = param_state['momentum_buffer']
                    buf.mul_(momentum).add_((1 - dampening), d_p)
                if nesterov:
                    d_p = d_p.add(momentum, buf)
                else:
                    d_p = buf
            p.data.add_((- group['lr']), d_p)
    return loss