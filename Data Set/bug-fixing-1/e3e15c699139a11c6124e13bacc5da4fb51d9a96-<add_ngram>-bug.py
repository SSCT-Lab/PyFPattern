

def add_ngram(sequences, token_indice, ngram_range=2):
    '\n    Augment the input list of list (sequences) by appending n-grams values.\n\n    Example: adding bi-gram\n    >>> sequences = [[1, 3, 4, 5], [1, 3, 7, 9, 2]]\n    >>> token_indice = {(1, 3): 1337, (9, 2): 42, (4, 5): 2017}\n    >>> add_ngram(sequences, token_indice, ngram_range=2)\n    [[1, 3, 4, 5, 1337, 2017], [1, 3, 7, 9, 2, 1337, 42]]\n\n    Example: adding tri-gram\n    >>> sequences = [[1, 3, 4, 5], [1, 3, 7, 9, 2]]\n    >>> token_indice = {(1, 3): 1337, (9, 2): 42, (4, 5): 2017, (7, 9, 2): 2018}\n    >>> add_ngram(sequences, token_indice, ngram_range=3)\n    [[1, 3, 4, 5, 1337], [1, 3, 7, 9, 2, 1337, 2018]]\n    '
    new_sequences = []
    for input_list in sequences:
        new_list = input_list[:]
        for i in range(((len(new_list) - ngram_range) + 1)):
            for ngram_value in range(2, (ngram_range + 1)):
                ngram = tuple(new_list[i:(i + ngram_value)])
                if (ngram in token_indice):
                    new_list.append(token_indice[ngram])
        new_sequences.append(new_list)
    return new_sequences
