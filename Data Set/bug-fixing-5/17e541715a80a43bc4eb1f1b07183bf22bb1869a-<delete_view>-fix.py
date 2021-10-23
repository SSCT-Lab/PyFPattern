def delete_view(self, request, instance_pk):
    "\n        Instantiates a class-based view to provide 'delete confirmation'\n        functionality for the assigned model, or redirect to Wagtail's delete\n        confirmation view if the assigned model extends 'Page'. The view class\n        used can be overridden by changing the 'delete_view_class'\n        attribute.\n        "
    kwargs = {
        'model_admin': self,
        'instance_pk': instance_pk,
    }
    view_class = self.delete_view_class
    return view_class.as_view(**kwargs)(request)