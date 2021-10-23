@classmethod
def get_entries_from_page(cls, page):
    entries = []
    for item in re.findall('class="data"[^<>]*>([^<>]+)</', page):
        song_mid = unescapeHTML(item).split('|')[(- 5)]
        entries.append(cls.url_result(('http://y.qq.com/#type=song&mid=' + song_mid), 'QQMusic', song_mid))
    return entries