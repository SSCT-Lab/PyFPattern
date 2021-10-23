def destroy_user(connection, module):
    user_name = module.params.get('name')
    user = get_user(connection, module, user_name)
    if (not user):
        module.exit_json(changed=False)
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        for policy in get_attached_policy_list(connection, module, user_name):
            connection.detach_user_policy(UserName=user_name, PolicyArn=policy['PolicyArn'])
    except (ClientError, BotoCoreError) as e:
        module.fail_json_aws(e, msg='Unable to delete user {0}'.format(user_name))
    try:
        access_keys = connection.list_access_keys(UserName=user_name)['AccessKeyMetadata']
        for access_key in access_keys:
            connection.delete_access_key(UserName=user_name, AccessKeyId=access_key['AccessKeyId'])
        delete_user_login_profile(connection, module, user_name)
        ssh_public_keys = connection.list_ssh_public_keys(UserName=user_name)['SSHPublicKeys']
        for ssh_public_key in ssh_public_keys:
            connection.delete_ssh_public_key(UserName=user_name, SSHPublicKeyId=ssh_public_key['SSHPublicKeyId'])
        service_credentials = connection.list_service_specific_credentials(UserName=user_name)['ServiceSpecificCredentials']
        for service_specific_credential in service_credentials:
            connection.delete_service_specific_credential(UserName=user_name, ServiceSpecificCredentialId=service_specific_credential['ServiceSpecificCredentialId'])
        signing_certificates = connection.list_signing_certificates(UserName=user_name)['Certificates']
        for signing_certificate in signing_certificates:
            connection.delete_signing_certificate(UserName=user_name, CertificateId=signing_certificate['CertificateId'])
        mfa_devices = connection.list_mfa_devices(UserName=user_name)['MFADevices']
        for mfa_device in mfa_devices:
            connection.deactivate_mfa_device(UserName=user_name, SerialNumber=mfa_device['SerialNumber'])
        inline_policies = connection.list_user_policies(UserName=user_name)['PolicyNames']
        for policy_name in inline_policies:
            connection.delete_user_policy(UserName=user_name, PolicyName=policy_name)
        user_groups = connection.list_groups_for_user(UserName=user_name)['Groups']
        for group in user_groups:
            connection.remove_user_from_group(UserName=user_name, GroupName=group['GroupName'])
        connection.delete_user(UserName=user_name)
    except (ClientError, BotoCoreError) as e:
        module.fail_json_aws(e, msg='Unable to delete user {0}'.format(user_name))
    module.exit_json(changed=True)