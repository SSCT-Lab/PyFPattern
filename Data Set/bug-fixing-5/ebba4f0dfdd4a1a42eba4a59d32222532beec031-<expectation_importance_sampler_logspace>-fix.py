def expectation_importance_sampler_logspace(log_f, log_p, sampling_dist_q, z=None, n=None, seed=None, name='expectation_importance_sampler_logspace'):
    'Importance sampling with a positive function, in log-space.\n\n  With `\\\\(p(z) := exp^{log_p(z)}\\\\)`, and `\\\\(f(z) = exp{log_f(z)}\\\\)`,\n  this `Op` returns\n\n  ```\n  \\\\(Log[ n^{-1} sum_{i=1}^n [ f(z_i) p(z_i) / q(z_i) ] ],  z_i ~ q,\\\\)\n  \\\\(\\approx Log[ E_q[ f(Z) p(Z) / q(Z) ] ]\\\\)\n  \\\\(=       Log[E_p[f(Z)]]\\\\)\n  ```\n\n  This integral is done in log-space with max-subtraction to better handle the\n  often extreme values that `f(z) p(z) / q(z)` can take on.\n\n  In contrast to `expectation_importance_sampler`, this `Op` returns values in\n  log-space.\n\n\n  User supplies either `Tensor` of samples `z`, or number of samples to draw `n`\n\n  Args:\n    log_f: Callable mapping samples from `sampling_dist_q` to `Tensors` with\n      shape broadcastable to `q.batch_shape`.\n      For example, `log_f` works "just like" `sampling_dist_q.log_prob`.\n    log_p:  Callable mapping samples from `sampling_dist_q` to `Tensors` with\n      shape broadcastable to `q.batch_shape`.\n      For example, `log_p` works "just like" `q.log_prob`.\n    sampling_dist_q:  The sampling distribution.\n      `tf.contrib.distributions.Distribution`.\n      `float64` `dtype` recommended.\n      `log_p` and `q` should be supported on the same set.\n    z:  `Tensor` of samples from `q`, produced by `q.sample` for some `n`.\n    n:  Integer `Tensor`.  Number of samples to generate if `z` is not provided.\n    seed:  Python integer to seed the random number generator.\n    name:  A name to give this `Op`.\n\n  Returns:\n    Logarithm of the importance sampling estimate.  `Tensor` with `shape` equal\n      to batch shape of `q`, and `dtype` = `q.dtype`.\n  '
    q = sampling_dist_q
    with ops.name_scope(name, values=[z, n]):
        z = _get_samples(q, z, n, seed)
        log_values = ((log_f(z) + log_p(z)) - q.log_prob(z))
        return _logspace_mean(log_values)