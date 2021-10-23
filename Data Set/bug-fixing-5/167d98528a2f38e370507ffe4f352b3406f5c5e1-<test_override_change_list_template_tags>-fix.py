def test_override_change_list_template_tags(self):
    '\n        admin_list template tags follow the standard search pattern\n        admin/app_label/model/template.html.\n        '
    factory = RequestFactory()
    request = factory.get(reverse('admin:admin_views_article_changelist'))
    request.user = self.superuser
    admin = ArticleAdmin(Article, site)
    admin.date_hierarchy = 'date'
    admin.search_fields = ('title', 'content')
    response = admin.changelist_view(request)
    response.render()
    self.assertContains(response, 'override-actions')
    self.assertContains(response, 'override-change_list_object_tools')
    self.assertContains(response, 'override-change_list_results')
    self.assertContains(response, 'override-date_hierarchy')
    self.assertContains(response, 'override-pagination')
    self.assertContains(response, 'override-search_form')