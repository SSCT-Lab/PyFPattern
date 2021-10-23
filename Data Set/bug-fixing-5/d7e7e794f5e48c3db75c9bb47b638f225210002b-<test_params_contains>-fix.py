def test_params_contains(self):
    for (Dist, params) in EXAMPLES:
        for (i, param) in enumerate(params):
            dist = Dist(**param)
            for (name, value) in param.items():
                if (not (torch.is_tensor(value) or isinstance(value, Variable))):
                    value = torch.Tensor([value])
                if ((Dist in (Categorical, OneHotCategorical, Multinomial)) and (name == 'probs')):
                    value = (value / value.sum((- 1), True))
                try:
                    constraint = dist.params[name]
                except KeyError:
                    continue
                if is_dependent(constraint):
                    continue
                message = '{} example {}/{} parameter {} = {}'.format(Dist.__name__, (i + 1), len(params), name, value)
                self.assertTrue(constraint.check(value).all(), msg=message)