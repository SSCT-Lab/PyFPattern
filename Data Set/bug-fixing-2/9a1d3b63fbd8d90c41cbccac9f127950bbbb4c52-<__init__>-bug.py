

def __init__(self, nlp, label='GPE'):
    'Initialise the pipeline component. The shared nlp instance is used\n        to initialise the matcher with the shared vocab, get the label ID and\n        generate Doc objects as phrase match patterns.\n        '
    r = requests.get('https://restcountries.eu/rest/v2/all')
    r.raise_for_status()
    countries = r.json()
    self.countries = {c['name']: c for c in countries}
    self.label = nlp.vocab.strings[label]
    patterns = [nlp(c) for c in self.countries.keys()]
    self.matcher = PhraseMatcher(nlp.vocab)
    self.matcher.add('COUNTRIES', None, *patterns)
    Token.set_extension('is_country', default=False)
    Token.set_extension('country_capital')
    Token.set_extension('country_latlng')
    Token.set_extension('country_flag')
    Doc.set_extension('has_country', getter=self.has_country)
    Span.set_extension('has_country', getter=self.has_country)
