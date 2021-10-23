@staticmethod
def apply(module, name, n_power_iterations, eps):
    fn = SpectralNorm(name, n_power_iterations, eps)
    weight = module._parameters[name]
    height = weight.size(0)
    u = normalize(weight.new_empty(height).normal_(0, 1), dim=0, eps=fn.eps)
    module.register_parameter((fn.name + '_org'), weight)
    module.register_buffer((fn.name + '_u'), u)
    module.register_forward_pre_hook(fn)
    return fn