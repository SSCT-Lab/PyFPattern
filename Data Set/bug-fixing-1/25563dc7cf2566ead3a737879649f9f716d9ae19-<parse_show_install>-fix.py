

def parse_show_install(data):
    'Helper method to parse the output of the \'show install all impact\' or\n        \'install all\' commands.\n\n    Sample Output:\n\n    Installer will perform impact only check. Please wait.\n\n    Verifying image bootflash:/nxos.7.0.3.F2.2.bin for boot variable "nxos".\n    [####################] 100% -- SUCCESS\n\n    Verifying image type.\n    [####################] 100% -- SUCCESS\n\n    Preparing "bios" version info using image bootflash:/nxos.7.0.3.F2.2.bin.\n    [####################] 100% -- SUCCESS\n\n    Preparing "nxos" version info using image bootflash:/nxos.7.0.3.F2.2.bin.\n    [####################] 100% -- SUCCESS\n\n    Performing module support checks.\n    [####################] 100% -- SUCCESS\n\n    Notifying services about system upgrade.\n    [####################] 100% -- SUCCESS\n\n\n\n    Compatibility check is done:\n    Module  bootable          Impact  Install-type  Reason\n    ------  --------  --------------  ------------  ------\n         8       yes      disruptive         reset  Incompatible image for ISSU\n        21       yes      disruptive         reset  Incompatible image for ISSU\n\n\n    Images will be upgraded according to following table:\n    Module       Image  Running-Version(pri:alt)    New-Version   Upg-Required\n    ------  ----------  ----------------------------------------  ------------\n         8       lcn9k                7.0(3)F3(2)    7.0(3)F2(2)           yes\n         8        bios                     v01.17         v01.17            no\n        21       lcn9k                7.0(3)F3(2)    7.0(3)F2(2)           yes\n        21        bios                     v01.70         v01.70            no\n    '
    if (len(data) > 0):
        data = massage_install_data(data)
    ud = {
        'raw': data,
    }
    ud['processed'] = []
    ud['disruptive'] = False
    ud['upgrade_needed'] = False
    ud['error'] = False
    ud['install_in_progress'] = False
    ud['server_error'] = False
    ud['upgrade_succeeded'] = False
    ud['use_impact_data'] = False
    if isinstance(data, int):
        if (data == (- 1)):
            ud['server_error'] = True
        elif (data >= 500):
            ud['server_error'] = True
        elif (data == (- 32603)):
            ud['server_error'] = True
        return ud
    else:
        ud['list_data'] = data.split('\n')
    for x in ud['list_data']:
        if re.search('Pre-upgrade check failed', x):
            ud['error'] = True
            break
        if re.search('[I|i]nvalid command', x):
            ud['error'] = True
            break
        if re.search('No install all data found', x):
            ud['error'] = True
            break
        if re.search('Another install procedure may\\s*be in progress', x):
            ud['install_in_progress'] = True
            break
        if re.search('Backend processing error', x):
            ud['server_error'] = True
            break
        if re.search('^(-1|5\\d\\d)$', x):
            ud['server_error'] = True
            break
        if re.search('Finishing the upgrade', x):
            ud['upgrade_succeeded'] = True
            break
        if re.search('Install has been successful', x):
            ud['upgrade_succeeded'] = True
            break
        if re.search('Switching over onto standby', x):
            ud['upgrade_succeeded'] = True
            break
        if re.search('timeout trying to send command: install', x):
            ud['upgrade_succeeded'] = True
            ud['use_impact_data'] = True
            break
        if re.search('[C|c]onnection failure: timed out', x):
            ud['upgrade_succeeded'] = True
            ud['use_impact_data'] = True
            break
        if re.search('----|Module|Images will|Compatibility', x):
            ud['processed'].append(x)
            continue
        rd = '(\\d+)\\s+(\\S+)\\s+(disruptive|non-disruptive)\\s+(\\S+)'
        mo = re.search(rd, x)
        if mo:
            ud['processed'].append(x)
            key = ('m%s' % mo.group(1))
            field = 'disruptive'
            if (mo.group(3) == 'non-disruptive'):
                ud[key] = {
                    field: False,
                }
            else:
                ud[field] = True
                ud[key] = {
                    field: True,
                }
            field = 'bootable'
            if (mo.group(2) == 'yes'):
                ud[key].update({
                    field: True,
                })
            else:
                ud[key].update({
                    field: False,
                })
            continue
        mo = re.search('(\\d+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(yes|no)', x)
        if mo:
            ud['processed'].append(x)
            key = ('m%s_%s' % (mo.group(1), mo.group(2)))
            field = 'upgrade_needed'
            if (mo.group(5) == 'yes'):
                ud[field] = True
                ud[key] = {
                    field: True,
                }
            else:
                ud[key] = {
                    field: False,
                }
            continue
    return ud
