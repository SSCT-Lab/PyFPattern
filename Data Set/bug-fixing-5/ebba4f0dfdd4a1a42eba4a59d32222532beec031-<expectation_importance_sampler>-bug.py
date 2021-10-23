def expectation_importance_sampler(f, log_p, sampling_dist_q, z=None, n=None, seed=None, name='expectation_importance_sampler'):
    'Monte Carlo estimate of `E_p[f(Z)] = E_q[f(Z) p(Z) / q(Z)]`.\n\n  With `p(z) := exp{log_p(z)}`, this `Op` returns\n\n  ```\n  n^{-1} sum_{i=1}^n [ f(z_i) p(z_i) / q(z_i) ],  z_i ~ q,\n  \\approx E_q[ f(Z) p(Z) / q(Z) ]\n  =       E_p[f(Z)]\n  ```\n\n  This integral is done in log-space with max-subtraction to better handle the\n  often extreme values that `f(z) p(z) / q(z)` can take on.\n\n  If `f >= 0`, it is up to 2x more efficient to exponentiate the result of\n  `expectation_importance_sampler_logspace` applied to `Log[f]`.\n\n  User supplies either `Tensor` of samples `z`, or number of samples to draw `n`\n\n  Args:\n    f: Callable mapping samples from `sampling_dist_q` to `Tensors` with shape\n      broadcastable to `q.batch_shape`.\n      For example, `f` works "just like" `q.log_prob`.\n    log_p:  Callable mapping samples from `sampling_dist_q` to `Tensors` with\n      shape broadcastable to `q.batch_shape`.\n      For example, `log_p` works "just like" `sampling_dist_q.log_prob`.\n    sampling_dist_q:  The sampling distribution.\n      `tf.contrib.distributions.Distribution`.\n      `float64` `dtype` recommended.\n      `log_p` and `q` should be supported on the same set.\n    z:  `Tensor` of samples from `q`, produced by `q.sample` for some `n`.\n    n:  Integer `Tensor`.  Number of samples to generate if `z` is not provided.\n    seed:  Python integer to seed the random number generator.\n    name:  A name to give this `Op`.\n\n  Returns:\n    The importance sampling estimate.  `Tensor` with `shape` equal\n      to batch shape of `q`, and `dtype` = `q.dtype`.\n  '
    q = sampling_dist_q
    with ops.name_scope(name, values=[z, n]):
        z = _get_samples(q, z, n, seed)
        log_p_z = log_p(z)
        q_log_prob_z = q.log_prob(z)

        def _importance_sampler_positive_f(log_f_z):
            log_values = ((log_f_z + log_p_z) - q_log_prob_z)
            return _logspace_mean(log_values)
        f_z = f(z)
        log_f_plus_z = math_ops.log((nn.relu(f_z) + 1.0))
        log_f_minus_z = math_ops.log((nn.relu(((- 1.0) * f_z)) + 1.0))
        log_f_plus_integral = _importance_sampler_positive_f(log_f_plus_z)
        log_f_minus_integral = _importance_sampler_positive_f(log_f_minus_z)
    return (math_ops.exp(log_f_plus_integral) - math_ops.exp(log_f_minus_integral))