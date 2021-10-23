

def updateOutput(self, input):
    assert (len(input) == 2)
    (a, b) = input
    assert ((a.ndimension() == 2) or (a.ndimension() == 3))
    assert (a.dim() == b.dim())
    if (a.ndimension() == 2):
        if self.transA:
            a = a.t()
        if self.transB:
            b = b.t()
        self.output.resize_(a.size(0), b.size(1))
        torch.mm(a, b, out=self.output)
    else:
        if self.transA:
            a = a.transpose(1, 2)
        if self.transB:
            b = b.transpose(1, 2)
        self.output.resize_(a.size(0), a.size(1), b.size(2))
        torch.bmm(a, b, out=self.output)
    return self.output
