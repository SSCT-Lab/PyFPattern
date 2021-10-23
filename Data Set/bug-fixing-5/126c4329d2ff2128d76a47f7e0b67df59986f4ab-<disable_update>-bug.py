def disable_update(self):
    'Disables update rules of all parameters under the link hierarchy.\n\n        This method sets the :attr:~chainer.UpdateRule.enabled` flag of the\n        update rule of each parameter variable to ``False``.\n\n        '
    for param in self.params():
        rule = param.update_rule
        if (rule is not None):
            rule.enabled = False