def segment_all_articles(file_path):
    'Extract article titles and sections from a MediaWiki bz2 database dump.\n\n    Parameters\n    ----------\n    file_path : str\n        Path to MediaWiki dump, typical filename is <LANG>wiki-<YYYYMMDD>-pages-articles.xml.bz2\n        or <LANG>wiki-latest-pages-articles.xml.bz2.\n\n    Yields\n    ------\n    (str, list of (str, str))\n        Structure contains (title, [(section_heading, section_content), ...]).\n\n    '
    with smart_open(file_path, 'rb') as xml_fileobj:
        wiki_sections_corpus = WikiSectionsCorpus(xml_fileobj)
        wiki_sections_corpus.metadata = True
        wiki_sections_text = wiki_sections_corpus.get_texts_with_sections()
        for (article_title, article_sections) in wiki_sections_text:
            (yield (article_title, article_sections))