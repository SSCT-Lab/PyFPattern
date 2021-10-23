def python(self, options):
    import code
    imported_objects = {
        
    }
    try:
        import readline
    except ImportError:
        pass
    else:
        import rlcompleter
        readline.set_completer(rlcompleter.Completer(imported_objects).complete)
        readline_doc = getattr(readline, '__doc__', '')
        if ((readline_doc is not None) and ('libedit' in readline_doc)):
            readline.parse_and_bind('bind ^I rl_complete')
        else:
            readline.parse_and_bind('tab:complete')
    if (not options['no_startup']):
        for pythonrc in OrderedSet([os.environ.get('PYTHONSTARTUP'), os.path.expanduser('~/.pythonrc.py')]):
            if (not pythonrc):
                continue
            if (not os.path.isfile(pythonrc)):
                continue
            with open(pythonrc) as handle:
                pythonrc_code = handle.read()
            try:
                exec(compile(pythonrc_code, pythonrc, 'exec'), imported_objects)
            except Exception:
                traceback.print_exc()
    code.interact(local=imported_objects)