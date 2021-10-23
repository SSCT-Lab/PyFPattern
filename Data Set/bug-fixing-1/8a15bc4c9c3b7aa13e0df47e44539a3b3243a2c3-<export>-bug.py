

def export(model, args, f, export_params=True, verbose=False, training=False, input_names=None, output_names=None, aten=False):
    '\n    Export a model into ONNX format.  This exporter runs your model\n    once in order to get a trace of its execution to be exported;\n    at the moment, it supports a limited set of dynamic models (e.g., RNNs.)\n\n    See also: :ref:`onnx-export`\n\n    Arguments:\n        model (torch.nn.Module): the model to be exported.\n        args (tuple of arguments): the inputs to\n            the model, e.g., such that ``model(*args)`` is a valid\n            invocation of the model.  Any non-Tensor arguments will\n            be hard-coded into the exported model; any Tensor arguments\n            will become inputs of the exported model, in the order they\n            occur in args.  If args is a Tensor, this is equivalent\n            to having called it with a 1-ary tuple of that Tensor.\n            (Note: passing keyword arguments to the model is not currently\n            supported.  Give us a shout if you need it.)\n        f: a file-like object (has to implement fileno that returns a file descriptor)\n            or a string containing a file name.  A binary Protobuf will be written\n            to this file.\n        export_params (bool, default True): if specified, all parameters will\n            be exported.  Set this to False if you want to export an untrained model.\n            In this case, the exported model will first take all of its parameters\n            as arguments, the ordering as specified by ``model.state_dict().values()``\n        verbose (bool, default False): if specified, we will print out a debug\n            description of the trace being exported.\n        training (bool, default False): export the model in training mode.  At\n            the moment, ONNX is oriented towards exporting models for inference\n            only, so you will generally not need to set this to True.\n        input_names(list of strings, default empty list): names to assign to the\n            input nodes of the graph, in order\n        output_names(list of strings, default empty list): names to assign to the\n            output nodes of the graph, in order\n        aten (bool, default False): export the model in aten mode. If using aten mode,\n            all the ops original exported by the functions in symbolic.py are exported\n            as ATen ops.\n    '
    _export(model, args, f, export_params, verbose, training, input_names, output_names)
