def get_random_cached_bottlenecks(sess, image_lists, how_many, category, bottleneck_dir, image_dir, jpeg_data_tensor, bottleneck_tensor):
    'Retrieves bottleneck values for cached images.\n\n  If no distortions are being applied, this function can retrieve the cached\n  bottleneck values directly from disk for images. It picks a random set of\n  images from the specified category.\n\n  Args:\n    sess: Current TensorFlow Session.\n    image_lists: Dictionary of training images for each label.\n    how_many: The number of bottleneck values to return.\n    category: Name string of which set to pull from - training, testing, or\n    validation.\n    bottleneck_dir: Folder string holding cached files of bottleneck values.\n    image_dir: Root folder string of the subfolders containing the training\n    images.\n    jpeg_data_tensor: The layer to feed jpeg image data into.\n    bottleneck_tensor: The bottleneck output layer of the CNN graph.\n\n  Returns:\n    List of bottleneck arrays and their corresponding ground truthes.\n  '
    class_count = len(image_lists.keys())
    bottlenecks = []
    ground_truthes = []
    for unused_i in range(how_many):
        label_index = random.randrange(class_count)
        label_name = list(image_lists.keys())[label_index]
        image_index = random.randrange(65536)
        bottleneck = get_or_create_bottleneck(sess, image_lists, label_name, image_index, image_dir, category, bottleneck_dir, jpeg_data_tensor, bottleneck_tensor)
        ground_truth = np.zeros(class_count, dtype=np.float32)
        ground_truth[label_index] = 1.0
        bottlenecks.append(bottleneck)
        ground_truthes.append(ground_truth)
    return (bottlenecks, ground_truthes)