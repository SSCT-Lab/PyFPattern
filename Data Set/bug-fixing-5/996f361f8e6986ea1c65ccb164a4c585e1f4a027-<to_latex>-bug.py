@Substitution(header='Write out the column names. If a list of strings is given, it is assumed to be aliases for the column names.')
@Appender((_shared_docs['to_latex'] % _shared_doc_kwargs))
def to_latex(self, buf=None, columns=None, col_space=None, header=True, index=True, na_rep='NaN', formatters=None, float_format=None, sparsify=None, index_names=True, bold_rows=False, column_format=None, longtable=None, escape=None, encoding=None, decimal='.', multicolumn=None, multicolumn_format=None, multirow=None):
    if (self.ndim == 1):
        self = self.to_frame()
    if (longtable is None):
        longtable = config.get_option('display.latex.longtable')
    if (escape is None):
        escape = config.get_option('display.latex.escape')
    if (multicolumn is None):
        multicolumn = config.get_option('display.latex.multicolumn')
    if (multicolumn_format is None):
        multicolumn_format = config.get_option('display.latex.multicolumn_format')
    if (multirow is None):
        multirow = config.get_option('display.latex.multirow')
    formatter = DataFrameFormatter(self, buf=buf, columns=columns, col_space=col_space, na_rep=na_rep, header=header, index=index, formatters=formatters, float_format=float_format, bold_rows=bold_rows, sparsify=sparsify, index_names=index_names, escape=escape, decimal=decimal)
    formatter.to_latex(column_format=column_format, longtable=longtable, encoding=encoding, multicolumn=multicolumn, multicolumn_format=multicolumn_format, multirow=multirow)
    if (buf is None):
        return formatter.buf.getvalue()