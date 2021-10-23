def _parse_spec_group_file(self):
    (pkg_specs, grp_specs, module_specs, filenames) = ([], [], [], [])
    already_loaded_comps = False
    for name in self.names:
        if name.endswith('.rpm'):
            if ('://' in name):
                name = self.fetch_rpm_from_url(name)
            filenames.append(name)
        elif (name.startswith('@') or ('/' in name)):
            if (not already_loaded_comps):
                self.base.read_comps()
                already_loaded_comps = True
            grp_env_mdl_candidate = name[1:].strip()
            if self.with_modules:
                mdl = self.module_base._get_modules(grp_env_mdl_candidate)
                if mdl[0]:
                    module_specs.append(grp_env_mdl_candidate)
                else:
                    grp_specs.append(grp_env_mdl_candidate)
            else:
                grp_specs.append(grp_env_mdl_candidate)
        else:
            pkg_specs.append(name)
    return (pkg_specs, grp_specs, module_specs, filenames)