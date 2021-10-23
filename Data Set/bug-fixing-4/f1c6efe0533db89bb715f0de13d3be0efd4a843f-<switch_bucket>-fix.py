def switch_bucket(self, bucket_key, data_shapes, label_shapes=None):
    'Switch to a different bucket. This will change `self.curr_module`.\n\n        Parameters\n        ----------\n        bucket_key : str (or any python object)\n            The key of the target bucket.\n        data_shapes : list of (str, tuple)\n            Typically `data_batch.provide_data`.\n        label_shapes : list of (str, tuple)\n            Typically `data_batch.provide_label`.\n        '
    assert self.binded, 'call bind before switching bucket'
    if (not (bucket_key in self._buckets)):
        (symbol, data_names, label_names) = self._sym_gen(bucket_key)
        module = Module(symbol, data_names, label_names, logger=self.logger, context=self._context, work_load_list=self._work_load_list)
        module.bind(data_shapes, label_shapes, self._curr_module.for_training, self._curr_module.inputs_need_grad, force_rebind=False, shared_module=self._curr_module)
        self._buckets[bucket_key] = module
    self._curr_module = self._buckets[bucket_key]