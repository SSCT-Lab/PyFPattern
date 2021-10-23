def _get_wd(self, index):
    'get weight decay for index.\n        Returns 0 for non-weights if the name of weights are provided for `__init__`.\n\n        Parameters\n        ----------\n        index : int\n            The index for weight.\n\n        Returns\n        -------\n        wd : float\n            Weight decay for this index.\n        '
    wd = self.wd
    if (index in self.wd_mult):
        wd *= self.wd_mult[index]
    elif (index in self.idx2name):
        wd *= self.wd_mult.get(self.idx2name[index], 1.0)
    return wd