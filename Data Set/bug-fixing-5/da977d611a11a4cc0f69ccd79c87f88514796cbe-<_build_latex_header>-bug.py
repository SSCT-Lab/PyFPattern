@staticmethod
def _build_latex_header():
    latex_preamble = get_preamble()
    latex_fontspec = get_fontspec()
    latex_header = ['% !TeX program = {}'.format(rcParams['pgf.texsystem']), '\\documentclass{minimal}', latex_preamble, latex_fontspec, '\\begin{document}', 'text $math \\mu$', '\\typeout{pgf_backend_query_start}']
    return '\n'.join(latex_header)