def get_running_config(module, current_config=None, flags=None):
    contents = module.params['running_config']
    if (not contents):
        if ((not module.params['defaults']) and current_config):
            (contents, banners) = extract_banners(current_config.config_text)
        else:
            contents = get_config(module, flags=flags)
    (contents, banners) = extract_banners(contents)
    return (NetworkConfig(indent=1, contents=contents), banners)