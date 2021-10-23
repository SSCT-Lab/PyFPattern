def compute_weight(self, module):
    weight = module._parameters[(self.name + '_org')]
    u = module._buffers[(self.name + '_u')]
    height = weight.size(0)
    weight_mat = weight.view(height, (- 1))
    for _ in range(self.n_power_iterations):
        v = normalize(torch.matmul(weight_mat.t(), u), dim=0, eps=self.eps)
        u = normalize(torch.matmul(weight_mat, v), dim=0, eps=self.eps)
    sigma = torch.dot(u, torch.matmul(weight_mat, v))
    weight.data /= sigma
    return (weight, u)