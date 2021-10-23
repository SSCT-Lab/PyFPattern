def compute_weight(self, module):
    weight = getattr(module, (self.name + '_org'))
    u = getattr(module, (self.name + '_u'))
    height = weight.size(0)
    weight_mat = weight.view(height, (- 1))
    with torch.no_grad():
        for _ in range(self.n_power_iterations):
            v = normalize(torch.matmul(weight_mat.t(), u), dim=0, eps=self.eps)
            u = normalize(torch.matmul(weight_mat, v), dim=0, eps=self.eps)
        sigma = torch.dot(u, torch.matmul(weight_mat, v))
    weight = (weight / sigma)
    return (weight, u)