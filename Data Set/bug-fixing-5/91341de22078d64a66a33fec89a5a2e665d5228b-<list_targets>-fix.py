def list_targets(self):
    'Lists the existing targets for the rule in AWS'
    try:
        targets = self.client.list_targets_by_rule(Rule=self.name)
    except botocore.exceptions.ClientError as e:
        error_code = e.response.get('Error', {
            
        }).get('Code')
        if (error_code == 'ResourceNotFoundException'):
            return []
        raise
    return self._snakify(targets)['targets']