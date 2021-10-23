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
            with suppress(NameError):
                with open(pythonrc) as handle:
                    exec(compile(handle.read(), pythonrc, 'exec'), imported_objects)
    code.interact(local=imported_objects)