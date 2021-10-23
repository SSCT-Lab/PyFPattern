def __getitem__(self, author_names, eps=None):
    '\n        Return topic distribution for input author as a list of\n        (topic_id, topic_probabiity) 2-tuples.\n\n        Ingores topics with probaility less than `eps`.\n\n        Do not call this method directly, instead use `model[author_names]`.\n\n        '
    if isinstance(author_names, list):
        items = []
        for a in author_names:
            items.append(self.get_author_topics(a, minimum_probability=eps))
    else:
        items = self.get_author_topics(author_names, minimum_probability=eps)
    return items