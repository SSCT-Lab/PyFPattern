def _get_lr(self, index):
    'Get the learning rate given the index of the weight.\n\n        Parameters\n        ----------\n        index : int\n            The index corresponding to the weight.\n\n        Returns\n        -------\n        lr : float\n            Learning rate for this index.\n        '
    if (self.lr_scheduler is not None):
        lr = self.lr_scheduler(self.num_update)
    else:
        lr = self.lr
    if (index in self.lr_mult):
        lr *= self.lr_mult[index]
    elif (index in self.idx2name):
        lr *= self.lr_mult.get(self.idx2name[index], 1.0)
    return lr