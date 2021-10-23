def _convert_model(flags):
    'Calls function to convert the TensorFlow model into a TFLite model.\n\n  Args:\n    flags: argparse.Namespace object.\n\n  Raises:\n    ValueError: Invalid flags.\n  '
    converter = _get_toco_converter(flags)
    if flags.inference_type:
        converter.inference_type = _types_pb2.IODataType.Value(flags.inference_type)
    if flags.inference_input_type:
        converter.inference_input_type = _types_pb2.IODataType.Value(flags.inference_input_type)
    if flags.output_format:
        converter.output_format = _toco_flags_pb2.FileFormat.Value(flags.output_format)
    if (flags.mean_values and flags.std_dev_values):
        input_arrays = converter.get_input_arrays()
        std_dev_values = _parse_array(flags.std_dev_values, type_fn=int)
        mean_values = _parse_array(flags.mean_values, type_fn=int)
        quant_stats = list(zip(mean_values, std_dev_values))
        if (((not flags.input_arrays) and (len(input_arrays) > 1)) or (len(input_arrays) != len(quant_stats))):
            raise ValueError("Mismatching --input_arrays, --std_dev_values, and --mean_values. The flags must have the same number of items. The current input arrays are '{0}'. --input_arrays must be present when specifying --std_dev_values and --mean_values with multiple input tensors in order to map between names and values.".format(','.join(input_arrays)))
        converter.quantized_input_stats = dict(zip(input_arrays, quant_stats))
    if ((flags.default_ranges_min is not None) and (flags.default_ranges_max is not None)):
        converter.default_ranges_stats = (flags.default_ranges_min, flags.default_ranges_max)
    if flags.drop_control_dependency:
        converter.drop_control_dependency = flags.drop_control_dependency
    if flags.reorder_across_fake_quant:
        converter.reorder_across_fake_quant = flags.reorder_across_fake_quant
    if flags.change_concat_input_ranges:
        converter.change_concat_input_ranges = flags.change_concat_input_ranges
    if flags.allow_custom_ops:
        converter.allow_custom_ops = flags.allow_custom_ops
    if flags.quantize_weights:
        if (flags.inference_type == lite_constants.QUANTIZED_UINT8):
            raise ValueError('--quantized_weights is not supported with --inference_type=QUANTIZED_UINT8')
        converter.quantize_weights = flags.quantize_weights
    if flags.dump_graphviz_dir:
        converter.dump_graphviz_dir = flags.dump_graphviz_dir
    if flags.dump_graphviz_video:
        converter.dump_graphviz_vode = flags.dump_graphviz_video
    output_data = converter.convert()
    with open(flags.output_file, 'wb') as f:
        f.write(output_data)