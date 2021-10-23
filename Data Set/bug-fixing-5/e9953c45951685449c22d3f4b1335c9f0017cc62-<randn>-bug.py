def randn(self, *args, **kwargs):
    x = torch.randn(*args, **kwargs)
    if self.is_cuda:
        x = x.cuda()
    return x