def _set_key_path(self):
    "\n        Sets full key path - if GCP_CONFIG_DIR points to absolute\n            directory, it tries to find the key in this directory. Otherwise it assumes\n            that Airflow is running from the directory where configuration is checked \n            out next to airflow directory in config directory\n            it tries to find the key folder in the workspace's config\n            directory.\n        :param : name of the key file to find.\n        "
    if ('GCP_CONFIG_DIR' in os.environ):
        gcp_config_dir = os.environ['GCP_CONFIG_DIR']
    else:
        gcp_config_dir = os.path.join(AIRFLOW_MAIN_FOLDER, os.pardir, 'config')
    if (not os.path.isdir(gcp_config_dir)):
        self.log.info('The {} is not a directory'.format(gcp_config_dir))
    key_dir = os.path.join(gcp_config_dir, 'keys')
    if (not os.path.isdir(key_dir)):
        self.log.info('The {} is not a directory'.format(key_dir))
        return
    key_path = os.path.join(key_dir, self.gcp_key)
    if (not os.path.isfile(key_path)):
        self.log.info('The {} is missing'.format(key_path))
    self.full_key_path = key_path