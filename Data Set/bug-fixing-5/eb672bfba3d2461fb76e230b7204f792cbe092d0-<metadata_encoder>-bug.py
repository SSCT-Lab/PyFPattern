def metadata_encoder(metadata):
    metadata_new = []
    for key in metadata:
        value = metadata[key]
        metadata_new.append({
            key: value,
        })
    return {
        'items': metadata_new,
    }