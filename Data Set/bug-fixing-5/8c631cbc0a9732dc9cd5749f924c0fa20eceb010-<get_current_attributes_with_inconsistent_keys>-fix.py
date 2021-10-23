def get_current_attributes_with_inconsistent_keys(instance):
    options = {
        
    }
    if instance.get('PendingModifiedValues', {
        
    }).get('PendingCloudwatchLogsExports', {
        
    }).get('LogTypesToEnable', []):
        current_enabled = instance['PendingModifiedValues']['PendingCloudwatchLogsExports']['LogTypesToEnable']
        current_disabled = instance['PendingModifiedValues']['PendingCloudwatchLogsExports']['LogTypesToDisable']
        options['CloudwatchLogsExportConfiguration'] = {
            'LogTypesToEnable': current_enabled,
            'LogTypesToDisable': current_disabled,
        }
    else:
        options['CloudwatchLogsExportConfiguration'] = {
            'LogTypesToEnable': instance.get('EnabledCloudwatchLogsExports', []),
            'LogTypesToDisable': [],
        }
    if instance.get('PendingModifiedValues', {
        
    }).get('Port'):
        options['DBPortNumber'] = instance['PendingModifiedValues']['Port']
    else:
        options['DBPortNumber'] = instance['Endpoint']['Port']
    if instance.get('PendingModifiedValues', {
        
    }).get('DBSubnetGroupName'):
        options['DBSubnetGroupName'] = instance['PendingModifiedValues']['DBSubnetGroupName']
    else:
        options['DBSubnetGroupName'] = instance['DBSubnetGroup']['DBSubnetGroupName']
    if instance.get('PendingModifiedValues', {
        
    }).get('ProcessorFeatures'):
        options['ProcessorFeatures'] = instance['PendingModifiedValues']['ProcessorFeatures']
    else:
        options['ProcessorFeatures'] = instance.get('ProcessorFeatures', {
            
        })
    options['OptionGroupName'] = [g['OptionGroupName'] for g in instance['OptionGroupMemberships']]
    options['DBSecurityGroups'] = [sg['DBSecurityGroupName'] for sg in instance['DBSecurityGroups'] if (sg['Status'] in ['adding', 'active'])]
    options['VpcSecurityGroupIds'] = [sg['VpcSecurityGroupId'] for sg in instance['VpcSecurityGroups'] if (sg['Status'] in ['adding', 'active'])]
    options['DBParameterGroupName'] = [parameter_group['DBParameterGroupName'] for parameter_group in instance['DBParameterGroups']]
    options['AllowMajorVersionUpgrade'] = None
    options['EnableIAMDatabaseAuthentication'] = instance['IAMDatabaseAuthenticationEnabled']
    options['EnablePerformanceInsights'] = instance.get('PerformanceInsightsEnabled', False)
    options['MasterUserPassword'] = None
    options['NewDBInstanceIdentifier'] = instance['DBInstanceIdentifier']
    return options