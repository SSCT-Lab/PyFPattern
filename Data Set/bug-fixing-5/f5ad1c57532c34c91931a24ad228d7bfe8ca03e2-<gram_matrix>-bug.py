def gram_matrix(x):
    assert (K.ndim(x) == 3)
    features = K.batch_flatten(x)
    gram = K.dot(features, K.transpose(features))
    return gram