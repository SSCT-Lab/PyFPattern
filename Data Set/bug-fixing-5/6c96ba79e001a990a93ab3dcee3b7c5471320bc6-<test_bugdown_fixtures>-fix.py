@slow('Aggregate of runs dozens of individual markdown tests')
def test_bugdown_fixtures(self) -> None:
    (format_tests, linkify_tests) = self.load_bugdown_tests()
    valid_keys = set(['name', 'input', 'expected_output', 'backend_only_rendering', 'marked_expected_output', 'text_content', 'translate_emoticons', 'ignore'])
    for (name, test) in format_tests.items():
        self.assertEqual(len((set(test.keys()) - valid_keys)), 0)
        if test.get('ignore', False):
            continue
        if test.get('translate_emoticons', False):
            user_profile = self.example_user('othello')
            do_set_user_display_setting(user_profile, 'translate_emoticons', True)
            msg = Message(sender=user_profile, sending_client=get_client('test'))
            converted = render_markdown(msg, test['input'])
        else:
            converted = bugdown_convert(test['input'])
        print(('Running Bugdown test %s' % (name,)))
        self.assertEqual(converted, test['expected_output'])

    def replaced(payload: Text, url: Text, phrase: Text='') -> Text:
        target = ' target="_blank"'
        if (url[:4] == 'http'):
            href = url
        elif ('@' in url):
            href = ('mailto:' + url)
            target = ''
        else:
            href = ('http://' + url)
        return (payload % (('<a href="%s"%s title="%s">%s</a>' % (href, target, href, url)),))
    print('Running Bugdown Linkify tests')
    with mock.patch('zerver.lib.url_preview.preview.link_embed_data_from_cache', return_value=None):
        for (inline_url, reference, url) in linkify_tests:
            try:
                match = replaced(reference, url, phrase=inline_url)
            except TypeError:
                match = reference
            converted = bugdown_convert(inline_url)
            self.assertEqual(match, converted)