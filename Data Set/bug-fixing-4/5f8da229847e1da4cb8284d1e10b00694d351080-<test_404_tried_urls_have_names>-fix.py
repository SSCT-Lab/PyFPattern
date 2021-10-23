def test_404_tried_urls_have_names(self):
    '\n        Verifies that the list of URLs that come back from a Resolver404\n        exception contains a list in the right format for printing out in\n        the DEBUG 404 page with both the patterns and URL names, if available.\n        '
    urls = 'urlpatterns_reverse.named_urls'
    url_types_names = [[{
        'type': RegexURLPattern,
        'name': 'named-url1',
    }], [{
        'type': RegexURLPattern,
        'name': 'named-url2',
    }], [{
        'type': RegexURLPattern,
        'name': None,
    }], [{
        'type': RegexURLResolver,
    }, {
        'type': RegexURLPattern,
        'name': 'named-url3',
    }], [{
        'type': RegexURLResolver,
    }, {
        'type': RegexURLPattern,
        'name': 'named-url4',
    }], [{
        'type': RegexURLResolver,
    }, {
        'type': RegexURLPattern,
        'name': None,
    }], [{
        'type': RegexURLResolver,
    }, {
        'type': RegexURLResolver,
    }]]
    with self.assertRaisesMessage(Resolver404, (b'tried' if six.PY2 else 'tried')) as cm:
        resolve('/included/non-existent-url', urlconf=urls)
    e = cm.exception
    self.assertIn('tried', e.args[0])
    tried = e.args[0]['tried']
    self.assertEqual(len(e.args[0]['tried']), len(url_types_names), ('Wrong number of tried URLs returned.  Expected %s, got %s.' % (len(url_types_names), len(e.args[0]['tried']))))
    for (tried, expected) in zip(e.args[0]['tried'], url_types_names):
        for (t, e) in zip(tried, expected):
            (self.assertIsInstance(t, e['type']), (str('%s is not an instance of %s') % (t, e['type'])))
            if ('name' in e):
                if (not e['name']):
                    self.assertIsNone(t.name, ('Expected no URL name but found %s.' % t.name))
                else:
                    self.assertEqual(t.name, e['name'], ('Wrong URL name.  Expected "%s", got "%s".' % (e['name'], t.name)))