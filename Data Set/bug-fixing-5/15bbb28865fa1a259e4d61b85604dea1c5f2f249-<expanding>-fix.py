@Substitution(name='groupby')
@Appender(_doc_template)
def expanding(self, *args, **kwargs):
    '\n        Return an expanding grouper, providing expanding\n        functionality per group\n\n        '
    from pandas.core.window import ExpandingGroupby
    return ExpandingGroupby(self, *args, **kwargs)