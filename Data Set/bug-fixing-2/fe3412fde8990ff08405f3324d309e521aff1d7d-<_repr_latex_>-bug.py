

def _repr_latex_(self):
    (off, scale) = self.mapparms()
    if ((off == 0) and (scale == 1)):
        term = 'x'
        needs_parens = False
    elif (scale == 1):
        term = '{} + x'.format(self._repr_latex_scalar(off))
        needs_parens = True
    elif (off == 0):
        term = '{}x'.format(self._repr_latex_scalar(scale))
        needs_parens = True
    else:
        term = '{} + {}x'.format(self._repr_latex_scalar(off), self._repr_latex_scalar(scale))
        needs_parens = True
    filtered_coeffs = [(i, c) for (i, c) in enumerate(self.coef)]
    mute = '\\color{{LightGray}}{{{}}}'.format
    parts = []
    for (i, c) in enumerate(self.coef):
        if (i == 0):
            coef_str = '{}'.format(self._repr_latex_scalar(c))
        elif (not isinstance(c, numbers.Real)):
            coef_str = ' + ({})'.format(self._repr_latex_scalar(c))
        elif (not np.signbit(c)):
            coef_str = ' + {}'.format(self._repr_latex_scalar(c))
        else:
            coef_str = ' - {}'.format(self._repr_latex_scalar((- c)))
        term_str = self._repr_latex_term(i, term, needs_parens)
        if (term_str == '1'):
            part = coef_str
        else:
            part = '{}\\,{}'.format(coef_str, term_str)
        if (c == 0):
            part = mute(part)
        parts.append(part)
    if parts:
        body = ''.join(parts)
    else:
        body = '0'
    return '$x \\mapsto {}$'.format(body)
