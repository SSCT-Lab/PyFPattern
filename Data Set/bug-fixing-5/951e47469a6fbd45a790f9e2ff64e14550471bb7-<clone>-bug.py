def clone(self, address, privatekey=None, address_index=None, root_inner_path='', overwrite=False):
    import shutil
    new_site = SiteManager.site_manager.need(address, all_file=False)
    default_dirs = []
    for dir_name in os.listdir(self.storage.directory):
        if ('-default' in dir_name):
            default_dirs.append(dir_name.replace('-default', ''))
    self.log.debug(('Cloning to %s, ignore dirs: %s, root: %s' % (address, default_dirs, root_inner_path)))
    if ((not new_site.storage.isFile('content.json')) and (not overwrite)):
        if ('size_limit' in self.settings):
            new_site.settings['size_limit'] = self.settings['size_limit']
        if self.storage.isFile((root_inner_path + '/content.json-default')):
            content_json = self.storage.loadJson((root_inner_path + '/content.json-default'))
        else:
            content_json = self.storage.loadJson('content.json')
        if ('domain' in content_json):
            del content_json['domain']
        content_json['title'] = ('my' + content_json['title'])
        content_json['cloned_from'] = self.address
        content_json['clone_root'] = root_inner_path
        content_json['files'] = {
            
        }
        if address_index:
            content_json['address_index'] = address_index
        new_site.storage.writeJson('content.json', content_json)
        new_site.content_manager.loadContent('content.json', add_bad_files=False, delete_removed_files=False, load_includes=False)
    for (content_inner_path, content) in list(self.content_manager.contents.items()):
        file_relative_paths = list(content.get('files', {
            
        }).keys())
        file_relative_paths.sort()
        file_relative_paths.sort(key=(lambda key: key.replace('-default', '').endswith('content.json')))
        for file_relative_path in file_relative_paths:
            file_inner_path = (helper.getDirname(content_inner_path) + file_relative_path)
            file_inner_path = file_inner_path.strip('/')
            if (not file_inner_path.startswith(root_inner_path)):
                self.log.debug(('[SKIP] %s (not in clone root)' % file_inner_path))
                continue
            if (file_inner_path.split('/')[0] in default_dirs):
                self.log.debug(('[SKIP] %s (has default alternative)' % file_inner_path))
                continue
            file_path = self.storage.getPath(file_inner_path)
            if root_inner_path:
                file_inner_path_dest = re.sub(('^%s/' % re.escape(root_inner_path)), '', file_inner_path)
                file_path_dest = new_site.storage.getPath(file_inner_path_dest)
            else:
                file_inner_path_dest = file_inner_path
                file_path_dest = new_site.storage.getPath(file_inner_path)
            self.log.debug(('[COPY] %s to %s...' % (file_inner_path, file_path_dest)))
            dest_dir = os.path.dirname(file_path_dest)
            if (not os.path.isdir(dest_dir)):
                os.makedirs(dest_dir)
            if (file_inner_path_dest.replace('-default', '') == 'content.json'):
                continue
            shutil.copy(file_path, file_path_dest)
            if ('-default' in file_inner_path):
                file_path_dest = new_site.storage.getPath(file_inner_path.replace('-default', ''))
                if (new_site.storage.isFile(file_inner_path.replace('-default', '')) and (not overwrite)):
                    self.log.debug(('[SKIP] Default file: %s (already exist)' % file_inner_path))
                    continue
                self.log.debug(('[COPY] Default file: %s to %s...' % (file_inner_path, file_path_dest)))
                dest_dir = os.path.dirname(file_path_dest)
                if (not os.path.isdir(dest_dir)):
                    os.makedirs(dest_dir)
                shutil.copy(file_path, file_path_dest)
                if file_path_dest.endswith('/content.json'):
                    new_site.storage.onUpdated(file_inner_path.replace('-default', ''))
                    new_site.content_manager.loadContent(file_inner_path.replace('-default', ''), add_bad_files=False, delete_removed_files=False, load_includes=False)
                    if privatekey:
                        new_site.content_manager.sign(file_inner_path.replace('-default', ''), privatekey, remove_missing_optional=True)
                        new_site.content_manager.loadContent(file_inner_path, add_bad_files=False, delete_removed_files=False, load_includes=False)
    if privatekey:
        new_site.content_manager.sign('content.json', privatekey, remove_missing_optional=True)
        new_site.content_manager.loadContent('content.json', add_bad_files=False, delete_removed_files=False, load_includes=False)
    if new_site.storage.isFile('dbschema.json'):
        new_site.storage.closeDb()
        try:
            new_site.storage.rebuildDb()
        except Exception as err:
            self.log.error(err)
    return new_site