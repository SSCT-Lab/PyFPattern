@AWSRetry.exponential_backoff()
def get_tags(self, file_system_id):
    '\n         Returns tag list for selected instance of EFS\n        '
    paginator = self.connection.get_paginator('describe_tags')
    return boto3_tag_list_to_ansible_dict(paginator.paginate(FileSystemId=file_system_id).build_full_result()['Tags'])