def __init__(self, module):
    self.module = module
    self.netapp_info = dict()
    self.info_subsets = {
        'net_dns_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'net-dns-get-iter',
                'attribute': 'net-dns-info',
                'field': 'vserver-name',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'net_interface_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'net-interface-get-iter',
                'attribute': 'net-interface-info',
                'field': 'interface-name',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'net_port_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'net-port-get-iter',
                'attribute': 'net-port-info',
                'field': ('node', 'port'),
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'cluster_node_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'cluster-node-get-iter',
                'attribute': 'cluster-node-info',
                'field': 'node-name',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'security_login_account_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'security-login-get-iter',
                'attribute': 'security-login-account-info',
                'field': ('vserver', 'user-name', 'application', 'authentication-method'),
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'aggregate_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'aggr-get-iter',
                'attribute': 'aggr-attributes',
                'field': 'aggregate-name',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'volume_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'volume-get-iter',
                'attribute': 'volume-attributes',
                'field': ('name', 'owning-vserver-name'),
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'lun_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'lun-get-iter',
                'attribute': 'lun-info',
                'field': ('vserver', 'path'),
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'storage_failover_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'cf-get-iter',
                'attribute': 'storage-failover-info',
                'field': 'node',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'vserver_motd_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'vserver-motd-get-iter',
                'attribute': 'vserver-motd-info',
                'field': 'vserver',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'vserver_login_banner_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'vserver-login-banner-get-iter',
                'attribute': 'vserver-login-banner-info',
                'field': 'vserver',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'security_key_manager_key_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'security-key-manager-key-get-iter',
                'attribute': 'security-key-manager-key-info',
                'field': ('node', 'key-id'),
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'vserver_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'vserver-get-iter',
                'attribute': 'vserver-info',
                'field': 'vserver-name',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'vserver_nfs_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'nfs-service-get-iter',
                'attribute': 'nfs-info',
                'field': 'vserver',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'net_ifgrp_info': {
            'method': self.get_ifgrp_info,
            'kwargs': {
                
            },
            'min_version': '0',
        },
        'ontap_version': {
            'method': self.ontapi,
            'kwargs': {
                
            },
            'min_version': '0',
        },
        'system_node_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'system-node-get-iter',
                'attribute': 'node-details-info',
                'field': 'node',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'igroup_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'igroup-get-iter',
                'attribute': 'initiator-group-info',
                'field': ('vserver', 'initiator-group-name'),
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'qos_policy_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'qos-policy-group-get-iter',
                'attribute': 'qos-policy-group-info',
                'field': 'policy-group',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '0',
        },
        'qos_adaptive_policy_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'qos-adaptive-policy-group-get-iter',
                'attribute': 'qos-adaptive-policy-group-info',
                'field': 'policy-group',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '130',
        },
        'nvme_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'nvme-get-iter',
                'attribute': 'nvme-target-service-info',
                'field': 'vserver',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '140',
        },
        'nvme_interface_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'nvme-interface-get-iter',
                'attribute': 'nvme-interface-info',
                'field': 'vserver',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '140',
        },
        'nvme_subsystem_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'nvme-subsystem-get-iter',
                'attribute': 'nvme-subsystem-info',
                'field': 'subsystem',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '140',
        },
        'nvme_namespace_info': {
            'method': self.get_generic_get_iter,
            'kwargs': {
                'call': 'nvme-namespace-get-iter',
                'attribute': 'nvme-namespace-info',
                'field': 'path',
                'query': {
                    'max-records': '1024',
                },
            },
            'min_version': '140',
        },
    }
    if (HAS_NETAPP_LIB is False):
        self.module.fail_json(msg='the python NetApp-Lib module is required')
    else:
        self.server = netapp_utils.setup_na_ontap_zapi(module=self.module)