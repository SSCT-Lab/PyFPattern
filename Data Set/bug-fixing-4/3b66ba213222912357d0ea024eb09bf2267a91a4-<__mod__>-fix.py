def __mod__(self, other):
    'Returns `self` modulo `other`.\n\n    Dimension moduli are computed as follows:\n\n    ```python\n    tf.compat.v1.Dimension(m)    % tf.compat.v1.Dimension(n)     ==\n    tf.compat.v1.Dimension(m % n)\n    tf.compat.v1.Dimension(m)    % tf.compat.v1.Dimension(None)  # equiv. to\n    tf.compat.v1.Dimension(None)\n    tf.compat.v1.Dimension(None) % tf.compat.v1.Dimension(n)     # equiv. to\n    tf.compat.v1.Dimension(None)\n    tf.compat.v1.Dimension(None) % tf.compat.v1.Dimension(None)  # equiv. to\n    tf.compat.v1.Dimension(None)\n    ```\n\n    Args:\n      other: Another Dimension, or a value accepted by `as_dimension`.\n\n    Returns:\n      A Dimension whose value is `self` modulo `other`.\n    '
    other = as_dimension(other)
    if ((self._value is None) or (other.value is None)):
        return Dimension(None)
    else:
        return Dimension((self._value % other.value))