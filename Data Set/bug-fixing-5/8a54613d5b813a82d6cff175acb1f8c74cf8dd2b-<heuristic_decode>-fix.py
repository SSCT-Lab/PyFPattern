def heuristic_decode(data, possible_content_type=None):
    '\n    Attempt to decode a HTTP body by trying JSON and Form URL decoders,\n    returning the decoded body (if decoding was successful) and the inferred\n    content type.\n    '
    inferred_content_type = possible_content_type
    form_encoded_parser = partial(parse_qs, strict_parsing=True, keep_blank_values=True)
    decoders = [('application/json', json.loads), ('application/x-www-form-urlencoded', form_encoded_parser)]
    decoders.sort(key=(lambda d: (d[0] == possible_content_type)), reverse=True)
    for (decoding_type, decoder) in decoders:
        try:
            return (decoder(data), decoding_type)
        except Exception:
            continue
    return (data, inferred_content_type)