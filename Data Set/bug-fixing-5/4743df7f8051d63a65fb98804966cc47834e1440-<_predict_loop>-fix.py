def _predict_loop(self, f, ins, batch_size=32, verbose=0, steps=None):
    'Abstract method to loop over some data in batches.\n\n        # Arguments\n            f: Keras function returning a list of tensors.\n            ins: list of tensors to be fed to `f`.\n            batch_size: integer batch size.\n            verbose: verbosity mode.\n            steps: Total number of steps (batches of samples)\n                before declaring `_predict_loop` finished.\n                Ignored with the default value of `None`.\n\n        # Returns\n            Array of predictions (if the model has a single output)\n            or list of arrays of predictions\n            (if the model has multiple outputs).\n        '
    num_samples = self._check_num_samples(ins, batch_size, steps, 'steps')
    if (verbose == 1):
        if (steps is not None):
            progbar = Progbar(target=steps)
        else:
            progbar = Progbar(target=num_samples)
    if (steps is not None):
        unconcatenated_outs = []
        for step in range(steps):
            batch_outs = f(ins)
            if (not isinstance(batch_outs, list)):
                batch_outs = [batch_outs]
            if (step == 0):
                for batch_out in batch_outs:
                    unconcatenated_outs.append([])
            for (i, batch_out) in enumerate(batch_outs):
                unconcatenated_outs[i].append(batch_out)
            if (verbose == 1):
                progbar.update((step + 1))
        if (len(unconcatenated_outs) == 1):
            return np.concatenate(unconcatenated_outs[0], axis=0)
        return [np.concatenate(unconcatenated_outs[i], axis=0) for i in range(len(unconcatenated_outs))]
    else:
        outs = []
        batches = _make_batches(num_samples, batch_size)
        index_array = np.arange(num_samples)
        for (batch_index, (batch_start, batch_end)) in enumerate(batches):
            batch_ids = index_array[batch_start:batch_end]
            if (ins and isinstance(ins[(- 1)], float)):
                ins_batch = (_slice_arrays(ins[:(- 1)], batch_ids) + [ins[(- 1)]])
            else:
                ins_batch = _slice_arrays(ins, batch_ids)
            batch_outs = f(ins_batch)
            if (not isinstance(batch_outs, list)):
                batch_outs = [batch_outs]
            if (batch_index == 0):
                for batch_out in batch_outs:
                    shape = ((num_samples,) + batch_out.shape[1:])
                    outs.append(np.zeros(shape, dtype=batch_out.dtype))
            for (i, batch_out) in enumerate(batch_outs):
                outs[i][batch_start:batch_end] = batch_out
            if (verbose == 1):
                progbar.update(batch_end)
        if (len(outs) == 1):
            return outs[0]
        return outs