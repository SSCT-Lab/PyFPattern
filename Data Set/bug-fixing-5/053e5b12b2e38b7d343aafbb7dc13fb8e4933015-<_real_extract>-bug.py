def _real_extract(self, url):
    mobj = re.match(self._VALID_URL, url)
    video_id = mobj.group('id')
    entry_id = mobj.group('kaltura_id')
    if (not entry_id):
        webpage = self._download_webpage(url, video_id)
        api_path = self._search_regex('["\\\']apiPath["\\\']\\s*:\\s*["\\\']([^"^\\\']+)["\\\']', webpage, 'api path')
        api_url = ('https://www.%s%s' % (mobj.group('host'), api_path))
        payload = {
            'query': 'query VideoContext($articleId: ID!) {\n                    article: node(id: $articleId) {\n                      ... on Article {\n                        mainAssetRelation {\n                          asset {\n                            ... on VideoAsset {\n                              kalturaId\n                            }\n                          }\n                        }\n                      }\n                    }\n                  }',
            'variables': {
                'articleId': ('Article:%s' % mobj.group('article_id')),
            },
        }
        json_data = self._download_json(api_url, video_id, headers={
            'Content-Type': 'application/json',
        }, data=json.dumps(payload).encode())
        entry_id = json_data['data']['article']['mainAssetRelation']['asset']['kalturaId']
    return self.url_result(('kaltura:%s:%s' % (self._PARTNER_ID, entry_id)), ie=KalturaIE.ie_key(), video_id=entry_id)