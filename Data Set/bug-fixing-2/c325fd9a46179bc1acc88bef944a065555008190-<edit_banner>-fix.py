

def edit_banner(self, candidate=None, multiline_delimiter='@', commit=True):
    '\n        Edit banner on remote device\n        :param banners: Banners to be loaded in json format\n        :param multiline_delimiter: Line delimiter for banner\n        :param commit: Boolean value that indicates if the device candidate\n               configuration should be  pushed in the running configuration or discarded.\n        :param diff: Boolean flag to indicate if configuration that is applied on remote host should\n                     generated and returned in response or not\n        :return: Returns response of executing the configuration command received\n             from remote host\n        '
    resp = {
        
    }
    banners_obj = json.loads(candidate)
    results = []
    requests = []
    if commit:
        for (key, value) in iteritems(banners_obj):
            key += (' %s' % multiline_delimiter)
            self.send_command('config terminal', sendonly=True)
            for cmd in [key, value, multiline_delimiter]:
                obj = {
                    'command': cmd,
                    'sendonly': True,
                }
                results.append(self.send_command(**obj))
                requests.append(cmd)
            self.send_command('end', sendonly=True)
            time.sleep(0.1)
            results.append(self.send_command('\n'))
            requests.append('\n')
    resp['request'] = requests
    resp['response'] = results
    return resp
