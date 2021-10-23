def sparse_categorical_crossentropy(target, output, from_logits=False):
    target = T.cast(T.flatten(target), 'int32')
    target = T.extra_ops.to_one_hot(target, nb_class=output.shape[(- 1)])
    target = reshape(target, shape(output))
    return categorical_crossentropy(target, output, from_logits)