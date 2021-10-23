def run_bottleneck_on_image(sess, image_data, image_data_tensor, bottleneck_tensor):
    "Runs inference on an image to extract the 'bottleneck' summary layer.\n\n  Args:\n    sess: Current active TensorFlow Session.\n    image_data: String of raw JPEG data.\n    image_data_tensor: Input data layer in the graph.\n    bottleneck_tensor: Layer before the final softmax.\n\n  Returns:\n    Numpy array of bottleneck values.\n  "
    bottleneck_values = sess.run(bottleneck_tensor, {
        image_data_tensor: image_data,
    })
    bottleneck_values = np.squeeze(bottleneck_values)
    return bottleneck_values