def _test_loop(self, f, ins, batch_size=None, verbose=0, steps=None):
    'Abstract method to loop over some data in batches.\n\n        # Arguments\n            f: Keras function returning a list of tensors.\n            ins: list of tensors to be fed to `f`.\n            batch_size: integer batch size or `None`.\n            verbose: verbosity mode.\n            steps: Total number of steps (batches of samples)\n                before declaring predictions finished.\n                Ignored with the default value of `None`.\n\n        # Returns\n            Scalar loss (if the model has a single output and no metrics)\n            or list of scalars (if the model has multiple outputs\n            and/or metrics). The attribute `model.metrics_names` will give you\n            the display labels for the scalar outputs.\n        '
    num_samples = self._check_num_samples(ins, batch_size, steps, 'steps')
    outs = []
    if (steps is not None):
        if (verbose == 1):
            progbar = Progbar(target=steps)
        for step in range(steps):
            batch_outs = f(ins)
            if isinstance(batch_outs, list):
                if (step == 0):
                    for _ in enumerate(batch_outs):
                        outs.append(0.0)
                for (i, batch_out) in enumerate(batch_outs):
                    outs[i] += batch_out
            else:
                if (step == 0):
                    outs.append(0.0)
                outs[0] += batch_outs
            if (verbose == 1):
                progbar.update(step)
        for i in range(len(outs)):
            outs[i] /= steps
    else:
        if (verbose == 1):
            progbar = Progbar(target=num_samples)
        batches = _make_batches(num_samples, batch_size)
        index_array = np.arange(num_samples)
        for (batch_index, (batch_start, batch_end)) in enumerate(batches):
            batch_ids = index_array[batch_start:batch_end]
            if isinstance(ins[(- 1)], float):
                ins_batch = (_slice_arrays(ins[:(- 1)], batch_ids) + [ins[(- 1)]])
            else:
                ins_batch = _slice_arrays(ins, batch_ids)
            batch_outs = f(ins_batch)
            if isinstance(batch_outs, list):
                if (batch_index == 0):
                    for batch_out in enumerate(batch_outs):
                        outs.append(0.0)
                for (i, batch_out) in enumerate(batch_outs):
                    outs[i] += (batch_out * len(batch_ids))
            else:
                if (batch_index == 0):
                    outs.append(0.0)
                outs[0] += (batch_outs * len(batch_ids))
            if (verbose == 1):
                progbar.update(batch_end)
        for i in range(len(outs)):
            outs[i] /= num_samples
    if (len(outs) == 1):
        return outs[0]
    return outs