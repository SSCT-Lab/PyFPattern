def metadata_decoder(metadata):
    items = {
        
    }
    if ('items' in metadata):
        metadata_items = metadata['items']
        for item in metadata_items:
            items[item['key']] = item['value']
    return items