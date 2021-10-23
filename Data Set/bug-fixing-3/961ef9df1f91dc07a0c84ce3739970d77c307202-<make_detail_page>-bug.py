def make_detail_page(info):
    ' return str of the rst text for the detail page of the file in info. '

    def a(s=''):
        ' append formatted s to output, which will be joined into lines '
        output.append(s.format(**info))
    output = []
    a('{title}')
    a(('=' * len(info['title'])))
    a('\n.. |pic{num}| image:: /images/examples/{dunder}.png\n   :width: 50%\n   :align: middle')
    a('\n|pic{num}|')
    a()
    for paragraph in info['enhanced_description']:
        for line in paragraph:
            a(line)
        a()
    last_lang = '.py'
    for fname in info['files']:
        full_name = slash(info['dir'], fname)
        ext = re.search('\\.\\w+$', fname).group(0)
        a((('\n.. _`' + fname) + '`:'))
        if (ext in ['.png', '.jpg', '.jpeg']):
            title = (('Image **' + full_name) + '**')
            a(('\n' + title))
            a(('~' * len(title)))
            a(('\n.. image:: ../../../examples/' + full_name))
            a('     :align:  center')
        else:
            title = (('File **' + full_name) + '**')
            a(('\n' + title))
            a(('~' * len(title)))
            if ((ext != last_lang) and (ext != '.txt')):
                a(('\n.. highlight:: ' + ext[1:]))
                a('    :linenothreshold: 3')
                last_lang = ext
            a(('\n.. include:: ../../../examples/' + full_name))
            a('    :code:')
    return ('\n'.join(output) + '\n')