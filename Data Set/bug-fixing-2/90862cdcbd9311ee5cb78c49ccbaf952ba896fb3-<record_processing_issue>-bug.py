

def record_processing_issue(self, raw_event, scope, object, type, data=None):
    'Records a new processing issue for the given raw event.'
    data = dict((data or {
        
    }))
    checksum = get_processing_issue_checksum(scope, object)
    data['_scope'] = scope
    data['_object'] = object
    (issue, _) = ProcessingIssue.objects.get_or_create(project_id=raw_event.project_id, checksum=checksum, type=type, data=data)
    ProcessingIssue.objects.filter(pk=issue.id).update(datetime=timezone.now())
    EventProcessingIssue.objects.get_or_create(raw_event=raw_event, processing_issue=issue)
