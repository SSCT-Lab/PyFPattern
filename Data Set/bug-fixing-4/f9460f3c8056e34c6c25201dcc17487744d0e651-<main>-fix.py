def main():
    module = AnsibleModule(argument_spec=dict(path=dict(aliases=['dest'], required=True, type='path'), release=dict(required=False, type='str', default=None), releases_path=dict(required=False, type='str', default='releases'), shared_path=dict(required=False, type='path', default='shared'), current_path=dict(required=False, type='path', default='current'), keep_releases=dict(required=False, type='int', default=5), clean=dict(required=False, type='bool', default=True), unfinished_filename=dict(required=False, type='str', default='DEPLOY_UNFINISHED'), state=dict(required=False, choices=['present', 'absent', 'clean', 'finalize', 'query'], default='present')), add_file_common_args=True, supports_check_mode=True)
    deploy_helper = DeployHelper(module)
    facts = deploy_helper.gather_facts()
    result = {
        'state': deploy_helper.state,
    }
    changes = 0
    if (deploy_helper.state == 'query'):
        result['ansible_facts'] = {
            'deploy_helper': facts,
        }
    elif (deploy_helper.state == 'present'):
        deploy_helper.check_link(facts['current_path'])
        changes += deploy_helper.create_path(facts['project_path'])
        changes += deploy_helper.create_path(facts['releases_path'])
        if deploy_helper.shared_path:
            changes += deploy_helper.create_path(facts['shared_path'])
        result['ansible_facts'] = {
            'deploy_helper': facts,
        }
    elif (deploy_helper.state == 'finalize'):
        if (not deploy_helper.release):
            module.fail_json(msg="'release' is a required parameter for state=finalize (try the 'deploy_helper.new_release' fact)")
        if (deploy_helper.keep_releases <= 0):
            module.fail_json(msg="'keep_releases' should be at least 1")
        changes += deploy_helper.remove_unfinished_file(facts['new_release_path'])
        changes += deploy_helper.create_link(facts['new_release_path'], facts['current_path'])
        if deploy_helper.clean:
            changes += deploy_helper.remove_unfinished_link(facts['project_path'])
            changes += deploy_helper.remove_unfinished_builds(facts['releases_path'])
            changes += deploy_helper.cleanup(facts['releases_path'], facts['new_release'])
    elif (deploy_helper.state == 'clean'):
        changes += deploy_helper.remove_unfinished_link(facts['project_path'])
        changes += deploy_helper.remove_unfinished_builds(facts['releases_path'])
        changes += deploy_helper.cleanup(facts['releases_path'], facts['new_release'])
    elif (deploy_helper.state == 'absent'):
        result['ansible_facts'] = {
            'deploy_helper': [],
        }
        changes += deploy_helper.delete_path(facts['project_path'])
    if (changes > 0):
        result['changed'] = True
    else:
        result['changed'] = False
    module.exit_json(**result)