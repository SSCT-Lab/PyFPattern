def _check_rh_versions(self, pkg_mgr_name, collected_facts):
    if (collected_facts['ansible_distribution'] == 'Fedora'):
        try:
            if (int(collected_facts['ansible_distribution_major_version']) < 23):
                for yum in [pkg_mgr for pkg_mgr in PKG_MGRS if (pkg_mgr['name'] == 'yum')]:
                    if os.path.exists(yum['path']):
                        pkg_mgr_name = 'yum'
                        break
            else:
                for dnf in [pkg_mgr for pkg_mgr in PKG_MGRS if (pkg_mgr['name'] == 'dnf')]:
                    if os.path.exists(dnf['path']):
                        pkg_mgr_name = 'dnf'
                        break
        except ValueError:
            pkg_mgr_name = 'dnf'
    return pkg_mgr_name