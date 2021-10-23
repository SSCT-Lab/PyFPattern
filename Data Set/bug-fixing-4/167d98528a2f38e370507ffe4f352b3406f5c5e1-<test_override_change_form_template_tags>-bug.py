def test_override_change_form_template_tags(self):
    '\n        admin_modify template tags follow the standard search pattern\n        admin/app_label/model/template.html.\n        '
    factory = RequestFactory()
    article = Article.objects.all()[0]
    request = factory.get(reverse('admin:admin_views_article_change', args=[article.pk]))
    request.user = self.superuser
    admin = ArticleAdmin(Article, site)
    extra_context = {
        'show_publish': True,
        'extra': True,
    }
    response = admin.change_view(request, str(article.pk), extra_context=extra_context)
    response.render()
    self.assertIs(response.context_data['show_publish'], True)
    self.assertIs(response.context_data['extra'], True)
    content = str(response.content)
    self.assertIn('name="_save"', content)
    self.assertIn('name="_publish"', content)
    self.assertIn('override-change_form_object_tools', content)
    self.assertIn('override-prepopulated_fields_js', content)