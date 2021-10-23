def main():
    'Validate BOTMETA'
    path = '.github/BOTMETA.yml'
    try:
        with open(path, 'r') as f_path:
            botmeta = yaml.safe_load(f_path)
    except yaml.error.MarkedYAMLError as ex:
        print(('%s:%d:%d: YAML load failed: %s' % (path, (ex.context_mark.line + 1), (ex.context_mark.column + 1), re.sub('\\s+', ' ', str(ex)))))
        sys.exit()
    except Exception as ex:
        print(('%s:%d:%d: YAML load failed: %s' % (path, 0, 0, re.sub('\\s+', ' ', str(ex)))))
        sys.exit()
    files_schema = Any(Schema(*string_types), Schema({
        'ignored': Any(list_string_types, *string_types),
        'keywords': Any(list_string_types, *string_types),
        'labels': Any(list_string_types, *string_types),
        'maintainers': Any(list_string_types, *string_types),
        'notified': Any(list_string_types, *string_types),
        'support': Any('core', 'network', 'community'),
    }))
    list_dict_file_schema = [{
        str_type: files_schema,
    } for str_type in string_types]
    schema = Schema({
        Required('automerge'): bool,
        Required('files'): Any(None, *list_dict_file_schema),
        Required('macros'): dict,
    })
    try:
        schema(botmeta)
    except MultipleInvalid as ex:
        for error in ex.errors:
            print(('%s:%d:%d: %s' % (path, 0, 0, humanize_error(botmeta, error))))
    botmeta_support = botmeta.get('files', {
        
    }).get('.github/BOTMETA.yml', {
        
    }).get('support', '')
    if (botmeta_support != 'core'):
        print(('%s:%d:%d: .github/BOTMETA.yml MUST be support: core' % (path, 0, 0)))
    module_utils_path = botmeta.get('macros', {
        
    }).get('module_utils', '')
    modules_path = botmeta.get('macros', {
        
    }).get('modules', '')
    if (module_utils_path != 'lib/ansible/module_utils'):
        print(('%s:%d:%d: [macros][module_utils] has been changed or removed' % (path, 0, 0)))
    if (modules_path != 'lib/ansible/modules'):
        print(('%s:%d:%d: [macros][modules] has been changed or removed' % (path, 0, 0)))
    for file in botmeta['files']:
        file = file.replace('$module_utils', module_utils_path)
        file = file.replace('$modules', modules_path)
        if (not os.path.exists(file)):
            if (not glob.glob(('%s*' % file))):
                print(("%s:%d:%d: Can't find '%s.*' in this branch" % (path, 0, 0, file)))