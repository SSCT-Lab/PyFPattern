def named_parameters(self, memo=None, prefix=''):
    "Returns an iterator over module parameters, yielding both the\n        name of the parameter as well as the parameter itself\n\n        Yields:\n            (string, Parameter): Tuple containing the name and parameter\n\n        Example:\n            >>> for name, param in self.named_parameters():\n            >>>    if name in ['bias']:\n            >>>        print(param.size())\n        "
    if (memo is None):
        memo = set()
    for (name, p) in self._parameters.items():
        if ((p is not None) and (p not in memo)):
            memo.add(p)
            (yield (((prefix + ('.' if prefix else '')) + name), p))
    for (mname, module) in self.named_children():
        submodule_prefix = ((prefix + ('.' if prefix else '')) + mname)
        for (name, p) in module.named_parameters(memo, submodule_prefix):
            (yield (name, p))