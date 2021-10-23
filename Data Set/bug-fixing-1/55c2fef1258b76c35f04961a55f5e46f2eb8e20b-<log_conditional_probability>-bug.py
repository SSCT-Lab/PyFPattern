

def log_conditional_probability(segmented_topics, per_topic_postings, num_docs):
    "\n    This function calculates the log-conditional-probability measure\n    which is used by coherence measures such as U_mass.\n    This is defined as: m_lc(S_i) = log[(P(W', W*) + e) / P(W*)]\n\n    Args:\n    ----\n    segmented_topics : Output from the segmentation module of the segmented topics. Is a list of list of tuples.\n    per_topic_postings : Output from the probability_estimation module. Is a dictionary of the posting list of all topics.\n    num_docs : Total number of documents in corresponding corpus.\n\n    Returns:\n    -------\n    m_lc : List of log conditional probability measure on each set in segmented topics.\n    "
    m_lc = []
    for s_i in segmented_topics:
        for (w_prime, w_star) in s_i:
            w_prime_docs = per_topic_postings[w_prime]
            w_star_docs = per_topic_postings[w_star]
            co_docs = w_prime_docs.intersection(w_star_docs)
            m_lc_i = np.log((((len(co_docs) / float(num_docs)) + EPSILON) / (len(w_star_docs) / float(num_docs))))
            m_lc.append(m_lc_i)
    return m_lc
