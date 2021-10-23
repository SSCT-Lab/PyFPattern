def discriminative_margin_based_clustering_loss(embeddings, labels, delta_v, delta_d, max_embedding_dim, norm=1, alpha=1.0, beta=1.0, gamma=0.001):
    'Discriminative margin-based clustering loss function\n\n    This is the implementation of the following paper:\n    https://arxiv.org/abs/1708.02551\n    This method is a semi-supervised solution to instance segmentation.\n    It calculates pixel embeddings, and calculates three different terms\n    based on those embeddings and applies them as loss.\n    The main idea is that the pixel embeddings\n    for same instances have to be closer to each other (pull force),\n    for different instances, they have to be further away (push force).\n    The loss also brings a weak regularization term to prevent overfitting.\n    This loss function calculates the following three parameters:\n\n    Variance Loss\n        Loss to penalize distances between pixels which are belonging\n        to the same instance. (Pull force)\n\n    Distance loss\n        Loss to penalize distances between the centers of instances.\n        (Push force)\n\n    Regularization loss\n        Small regularization loss to penalize weights against overfitting.\n\n    Args:\n        embeddings (:class:`~chainer.Variable` or :class:`numpy.ndarray` or         :class:`cupy.ndarray`):             predicted embedding vectors\n            (batch size, max embedding dimensions, height, width)\n\n        labels (:class:`numpy.ndarray` or :class:`cupy.ndarray`):             instance segmentation ground truth\n            each unique value has to be denoting one instance\n            (batch size, height, width)\n        delta_v (float): Minimum distance to start penalizing variance\n        delta_d (float): Maximum distance to stop penalizing distance\n        max_embedding_dim (int): Maximum number of embedding dimensions\n        norm (int): Norm to calculate pixels and cluster center distances\n        alpha (float): Weight for variance loss\n        beta (float): Weight for distance loss\n        gamma (float): Weight for regularization loss\n\n    Returns:\n        :class:`tuple` of :class:`chainer.Variable`:\n        - *Variance loss*: Variance loss multiplied by ``alpha``\n        - *Distance loss*: Distance loss multiplied by ``beta``\n        - *Regularization loss*: Regularization loss multiplied by ``gamma``\n\n    '
    loss = DiscriminativeMarginBasedClusteringLoss(delta_v, delta_d, max_embedding_dim, norm, alpha, beta, gamma)
    return loss(embeddings, labels)