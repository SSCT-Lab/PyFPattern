def print_gtk(x, start_viewer=True):
    'Print to Gtkmathview, a gtk widget capable of rendering MathML.\n\n    Needs libgtkmathview-bin'
    with tempfile.NamedTemporaryFile('w') as file:
        file.write(c2p(mathml(x), simple=True))
        file.flush()
        if start_viewer:
            subprocess.check_call(('mathmlviewer', file.name))