

def masked_copy_(self, *args, **kwargs):
    warnings.warn('masked_copy_ is deprecated and renamed to masked_scatter_, and will be removed in v0.3')
    return self.masked_scatter_(self, *args, **kwargs)
