def __enter__(self):
    contexts = [chainer.using_config('use_cudnn', self.use_cudnn), chainer.using_config('cudnn_deterministic', self.cudnn_deterministic), chainer.using_config('autotune', self.autotune), chainer.using_config('use_ideep', self.use_ideep), chainer.using_device(self.device)]
    for c in contexts:
        c.__enter__()
    self._contexts.append(contexts)
    return self