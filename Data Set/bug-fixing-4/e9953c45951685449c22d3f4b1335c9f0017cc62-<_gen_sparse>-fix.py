def _gen_sparse(self, d, nnz, with_size):
    if isinstance(with_size, Number):
        with_size = ([with_size] * d)
    if self.is_uncoalesced:
        v_size = ([(nnz * 2)] + list(with_size[d:]))
        v = torch.randn(*v_size)
        r = torch.rand(d, nnz)
        i = (torch.cat([r, r], dim=1) * torch.Tensor(with_size[:d]).repeat((nnz * 2), 1).transpose(0, 1))
        i = i.type(torch.LongTensor)
        x = torch.sparse.DoubleTensor(i, v, torch.Size(with_size))
        self.assert_uncoalesced(x)
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