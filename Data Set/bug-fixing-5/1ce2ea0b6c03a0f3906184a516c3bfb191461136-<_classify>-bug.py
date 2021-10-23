def _classify(self, path):
    '\n        :type path: str\n        :rtype: dict[str, str] | None\n        '
    filename = os.path.basename(path)
    (name, ext) = os.path.splitext(filename)
    minimal = {
        
    }
    if path.startswith('.github/'):
        return minimal
    if path.startswith('bin/'):
        return minimal
    if path.startswith('contrib/'):
        return {
            'units': 'test/units/contrib/',
        }
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
        module = self.module_names_by_path.get(path)
        if module:
            return {
                'units': (module if (module in self.units_modules) else None),
                'integration': (self.posix_integration_by_module.get(module) if (ext == '.py') else None),
                'windows-integration': (self.windows_integration_by_module.get(module) if (ext == '.ps1') else None),
                'network-integration': self.network_integration_by_module.get(module),
            }
        return minimal
    if path.startswith('lib/ansible/module_utils/'):
        if (ext == '.ps1'):
            return {
                'windows-integration': 'all',
            }
        if (ext == '.py'):
            return minimal
    if path.startswith('lib/ansible/plugins/connection/'):
        if (name == '__init__'):
            return {
                'integration': 'all',
                'windows-integration': 'all',
                'network-integration': 'all',
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
                'windows-integration': 'all',
                'units': units_path,
            }
        if (name == 'local'):
            return {
                'integration': 'all',
                'network-integration': 'all',
                'units': units_path,
            }
        if (name == 'network_cli'):
            return {
                'network-integration': 'all',
                'units': units_path,
            }
        return {
            'integration': integration_name,
            'units': units_path,
        }
    if path.startswith('lib/ansible/plugins/terminal/'):
        if (ext == '.py'):
            if ((name in self.prefixes) and (self.prefixes[name] == 'network')):
                network_target = ('network/%s/' % name)
                if (network_target in self.integration_targets_by_alias):
                    return {
                        'network-integration': network_target,
                        'units': 'all',
                    }
                display.warning(('Integration tests for "%s" not found.' % network_target))
                return {
                    'units': 'all',
                }
            return {
                'network-integration': 'all',
                'units': 'all',
            }
    if path.startswith('lib/ansible/utils/module_docs_fragments/'):
        return {
            'sanity': 'all',
        }
    if path.startswith('lib/ansible/'):
        return all_tests()
    if path.startswith('packaging/'):
        return minimal
    if path.startswith('test/compile/'):
        return {
            'compile': 'all',
        }
    if path.startswith('test/results/'):
        return minimal
    if path.startswith('test/integration/roles/'):
        return minimal
    if path.startswith('test/integration/targets/'):
        target = self.integration_targets_by_name[path.split('/')[3]]
        if ('hidden/' in target.aliases):
            return {
                'integration': 'all',
                'windows-integration': 'all',
                'network-integration': 'all',
            }
        return {
            'integration': (target.name if ('posix/' in target.aliases) else None),
            'windows-integration': (target.name if ('windows/' in target.aliases) else None),
            'network-integration': (target.name if ('network/' in target.aliases) else None),
        }
    if path.startswith('test/integration/'):
        return {
            'integration': 'all',
            'windows-integration': 'all',
            'network-integration': 'all',
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
    if path.startswith('test/runner/'):
        return all_tests()
    if path.startswith('test/utils/shippable/'):
        return all_tests()
    if path.startswith('test/utils/'):
        return minimal
    if (path == 'test/README.md'):
        return minimal
    if path.startswith('ticket_stubs/'):
        return minimal
    if ('/' not in path):
        if (path in ('.gitattributes', '.gitignore', '.gitmodules', '.mailmap', 'tox.ini', 'COPYING', 'VERSION', 'Makefile', 'setup.py')):
            return minimal
        if (path in ('shippable.yml', '.coveragerc')):
            return all_tests()
        if (path == '.yamllint'):
            return {
                'sanity': 'all',
            }
        if (ext in ('.md', '.rst', '.txt', '.xml', '.in')):
            return minimal
    return None