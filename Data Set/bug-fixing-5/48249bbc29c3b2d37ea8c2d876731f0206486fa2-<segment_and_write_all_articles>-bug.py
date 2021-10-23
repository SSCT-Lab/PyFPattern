def segment_and_write_all_articles(file_path, output_file, min_article_character=200, workers=None):
    "Write article title and sections to `output_file` (or stdout, if output_file is None).\n\n    The output format is one article per line, in json-line format with 3 fields::\n\n        'title' - title of article,\n        'section_titles' - list of titles of sections,\n        'section_texts' - list of content from sections.\n\n    Parameters\n    ----------\n    file_path : str\n        Path to MediaWiki dump, typical filename is <LANG>wiki-<YYYYMMDD>-pages-articles.xml.bz2\n        or <LANG>wiki-latest-pages-articles.xml.bz2.\n\n    output_file : str or None\n        Path to output file in json-lines format, or None for printing to stdout.\n\n    min_article_character : int, optional\n        Minimal number of character for article (except titles and leading gaps).\n\n    workers: int or None\n        Number of parallel workers, max(1, multiprocessing.cpu_count() - 1) if None.\n\n    "
    if (output_file is None):
        outfile = sys.stdout
    else:
        outfile = smart_open(output_file, 'wb')
    try:
        article_stream = segment_all_articles(file_path, min_article_character, workers=workers)
        for (idx, (article_title, article_sections)) in enumerate(article_stream):
            output_data = {
                'title': article_title,
                'section_titles': [],
                'section_texts': [],
            }
            for (section_heading, section_content) in article_sections:
                output_data['section_titles'].append(section_heading)
                output_data['section_texts'].append(section_content)
            if (((idx + 1) % 100000) == 0):
                logger.info('processed #%d articles (at %r now)', (idx + 1), article_title)
            outfile.write((json.dumps(output_data) + '\n'))
    finally:
        outfile.close()