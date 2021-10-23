def collect(self, module=None, collected_facts=None):
    '\n        Example of contents of /etc/iscsi/initiatorname.iscsi:\n\n        ## DO NOT EDIT OR REMOVE THIS FILE!\n        ## If you remove this file, the iSCSI daemon will not start.\n        ## If you change the InitiatorName, existing access control lists\n        ## may reject this initiator.  The InitiatorName must be unique\n        ## for each iSCSI initiator.  Do NOT duplicate iSCSI InitiatorNames.\n        InitiatorName=iqn.1993-08.org.debian:01:44a42c8ddb8b\n\n        Example of output from the AIX lsattr command:\n\n        # lsattr -E -l iscsi0\n        disc_filename  /etc/iscsi/targets            Configuration file                            False\n        disc_policy    file                          Discovery Policy                              True\n        initiator_name iqn.localhost.hostid.7f000001 iSCSI Initiator Name                          True\n        isns_srvnames  auto                          iSNS Servers IP Addresses                     True\n        isns_srvports                                iSNS Servers Port Numbers                     True\n        max_targets    16                            Maximum Targets Allowed                       True\n        num_cmd_elems  200                           Maximum number of commands to queue to driver True\n        '
    iscsi_facts = ''
    iscsi_facts['iscsi_iqn'] = ''
    if (sys.platform.startswith('linux') or sys.platform.startswith('sunos')):
        for line in get_file_content('/etc/iscsi/initiatorname.iscsi', '').splitlines():
            if (line.startswith('#') or line.startswith(';') or (line.strip() == '')):
                continue
            if line.startswith('InitiatorName='):
                iscsi_facts['iscsi_iqn'] = line.split('=', 1)[1]
                break
    elif sys.platform.startswith('aix'):
        aixcmd = '/usr/sbin/lsattr -E -l iscsi0 | grep initiator_name'
        aixret = subprocess.check_output(aixcmd, shell=True)
        if aixret[0].isalpha():
            iscsi_facts['iscsi_iqn'] = aixret.split()[1].rstrip()
    return iscsi_facts