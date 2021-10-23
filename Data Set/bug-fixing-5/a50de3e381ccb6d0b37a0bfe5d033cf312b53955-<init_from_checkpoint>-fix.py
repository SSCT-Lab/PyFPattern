@tf_export('train.init_from_checkpoint')
def init_from_checkpoint(ckpt_dir_or_file, assignment_map):
    "Initializes current variables with tensors loaded from given checkpoint.\n\n  Note: This overrides default initialization ops of specified variables and\n  redefines dtype.\n\n  Assignment map supports following syntax:\n\n  * `'checkpoint_scope_name/': 'scope_name/'` - will load all variables in\n    current `scope_name` from `checkpoint_scope_name` with matching tensor\n    names.\n  * `'checkpoint_scope_name/some_other_variable': 'scope_name/variable_name'` -\n    will initialize `scope_name/variable_name` variable\n    from `checkpoint_scope_name/some_other_variable`.\n  * `'scope_variable_name': variable` - will initialize given `tf.Variable`\n    object with tensor 'scope_variable_name' from the checkpoint.\n  * `'scope_variable_name': list(variable)` - will initialize list of\n    partitioned variables with tensor 'scope_variable_name' from the checkpoint.\n  * `'/': 'scope_name/'` - will load all variables in current `scope_name` from\n    checkpoint's root (e.g. no scope).\n\n  Supports loading into partitioned variables, which are represented as\n  `'<variable>/part_<part #>'`.\n\n  Example:\n\n  ```python\n\n  # Say, '/tmp/model.ckpt' has the following tensors:\n  #  -- name='old_scope_1/var1', shape=[20, 2]\n  #  -- name='old_scope_1/var2', shape=[50, 4]\n  #  -- name='old_scope_2/var3', shape=[100, 100]\n\n  # Create new model's variables\n  with tf.variable_scope('new_scope_1'):\n    var1 = tf.get_variable('var1', shape=[20, 2],\n                           initializer=tf.zeros_initializer())\n  with tf.variable_scope('new_scope_2'):\n    var2 = tf.get_variable('var2', shape=[50, 4],\n                           initializer=tf.zeros_initializer())\n    # Partition into 5 variables along the first axis.\n    var3 = tf.get_variable(name='var3', shape=[100, 100],\n                           initializer=tf.zeros_initializer(),\n                           partitioner=lambda shape, dtype: [5, 1])\n\n  # Initialize all variables in `new_scope_1` from `old_scope_1`.\n  init_from_checkpoint('/tmp/model.ckpt', {'old_scope_1/': 'new_scope_1'})\n\n  # Use names to specify which variables to initialize from checkpoint.\n  init_from_checkpoint('/tmp/model.ckpt',\n                       {'old_scope_1/var1': 'new_scope_1/var1',\n                        'old_scope_1/var2': 'new_scope_2/var2'})\n\n  # Or use tf.Variable objects to identify what to initialize.\n  init_from_checkpoint('/tmp/model.ckpt',\n                       {'old_scope_1/var1': var1,\n                        'old_scope_1/var2': var2})\n\n  # Initialize partitioned variables using variable's name\n  init_from_checkpoint('/tmp/model.ckpt',\n                       {'old_scope_2/var3': 'new_scope_2/var3'})\n\n  # Or specify the list of tf.Variable objects.\n  init_from_checkpoint('/tmp/model.ckpt',\n                       {'old_scope_2/var3': var3._get_variable_list()})\n\n  ```\n\n  Args:\n    ckpt_dir_or_file: Directory with checkpoints file or path to checkpoint.\n    assignment_map: Dict, where keys are names of the variables in the\n      checkpoint and values are current variables or names of current variables\n      (in default graph).\n\n  Raises:\n    tf.errors.OpError: If missing checkpoints or tensors in checkpoints.\n    ValueError: If missing variables in current graph.\n  "
    ckpt_file = _get_checkpoint_filename(ckpt_dir_or_file)
    reader = load_checkpoint(ckpt_dir_or_file)
    variable_map = reader.get_variable_to_shape_map()
    for (tensor_name_in_ckpt, current_var_or_name) in sorted(six.iteritems(assignment_map)):
        var = None
        is_var = (lambda x: isinstance(x, variables.Variable))
        if (is_var(current_var_or_name) or (isinstance(current_var_or_name, list) and all((is_var(v) for v in current_var_or_name)))):
            var = current_var_or_name
        else:
            store_vars = vs._get_default_variable_store()._vars
            var = store_vars.get(current_var_or_name, None)
            if (var is None):
                var = _collect_partitioned_variable(current_var_or_name, store_vars)
        if (var is not None):
            if (tensor_name_in_ckpt not in variable_map):
                raise ValueError(('Tensor %s is not found in %s checkpoint %s' % (tensor_name_in_ckpt, ckpt_dir_or_file, variable_map)))
            if is_var(var):
                if (not var.get_shape().is_compatible_with(variable_map[tensor_name_in_ckpt])):
                    raise ValueError(("Shape of variable %s (%s) doesn't match with shape of tensor %s (%s) from checkpoint reader." % (var.name, str(var.get_shape()), tensor_name_in_ckpt, str(variable_map[tensor_name_in_ckpt]))))
                var_name = var.name
            else:
                var_name = ','.join([v.name for v in var])
            _set_variable_or_list_initializer(var, ckpt_file, tensor_name_in_ckpt)
            logging.debug('Initialize variable %s from checkpoint %s with %s', var_name, ckpt_dir_or_file, tensor_name_in_ckpt)
        else:
            scopes = ''
            if ('/' in current_var_or_name):
                scopes = current_var_or_name[:current_var_or_name.rindex('/')]
            if (not tensor_name_in_ckpt.endswith('/')):
                raise ValueError("Assignment map with scope only name {} should map to scope only {}. Should be 'scope/': 'other_scope/'.".format(scopes, tensor_name_in_ckpt))
            scope_variables = set()
            for var_name in store_vars:
                if ((not scopes) or var_name.startswith((scopes + '/'))):
                    if ('/part_' in var_name):
                        var_name = var_name[:var_name.index('/part_')]
                    scope_variables.add(var_name)
            for var_name in sorted(scope_variables):
                full_tensor_name = var_name[len(scopes):]
                if (current_var_or_name != '/'):
                    full_tensor_name = full_tensor_name[1:]
                if (tensor_name_in_ckpt != '/'):
                    full_tensor_name = (tensor_name_in_ckpt + full_tensor_name)
                if full_tensor_name.endswith('/'):
                    full_tensor_name = full_tensor_name[:(- 1)]
                if (full_tensor_name not in variable_map):
                    raise ValueError(('Tensor %s (%s in %s) is not found in %s checkpoint' % (full_tensor_name, var_name[(len(scopes) + 1):], tensor_name_in_ckpt, ckpt_dir_or_file)))
                var = store_vars.get(var_name, None)
                if (var is None):
                    var = _collect_partitioned_variable(var_name, store_vars)
                _set_variable_or_list_initializer(var, ckpt_file, full_tensor_name)
                logging.debug('Initialize variable %s from checkpoint %s with %s', var_name, ckpt_dir_or_file, full_tensor_name)