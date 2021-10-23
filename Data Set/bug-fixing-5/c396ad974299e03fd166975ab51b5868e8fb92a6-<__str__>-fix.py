def __str__(self):
    'Get a string representation of object.\n\n        Returns\n        -------\n        str\n            String representation of current instance.\n\n        '
    return ('AuthorTopicModel(num_terms=%s, num_topics=%s, num_authors=%s, decay=%s, chunksize=%s)' % (self.num_terms, self.num_topics, self.num_authors, self.decay, self.chunksize))