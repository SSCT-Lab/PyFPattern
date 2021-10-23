def _preprocess_numpy_input(x, data_format, mode):
    'Preprocesses a Numpy array encoding a batch of images.\n\n    # Arguments\n        x: Input array, 3D or 4D.\n        data_format: Data format of the image array.\n        mode: One of "caffe", "tf".\n            - caffe: will convert the images from RGB to BGR,\n                then will zero-center each color channel with\n                respect to the ImageNet dataset,\n                without scaling.\n            - tf: will scale pixels between -1 and 1,\n                sample-wise.\n\n    # Returns\n        Preprocessed Numpy array.\n    '
    if (mode == 'tf'):
        x /= 127.5
        x -= 1.0
        return x
    if (mode == 'torch'):
        x /= 255.0
        mean = [0.485, 0.456, 0.406]
        std = [0.229, 0.224, 0.225]
    else:
        if (data_format == 'channels_first'):
            if (x.ndim == 3):
                x = x[::(- 1), ...]
            else:
                x = x[:, ::(- 1), ...]
        else:
            x = x[..., ::(- 1)]
        mean = [103.939, 116.779, 123.68]
        std = None
    if (data_format == 'channels_first'):
        if (x.ndim == 3):
            x[0, :, :] -= mean[0]
            x[1, :, :] -= mean[1]
            x[2, :, :] -= mean[2]
            if (std is not None):
                x[0, :, :] /= std[0]
                x[1, :, :] /= std[1]
                x[2, :, :] /= std[2]
        else:
            x[:, 0, :, :] -= mean[0]
            x[:, 1, :, :] -= mean[1]
            x[:, 2, :, :] -= mean[2]
            if (std is not None):
                x[:, 0, :, :] /= std[0]
                x[:, 1, :, :] /= std[1]
                x[:, 2, :, :] /= std[2]
    else:
        x[(..., 0)] -= mean[0]
        x[(..., 1)] -= mean[1]
        x[(..., 2)] -= mean[2]
        if (std is not None):
            x[(..., 0)] /= std[0]
            x[(..., 1)] /= std[1]
            x[(..., 2)] /= std[2]
    return x