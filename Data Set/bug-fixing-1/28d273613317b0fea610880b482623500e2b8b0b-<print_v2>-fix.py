

@tf_export('print', v1=[])
def print_v2(*inputs, **kwargs):
    'Print the specified inputs.\n\n  Returns an operator that prints the specified inputs to a desired\n  output stream or logging level. The inputs may be dense or sparse Tensors,\n  primitive python objects, data structures that contain Tensors, and printable\n  python objects. Printed tensors will recursively show the first and last\n  `summarize` elements of each dimension.\n\n  With eager execution enabled and/or inside a `tf.funtion` this\n  operator will automatically execute, and users only need to call `tf.print`\n  without using the return value. When constructing graphs outside of a\n  `tf.funtion`, one must either include the returned op\n  in the input to `session.run`, or use the operator as a control dependency for\n  executed ops by specifying `with tf.control_dependencies([print_op])`.\n\n  @compatibility(python2)\n  In python 2.7, make sure to import the following:\n  `from __future__ import print_function`\n  @end_compatibility\n\n  Example:\n    Single-input usage:\n    ```python\n    tensor = tf.range(10)\n    tf.print(tensor, output_stream=sys.stderr)\n    ```\n    (This prints "[0 1 2 ... 7 8 9]" to sys.stderr)\n\n    Multi-input usage:\n    ```python\n    tensor = tf.range(10)\n    tf.print("tensors:", tensor, {2: tensor * 2}, output_stream=sys.stdout)\n    ```\n    (This prints "tensors: [0 1 2 ... 7 8 9] {2: [0 2 4 ... 14 16 18]}" to\n    sys.stdout)\n\n    Usage in a defun:\n    ```python\n    from tensorflow.python.eager import function\n    @function.defun\n    def f():\n        tensor = tf.range(10)\n        tf.print(tensor, output_stream=sys.stderr)\n        return tensor\n\n    range_tensor = f()\n    ```\n    (This prints "[0 1 2 ... 7 8 9]" to sys.stderr)\n\n    Usage when constructing graphs:\n    ```python\n    tensor = tf.range(10)\n    print_op = tf.print("tensors:", tensor, {2: tensor * 2},\n                        output_stream=sys.stdout)\n    with tf.control_dependencies([print_op]):\n      tripled_tensor = tensor * 3\n    ```\n\n    (This prints "tensors: [0 1 2 ... 7 8 9] {2: [0 2 4 ... 14 16 18]}" to\n    sys.stdout)\n\n  Note: In Jupyter notebooks and colabs, this operator prints to the notebook\n    cell outputs. It will not write to the notebook kernel\'s console logs.\n\n  Args:\n    *inputs: Positional arguments that are the inputs to print. Inputs in the\n      printed output will be separated by spaces. Inputs may be python\n      primitives, tensors, data structures such as dicts and lists that may\n      contain tensors (with the data structures possibly nested in arbitrary\n      ways), and printable python objects.\n    output_stream: The output stream, logging level, or file to print to.\n      Defaults to sys.stderr, but sys.stdout, tf.compat.v1.logging.info,\n      tf.compat.v1.logging.warning, and tf.compat.v1.logging.error are also\n      supported. To print to\n      a file, pass a string started with "file://" followed by the file path,\n      e.g., "file:///tmp/foo.out".\n    summarize: The first and last `summarize` elements within each dimension are\n      recursively printed per Tensor. If None, then the first 3 and last 3\n      elements of each dimension are printed for each tensor. If set to -1, it\n      will print all elements of every tensor.\n    sep: The string to use to separate the inputs. Defaults to " ".\n    end: End character that is appended at the end the printed string.\n      Defaults to the newline character.\n    name: A name for the operation (optional).\n\n  Returns:\n    A print operator that prints the specified inputs in the specified output\n    stream or logging level.\n\n  Raises:\n    ValueError: If an unsupported output stream is specified.\n  '
    output_stream = kwargs.pop('output_stream', sys.stderr)
    name = kwargs.pop('name', None)
    summarize = kwargs.pop('summarize', 3)
    sep = kwargs.pop('sep', ' ')
    end = kwargs.pop('end', os.linesep)
    if kwargs:
        raise ValueError(('Unrecognized keyword arguments for tf.print: %s' % kwargs))
    format_name = None
    if name:
        format_name = (name + '_format')
    output_stream_to_constant = {
        sys.stdout: 'stdout',
        sys.stderr: 'stderr',
        tf_logging.INFO: 'log(info)',
        tf_logging.info: 'log(info)',
        tf_logging.WARN: 'log(warning)',
        tf_logging.warning: 'log(warning)',
        tf_logging.warn: 'log(warning)',
        tf_logging.ERROR: 'log(error)',
        tf_logging.error: 'log(error)',
    }
    if _is_filepath(output_stream):
        output_stream_string = output_stream
    else:
        output_stream_string = output_stream_to_constant.get(output_stream)
        if (not output_stream_string):
            raise ValueError(((('Unsupported output stream, logging level, or file.' + str(output_stream)) + '. Supported streams are sys.stdout, sys.stderr, tf.logging.info, tf.logging.warning, tf.logging.error. ') + "File needs to be in the form of 'file://<filepath>'."))
    if ((len(inputs) == 1) and tensor_util.is_tensor(inputs[0]) and (not isinstance(inputs[0], sparse_tensor.SparseTensor)) and (inputs[0].shape.ndims == 0) and (inputs[0].dtype == dtypes.string)):
        formatted_string = inputs[0]
    else:
        templates = []
        tensors = []
        tensor_free_structure = nest.map_structure((lambda x: ('' if tensor_util.is_tensor(x) else x)), inputs)
        tensor_free_template = ' '.join((pprint.pformat(x) for x in tensor_free_structure))
        placeholder = _generate_placeholder_string(tensor_free_template)
        for input_ in inputs:
            placeholders = []
            for x in nest.flatten(input_):
                if isinstance(x, sparse_tensor.SparseTensor):
                    tensors.extend([x.indices, x.values, x.dense_shape])
                    placeholders.append('SparseTensor(indices={}, values={}, shape={})'.format(placeholder, placeholder, placeholder))
                elif tensor_util.is_tensor(x):
                    tensors.append(x)
                    placeholders.append(placeholder)
                else:
                    placeholders.append(x)
            if isinstance(input_, six.string_types):
                cur_template = input_
            else:
                cur_template = pprint.pformat(nest.pack_sequence_as(input_, placeholders))
            templates.append(cur_template)
        template = sep.join(templates)
        template = template.replace((("'" + placeholder) + "'"), placeholder)
        formatted_string = string_ops.string_format(inputs=tensors, template=template, placeholder=placeholder, summarize=summarize, name=format_name)
    if compat.forward_compatible(2019, 5, 27):
        return gen_logging_ops.print_v2(formatted_string, output_stream=output_stream_string, name=name, end=end)
    else:
        if (end == os.linesep):
            end = ''
        return gen_logging_ops.print_v2((formatted_string + end), output_stream=output_stream_string, name=name)
