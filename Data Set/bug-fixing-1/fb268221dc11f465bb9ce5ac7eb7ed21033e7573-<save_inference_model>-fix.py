

def save_inference_model(dirname, feeded_var_names, target_vars, executor, main_program=None, model_filename=None, params_filename=None, export_for_deployment=True):
    '\n    Prune the given `main_program` to build a new program especially for inference,\n    and then save it and all related parameters to given `dirname` by the `executor`.\n\n    Args:\n        dirname(str): The directory path to save the inference model.\n        feeded_var_names(list[str]): Names of variables that need to be feeded data\n                                     during inference.\n        target_vars(list[Variable]): Variables from which we can get inference\n                                     results.\n        executor(Executor): The executor that saves the inference model.\n        main_program(Program|None): The original program, which will be pruned to\n                                    build the inference model. If is setted None,\n                                    the default main program will be used.\n                                    Default: None.\n        model_filename(str|None): The name of file to save the inference program\n                                  itself. If is setted None, a default filename\n                                  `__model__` will be used.\n        params_filename(str|None): The name of file to save all related parameters.\n                                   If it is setted None, parameters will be saved\n                                   in separate files .\n        export_for_deployment(bool): If True, programs are modified to only support\n                                     direct inference deployment. Otherwise,\n                                     more information will be stored for flexible\n                                     optimization and re-training. Currently, only\n                                     True is supported.\n\n    Returns:\n        None\n\n    Raises:\n        ValueError: If `feed_var_names` is not a list of basestring.\n        ValueError: If `target_vars` is not a list of Variable.\n\n    Examples:\n        .. code-block:: python\n\n            exe = fluid.Executor(fluid.CPUPlace())\n            path = "./infer_model"\n            fluid.io.save_inference_model(dirname=path, feeded_var_names=[\'img\'],\n                         target_vars=[predict_var], executor=exe)\n\n            # In this exsample, the function will prune the default main program\n            # to make it suitable for infering the `predict_var`. The pruned\n            # inference program is going to be saved in the "./infer_model/__model__"\n            # and parameters are going to be saved in separate files under folder\n            # "./infer_model".\n\n    '
    if isinstance(feeded_var_names, six.string_types):
        feeded_var_names = [feeded_var_names]
    elif export_for_deployment:
        if (len(feeded_var_names) > 0):
            if (not (bool(feeded_var_names) and all((isinstance(name, six.string_types) for name in feeded_var_names)))):
                raise ValueError("'feed_var_names' should be a list of str.")
    if isinstance(target_vars, Variable):
        target_vars = [target_vars]
    elif export_for_deployment:
        if (not (bool(target_vars) and all((isinstance(var, Variable) for var in target_vars)))):
            raise ValueError("'target_vars' should be a list of Variable.")
    if (main_program is None):
        main_program = default_main_program()
    try:
        os.makedirs(dirname)
    except OSError as e:
        if (e.errno != errno.EEXIST):
            raise
    if (model_filename is not None):
        model_basename = os.path.basename(model_filename)
    else:
        model_basename = '__model__'
    model_basename = os.path.join(dirname, model_basename)
    origin_program = main_program.clone()
    if export_for_deployment:
        main_program = main_program.clone()
        global_block = main_program.global_block()
        need_to_remove_op_index = []
        for (i, op) in enumerate(global_block.ops):
            op.desc.set_is_target(False)
            if ((op.type == 'feed') or (op.type == 'fetch')):
                need_to_remove_op_index.append(i)
        for index in need_to_remove_op_index[::(- 1)]:
            global_block._remove_op(index)
        main_program.desc.flush()
        main_program = main_program._prune(targets=target_vars)
        main_program = main_program._inference_optimize(prune_read_op=True)
        fetch_var_names = [v.name for v in target_vars]
        prepend_feed_ops(main_program, feeded_var_names)
        append_fetch_ops(main_program, fetch_var_names)
        with open(model_basename, 'wb') as f:
            f.write(main_program.desc.serialize_to_string())
    else:
        with open((model_basename + '.main_program'), 'wb') as f:
            f.write(main_program.desc.serialize_to_string())
    main_program._copy_dist_param_info_from(origin_program)
    if (params_filename is not None):
        params_filename = os.path.basename(params_filename)
    save_persistables(executor, dirname, main_program, params_filename)
