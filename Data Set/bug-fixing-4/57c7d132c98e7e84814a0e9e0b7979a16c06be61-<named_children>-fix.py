def named_children(self):
    "Returns an iterator over immediate children modules, yielding both\n        the name of the module as well as the module itself.\n\n        Yields:\n            (string, Module): Tuple containing a name and child module\n\n        Example::\n\n            >>> for name, module in model.named_children():\n            >>>     if name in ['conv4', 'conv5']:\n            >>>         print(module)\n\n        "
    memo = set()
    for (name, module) in self._modules.items():
        if ((module is not None) and (module not in memo)):
            memo.add(module)
            (yield (name, module))