def _check_rh_versions(self, collected_facts):
    if (collected_facts['ansible_distribution'] == 'Fedora'):
        try:
            if (int(collected_facts['ansible_distribution_major_version']) < 15):
                pkg_mgr_name = 'yum'
            else:
                pkg_mgr_name = 'dnf'
        except ValueError:
            pkg_mgr_name = 'dnf'
    return pkg_mgr_name