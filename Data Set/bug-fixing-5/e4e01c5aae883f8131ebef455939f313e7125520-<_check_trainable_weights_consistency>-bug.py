def _check_trainable_weights_consistency(self):
    'Check trainable weights count consistency.\n\n        This will raise a warning if `trainable_weights` and\n        `_collected_trainable_weights` are consistent (i.e. have the same\n        number of parameters).\n        Inconsistency will typically arise when one modifies `model.trainable`\n        without calling `model.compile` again.\n        '
    if (not hasattr(self, '_collected_trainable_weights')):
        return
    if (len(self.trainable_weights) != len(self._collected_trainable_weights)):
        warnings.warn(UserWarning('Discrepancy between trainable weights and collected trainable weights, did you set `model.trainable` without calling `model.compile` after ?'))