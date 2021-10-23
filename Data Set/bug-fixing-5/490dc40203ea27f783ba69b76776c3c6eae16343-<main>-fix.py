def main():
    module = AnsibleModule(argument_spec=dict(command=dict(choices=['droplet', 'ssh'], default='droplet'), state=dict(choices=['active', 'present', 'absent', 'deleted'], default='present'), api_token=dict(aliases=['API_TOKEN'], no_log=True, fallback=(env_fallback, ['DO_API_TOKEN', 'DO_API_KEY'])), name=dict(type='str'), size_id=dict(), image_id=dict(), region_id=dict(), ssh_key_ids=dict(type='list'), virtio=dict(type='bool', default='yes'), private_networking=dict(type='bool', default='no'), backups_enabled=dict(type='bool', default='no'), id=dict(aliases=['droplet_id'], type='int'), unique_name=dict(type='bool', default='no'), user_data=dict(default=None), ipv6=dict(type='bool', default='no'), wait=dict(type='bool', default=True), wait_timeout=dict(default=300, type='int'), ssh_pub_key=dict(type='str')), required_together=(['size_id', 'image_id', 'region_id'],), mutually_exclusive=(['size_id', 'ssh_pub_key'], ['image_id', 'ssh_pub_key'], ['region_id', 'ssh_pub_key']), required_one_of=(['id', 'name'],))
    if ((not HAS_DOPY) and (not HAS_SIX)):
        module.fail_json(msg='dopy >= 0.3.2 is required for this module. dopy requires six but six is not installed. Make sure both dopy and six are installed.')
    if (not HAS_DOPY):
        module.fail_json(msg='dopy >= 0.3.2 required for this module')
    try:
        core(module)
    except TimeoutError as e:
        module.fail_json(msg=str(e), id=e.id)
    except (DoError, Exception) as e:
        module.fail_json(msg=str(e), exception=traceback.format_exc())