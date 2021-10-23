def _build_folder_map(self, folder, vmap={
    
}, inpath='/'):
    ' Build a searchable index for vms+uuids+folders '
    if isinstance(folder, tuple):
        folder = folder[1]
    if (not ('names' in vmap)):
        vmap['names'] = {
            
        }
    if (not ('uuids' in vmap)):
        vmap['uuids'] = {
            
        }
    if (not ('paths' in vmap)):
        vmap['paths'] = {
            
        }
    if (inpath == '/'):
        thispath = '/vm'
    else:
        thispath = os.path.join(inpath, folder['name'])
    if (thispath not in vmap['paths']):
        vmap['paths'][thispath] = []
    if (not ('path_by_fvim' in vmap)):
        vmap['path_by_fvim'] = {
            
        }
    if (not ('fvim_by_path' in vmap)):
        vmap['fvim_by_path'] = {
            
        }
    vmap['fvim_by_path'][thispath] = folder['vimobj']
    vmap['path_by_fvim'][folder['vimobj']] = thispath
    if (not ('path_by_vvim' in vmap)):
        vmap['path_by_vvim'] = {
            
        }
    if (not ('vvim_by_path' in vmap)):
        vmap['vvim_by_path'] = {
            
        }
    if (thispath not in vmap['vvim_by_path']):
        vmap['vvim_by_path'][thispath] = []
    for item in folder.items():
        k = item[0]
        v = item[1]
        if (k == 'name'):
            pass
        elif (k == 'subfolders'):
            for x in v.items():
                vmap = self._build_folder_map(x, vmap=vmap, inpath=thispath)
        elif (k == 'virtualmachines'):
            for x in v:
                if (not (x.config.name in vmap['names'])):
                    vmap['names'][x.config.name] = []
                vmap['names'][x.config.name].append(x.config.uuid)
                vmap['uuids'][x.config.uuid] = x.config.name
                vmap['paths'][thispath].append(x.config.uuid)
                if (x not in vmap['vvim_by_path'][thispath]):
                    vmap['vvim_by_path'][thispath].append(x)
                if (x not in vmap['path_by_vvim']):
                    vmap['path_by_vvim'][x] = thispath
    return vmap