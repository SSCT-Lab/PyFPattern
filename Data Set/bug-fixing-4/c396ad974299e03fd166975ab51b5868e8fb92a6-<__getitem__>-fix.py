def __getitem__(self, author_names, eps=None):
    'Get topic distribution for input `author_names`.\n\n        Parameters\n        ----------\n        author_names : {str, list of str}\n            Name(s) of the author for which the topic distribution needs to be estimated.\n        eps : float, optional\n            The minimum probability value for showing the topics of a given author, topics with probability < `eps`\n            will be ignored.\n\n        Returns\n        -------\n        list of (int, float) **or** list of list of (int, float)\n            Topic distribution for the author(s), type depends on type of `author_names`.\n\n        '
    if isinstance(author_names, list):
        items = []
        for a in author_names:
            items.append(self.get_author_topics(a, minimum_probability=eps))
    else:
        items = self.get_author_topics(author_names, minimum_probability=eps)
    return items