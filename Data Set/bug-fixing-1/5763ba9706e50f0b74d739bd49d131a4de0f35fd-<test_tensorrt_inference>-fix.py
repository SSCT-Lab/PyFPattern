

def test_tensorrt_inference():
    'Run LeNet-5 inference comparison between MXNet and TensorRT.'
    check_tensorrt_installation()
    mnist = mx.test_utils.get_mnist()
    num_epochs = 10
    batch_size = 128
    model_name = 'lenet5'
    model_dir = os.getenv('LENET_MODEL_DIR', '/tmp')
    model_file = ('%s/%s-symbol.json' % (model_dir, model_name))
    params_file = ('%s/%s-%04d.params' % (model_dir, model_name, num_epochs))
    (_, _, _, all_test_labels) = get_iters(mnist, batch_size)
    (sym, arg_params, aux_params) = mx.model.load_checkpoint(model_name, num_epochs)
    print('LeNet-5 test')
    print('Running inference in MXNet')
    mx_pct = run_inference(sym, arg_params, aux_params, mnist, all_test_labels, batch_size=batch_size, use_tensorrt=False)
    print('Running inference in MXNet-TensorRT')
    trt_pct = run_inference(sym, arg_params, aux_params, mnist, all_test_labels, batch_size=batch_size, use_tensorrt=True)
    print(('MXNet accuracy: %f' % mx_pct))
    print(('MXNet-TensorRT accuracy: %f' % trt_pct))
    absolute_accuracy_diff = abs((mx_pct - trt_pct))
    epsilon = 0.0101
    assert (absolute_accuracy_diff < epsilon), ('Absolute diff. between MXNet & TensorRT accuracy (%f) exceeds threshold (%f):\n           MXNet = %f, TensorRT = %f' % (absolute_accuracy_diff, epsilon, mx_pct, trt_pct))
