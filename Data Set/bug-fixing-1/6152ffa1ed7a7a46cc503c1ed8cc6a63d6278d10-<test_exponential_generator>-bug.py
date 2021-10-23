

@with_seed()
def test_exponential_generator():
    ctx = mx.context.current_context()
    for dtype in ['float16', 'float32', 'float64']:
        for scale in [0.1, 1.0]:
            (buckets, probs) = gen_buckets_probs_with_ppf((lambda x: ss.expon.ppf(x, loc=0, scale=scale)), 5)
            generator_mx = (lambda x: mx.nd.random.exponential(scale, shape=x, ctx=ctx, dtype=dtype).asnumpy())
            verify_generator(generator=generator_mx, buckets=buckets, probs=probs)
            generator_mx_same_seed = (lambda x: np.concatenate([mx.nd.random.exponential(scale, shape=(x // 10), ctx=ctx, dtype=dtype).asnumpy() for _ in range(10)]))
            verify_generator(generator=generator_mx_same_seed, buckets=buckets, probs=probs)
