def test_keystore(module, keystore_path):
    ' Check if we can access keystore as file or not '
    if (keystore_path is None):
        keystore_path = ''
    if ((not os.path.exists(keystore_path)) and (not os.path.isfile(keystore_path))):
        module.fail_json(changed=False, msg=("Module require existing keystore at keystore_path '%s'" % keystore_path))