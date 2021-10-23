

@plac.annotations(input_file=('Input file', 'positional', None, str), output_dir=('Output directory for converted file', 'positional', None, str), file_type=("Type of data to produce: 'jsonl' or 'json'", 'option', 't', str), n_sents=('Number of sentences per doc', 'option', 'n', int), converter=('Name of converter (auto, iob, conllu or ner)', 'option', 'c', str), lang=('Language (if tokenizer required)', 'option', 'l', str), morphology=('Enable appending morphology to tags', 'flag', 'm', bool))
def convert(input_file, output_dir='-', file_type='jsonl', n_sents=1, morphology=False, converter='auto', lang=None):
    '\n    Convert files into JSON format for use with train command and other\n    experiment management functions. If no output_dir is specified, the data\n    is written to stdout, so you can pipe them forward to a JSONL file:\n    $ spacy convert some_file.conllu > some_file.jsonl\n    '
    msg = Printer()
    input_path = Path(input_file)
    if (file_type not in FILE_TYPES):
        msg.fail("Unknown file type: '{}'".format(file_type), "Supported file types: '{}'".format(', '.join(FILE_TYPES)), exits=1)
    if (not input_path.exists()):
        msg.fail('Input file not found', input_path, exits=1)
    if ((output_dir != '-') and (not Path(output_dir).exists())):
        msg.fail('Output directory not found', output_dir, exits=1)
    if (converter == 'auto'):
        converter = input_path.suffix[1:]
    if (converter not in CONVERTERS):
        msg.fail("Can't find converter for {}".format(converter), exits=1)
    func = CONVERTERS[converter]
    input_data = input_path.open('r', encoding='utf-8').read()
    data = func(input_data, n_sents=n_sents, use_morphology=morphology, lang=lang)
    if (output_dir != '-'):
        suffix = '.{}'.format(file_type)
        output_file = (Path(output_dir) / Path(input_path.parts[(- 1)]).with_suffix(suffix))
        if (file_type == 'json'):
            srsly.write_json(output_file, data)
        elif (file_type == 'jsonl'):
            srsly.write_jsonl(output_file, data)
        msg.good('Generated output file ({} documents)'.format(len(data)), output_file)
    elif (file_type == 'json'):
        srsly.write_json('-', data)
    elif (file_type == 'jsonl'):
        srsly.write_jsonl('-', data)
