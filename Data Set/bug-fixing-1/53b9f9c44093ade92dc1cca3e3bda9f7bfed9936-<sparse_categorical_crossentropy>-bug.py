

def sparse_categorical_crossentropy(output, target, from_logits=False):
    target = T.cast(T.flatten(target), 'int32')
    target = T.extra_ops.to_one_hot(target, num_classes=output.shape[(- 1)])
    target = reshape(target, shape(output))
    return categorical_crossentropy(output, target, from_logits)
