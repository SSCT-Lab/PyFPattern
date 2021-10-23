def check_cuda_available():
    'Checks if CUDA is available.\n\n    When CUDA is correctly set up, nothing happens.\n    Otherwise it raises ``RuntimeError``.\n    '
    if (not available):
        msg = 'CUDA environment is not correctly set up\n(see https://github.com/pfnet/chainer#installation).'
        msg += str(_resolution_error)
        raise RuntimeError(msg)
    if ((not cudnn_enabled) and (not getattr(check_cuda_available, '_already_warned', False))):
        warnings.warn('cuDNN is not enabled.\nPlease reinstall chainer after you install cudnn\n(see https://github.com/pfnet/chainer#installation).')
        check_cuda_available._already_warned = True