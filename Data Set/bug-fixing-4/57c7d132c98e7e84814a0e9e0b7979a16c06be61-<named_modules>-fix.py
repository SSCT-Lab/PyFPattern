def named_modules(self, memo=None, prefix=''):
    "Returns an iterator over all modules in the network, yielding\n        both the name of the module as well as the module itself.\n\n        Yields:\n            (string, Module): Tuple of name and module\n\n        Note:\n            Duplicate modules are returned only once. In the following\n            example, ``l`` will be returned only once.\n\n        Example::\n            >>> l = nn.Linear(2, 2)\n            >>> net = nn.Sequential(l, l)\n            >>> for idx, m in enumerate(net.named_modules()):\n                    print(idx, '->', m)\n\n            0 -> ('', Sequential (\n              (0): Linear (2 -> 2)\n              (1): Linear (2 -> 2)\n            ))\n            1 -> ('0', Linear (2 -> 2))\n\n        "
    if (memo is None):
        memo = set()
    if (self not in memo):
        memo.add(self)
        (yield (prefix, self))
        for (name, module) in self._modules.items():
            if (module is None):
                continue
            submodule_prefix = ((prefix + ('.' if prefix else '')) + name)
            for m in module.named_modules(memo, submodule_prefix):
                (yield m)