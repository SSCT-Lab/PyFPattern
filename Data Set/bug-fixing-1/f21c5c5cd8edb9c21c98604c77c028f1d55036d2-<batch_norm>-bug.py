

def batch_norm(g, input, weight, bias, running_mean, running_var, training, momentum, eps, cudnn_enabled):
    out = g.op('BatchNormalization', input, weight, bias, running_mean, running_var, is_test_i=(not training), epsilon_f=eps, momentum_f=(1 - momentum), outputs=(1 if (not training) else 5))
    if (not training):
        return out
    else:
        (res, new_running_mean, new_running_var, saved_mean, saved_var) = out
        new_running_mean.setType(running_mean.type())
        new_running_var.setType(running_var.type())
        saved_mean.setUniqueName(('batch_norm_dead_output-' + saved_mean.uniqueName()))
        saved_var.setUniqueName(('batch_norm_dead_output-' + saved_var.uniqueName()))
        return res
