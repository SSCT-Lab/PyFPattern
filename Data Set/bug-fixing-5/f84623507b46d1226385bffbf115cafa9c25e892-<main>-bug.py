def main(unused_args):
    freeze_graph(FLAGS.input_graph, FLAGS.input_saver, FLAGS.input_binary, FLAGS.input_checkpoint, FLAGS.output_node_names, FLAGS.restore_op_name, FLAGS.filename_tensor_name, FLAGS.output_graph, FLAGS.clear_devices, FLAGS.initializer_nodes, FLAGS.variable_names_whitelist, FLAGS.variable_names_blacklist, FLAGS.input_meta_graph, FLAGS.input_saved_model_dir, FLAGS.saved_model_tags, checkpoint_version=checkpoint_version)