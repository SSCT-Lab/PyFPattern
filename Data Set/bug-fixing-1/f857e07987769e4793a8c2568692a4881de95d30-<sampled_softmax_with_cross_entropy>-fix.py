

def sampled_softmax_with_cross_entropy(logits, label, num_samples, num_true=1, remove_accidental_hits=True, use_customized_samples=False, customized_samples=None, customized_probabilities=None, seed=0):
    "\n    **Sampled Softmax With Cross Entropy Operator.**\n\n    Cross entropy loss with sampled softmax is used as the output layer for \n    larger output classes extensively. This operator samples a number of samples\n    for all examples, and computes the softmax normalized values for each \n    row of the sampled tensor, after which cross-entropy loss is computed. \n\n    Because this operator performs a softmax on logits internally, it expects\n    unscaled logits. This operator should not be used with the output of\n    softmax operator since that would produce incorrect results.\n    \n    For examples with T true labels (T >= 1), we assume that each true label has\n    a probability of 1/T. For each sample, S samples are generated using a\n    log uniform distribution. True labels are concatenated with these samples to\n    form T + S samples for each example. So, assume the shape of logits is\n    [N x K], the shape for samples is [N x (T+S)]. For each sampled label, a \n    probability is calculated, which corresponds to the Q(y|x) in \n    [Jean et al., 2014](http://arxiv.org/abs/1412.2007).\n    \n    Logits are sampled according to the sampled labels. Then if \n    remove_accidental_hits is True, if a sample[i, j] accidentally hits true \n    labels, then the corresponding sampled_logits[i, j] is minus by 1e20 to \n    make its softmax result close to zero. Then sampled logits are subtracted by\n    logQ(y|x), these sampled logits and re-indexed labels are used to compute \n    a softmax with cross entropy.\n\n    Args:\n        logits (Variable): The unscaled log probabilities, which is a 2-D tensor\n            with shape [N x K]. N is the batch_size, and K is the class number.\n        label (Variable): The ground truth which is a 2-D tensor. Label is a \n            Tensor<int64> with shape [N x T], where T is the number of true \n            labels per example. \n        num_samples (int): The number for each example, num_samples should be \n            less than the number of class.\n        num_true(int): The number of target classes per training example.\n        remove_accidental_hits (bool): A flag indicating whether to remove \n            accidental hits when sampling. If True and if a sample[i, j] \n            accidentally hits true labels, then the corresponding \n            sampled_logits[i, j] is minus by 1e20 to make its softmax result \n            close to zero. Default is True.\n        use_customized_samples (bool): Whether to use custom samples and probabities to sample\n            logits.\n        customized_samples (Variable): User defined samples, which is a 2-D tensor\n            with shape [N, T + S]. S is the num_samples, and T is the number of true \n            labels per example. \n        customized_probabilities (Variable): User defined probabilities of samples, \n            a 2-D tensor which has the same shape with customized_samples.\n        seed (int): The random seed for generating random number, which is used\n            in the process of sampling. Default is 0.\n\n    Returns:\n        Variable: Return the cross entropy loss which is a 2-D tensor with shape\n                  [N x 1].\n\n    Examples:\n        .. code-block:: python\n\n            logits = fluid.layers.data(name='data', shape=[256], dtype='float32')\n            label = fluid.layers.data(name='label', shape=[5], dtype='int64')\n            fc = fluid.layers.fc(input=data, size=100)\n            out = fluid.layers.sampled_softmax_with_cross_entropy(\n                logits=fc, label=label, num_samples=25)\n    "
    helper = LayerHelper('sample_logits', **locals())
    samples = helper.create_variable_for_type_inference(dtype='int64')
    probabilities = helper.create_variable_for_type_inference(dtype=logits.dtype)
    sampled_logits = helper.create_variable_for_type_inference(dtype=logits.dtype)
    sampled_label = helper.create_variable_for_type_inference(dtype='int64')
    sampled_softlabel = helper.create_variable_for_type_inference(dtype=logits.dtype)
    helper.append_op(type='sample_logits', inputs={
        'Logits': logits,
        'Labels': label,
        'CustomizedSamples': customized_samples,
        'CustomizedProbabilities': customized_probabilities,
    }, outputs={
        'Samples': samples,
        'Probabilities': probabilities,
        'SampledLabels': sampled_label,
        'SampledLogits': sampled_logits,
    }, attrs={
        'use_customized_samples': use_customized_samples,
        'uniq': True,
        'remove_accidental_hits': remove_accidental_hits,
        'num_samples': num_samples,
        'seed': seed,
    })
    loss = helper.create_variable_for_type_inference(dtype=logits.dtype)
    softmax = helper.create_variable_for_type_inference(dtype=logits.dtype)
    helper.append_op(type='one_hot', inputs={
        'X': sampled_label,
    }, attrs={
        'depth': (num_samples + 1),
    }, outputs={
        'Out': sampled_softlabel,
    })
    helper.append_op(type='softmax_with_cross_entropy', inputs={
        'Logits': sampled_logits,
        'Label': sampled_softlabel,
    }, outputs={
        'Softmax': softmax,
        'Loss': loss,
    }, attrs={
        'soft_label': True,
        'ignore_index': False,
        'numeric_stable_mode': False,
    })
    return (loss / num_true)
