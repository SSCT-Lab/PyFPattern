

@click.command(name='exec', context_settings=dict(ignore_unknown_options=True, allow_extra_args=True))
@click.option('-c', default='', help='Read script from string.')
@click.argument('file', default=None, required=False)
def exec_(c, file):
    "\n    Execute a script.\n\n    Also compatible with hashbang `#!/usr/bin/env sentry exec`\n\n    For convenience, the following preample is attached to scripts:\n\n    \x08\n      from sentry.runner import configure; configure()\n      from django.conf import settings\n      from sentry.models import *\n\n    Examples:\n\n    \x08\n      $ sentry exec -c 'print(Project.objects.count())'\n      $ echo 'print(Project.objects.count())' | sentry exec\n      $ sentry exec something.py\n\n    Note: All scripts are assumed utf-8.\n    "
    if (c and file):
        file = None
    if (not (c or file)):
        file = '-'
    if file:
        if (file == '-'):
            file = '<string>'
            c = click.get_text_stream('stdin').read()
        else:
            try:
                with open(file, 'rb') as fp:
                    c = fp.read().decode('utf8')
            except (IOError, OSError) as e:
                raise click.ClickException(six.text_type(e))
    else:
        file = '<string>'
    header = []
    if ('from __future__' in c):
        body = []
        state = 0
        for line in c.splitlines():
            if line.startswith('from __future__'):
                state = 1
            elif (line and (not line.startswith(('#', '"', "'"))) and (state == 1)):
                state = 2
            if (state == 2):
                body.append(line)
            else:
                header.append(line)
        body = '\n'.join(body)
    else:
        header = []
        body = c
    if ('from sentry.runner import configure' not in c):
        header.extend(['from sentry.runner import configure; configure()', 'from django.conf import settings', 'from sentry.models import *'])
    header.append('class ScriptError(Exception): pass')
    script = (SCRIPT_TEMPLATE % {
        'body': body.replace('\n', ('\n' + (' ' * 4))),
        'header': '\n'.join(header),
        'filename': file,
    })
    sys.argv = sys.argv[1:]
    g = {
        '__name__': '__main__',
        '__file__': '<script>',
    }
    six.exec_(compile(script, file, 'exec'), g, g)
