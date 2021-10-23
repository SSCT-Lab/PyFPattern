

def batch_normalization(x, mean, var, beta, gamma, epsilon=0.0001):
    'Apply batch normalization on x given mean, var, beta and gamma.\n    '
    ndim = x.ndim
    dev = theano.config.device
    use_cudnn = ((ndim < 5) and (dev.startswith('cuda') or dev.startswith('gpu')))
    if use_cudnn:
        try:
            axis = mean.broadcastable.index(False)
            if (axis != 1):
                shuffle_pattern = list(range(ndim))
                shuffle_pattern[1] = shuffle_pattern[axis]
                shuffle_pattern[axis] = 1
                x = x.dimshuffle(shuffle_pattern)
                mean = mean.dimshuffle(shuffle_pattern)
                var = var.dimshuffle(shuffle_pattern)
                beta = beta.dimshuffle(shuffle_pattern)
                gamma = gamma.dimshuffle(shuffle_pattern)
            normed = theano.sandbox.cuda.dnn.dnn_batch_normalization_test(x, gamma, beta, mean, var, 'spatial', epsilon)
            if (axis != 1):
                normed = normed.dimshuffle(shuffle_pattern)
            return normed
        except AttributeError:
            pass
        except ValueError:
            pass
    return T.nnet.bn.batch_normalization(x, gamma, beta, mean, sqrt((var + epsilon)), mode='high_mem')
