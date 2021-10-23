def print_gtk(x, start_viewer=True):
    'Print to Gtkmathview, a gtk widget capable of rendering MathML.\n\n    Needs libgtkmathview-bin\n    '
    from sympy.utilities.mathml import c2p
    tmp = tempfile.mkstemp()
    with open(tmp, 'wb') as file:
        file.write(c2p(mathml(x), simple=True))
    if start_viewer:
        os.system(('mathmlviewer ' + tmp))