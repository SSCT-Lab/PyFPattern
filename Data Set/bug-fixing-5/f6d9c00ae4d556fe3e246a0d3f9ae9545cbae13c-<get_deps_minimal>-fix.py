def get_deps_minimal(exclude_ignored=True, **kwargs):
    "Returns Kivy hidden modules as well as excluded modules to be used\n    with ``Analysis``.\n\n    The function takes core modules as keyword arguments and their value\n    indicates which of the providers to include/exclude from the compiled app.\n\n    The possible keyword names are ``audio, camera, clipboard, image, spelling,\n    text, video, and window``. Their values can be:\n\n        ``True``: Include current provider\n            The providers imported when the core module is\n            loaded on this system are added to hidden imports. This is the\n            default if the keyword name is not specified.\n        ``None``: Exclude\n            Don't return this core module at all.\n        ``A string or list of strings``: Providers to include\n            Each string is the name of a provider for this module to be\n            included.\n\n    For example, ``get_deps_minimal(video=None, window=True,\n    audio=['gstplayer', 'ffpyplayer'], spelling='enchant')`` will exclude all\n    the video providers, will include the gstreamer and ffpyplayer providers\n    for audio, will include the enchant provider for spelling, and will use the\n    current default provider for ``window``.\n\n    ``exclude_ignored``, if ``True`` (the default), if the value for a core\n    library is ``None``, then if ``exclude_ignored`` is True, not only will the\n    library not be included in the hiddenimports but it'll also added to the\n    excluded imports to prevent it being included accidentally by pyinstaller.\n\n    :returns:\n\n        A dict with two keys, ``hiddenimports`` and ``excludes``. Their values\n        are a list of the corresponding modules to include/exclude. This can\n        be passed directly to `Analysis`` with e.g. ::\n\n            a = Analysis(['..\\kivy\\examples\\demo\\touchtracer\\main.py'],\n                        ...\n                         hookspath=hookspath(),\n                         runtime_hooks=[],\n                         win_no_prefer_redirects=False,\n                         win_private_assemblies=False,\n                         cipher=block_cipher,\n                         **get_deps_minimal(video=None, audio=None))\n    "
    core_mods = ['audio', 'camera', 'clipboard', 'image', 'spelling', 'text', 'video', 'window']
    mods = kivy_modules[:]
    excludes = excludedimports[:]
    for (mod_name, val) in kwargs.items():
        if (mod_name not in core_mods):
            raise KeyError('{} not found in {}'.format(mod_name, core_mods))
        full_name = 'kivy.core.{}'.format(mod_name)
        if (not val):
            core_mods.remove(mod_name)
            if exclude_ignored:
                excludes.extend(collect_submodules(full_name))
            continue
        if (val is True):
            continue
        core_mods.remove(mod_name)
        mods.append(full_name)
        single_mod = False
        if (sys.version < '3.0'):
            if isinstance(val, basestring):
                single_mod = True
                mods.append('kivy.core.{0}.{0}_{1}'.format(mod_name, val))
        elif isinstance(val, (str, bytes)):
            single_mod = True
            mods.append('kivy.core.{0}.{0}_{1}'.format(mod_name, val))
        if (not single_mod):
            for v in val:
                mods.append('kivy.core.{0}.{0}_{1}'.format(mod_name, v))
    for mod_name in core_mods:
        full_name = 'kivy.core.{}'.format(mod_name)
        mods.append(full_name)
        m = importlib.import_module(full_name)
        if ((mod_name == 'clipboard') and m.CutBuffer):
            mods.append(m.CutBuffer.__module__)
        if hasattr(m, mod_name.capitalize()):
            val = getattr(m, mod_name.capitalize())
            if val:
                mods.append(getattr(val, '__module__'))
        if (hasattr(m, 'libs_loaded') and m.libs_loaded):
            for name in m.libs_loaded:
                mods.append('kivy.core.{}.{}'.format(mod_name, name))
    mods = sorted(set(mods))
    if (exclude_ignored and (not any((('gstplayer' in m) for m in mods)))):
        excludes.append('kivy.lib.gstplayer')
    return {
        'hiddenimports': mods,
        'excludes': excludes,
    }