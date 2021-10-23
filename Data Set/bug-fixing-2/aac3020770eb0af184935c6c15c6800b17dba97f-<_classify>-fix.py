

def _classify(self, path):
    '\n        :type path: str\n        :rtype: dict[str, str] | None\n        '
    dirname = os.path.dirname(path)
    filename = os.path.basename(path)
    (name, ext) = os.path.splitext(filename)
    minimal = {
        
    }
    if path.startswith('.github/'):
        return minimal
    if path.startswith('bin/'):
        return all_tests(self.args)
    if path.startswith('contrib/'):
        return {
            'units': 'test/units/contrib/',
        }
    if path.startswith('changelogs/'):
        return minimal
    if path.startswith('docs/'):
        return minimal
    if path.startswith('examples/'):
        if (path == 'examples/scripts/ConfigureRemotingForAnsible.ps1'):
            return {
                'windows-integration': 'connection_winrm',
            }
        return minimal
    if path.startswith('hacking/'):
        return minimal
    if path.startswith('lib/ansible/modules/'):
        module_name = self.module_names_by_path.get(path)
        if module_name:
            return {
                'units': (module_name if (module_name in self.units_modules) else None),
                'integration': (self.posix_integration_by_module.get(module_name) if (ext == '.py') else None),
                'windows-integration': (self.windows_integration_by_module.get(module_name) if (ext == '.ps1') else None),
                'network-integration': self.network_integration_by_module.get(module_name),
                FOCUSED_TARGET: True,
            }
        return minimal
    if path.startswith('lib/ansible/module_utils/'):
        if (ext == '.psm1'):
            return minimal
        if (ext == '.py'):
            return minimal
    if path.startswith('lib/ansible/plugins/action/'):
        if (ext == '.py'):
            if name.startswith('net_'):
                network_target = ('network/.*_%s' % name[4:])
                if any((re.search(('^%s$' % network_target), alias) for alias in self.integration_targets_by_alias)):
                    return {
                        'network-integration': network_target,
                        'units': 'all',
                    }
                return {
                    'network-integration': self.integration_all_target,
                    'units': 'all',
                }
            if (self.prefixes.get(name) == 'network'):
                network_platform = name
            elif (name.endswith('_config') and (self.prefixes.get(name[:(- 7)]) == 'network')):
                network_platform = name[:(- 7)]
            elif (name.endswith('_template') and (self.prefixes.get(name[:(- 9)]) == 'network')):
                network_platform = name[:(- 9)]
            else:
                network_platform = None
            if network_platform:
                network_target = ('network/%s/' % network_platform)
                if (network_target in self.integration_targets_by_alias):
                    return {
                        'network-integration': network_target,
                        'units': 'all',
                    }
                display.warning(('Integration tests for "%s" not found.' % network_target), unique=True)
                return {
                    'units': 'all',
                }
    if path.startswith('lib/ansible/plugins/connection/'):
        if (name == '__init__'):
            return {
                'integration': self.integration_all_target,
                'windows-integration': self.integration_all_target,
                'network-integration': self.integration_all_target,
                'units': 'test/units/plugins/connection/',
            }
        units_path = ('test/units/plugins/connection/test_%s.py' % name)
        if (units_path not in self.units_paths):
            units_path = None
        integration_name = ('connection_%s' % name)
        if (integration_name not in self.integration_targets_by_name):
            integration_name = None
        if (name == 'winrm'):
            return {
                'windows-integration': self.integration_all_target,
                'units': units_path,
            }
        if (name == 'local'):
            return {
                'integration': self.integration_all_target,
                'network-integration': self.integration_all_target,
                'units': units_path,
            }
        if (name == 'network_cli'):
            return {
                'network-integration': self.integration_all_target,
                'units': units_path,
            }
        return {
            'integration': integration_name,
            'units': units_path,
        }
    if (path.startswith('lib/ansible/plugins/terminal/') or path.startswith('lib/ansible/plugins/cliconf/') or path.startswith('lib/ansible/plugins/netconf/')):
        if (ext == '.py'):
            if ((name in self.prefixes) and (self.prefixes[name] == 'network')):
                network_target = ('network/%s/' % name)
                if (network_target in self.integration_targets_by_alias):
                    return {
                        'network-integration': network_target,
                        'units': 'all',
                    }
                display.warning(('Integration tests for "%s" not found.' % network_target), unique=True)
                return {
                    'units': 'all',
                }
            return {
                'network-integration': self.integration_all_target,
                'units': 'all',
            }
    if path.startswith('lib/ansible/utils/module_docs_fragments/'):
        return {
            'sanity': 'all',
        }
    if path.startswith('lib/ansible/'):
        return all_tests(self.args)
    if path.startswith('packaging/'):
        if path.startswith('packaging/requirements/'):
            if (name.startswith('requirements-') and (ext == '.txt')):
                component = name.split('-', 1)[1]
                candidates = (('cloud/%s/' % component),)
                for candidate in candidates:
                    if (candidate in self.integration_targets_by_alias):
                        return {
                            'integration': candidate,
                        }
            return all_tests(self.args)
        return minimal
    if path.startswith('test/cache/'):
        return minimal
    if path.startswith('test/results/'):
        return minimal
    if path.startswith('test/legacy/'):
        return minimal
    if path.startswith('test/integration/roles/'):
        return minimal
    if path.startswith('test/integration/targets/'):
        if (not os.path.exists(path)):
            return minimal
        target = self.integration_targets_by_name[path.split('/')[3]]
        if ('hidden/' in target.aliases):
            if (target.type == 'role'):
                return minimal
            return {
                'integration': self.integration_all_target,
                'windows-integration': self.integration_all_target,
                'network-integration': self.integration_all_target,
            }
        return {
            'integration': (target.name if ('posix/' in target.aliases) else None),
            'windows-integration': (target.name if ('windows/' in target.aliases) else None),
            'network-integration': (target.name if ('network/' in target.aliases) else None),
            FOCUSED_TARGET: True,
        }
    if path.startswith('test/integration/'):
        if (dirname == 'test/integration'):
            if ((self.prefixes.get(name) == 'network') and (ext == '.yaml')):
                return minimal
            if (filename == 'network-all.yaml'):
                return minimal
            if (filename == 'platform_agnostic.yaml'):
                return minimal
            for command in ('integration', 'windows-integration', 'network-integration'):
                if ((name == command) and (ext == '.cfg')):
                    return {
                        command: self.integration_all_target,
                    }
            if name.startswith('cloud-config-'):
                cloud_target = ('cloud/%s/' % name.split('-')[2].split('.')[0])
                if (cloud_target in self.integration_targets_by_alias):
                    return {
                        'integration': cloud_target,
                    }
        return {
            'integration': self.integration_all_target,
            'windows-integration': self.integration_all_target,
            'network-integration': self.integration_all_target,
        }
    if path.startswith('test/sanity/'):
        return {
            'sanity': 'all',
        }
    if path.startswith('test/units/'):
        if (path in self.units_paths):
            return {
                'units': path,
            }
        test_path = os.path.dirname(path)
        while test_path:
            if ((test_path + '/') in self.units_paths):
                return {
                    'units': (test_path + '/'),
                }
            test_path = os.path.dirname(test_path)
    if path.startswith('test/runner/completion/'):
        if (path == 'test/runner/completion/docker.txt'):
            return all_tests(self.args, force=True)
    if path.startswith('test/runner/docker/'):
        return minimal
    if path.startswith('test/runner/lib/cloud/'):
        cloud_target = ('cloud/%s/' % name)
        if (cloud_target in self.integration_targets_by_alias):
            return {
                'integration': cloud_target,
            }
        return all_tests(self.args)
    if path.startswith('test/runner/lib/sanity/'):
        return {
            'sanity': 'all',
        }
    if path.startswith('test/runner/requirements/'):
        if (name in ('integration', 'network-integration', 'windows-integration')):
            return {
                name: self.integration_all_target,
            }
        if (name in ('sanity', 'units')):
            return {
                name: 'all',
            }
        if name.startswith('integration.cloud.'):
            cloud_target = ('cloud/%s/' % name.split('.')[2])
            if (cloud_target in self.integration_targets_by_alias):
                return {
                    'integration': cloud_target,
                }
    if path.startswith('test/runner/'):
        if ((dirname == 'test/runner') and (name in ('Dockerfile', '.dockerignore'))):
            return minimal
        return all_tests(self.args)
    if path.startswith('test/utils/shippable/tools/'):
        return minimal
    if path.startswith('test/utils/shippable/'):
        if (dirname == 'test/utils/shippable'):
            test_map = {
                'cloud.sh': 'integration:cloud/',
                'freebsd.sh': 'integration:all',
                'linux.sh': 'integration:all',
                'network.sh': 'network-integration:all',
                'osx.sh': 'integration:all',
                'rhel.sh': 'integration:all',
                'sanity.sh': 'sanity:all',
                'units.sh': 'units:all',
                'windows.sh': 'windows-integration:all',
            }
            test_match = test_map.get(filename)
            if test_match:
                (test_command, test_target) = test_match.split(':')
                return {
                    test_command: test_target,
                }
        return all_tests(self.args)
    if path.startswith('test/utils/'):
        return minimal
    if (path == 'test/README.md'):
        return minimal
    if path.startswith('ticket_stubs/'):
        return minimal
    if ('/' not in path):
        if (path in ('.gitattributes', '.gitignore', '.gitmodules', '.mailmap', 'tox.ini', 'COPYING', 'VERSION', 'Makefile')):
            return minimal
        if (path in ('shippable.yml', '.coveragerc')):
            return all_tests(self.args)
        if (path == 'setup.py'):
            return all_tests(self.args)
        if (path == '.yamllint'):
            return {
                'sanity': 'all',
            }
        if (ext in ('.md', '.rst', '.txt', '.xml', '.in')):
            return minimal
    return None
