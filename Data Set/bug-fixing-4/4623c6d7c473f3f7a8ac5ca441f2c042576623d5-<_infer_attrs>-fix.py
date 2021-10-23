def _infer_attrs(self, infer_fn, attr, *args):
    'Generic infer attributes.'
    (inputs, out) = self._get_graph(*args)
    (args, _) = _flatten(args)
    with warnings.catch_warnings(record=True) as w:
        (arg_attrs, _, aux_attrs) = getattr(out, infer_fn)(**{i.name: getattr(j, attr) for (i, j) in zip(inputs, args)})
        if (arg_attrs is None):
            raise ValueError(w[0].message)
    sdict = {i: j for (i, j) in zip(out.list_arguments(), arg_attrs)}
    sdict.update({name: attr for (name, attr) in zip(out.list_auxiliary_states(), aux_attrs)})
    for i in self.collect_params().values():
        setattr(i, attr, sdict[i.name])