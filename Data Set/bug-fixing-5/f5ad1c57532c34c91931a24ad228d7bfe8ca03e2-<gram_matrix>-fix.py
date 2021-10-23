def gram_matrix(x):
    assert (K.ndim(x) == 3)
    if (K.image_dim_ordering() == 'th'):
        features = K.batch_flatten(x)
    else:
        features = K.batch_flatten(K.permute_dimensions(x, (2, 0, 1)))
    gram = K.dot(features, K.transpose(features))
    return gram