def handle_message(self, message, client, state_handler):
    query = message['content']
    for prefix in ['@wikipedia', '@wiki']:
        if query.startswith(prefix):
            query = query[(len(prefix) + 1):]
            break
    query_wiki_link = ('https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=%s&format=json' % (query,))
    try:
        data = requests.get(query_wiki_link)
    except requests.exceptions.RequestException:
        logging.error('broken link')
        return
    if (data.status_code != 200):
        logging.error('unsuccessful data')
        return
    search_string = data.json()['query']['search'][0]['title'].replace(' ', '_')
    url = ('https://wikipedia.org/wiki/' + search_string)
    new_content = ('For search term "' + query)
    if (len(data.json()['query']['search']) == 0):
        new_content = 'I am sorry. The search term you provided is not found :slightly_frowning_face:'
    else:
        new_content = ((new_content + '", ') + url)
    client.send_message(dict(type=message['type'], to=message['display_recipient'], subject=message['subject'], content=new_content))