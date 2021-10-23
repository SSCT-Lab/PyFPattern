@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    if page_perms.can_edit():
        (yield PageListingButton(_('Edit'), reverse('wagtailadmin_pages:edit', args=[page.id]), attrs={
            'title': _('Edit this page'),
        }, priority=10))
    if page.has_unpublished_changes:
        (yield PageListingButton(_('View draft'), reverse('wagtailadmin_pages:view_draft', args=[page.id]), attrs={
            'title': _('Preview draft'),
            'target': '_blank',
        }, priority=20))
    if (page.live and page.url):
        (yield PageListingButton(_('View live'), page.url, attrs={
            'target': '_blank',
            'title': _('View live'),
        }, priority=30))
    if page_perms.can_add_subpage():
        if is_parent:
            (yield Button(_('Add child page'), reverse('wagtailadmin_pages:add_subpage', args=[page.id]), attrs={
                'title': _("Add a child page to '{0}' ").format(page.get_admin_display_title()),
            }, classes={'button', 'button-small', 'bicolor', 'icon', 'white', 'icon-plus'}, priority=40))
        else:
            (yield PageListingButton(_('Add child page'), reverse('wagtailadmin_pages:add_subpage', args=[page.id]), attrs={
                'title': _("Add a child page to '{0}' ").format(page.get_admin_display_title()),
            }, priority=40))
    (yield ButtonWithDropdownFromHook(_('More'), hook_name='register_page_listing_more_buttons', page=page, page_perms=page_perms, is_parent=is_parent, attrs={
        'target': '_blank',
        'title': _('View more options'),
    }, priority=50))