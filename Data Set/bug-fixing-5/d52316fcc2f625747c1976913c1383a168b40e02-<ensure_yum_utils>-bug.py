def ensure_yum_utils(module):
    repoquerybin = module.get_bin_path('repoquery', required=False)
    if (module.params['install_repoquery'] and (not repoquerybin) and (not module.check_mode)):
        yum_path = module.get_bin_path('yum')
        if yum_path:
            (rc, so, se) = module.run_command(('%s -y install yum-utils' % yum_path))
        repoquerybin = module.get_bin_path('repoquery', required=False)
    return repoquerybin