def parameters(self):
    "Returns an iterator over module parameters.\n\n        This is typically passed to an optimizer.\n\n        Yields:\n            Parameter: module parameter\n\n        Example:\n            >>> for param in model.parameters():\n            >>>     print(type(param.data), param.size())\n            <class 'torch.FloatTensor'> (20L,)\n            <class 'torch.FloatTensor'> (20L, 1L, 5L, 5L)\n        "
    for (name, param) in self.named_parameters():
        (yield param)