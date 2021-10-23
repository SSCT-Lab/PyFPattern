def main():
    argument_spec = openstack_full_argument_spec()
    module_kwargs = openstack_module_kwargs()
    module = AnsibleModule(argument_spec, **module_kwargs)
    if (not HAS_SHADE):
        module.fail_json(msg='shade is required for this module')
    try:
        cloud = shade.openstack_cloud(**module.params)
        module.exit_json(changed=False, ansible_facts=dict(auth_token=cloud.auth_token, service_catalog=cloud.service_catalog))
    except Exception as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())