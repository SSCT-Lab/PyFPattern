def handle_response(response):
    results = []
    if response['ins_api'].get('outputs'):
        for output in to_list(response['ins_api']['outputs']['output']):
            if (output['code'] != '200'):
                raise ConnectionError(('%s: %s' % (output['input'], output['msg'])))
            elif ('body' in output):
                result = output['body']
                if isinstance(result, dict):
                    result = json.dumps(result)
                results.append(result.strip())
    return results