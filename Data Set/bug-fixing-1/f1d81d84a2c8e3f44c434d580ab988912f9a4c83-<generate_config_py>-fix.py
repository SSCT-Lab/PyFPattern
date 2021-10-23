

def generate_config_py(target):
    "Generate config.py file containing system_info information\n    used during building the package.\n\n    Usage:\n        config['py_modules'].append((packagename, '__config__',generate_config_py))\n    "
    from numpy.distutils.system_info import system_info
    from distutils.dir_util import mkpath
    mkpath(os.path.dirname(target))
    f = open(target, 'w')
    f.write(("# This file is generated by numpy's %s\n" % os.path.basename(sys.argv[0])))
    f.write('# It contains system_info results at the time of building this package.\n')
    f.write('__all__ = ["get_info","show"]\n\n')
    f.write('\n\nimport os\nimport sys\n\nextra_dll_dir = os.path.join(os.path.dirname(__file__), \'.libs\')\n\nif os.path.isdir(extra_dll_dir) and sys.platform == \'win32\':\n    try:\n        from ctypes import windll, c_wchar_p\n        _AddDllDirectory = windll.kernel32.AddDllDirectory\n        _AddDllDirectory.argtypes = [c_wchar_p]\n        # Needed to initialize AddDllDirectory modifications\n        windll.kernel32.SetDefaultDllDirectories(0x1000)\n    except AttributeError:\n        def _AddDllDirectory(dll_directory):\n            os.environ["PATH"] += os.pathsep + dll_directory\n\n    _AddDllDirectory(extra_dll_dir)\n\n')
    for (k, i) in system_info.saved_results.items():
        f.write(('%s=%r\n' % (k, i)))
    f.write('\ndef get_info(name):\n    g = globals()\n    return g.get(name, g.get(name + "_info", {}))\n\ndef show():\n    for name,info_dict in globals().items():\n        if name[0] == "_" or type(info_dict) is not type({}): continue\n        print(name + ":")\n        if not info_dict:\n            print("  NOT AVAILABLE")\n        for k,v in info_dict.items():\n            v = str(v)\n            if k == "sources" and len(v) > 200:\n                v = v[:60] + " ...\\n... " + v[-60:]\n            print("    %s = %s" % (k,v))\n    ')
    f.close()
    return target
