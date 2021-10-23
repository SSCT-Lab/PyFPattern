

def _add_library(self, name, sources, install_dir, build_info):
    'Common implementation for add_library and add_installed_library. Do\n        not use directly'
    build_info = copy.copy(build_info)
    name = name
    build_info['sources'] = sources
    if (not ('depends' in build_info)):
        build_info['depends'] = []
    self._fix_paths_dict(build_info)
    self.libraries.append((name, build_info))
