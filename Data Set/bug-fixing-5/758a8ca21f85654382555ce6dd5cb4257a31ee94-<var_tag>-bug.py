def var_tag(var):
    'Parse tag attribute of variable node.'
    tag = var.tag
    if (hasattr(tag, 'trace') and len(tag.trace) and (len(tag.trace[0]) == 4)):
        (path, line, _, src) = tag.trace[0]
        path = os.path.basename(path)
        path = path.replace('<', '')
        path = path.replace('>', '')
        src = src.encode()
        return [path, line, src]
    else:
        return None