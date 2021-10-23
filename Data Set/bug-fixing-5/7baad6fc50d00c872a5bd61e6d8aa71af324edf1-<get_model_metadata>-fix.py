def get_model_metadata(model_file):
    "\n    Returns the name and shape information of input and output tensors of the given ONNX model file.\n\n    Parameters\n    ----------\n    model_file : str\n        ONNX model file name\n\n    Returns\n    -------\n    model_metadata : dict\n        A dictionary object mapping various metadata to its corresponding value.\n        The dictionary will have the following template::\n\n          'input_tensor_data' : list of tuples representing the shape of the input paramters\n          'output_tensor_data' : list of tuples representing the shape of the output of the model\n    "
    graph = GraphProto()
    try:
        import onnx
    except ImportError:
        raise ImportError(('Onnx and protobuf need to be installed. ' + 'Instructions to install - https://github.com/onnx/onnx'))
    model_proto = onnx.load_model(model_file)
    metadata = graph.get_graph_metadata(model_proto.graph)
    return metadata