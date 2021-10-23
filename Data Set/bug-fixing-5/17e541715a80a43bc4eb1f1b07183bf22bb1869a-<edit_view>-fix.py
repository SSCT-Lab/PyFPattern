def edit_view(self, request, instance_pk):
    "\n        Instantiates a class-based view to provide 'edit' functionality for the\n        assigned model, or redirect to Wagtail's edit view if the assigned\n        model extends 'Page'. The view class used can be overridden by changing\n        the  'edit_view_class' attribute.\n        "
    kwargs = {
        'model_admin': self,
        'instance_pk': instance_pk,
    }
    view_class = self.edit_view_class
    return view_class.as_view(**kwargs)(request)