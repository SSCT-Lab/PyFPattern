def import_to_tensorboard(model_dir, log_dir):
    'View an imported protobuf model (`.pb` file) as a graph in Tensorboard.\n\n  Args:\n    model_dir: The location of the protobuf (`pb`) model to visualize\n    log_dir: The location for the Tensorboard log to begin visualization from.\n\n  Usage:\n    Call this function with your model location and desired log directory.\n    Launch Tensorboard by pointing it to the log directory.\n    View your imported `.pb` model as a graph.\n  '
    with session.Session(graph=ops.Graph()) as sess:
        with gfile.GFile(model_dir, 'rb') as f:
            graph_def = graph_pb2.GraphDef()
            graph_def.ParseFromString(f.read())
            importer.import_graph_def(graph_def)
        pb_visual_writer = summary.FileWriter(log_dir)
        pb_visual_writer.add_graph(sess.graph)
        print('Model Imported. Visualize by running: tensorboard --logdir={}'.format(log_dir))