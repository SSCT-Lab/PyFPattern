def set_wd_mult(self, args_wd_mult):
    "Set individual weight decay multipler for parameters.\n        By default wd multipler is 0 for all params whose name doesn't\n        end with _weight, if param_idx2name is provided.\n\n        Parameters\n        ----------\n        args_wd_mult : dict of string/int to float\n            set the wd multipler for name/index to float.\n            setting multipler by index is supported for backward compatibility,\n            but we recommend using name and symbol.\n        "
    self.wd_mult = {
        
    }
    for n in self.idx2name.values():
        if (not n.endswith('_weight')):
            self.wd_mult[n] = 0.0
    if (self.sym is not None):
        attr = self.sym.list_attr()
        for (k, v) in attr.items():
            if k.endswith('_wd_mult'):
                self.wd_mult[k[:(- len('_wd_mult'))]] = float(v)
    self.wd_mult.update(args_wd_mult)