def randn(self, *args, **kwargs):
    '\n        Variant of torch.randn that also works in the TEST_CUDA case.\n        '
    return self.ValueTensor(*args, **kwargs).normal_()