@skip_doctest
def extract_symbols(code, symbols):
    '\n    Return a tuple  (blocks, not_found)\n    where ``blocks`` is a list of code fragments\n    for each symbol parsed from code, and ``not_found`` are\n    symbols not found in the code.\n\n    For example::\n\n        >>> code = \'\'\'a = 10\n\n        def b(): return 42\n\n        class A: pass\'\'\'\n\n        >>> extract_symbols(code, \'A,b,z\')\n        (["class A: pass", "def b(): return 42"], [\'z\'])\n    '
    symbols = symbols.split(',')
    py_code = ast.parse(code)
    marks = [(getattr(s, 'name', None), s.lineno) for s in py_code.body]
    code = code.split('\n')
    symbols_lines = {
        
    }
    end = len(code)
    for (name, start) in reversed(marks):
        while (not code[(end - 1)].strip()):
            end -= 1
        if name:
            symbols_lines[name] = ((start - 1), end)
        end = (start - 1)
    blocks = []
    not_found = []
    for symbol in symbols:
        if (symbol in symbols_lines):
            (start, end) = symbols_lines[symbol]
            blocks.append(('\n'.join(code[start:end]) + '\n'))
        else:
            not_found.append(symbol)
    return (blocks, not_found)