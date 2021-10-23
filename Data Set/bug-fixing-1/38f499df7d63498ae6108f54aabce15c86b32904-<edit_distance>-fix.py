

def edit_distance(input, label, normalized=True, ignored_tokens=None):
    '\n    EditDistance operator computes the edit distances between a batch of\n    hypothesis strings and their references. Edit distance, also called\n    Levenshtein distance, measures how dissimilar two strings are by counting\n    the minimum number of operations to transform one string into anthor.\n    Here the operations include insertion, deletion, and substitution.\n\n    For example, given hypothesis string A = "kitten" and reference\n    B = "sitting", the edit distance is 3 for A will be transformed into B\n    at least after two substitutions and one insertion:\n\n    "kitten" -> "sitten" -> "sittin" -> "sitting"\n\n    The input is a LoDTensor consisting of all the hypothesis strings with\n    the total number denoted by `batch_size`, and the separation is specified\n    by the LoD information. And the `batch_size` reference strings are arranged\n    in order in the same way in the input LoDTensor.\n\n    The output contains the `batch_size` results and each stands for the edit\n    distance for a pair of strings respectively. If Attr(normalized) is true,\n    the edit distance will be divided by the length of reference string.\n\n    Args:\n        input(Variable): The indices for hypothesis strings.\n        label(Variable): The indices for reference strings.\n        normalized(bool, default True): Indicated whether to normalize the edit distance by\n                          the length of reference string.\n        ignored_tokens(list<int>, default None): Tokens that should be removed before\n                                     calculating edit distance.\n        name (str): The name of this layer. It is optional.\n\n    Returns:\n        Variable: sequence-to-sequence edit distance in shape [batch_size, 1].\n\n    Examples:\n        .. code-block:: python\n\n            x = fluid.layers.data(name=\'x\', shape=[1], dtype=\'float32\')\n            y = fluid.layers.data(name=\'y\', shape=[1], dtype=\'float32\')\n            cost = fluid.layers.edit_distance(input=x,label=y)\n    '
    helper = LayerHelper('edit_distance', **locals())
    if ((ignored_tokens is not None) and (len(ignored_tokens) > 0)):
        erased_input = helper.create_variable_for_type_inference(dtype='int64')
        erased_label = helper.create_variable_for_type_inference(dtype='int64')
        helper.append_op(type='sequence_erase', inputs={
            'X': [input],
        }, outputs={
            'Out': [erased_input],
        }, attrs={
            'tokens': ignored_tokens,
        })
        input = erased_input
        helper.append_op(type='sequence_erase', inputs={
            'X': [label],
        }, outputs={
            'Out': [erased_label],
        }, attrs={
            'tokens': ignored_tokens,
        })
        label = erased_label
    edit_distance_out = helper.create_variable_for_type_inference(dtype='int64')
    sequence_num = helper.create_variable_for_type_inference(dtype='int64')
    helper.append_op(type='edit_distance', inputs={
        'Hyps': [input],
        'Refs': [label],
    }, outputs={
        'Out': [edit_distance_out],
        'SequenceNum': [sequence_num],
    }, attrs={
        'normalized': normalized,
    })
    return (edit_distance_out, sequence_num)
