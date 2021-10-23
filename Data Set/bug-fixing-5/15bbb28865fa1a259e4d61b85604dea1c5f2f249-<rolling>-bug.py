@Substitution(name='groupby')
@Appender(_doc_template)
def rolling(self, *args, **kwargs):
    '\n        Return a rolling grouper, providing rolling\n        functionaility per group\n\n        '
    from pandas.core.window import RollingGroupby
    return RollingGroupby(self, *args, **kwargs)