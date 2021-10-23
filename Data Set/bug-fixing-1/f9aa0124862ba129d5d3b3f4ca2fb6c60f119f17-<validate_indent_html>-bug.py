

def validate_indent_html(fn):
    file = open(fn)
    html = file.read()
    phtml = pretty_print_html(html)
    file.close()
    if (not (html.split('\n') == phtml.split('\n'))):
        temp_file = open('/var/tmp/pretty_html.txt', 'w')
        temp_file.write(phtml)
        temp_file.close()
        print(('Invalid Indentation detected in file: %s\nDiff for the file against expected indented file:' % fn))
        subprocess.call(['diff', fn, '/var/tmp/pretty_html.txt'], stderr=subprocess.STDOUT)
        return 0
    return 1
