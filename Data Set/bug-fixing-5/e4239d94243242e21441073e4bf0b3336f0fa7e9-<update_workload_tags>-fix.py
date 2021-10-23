def update_workload_tags(self, check_mode=False):
    'Check the status of the workload tag and update storage array definitions if necessary.\n\n        When the workload attributes are not provided but an existing workload tag name is, then the attributes will be\n        used.\n\n        :return bool: Whether changes were required to be made.'
    change_required = False
    workload_tags = None
    request_body = None
    ansible_profile_id = None
    if self.workload_name:
        try:
            (rc, workload_tags) = self.request(('storage-systems/%s/workloads' % self.ssid))
        except Exception as error:
            self.module.fail_json(msg=('Failed to retrieve storage array workload tags. Array [%s]' % self.ssid))
        current_tag_index_list = [int(pair['value'].replace('ansible_workload_', '')) for tag in workload_tags for pair in tag['workloadAttributes'] if ((pair['key'] == 'profileId') and ('ansible_workload_' in pair['value']) and str(pair['value']).replace('ansible_workload_', '').isdigit())]
        tag_index = 1
        if current_tag_index_list:
            tag_index = (max(current_tag_index_list) + 1)
        ansible_profile_id = ('ansible_workload_%d' % tag_index)
        request_body = dict(name=self.workload_name, profileId=ansible_profile_id, workloadInstanceIndex=None, isValid=True)
        for tag in workload_tags:
            if (tag['name'] == self.workload_name):
                self.workload_id = tag['id']
                if (not self.metadata):
                    break
                metadata_set = set((tuple(sorted(attr.items())) for attr in self.metadata))
                tag_set = set((tuple(sorted(attr.items())) for attr in tag['workloadAttributes'] if (attr['key'] != 'profileId')))
                if (metadata_set != tag_set):
                    self.module.log('Workload tag change is required!')
                    change_required = True
                if (change_required and (not check_mode)):
                    self.metadata.append(dict(key='profileId', value=ansible_profile_id))
                    request_body.update(dict(isNewWorkloadInstance=False, isWorkloadDataInitialized=True, isWorkloadCardDataToBeReset=True, workloadAttributes=self.metadata))
                    try:
                        (rc, resp) = self.request(('storage-systems/%s/workloads/%s' % (self.ssid, tag['id'])), data=request_body, method='POST')
                    except Exception as error:
                        self.module.fail_json(msg=('Failed to create new workload tag. Array [%s]. Error [%s]' % (self.ssid, to_native(error))))
                    self.module.log(('Workload tag [%s] required change.' % self.workload_name))
                break
        else:
            change_required = True
            self.module.log('Workload tag creation is required!')
            if (change_required and (not check_mode)):
                if self.metadata:
                    self.metadata.append(dict(key='profileId', value=ansible_profile_id))
                else:
                    self.metadata = [dict(key='profileId', value=ansible_profile_id)]
                request_body.update(dict(isNewWorkloadInstance=True, isWorkloadDataInitialized=False, isWorkloadCardDataToBeReset=False, workloadAttributes=self.metadata))
                try:
                    (rc, resp) = self.request(('storage-systems/%s/workloads' % self.ssid), method='POST', data=request_body)
                    self.workload_id = resp['id']
                except Exception as error:
                    self.module.fail_json(msg=('Failed to create new workload tag. Array [%s]. Error [%s]' % (self.ssid, to_native(error))))
            self.module.log(('Workload tag [%s] was added.' % self.workload_name))
    return change_required