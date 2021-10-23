def delete_selected(modeladmin, request, queryset):
    '\n    Default action which deletes the selected objects.\n\n    This action first displays a confirmation page which shows all the\n    deleteable objects, or, if the user has no permission one of the related\n    childs (foreignkeys), a "permission denied" message.\n\n    Next, it deletes all selected objects and redirects back to the change list.\n    '
    opts = modeladmin.model._meta
    app_label = opts.app_label
    if (not modeladmin.has_delete_permission(request)):
        raise PermissionDenied
    using = router.db_for_write(modeladmin.model)
    (deletable_objects, model_count, perms_needed, protected) = get_deleted_objects(queryset, opts, request.user, modeladmin.admin_site, using)
    if (request.POST.get('post') and (not protected)):
        if perms_needed:
            raise PermissionDenied
        n = queryset.count()
        if n:
            for obj in queryset:
                obj_display = str(obj)
                modeladmin.log_deletion(request, obj, obj_display)
            queryset.delete()
            modeladmin.message_user(request, (_('Successfully deleted %(count)d %(items)s.') % {
                'count': n,
                'items': model_ngettext(modeladmin.opts, n),
            }), messages.SUCCESS)
        return None
    objects_name = model_ngettext(queryset)
    if (perms_needed or protected):
        title = (_('Cannot delete %(name)s') % {
            'name': objects_name,
        })
    else:
        title = _('Are you sure?')
    context = dict(modeladmin.admin_site.each_context(request), title=title, objects_name=str(objects_name), deletable_objects=[deletable_objects], model_count=dict(model_count).items(), queryset=queryset, perms_lacking=perms_needed, protected=protected, opts=opts, action_checkbox_name=helpers.ACTION_CHECKBOX_NAME, media=modeladmin.media)
    request.current_app = modeladmin.admin_site.name
    return TemplateResponse(request, (modeladmin.delete_selected_confirmation_template or [('admin/%s/%s/delete_selected_confirmation.html' % (app_label, opts.model_name)), ('admin/%s/delete_selected_confirmation.html' % app_label), 'admin/delete_selected_confirmation.html']), context)