def get_available_features(feature, module):
    available_features = {
        
    }
    feature_regex = '(?P<feature>\\S+)\\s+\\d+\\s+(?P<state>.*)'
    command = 'show feature'
    command = {
        'command': command,
        'output': 'text',
    }
    try:
        body = run_commands(module, [command])[0]
        split_body = body.splitlines()
    except (KeyError, AttributeError, IndexError):
        return {
            
        }
    for line in split_body:
        try:
            match_feature = re.match(feature_regex, line, re.DOTALL)
            feature_group = match_feature.groupdict()
            feature = feature_group['feature']
            state = feature_group['state']
        except AttributeError:
            feature = ''
            state = ''
        if (feature and state):
            if ('enabled' in state):
                state = 'enabled'
            if (feature not in available_features):
                available_features[feature] = state
            elif ((available_features[feature] == 'disabled') and (state == 'enabled')):
                available_features[feature] = state
    return available_features