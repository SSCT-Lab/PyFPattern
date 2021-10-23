

def map_config_to_obj(module):
    objs = []
    output = run_commands(module, {
        'command': 'show vrf',
    })
    if (output is not None):
        vrfText = output[0].strip()
        vrfList = vrfText.split('VRF')
        for vrfItem in vrfList:
            if ('FIB ID' in vrfItem):
                obj = dict()
                list_of_words = vrfItem.split()
                vrfName = list_of_words[0]
                obj['name'] = vrfName[:(- 1)]
                obj['rd'] = list_of_words[(list_of_words.index('RD') + 1)]
                start = False
                obj['interfaces'] = []
                for intName in list_of_words:
                    if ('Interfaces' in intName):
                        start = True
                    if (start is True):
                        if (('!' not in intName) and ('Interfaces' not in intName)):
                            obj['interfaces'].append(intName.strip().lower())
                objs.append(obj)
    else:
        module.fail_json(msg='Could not fetch VRF details from device')
    return objs
