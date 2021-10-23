def make_sampling_table(size, sampling_factor=1e-05):
    "Generates a word rank-based probabilistic sampling table.\n\n    This generates an array where the ith element\n    is the probability that a word of rank i would be sampled,\n    according to the sampling distribution used in word2vec.\n\n    The word2vec formula is:\n        p(word) = min(1, sqrt(word.frequency/sampling_factor) / (word.frequency/sampling_factor))\n\n    We assume that the word frequencies follow Zipf's law (s=1) to derive\n    a numerical approximation of frequency(rank):\n       frequency(rank) ~ 1/(rank * (log(rank) + gamma) + 1/2 - 1/(12*rank))\n        where gamma is the Euler-Mascheroni constant.\n\n    # Arguments\n        size: int, number of possible words to sample.\n        sampling_factor: the sampling factor in the word2vec formula.\n\n    # Returns\n        A 1D Numpy array of length `size` where the ith entry\n        is the probability that a word of rank i should be sampled.\n    "
    gamma = 0.577
    rank = np.array(list(range(size)))
    rank[0] = 1
    inv_fq = (((rank * (np.log(rank) + gamma)) + 0.5) - (1.0 / (12.0 * rank)))
    f = (sampling_factor * inv_fq)
    return np.minimum(1.0, (f / np.sqrt(f)))