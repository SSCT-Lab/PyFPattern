

def batch_normalization(x, mean, var, beta, gamma, epsilon=0.0001):
    'Apply batch normalization on x given mean, var, beta and gamma.\n    '
    ndim = x.ndim
    dev = theano.config.device
    use_cudnn = ((ndim < 5) and (dev.startswith('cuda') or dev.startswith('gpu')))
    if use_cudnn:
        try:
            return theano.sandbox.cuda.dnn.dnn_batch_normalization_test(x, gamma, beta, mean, var, 'spatial', epsilon)
        except AttributeError:
            pass
    return T.nnet.bn.batch_normalization(x, gamma, beta, mean, sqrt((var + epsilon)), mode='high_mem')
