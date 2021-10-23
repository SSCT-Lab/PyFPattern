def log_conditional_probability(segmented_topics, accumulator, with_std=False, with_support=False):
    "Calculate the log-conditional-probability measure which is used by coherence measures such as `U_mass`.\n    This is defined as :math:`m_{lc}(S_i) = log \\frac{P(W', W^{*}) + \\epsilon}{P(W^{*})}`.\n\n    Parameters\n    ----------\n    segmented_topics : list of lists of (int, int)\n        Output from the :func:`~gensim.topic_coherence.segmentation.s_one_pre`,\n        :func:`~gensim.topic_coherence.segmentation.s_one_one`.\n    accumulator : :class:`~gensim.topic_coherence.text_analysis.InvertedIndexAccumulator`\n        Word occurrence accumulator from :mod:`gensim.topic_coherence.probability_estimation`.\n    with_std : bool, optional\n        True to also include standard deviation across topic segment sets in addition to the mean coherence\n        for each topic.\n    with_support : bool, optional\n        True to also include support across topic segments. The support is defined as the number of pairwise\n        similarity comparisons were used to compute the overall topic coherence.\n\n    Returns\n    -------\n    list of float\n        Log conditional probabilities measurement for each topic.\n\n    Examples\n    --------\n    .. sourcecode:: pycon\n\n        >>> from gensim.topic_coherence import direct_confirmation_measure, text_analysis\n        >>> from collections import namedtuple\n        >>>\n        >>> # Create dictionary\n        >>> id2token = {1: 'test', 2: 'doc'}\n        >>> token2id = {v: k for k, v in id2token.items()}\n        >>> dictionary = namedtuple('Dictionary', 'token2id, id2token')(token2id, id2token)\n        >>>\n        >>> # Initialize segmented topics and accumulator\n        >>> segmentation = [[(1, 2)]]\n        >>>\n        >>> accumulator = text_analysis.InvertedIndexAccumulator({1, 2}, dictionary)\n        >>> accumulator._inverted_index = {0: {2, 3, 4}, 1: {3, 5}}\n        >>> accumulator._num_docs = 5\n        >>>\n        >>> # result should be ~ ln(1 / 2) = -0.693147181\n        >>> result = direct_confirmation_measure.log_conditional_probability(segmentation, accumulator)[0]\n\n    "
    topic_coherences = []
    num_docs = float(accumulator.num_docs)
    for s_i in segmented_topics:
        segment_sims = []
        for (w_prime, w_star) in s_i:
            try:
                w_star_count = accumulator[w_star]
                co_occur_count = accumulator[(w_prime, w_star)]
                m_lc_i = np.log((((co_occur_count / num_docs) + EPSILON) / (w_star_count / num_docs)))
            except KeyError:
                m_lc_i = 0.0
            segment_sims.append(m_lc_i)
        topic_coherences.append(aggregate_segment_sims(segment_sims, with_std, with_support))
    return topic_coherences