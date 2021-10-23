def add(self, module, **kwargs):
    'Add a module to the chain.\n\n        Parameters\n        ----------\n        module : BaseModule\n            The new module to add.\n        kwargs : **keywords\n            All the keyword arguments are saved as meta information\n            for the added module. The currently known meta includes\n\n            - `take_labels`: indicating whether the module expect to\n              take labels when doing computation. Note any module in\n              the chain can take labels (not necessarily only the top\n              most one), and they all take the same labels passed\n              from the original data batch for the `SequentialModule`.\n\n        Returns\n        -------\n        This function returns `self` to allow us to easily chain a\n        series of `add` calls.\n\n        Examples\n        --------\n        An example of addinging two modules to a chain::\n            >>> seq_mod = mx.mod.SequentialModule()\n            >>> seq_mod.add(mod1)\n            >>> seq_mod.add(mod2)\n        '
    self._modules.append(module)
    for key in kwargs.iterkeys():
        assert (key in self._meta_keys), ('Unknown meta "%s", a typo?' % key)
    self._metas.append(kwargs)
    self.binded = False
    self.params_initialized = False
    self.optimizer_initialized = False
    return self