def expectation(f, samples, log_prob=None, use_reparametrization=True, axis=0, keep_dims=False, name=None):
    'Computes the Monte-Carlo approximation of `\\(E_p[f(X)]\\)`.\n\n  This function computes the Monte-Carlo approximation of an expectation, i.e.,\n\n  ```none\n  \\(E_p[f(X)] \x07pprox= m^{-1} sum_i^m f(x_j),  x_j\\  ~iid\\ p(X)\\)\n  ```\n\n  where:\n\n  - `x_j = samples[j, ...]`,\n  - `log(p(samples)) = log_prob(samples)` and\n  - `m = prod(shape(samples)[axis])`.\n\n  Tricks: Reparameterization and Score-Gradient\n\n  When p is "reparameterized", i.e., a diffeomorphic transformation of a\n  parameterless distribution (e.g.,\n  `Normal(Y; m, s) <=> Y = sX + m, X ~ Normal(0,1)`), we can swap gradient and\n  expectation, i.e.,\n  `grad[ Avg{ \\(s_i : i=1...n\\) } ] = Avg{ grad[\\(s_i\\)] : i=1...n }` where\n  `S_n = Avg{\\(s_i\\)}` and `\\(s_i = f(x_i), x_i ~ p\\)`.\n\n  However, if p is not reparameterized, TensorFlow\'s gradient will be incorrect\n  since the chain-rule stops at samples of non-reparameterized distributions.\n  (The non-differentiated result, `approx_expectation`, is the same regardless\n  of `use_reparametrization`.) In this circumstance using the Score-Gradient\n  trick results in an unbiased gradient, i.e.,\n\n  ```none\n  grad[ E_p[f(X)] ]\n  = grad[ int dx p(x) f(x) ]\n  = int dx grad[ p(x) f(x) ]\n  = int dx [ p\'(x) f(x) + p(x) f\'(x) ]\n  = int dx p(x) [p\'(x) / p(x) f(x) + f\'(x) ]\n  = int dx p(x) grad[ f(x) p(x) / stop_grad[p(x)] ]\n  = E_p[ grad[ f(x) p(x) / stop_grad[p(x)] ] ]\n  ```\n\n  Unless p is not reparametrized, it is usually preferable to\n  `use_reparametrization = True`.\n\n  Warning: users are responsible for verifying `p` is a "reparameterized"\n  distribution.\n\n  Example Use:\n\n  ```python\n  bf = tf.contrib.bayesflow\n  ds = tf.contrib.distributions\n\n  # Monte-Carlo approximation of a reparameterized distribution, e.g., Normal.\n\n  num_draws = int(1e5)\n  p = ds.Normal(loc=0., scale=1.)\n  q = ds.Normal(loc=1., scale=2.)\n  exact_kl_normal_normal = ds.kl_divergence(p, q)\n  # ==> 0.44314718\n  approx_kl_normal_normal = bf.expectation(\n      f=lambda x: p.log_prob(x) - q.log_prob(x),\n      samples=p.sample(num_draws, seed=42),\n      log_prob=p.log_prob,\n      use_reparametrization=(p.reparameterization_type\n                             == distribution.FULLY_REPARAMETERIZED))\n  # ==> 0.44632751\n  # Relative Error: <1%\n\n  # Monte-Carlo approximation of non-reparameterized distribution, e.g., Gamma.\n\n  num_draws = int(1e5)\n  p = ds.Gamma(concentration=1., rate=1.)\n  q = ds.Gamma(concentration=2., rate=3.)\n  exact_kl_gamma_gamma = ds.kl_divergence(p, q)\n  # ==> 0.37999129\n  approx_kl_gamma_gamma = bf.expectation(\n      f=lambda x: p.log_prob(x) - q.log_prob(x),\n      samples=p.sample(num_draws, seed=42),\n      log_prob=p.log_prob,\n      use_reparametrization=(p.reparameterization_type\n                             == distribution.FULLY_REPARAMETERIZED))\n  # ==> 0.37696719\n  # Relative Error: <1%\n\n  # For comparing the gradients, see `monte_carlo_test.py`.\n  ```\n\n  Note: The above example is for illustration only. To compute approximate\n  KL-divergence, the following is preferred:\n\n  ```python\n  approx_kl_p_q = bf.monte_carlo_csiszar_f_divergence(\n      f=bf.kl_reverse,\n      p_log_prob=q.log_prob,\n      q=p,\n      num_draws=num_draws)\n  ```\n\n  Args:\n    f: Python callable which can return `f(samples)`.\n    samples: `Tensor` of samples used to form the Monte-Carlo approximation of\n      `\\(E_p[f(X)]\\)`.  A batch of samples should be indexed by `axis`\n      dimensions.\n    log_prob: Python callable which can return `log_prob(samples)`. Must\n      correspond to the natural-logarithm of the pdf/pmf of each sample. Only\n      required/used if `use_reparametrization=False`.\n      Default value: `None`.\n    use_reparametrization: Python `bool` indicating that the approximation\n      should use the fact that the gradient of samples is unbiased. Whether\n      `True` or `False`, this arg only affects the gradient of the resulting\n      `approx_expectation`.\n      Default value: `True`.\n    axis: The dimensions to average. If `None`, averages all\n      dimensions.\n      Default value: `0` (the left-most dimension).\n    keep_dims: If True, retains averaged dimensions using size `1`.\n      Default value: `False`.\n    name: A `name_scope` for operations created by this function.\n      Default value: `None` (which implies "expectation").\n\n  Returns:\n    approx_expectation: `Tensor` corresponding to the Monte-Carlo approximation\n      of `\\(E_p[f(X)]\\)`.\n\n  Raises:\n    ValueError: if `f` is not a Python `callable`.\n    ValueError: if `use_reparametrization=False` and `log_prob` is not a Python\n      `callable`.\n  '
    with ops.name_scope(name, 'expectation', [samples]):
        if (not callable(f)):
            raise ValueError('`f` must be a callable function.')
        if use_reparametrization:
            return math_ops.reduce_mean(f(samples), axis=axis, keepdims=keep_dims)
        else:
            if (not callable(log_prob)):
                raise ValueError('`log_prob` must be a callable function.')
            stop = array_ops.stop_gradient
            x = stop(samples)
            logpx = log_prob(x)
            fx = f(x)
            fx += (stop(fx) * (logpx - stop(logpx)))
            return math_ops.reduce_mean(fx, axis=axis, keepdims=keep_dims)