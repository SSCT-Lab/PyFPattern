def preflight_validation(bin_path, project_path, variables_file=None, plan_file=None):
    if (not os.path.exists(bin_path)):
        module.fail_json(msg="Path for Terraform binary '{0}' doesn't exist on this host - check the path and try again please.".format(project_path))
    if (not os.path.isdir(project_path)):
        module.fail_json(msg="Path for Terraform project '{0}' doesn't exist on this host - check the path and try again please.".format(project_path))
    (rc, out, err) = module.run_command([bin_path, 'validate'], cwd=project_path)
    if (rc != 0):
        module.fail_json(msg='Failed to validate Terraform configuration files:\r\n{0}'.format(err))