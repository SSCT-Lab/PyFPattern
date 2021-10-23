def get_random_distorted_bottlenecks(sess, image_lists, how_many, category, image_dir, input_jpeg_tensor, distorted_image, resized_input_tensor, bottleneck_tensor):
    "Retrieves bottleneck values for training images, after distortions.\n\n  If we're training with distortions like crops, scales, or flips, we have to\n  recalculate the full model for every image, and so we can't use cached\n  bottleneck values. Instead we find random images for the requested category,\n  run them through the distortion graph, and then the full graph to get the\n  bottleneck results for each.\n\n  Args:\n    sess: Current TensorFlow Session.\n    image_lists: Dictionary of training images for each label.\n    how_many: The integer number of bottleneck values to return.\n    category: Name string of which set of images to fetch - training, testing,\n    or validation.\n    image_dir: Root folder string of the subfolders containing the training\n    images.\n    input_jpeg_tensor: The input layer we feed the image data to.\n    distorted_image: The output node of the distortion graph.\n    resized_input_tensor: The input node of the recognition graph.\n    bottleneck_tensor: The bottleneck output layer of the CNN graph.\n\n  Returns:\n    List of bottleneck arrays and their corresponding ground truths.\n  "
    class_count = len(image_lists.keys())
    bottlenecks = []
    ground_truths = []
    for unused_i in range(how_many):
        label_index = random.randrange(class_count)
        label_name = list(image_lists.keys())[label_index]
        image_index = random.randrange(65536)
        image_path = get_image_path(image_lists, label_name, image_index, image_dir, category)
        if (not gfile.Exists(image_path)):
            tf.logging.fatal('File does not exist %s', image_path)
        jpeg_data = gfile.FastGFile(image_path, 'rb').read()
        distorted_image_data = sess.run(distorted_image, {
            input_jpeg_tensor: jpeg_data,
        })
        bottleneck = run_bottleneck_on_image(sess, distorted_image_data, resized_input_tensor, bottleneck_tensor)
        ground_truth = np.zeros(class_count, dtype=np.float32)
        ground_truth[label_index] = 1.0
        bottlenecks.append(bottleneck)
        ground_truths.append(ground_truth)
    return (bottlenecks, ground_truths)