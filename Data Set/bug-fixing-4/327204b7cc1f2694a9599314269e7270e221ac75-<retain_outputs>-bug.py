def retain_outputs(self, indexes):
    'Lets specified output variable nodes keep data arrays.\n\n        By calling this method from :meth:`forward`, the function node can\n        specify which outputs are required for backprop. If this method is not\n        called, any output variables are not marked to keep the data array at\n        the point of returning from :meth:`apply`. The output variables with\n        retained arrays can be obtained by :meth:`get_retained_outputs` from\n        :meth:`backward`.\n\n        .. note::\n\n           It is recommended to use this method if the function requires some\n           or all output arrays in backprop. The function can also use output\n           arrays just by keeping references to them directly, whereas it might\n           influence on the performance of later function applications to the\n           output variables.\n\n        Note that **this method must not be called from the outside of\n        forward method.**\n\n        Args:\n            indexes (iterable of int): Indexes of input variables that the\n                function does not require for backprop.\n\n        '
    self._output_indexes_to_retain = indexes