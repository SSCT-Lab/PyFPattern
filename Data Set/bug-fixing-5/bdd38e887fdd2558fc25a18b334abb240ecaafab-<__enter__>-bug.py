def __enter__(self):
    self._contexts = [chainer.using_config('use_cudnn', self.use_cudnn), chainer.using_config('cudnn_deterministic', self.cudnn_deterministic), chainer.using_config('autotune', self.autotune), chainer.using_config('use_ideep', self.use_ideep), chainer.using_device(self.device)]
    for c in self._contexts:
        c.__enter__()
    return self