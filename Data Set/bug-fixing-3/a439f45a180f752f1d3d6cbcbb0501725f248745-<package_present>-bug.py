def package_present(names, pkg_spec, module):
    build = module.params['build']
    for name in names:
        if pkg_spec['package_latest_leftovers']:
            if (name not in pkg_spec['package_latest_leftovers']):
                module.debug(("package_present(): ignoring '%s' which is not a package_latest() leftover" % name))
                continue
            else:
                module.debug(("package_present(): handling package_latest() leftovers, installing '%s'" % name))
        if module.check_mode:
            install_cmd = 'pkg_add -Imn'
        elif (build is True):
            port_dir = ('%s/%s' % (module.params['ports_dir'], get_package_source_path(name, pkg_spec, module)))
            if os.path.isdir(port_dir):
                if pkg_spec[name]['flavor']:
                    flavors = pkg_spec[name]['flavor'].replace('-', ' ')
                    install_cmd = ('cd %s && make clean=depends && FLAVOR="%s" make install && make clean=depends' % (port_dir, flavors))
                elif pkg_spec[name]['subpackage']:
                    install_cmd = ('cd %s && make clean=depends && SUBPACKAGE="%s" make install && make clean=depends' % (port_dir, pkg_spec[name]['subpackage']))
                else:
                    install_cmd = ('cd %s && make install && make clean=depends' % port_dir)
            else:
                module.fail_json(msg=('the port source directory %s does not exist' % port_dir))
        else:
            install_cmd = 'pkg_add -Im'
        if (pkg_spec[name]['installed_state'] is False):
            if ((build is True) and (not module.check_mode)):
                (pkg_spec[name]['rc'], pkg_spec[name]['stdout'], pkg_spec[name]['stderr']) = module.run_command(install_cmd, module, use_unsafe_shell=True)
            else:
                (pkg_spec[name]['rc'], pkg_spec[name]['stdout'], pkg_spec[name]['stderr']) = execute_command(('%s %s' % (install_cmd, name)), module)
            if (pkg_spec[name]['version'] or (build is True)):
                module.debug(("package_present(): depending on return code for name '%s'" % name))
                if pkg_spec[name]['rc']:
                    pkg_spec[name]['changed'] = False
            else:
                module.debug(("package_present(): depending on stderr for name '%s'" % name))
                if pkg_spec[name]['stderr']:
                    if (pkg_spec[name]['style'] == 'branch'):
                        match = re.search(('\\W%s-[^:]+: ok\\W' % pkg_spec[name]['pkgname']), pkg_spec[name]['stdout'])
                    else:
                        match = re.search(('\\W%s-[^:]+: ok\\W' % name), pkg_spec[name]['stdout'])
                    if match:
                        module.debug(("package_present(): we were able to install package for name '%s'" % name))
                    else:
                        module.debug(("package_present(): we really did fail for name '%s'" % name))
                        pkg_spec[name]['rc'] = 1
                        pkg_spec[name]['changed'] = False
                else:
                    module.debug(("package_present(): stderr was not set for name '%s'" % name))
            if (pkg_spec[name]['rc'] == 0):
                pkg_spec[name]['changed'] = True
        else:
            pkg_spec[name]['rc'] = 0
            pkg_spec[name]['stdout'] = ''
            pkg_spec[name]['stderr'] = ''
            pkg_spec[name]['changed'] = False