def data_parallel(module, inputs, device_ids=None, output_device=None, dim=0, module_kwargs=None):
    'Evaluates module(input) in parallel across the GPUs given in device_ids.\n\n    This is the functional version of the DataParallel module.\n\n    Args:\n        module: the module to evaluate in parallel\n        inputs: inputs to the module\n        device_ids: GPU ids on which to replicate module\n        output_device: GPU location of the output  Use -1 to indicate the CPU.\n            (default: device_ids[0])\n    Returns:\n        a Variable containing the result of module(input) located on\n        output_device\n    '
    if (not isinstance(inputs, tuple)):
        inputs = (inputs,)
    if (device_ids is None):
        device_ids = list(range(torch.cuda.device_count()))
    if (output_device is None):
        output_device = device_ids[0]
    (inputs, module_kwargs) = scatter_kwargs(inputs, module_kwargs, device_ids, dim)
    if (len(device_ids) == 1):
        return module(*inputs[0], **module_kwargs[0])
    replicas = replicate(module, device_ids[:len(inputs)])
    outputs = parallel_apply(replicas, inputs, module_kwargs, device_ids)
    return gather(outputs, output_device, dim)