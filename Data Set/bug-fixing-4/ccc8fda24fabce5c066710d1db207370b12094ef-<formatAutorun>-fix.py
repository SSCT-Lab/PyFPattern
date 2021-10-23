def formatAutorun(self):
    args = sys.argv[:]
    if (not getattr(sys, 'frozen', False)):
        args.insert(0, sys.executable)
        cwd = os.getcwd()
    else:
        cwd = os.path.dirname(sys.executable)
    if (sys.platform == 'win32'):
        args = [('"%s"' % arg) for arg in args if arg]
    cmd = ' '.join(args)
    cmd = cmd.replace('start.py', 'zeronet.py').replace('"--open_browser"', '').replace('"default_browser"', '').strip()
    cmd += ' --open_browser ""'
    return ('\n            @echo off\n            chcp 65001 > nul\n            set PYTHONIOENCODING=utf-8\n            cd /D "%s"\n            start "" %s\n        ' % (cwd, cmd))