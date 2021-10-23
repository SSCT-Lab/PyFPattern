def get_author_topics(self, author_name, minimum_probability=None):
    '\n        Return topic distribution the given author.\n\n        Input as as a list of\n        (topic_id, topic_probability) 2-tuples.\n        Ignore topics with very low probability (below `minimum_probability`).\n        Obtaining topic probabilities of each word, as in LDA (via `per_word_topics`),\n        is not supported.\n        '
    author_id = self.author2id[author_name]
    if (minimum_probability is None):
        minimum_probability = self.minimum_probability
    minimum_probability = max(minimum_probability, 1e-08)
    topic_dist = (self.state.gamma[author_id, :] / sum(self.state.gamma[author_id, :]))
    author_topics = [(topicid, topicvalue) for (topicid, topicvalue) in enumerate(topic_dist) if (topicvalue >= minimum_probability)]
    return author_topics