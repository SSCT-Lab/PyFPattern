

@tf_export('data.experimental.enumerate_dataset')
def enumerate_dataset(start=0):
    "A transformation that enumerate the elements of a dataset.\n\n  It is Similar to python's `enumerate`.\n  For example:\n\n  ```python\n  # NOTE: The following examples use `{ ... }` to represent the\n  # contents of a dataset.\n  a = { 1, 2, 3 }\n  b = { (7, 8), (9, 10) }\n\n  # The nested structure of the `datasets` argument determines the\n  # structure of elements in the resulting dataset.\n  a.apply(tf.data.experimental.enumerate(start=5)) == { (5, 1), (6, 2), (7, 3) }\n  b.apply(tf.data.experimental.enumerate()) == { (0, (7, 8)), (1, (9, 10)) }\n  ```\n\n  Args:\n    start: A `tf.int64` scalar `tf.Tensor`, representing the start\n      value for enumeration.\n\n  Returns:\n    A `Dataset` transformation function, which can be passed to\n    `tf.data.Dataset.apply`.\n  "

    def _apply_fn(dataset):
        max_value = np.iinfo(dtypes.int64.as_numpy_dtype).max
        return dataset_ops.Dataset.zip((dataset_ops.Dataset.range(start, max_value), dataset))
    return _apply_fn
