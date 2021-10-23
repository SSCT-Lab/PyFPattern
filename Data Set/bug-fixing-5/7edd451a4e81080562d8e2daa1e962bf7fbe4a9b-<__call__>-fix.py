def __call__(self, module, inputs):
    (weight, u) = self.compute_weight(module)
    setattr(module, self.name, weight)
    with torch.no_grad():
        getattr(module, self.name).copy_(weight)