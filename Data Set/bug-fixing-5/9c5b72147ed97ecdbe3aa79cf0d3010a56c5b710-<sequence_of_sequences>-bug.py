def sequence_of_sequences(min=None, max=None):
    return All(Any(None, [Length(min=min, max=max)], tuple([Length(min=min, max=max)])), Any(None, [Any(list, tuple)], tuple([Any(list, tuple)])))