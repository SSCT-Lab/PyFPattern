def _gen_sparse(self, d, nnz, with_size):
    if isinstance(with_size, Number):
        v = torch.randn(nnz)
        i = (torch.rand(d, nnz) * with_size).type(torch.LongTensor)
        x = torch.sparse.DoubleTensor(i, v)
    else:
        v_size = ([nnz] + list(with_size[d:]))
        v = torch.randn(*v_size)
        i = (torch.rand(d, nnz) * torch.Tensor(with_size[:d]).repeat(nnz, 1).transpose(0, 1))
        i = i.type(torch.LongTensor)
        x = torch.sparse.DoubleTensor(i, v, torch.Size(with_size))
    if self.is_cuda:
        return (x.cuda(), i.cuda(), v.cuda())
    else:
        return (x, i.clone(), v.clone())