

@with_seed()
def test_multinomial_generator():

    def quantize_probs(probs, dtype):
        if (dtype == 'float16'):
            num_quanta = 2048.0
            quantized_probs = (np.rint((np.array(probs) * num_quanta)) / num_quanta)
            quantized_probs[0] += (1.0 - quantized_probs.sum())
        else:
            quantized_probs = np.array(probs)
        return quantized_probs
    ctx = mx.context.current_context()
    probs = [0.1, 0.2, 0.3, 0.05, 0.15, 0.2]
    samples = 1000000
    trials = 5
    buckets = list(range(6))
    for dtype in ['float16', 'float32', 'float64']:
        quantized_probs = quantize_probs(probs, dtype)
        generator_mx = (lambda x: mx.nd.random.multinomial(data=mx.nd.array(quantized_probs, ctx=ctx, dtype=dtype), shape=x).asnumpy())
        verify_generator(generator=generator_mx, buckets=buckets, probs=quantized_probs, nsamples=samples, nrepeat=trials, success_rate=0.2)
        generator_mx_same_seed = (lambda x: np.concatenate([mx.nd.random.multinomial(data=mx.nd.array(quantized_probs, ctx=ctx, dtype=dtype), shape=(x // 10)).asnumpy() for _ in range(10)]))
        verify_generator(generator=generator_mx_same_seed, buckets=buckets, probs=quantized_probs, nsamples=samples, nrepeat=trials, success_rate=0.2)
