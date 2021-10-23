def extract_symbols(code, symbols):
    "\n    Return a tuple  (blocks, not_found)\n    where ``blocks`` is a list of code fragments\n    for each symbol parsed from code, and ``not_found`` are\n    symbols not found in the code.\n\n    For example::\n\n        In [1]: code = '''a = 10\n           ...: def b(): return 42\n           ...: class A: pass'''\n\n        In [2]: extract_symbols(code, 'A,b,z')\n        Out[2]: (['class A: pass\\n', 'def b(): return 42\\n'], ['z'])\n    "
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