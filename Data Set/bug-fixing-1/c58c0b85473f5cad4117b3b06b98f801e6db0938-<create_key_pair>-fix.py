

def create_key_pair(module, ec2_client, name, key_material, force):
    key = find_key_pair(module, ec2_client, name)
    if key:
        if (key_material and force):
            if (not module.check_mode):
                new_fingerprint = get_key_fingerprint(module, ec2_client, key_material)
                if (key['KeyFingerprint'] != new_fingerprint):
                    delete_key_pair(module, ec2_client, name, finish_task=False)
                    key = import_key_pair(module, ec2_client, name, key_material)
                    key_data = extract_key_data(key)
                    module.exit_json(changed=True, key=key_data, msg='key pair updated')
            else:
                module.exit_json(changed=True, key=extract_key_data(key), msg='key pair updated')
        key_data = extract_key_data(key)
        module.exit_json(changed=False, key=key_data, msg='key pair already exists')
    else:
        key_data = None
        if (not module.check_mode):
            if key_material:
                key = import_key_pair(module, ec2_client, name, key_material)
            else:
                try:
                    key = ec2_client.create_key_pair(KeyName=name)
                except ClientError as err:
                    module.fail_json_aws(err, msg='error creating key')
            key_data = extract_key_data(key)
        module.exit_json(changed=True, key=key_data, msg='key pair created')
