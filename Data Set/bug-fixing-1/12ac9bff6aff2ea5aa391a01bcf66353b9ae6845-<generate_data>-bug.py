

def generate_data(args):

    def prepare_dir(path):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)
    node_cases = node_test.collect_testcases()
    for case in node_cases:
        output_dir = os.path.join(args.output, 'node', case.name)
        prepare_dir(output_dir)
        with open(os.path.join(output_dir, 'node.pb'), 'wb') as f:
            f.write(case.node.SerializeToString())
        for (i, input_np) in enumerate(case.inputs):
            tensor = numpy_helper.from_array(input_np, case.node.input[i])
            with open(os.path.join(output_dir, 'input_{}.pb'.format(i)), 'wb') as f:
                f.write(tensor.SerializeToString())
        for (i, output_np) in enumerate(case.outputs):
            tensor = numpy_helper.from_array(output_np, case.node.output[i])
            with open(os.path.join(output_dir, 'output_{}.pb'.format(i)), 'wb') as f:
                f.write(tensor.SerializeToString())
    model_cases = model_test.collect_testcases()
    for case in model_cases:
        output_dir = os.path.join(args.output, 'model', case.name)
        prepare_dir(output_dir)
        with open(os.path.join(output_dir, 'data.json'), 'w') as f:
            json.dump({
                'url': case.url,
                'model_name': case.model_name,
            }, f, sort_keys=True)
