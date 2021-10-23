def get_word_dict():
    '\n    Sorted the words by the frequency of words which occur in sample\n    :return:\n        words_freq_sorted\n    '
    words_freq_sorted = list()
    word_freq_dict = collections.defaultdict(int)
    download_data_if_not_yet()
    for category in movie_reviews.categories():
        for field in movie_reviews.fileids(category):
            for words in movie_reviews.words(field):
                word_freq_dict[words] += 1
    words_sort_list = six.iteritems(word_freq_dict)
    words_sort_list.sort(cmp=(lambda a, b: (b[1] - a[1])))
    for (index, word) in enumerate(words_sort_list):
        words_freq_sorted.append((word[0], index))
    return words_freq_sorted