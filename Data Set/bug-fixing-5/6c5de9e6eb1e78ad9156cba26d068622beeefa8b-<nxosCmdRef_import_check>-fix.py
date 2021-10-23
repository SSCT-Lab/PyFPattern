def nxosCmdRef_import_check():
    'Return import error messages or empty string'
    msg = ''
    if PY2:
        if ((not HAS_ORDEREDDICT) and (sys.version_info[:2] < (2, 7))):
            msg += "Mandatory python library 'ordereddict' is not present, try 'pip install ordereddict'\n"
        if (not HAS_YAML):
            msg += "Mandatory python library 'yaml' is not present, try 'pip install yaml'\n"
    elif PY3:
        if (not HAS_YAML):
            msg += "Mandatory python library 'PyYAML' is not present, try 'pip install PyYAML'\n"
    return msg