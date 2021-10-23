

def generate_ansible_template_vars(path):
    b_path = to_bytes(path)
    try:
        template_uid = pwd.getpwuid(os.stat(b_path).st_uid).pw_name
    except (KeyError, TypeError):
        template_uid = os.stat(b_path).st_uid
    temp_vars = {
        
    }
    temp_vars['template_host'] = to_text(os.uname()[1])
    temp_vars['template_path'] = path
    temp_vars['template_mtime'] = datetime.datetime.fromtimestamp(os.path.getmtime(b_path))
    temp_vars['template_uid'] = to_text(template_uid)
    temp_vars['template_fullpath'] = os.path.abspath(path)
    temp_vars['template_run_date'] = datetime.datetime.now()
    managed_default = C.DEFAULT_MANAGED_STR
    managed_str = managed_default.format(host=temp_vars['template_host'], uid=temp_vars['template_uid'], file=temp_vars['template_path'])
    temp_vars['ansible_managed'] = to_text(time.strftime(to_native(managed_str), time.localtime(os.path.getmtime(b_path))))
    return temp_vars
