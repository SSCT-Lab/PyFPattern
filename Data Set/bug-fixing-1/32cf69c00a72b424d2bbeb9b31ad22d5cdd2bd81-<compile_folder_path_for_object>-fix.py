

def compile_folder_path_for_object(vobj):
    ' make a /vm/foo/bar/baz like folder path for an object '
    paths = []
    if isinstance(vobj, vim.Folder):
        paths.append(vobj.name)
    thisobj = vobj
    while hasattr(thisobj, 'parent'):
        thisobj = thisobj.parent
        if (thisobj._moId == 'group-d1'):
            break
        if isinstance(thisobj, vim.Folder):
            paths.append(thisobj.name)
    paths.reverse()
    return ('/' + '/'.join(paths))
