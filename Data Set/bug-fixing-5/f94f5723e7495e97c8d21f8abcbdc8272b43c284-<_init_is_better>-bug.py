def _init_is_better(self, mode, threshold, threshold_mode):
    if (mode not in {'min', 'max'}):
        raise ValueError((('mode ' + mode) + ' is unknown!'))
    if (threshold_mode not in {'rel', 'abs'}):
        raise ValueError((('threshold mode ' + mode) + ' is unknown!'))
    if ((mode == 'min') and (threshold_mode == 'rel')):
        rel_epsilon = (1.0 - threshold)
        self.is_better = (lambda a, best: (a < (best * rel_epsilon)))
        self.mode_worse = float('Inf')
    elif ((mode == 'min') and (threshold_mode == 'abs')):
        self.is_better = (lambda a, best: (a < (best - threshold)))
        self.mode_worse = float('Inf')
    elif ((mode == 'max') and (threshold_mode == 'rel')):
        rel_epsilon = (threshold + 1.0)
        self.is_better = (lambda a, best: (a > (best * rel_epsilon)))
        self.mode_worse = (- float('Inf'))
    else:
        self.is_better = (lambda a, best: (a > (best + threshold)))
        self.mode_worse = (- float('Inf'))