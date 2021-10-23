def index_table_from_tensor(mapping, num_oov_buckets=0, default_value=(- 1), hasher_spec=FastHashSpec, dtype=dtypes.string, name=None):
    'Returns a lookup table that converts a string tensor into int64 IDs.\n\n  This operation constructs a lookup table to convert tensor of strings into\n  int64 IDs. The mapping can be initialized from a string `mapping` 1-D tensor\n  where each element is a key and corresponding index within the tensor is the\n  value.\n\n  Any lookup of an out-of-vocabulary token will return a bucket ID based on its\n  hash if `num_oov_buckets` is greater than zero. Otherwise it is assigned the\n  `default_value`.\n  The bucket ID range is `[mapping size, mapping size + num_oov_buckets]`.\n\n  The underlying table must be initialized by calling\n  `tf.tables_initializer.run()` or `table.init.run()` once.\n\n  Elements in `mapping` cannot have duplicates, otherwise when executing the\n  table initializer op, it will throw a `FailedPreconditionError`.\n\n  Sample Usages:\n\n  ```python\n  mapping_strings = tf.constant(["emerson", "lake", "palmer"])\n  table = tf.contrib.lookup.index_table_from_tensor(\n      mapping=mapping_strings, num_oov_buckets=1, default_value=-1)\n  features = tf.constant(["emerson", "lake", "and", "palmer"])\n  ids = table.lookup(features)\n  ...\n  tf.tables_initializer().run()\n\n  ids.eval()  ==> [0, 1, 4, 2]\n  ```\n\n  Args:\n    mapping: A 1-D `Tensor` that specifies the mapping of keys to indices. The\n      type of this object must be castable to `dtype`.\n    num_oov_buckets: The number of out-of-vocabulary buckets.\n    default_value: The value to use for out-of-vocabulary feature values.\n      Defaults to -1.\n    hasher_spec: A `HasherSpec` to specify the hash function to use for\n      assignment of out-of-vocabulary buckets.\n    dtype: The type of values passed to `lookup`. Only string and integers are\n      supported.\n    name: A name for this op (optional).\n\n  Returns:\n    The lookup table to map an input `Tensor` to index `int64` `Tensor`.\n\n  Raises:\n    ValueError: If `mapping` is invalid.\n    ValueError: If `num_oov_buckets` is negative.\n  '
    if (mapping is None):
        raise ValueError('mapping must be specified.')
    return lookup_ops.index_table_from_tensor(vocabulary_list=mapping, num_oov_buckets=num_oov_buckets, default_value=default_value, hasher_spec=hasher_spec, dtype=dtype, name=name)