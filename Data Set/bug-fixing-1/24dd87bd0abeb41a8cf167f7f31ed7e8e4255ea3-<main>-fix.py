

def main():
    base_dir = (os.getcwd() + os.sep)
    docs_dir = os.path.abspath('docs/docsite')
    cmd = ['make', 'singlehtmldocs']
    sphinx = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=docs_dir)
    (stdout, stderr) = sphinx.communicate()
    if (sphinx.returncode != 0):
        print(("Command '%s' failed with status code: %d" % (' '.join(cmd), sphinx.returncode)))
        print(stdout)
        print(stderr)
        return
    with open('docs/docsite/rst_warnings', 'r') as warnings_fd:
        output = warnings_fd.read().strip()
        lines = output.splitlines()
    known_warnings = {
        'block-quote-missing-blank-line': '^Block quote ends without a blank line; unexpected unindent.$',
        'literal-block-lex-error': '^Could not lex literal_block as "[^"]*". Highlighting skipped.$',
        'duplicate-label': '^duplicate label ',
        'undefined-label': 'undefined label: ',
        'unknown-document': 'unknown document: ',
        'toc-tree-missing-document': 'toctree contains reference to nonexisting document ',
        'reference-target-not-found': '[^ ]* reference target not found: ',
        'not-in-toc-tree': "document isn't included in any toctree$",
        'unexpected-indentation': '^Unexpected indentation.$',
        'definition-list-missing-blank-line': '^Definition list ends without a blank line; unexpected unindent.$',
        'explicit-markup-missing-blank-line': 'Explicit markup ends without a blank line; unexpected unindent.$',
        'toc-tree-glob-pattern-no-match': "^toctree glob pattern '[^']*' didn't match any documents$",
        'unknown-interpreted-text-role': '^Unknown interpreted text role "[^"]*".$',
    }
    ignore_codes = ['reference-target-not-found']
    used_ignore_codes = set()
    for line in lines:
        match = re.search('^(?P<path>[^:]+):((?P<line>[0-9]+):)?((?P<column>[0-9]+):)? (?P<level>WARNING|ERROR): (?P<message>.*)$', line)
        if (not match):
            path = 'docs/docsite/rst/index.rst'
            lineno = 0
            column = 0
            code = 'unknown'
            message = line
            print(('%s:%d:%d: %s: %s' % (path, lineno, column, code, message)))
            continue
        path = match.group('path')
        lineno = int((match.group('line') or 0))
        column = int((match.group('column') or 0))
        level = match.group('level').lower()
        message = match.group('message')
        path = os.path.abspath(path)
        if path.startswith(base_dir):
            path = path[len(base_dir):]
        if path.startswith('rst/'):
            path = ('docs/docsite/' + path)
        if (level == 'warning'):
            code = 'warning'
            for (label, pattern) in known_warnings.items():
                if re.search(pattern, message):
                    code = label
                    break
        else:
            code = 'error'
        if ((code == 'not-in-toc-tree') and path.startswith('docs/docsite/rst/modules/')):
            continue
        if (code in ignore_codes):
            used_ignore_codes.add(code)
            continue
        print(('%s:%d:%d: %s: %s' % (path, lineno, column, code, message)))
    unused_ignore_codes = (set(ignore_codes) - used_ignore_codes)
    for code in unused_ignore_codes:
        print(('test/sanity/code-smell/docs-build.py:0:0: remove `%s` from the `ignore_codes` list as it is no longer needed' % code))
