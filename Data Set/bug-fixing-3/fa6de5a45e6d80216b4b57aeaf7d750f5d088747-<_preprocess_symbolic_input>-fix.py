def _preprocess_symbolic_input(x, data_format, mode):
    'Preprocesses a tensor encoding a batch of images.\n\n    # Arguments\n        x: Input tensor, 3D or 4D.\n        data_format: Data format of the image tensor.\n        mode: One of "caffe", "tf" or "torch".\n            - caffe: will convert the images from RGB to BGR,\n                then will zero-center each color channel with\n                respect to the ImageNet dataset,\n                without scaling.\n            - tf: will scale pixels between -1 and 1,\n                sample-wise.\n            - torch: will scale pixels between 0 and 1 and then\n                will normalize each channel with respect to the\n                ImageNet dataset.\n\n    # Returns\n        Preprocessed tensor.\n    '
    global _IMAGENET_MEAN
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
            if (K.ndim(x) == 3):
                x = x[::(- 1), ...]
            else:
                x = x[:, ::(- 1), ...]
        else:
            x = x[..., ::(- 1)]
        mean = [103.939, 116.779, 123.68]
        std = None
    if (_IMAGENET_MEAN is None):
        _IMAGENET_MEAN = K.constant((- np.array(mean)))
    if (K.dtype(x) != K.dtype(_IMAGENET_MEAN)):
        x = K.bias_add(x, K.cast(_IMAGENET_MEAN, K.dtype(x)), data_format)
    else:
        x = K.bias_add(x, _IMAGENET_MEAN, data_format)
    if (std is not None):
        x /= std
    return x