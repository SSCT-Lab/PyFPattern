def main():
    'Entrypoint for test_converter'
    parser = argparse.ArgumentParser(description='Test Caffe converter')
    parser.add_argument('--cpu', action='store_true', help='use cpu?')
    parser.add_argument('--image_url', type=str, default='http://writm.com/wp-content/uploads/2016/08/Cat-hd-wallpapers.jpg', help='input image to test inference, can be either file path or url')
    args = parser.parse_args()
    if args.cpu:
        gpus = [(- 1)]
        batch_size = 32
    else:
        gpus = mx.test_utils.list_gpus()
        assert gpus, 'At least one GPU is needed to run test_converter in GPU mode'
        batch_size = (32 * len(gpus))
    models = ['bvlc_googlenet', 'vgg-16', 'resnet-50']
    val = download_data()
    for m in models:
        test_model_weights_and_outputs(m, args.image_url, gpus[0])
        test_imagenet_model_performance(m, val, gpus, batch_size)