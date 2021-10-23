def run(self, terms, variables=None, **kwargs):
    ret = []
    for term in terms:
        term_file = os.path.basename(term)
        dwimmed_path = self.find_file_in_search_path(variables, 'files', os.path.dirname(term))
        globbed = glob.glob(os.path.join(dwimmed_path, term_file))
        ret.extend((g for g in globbed if os.path.isfile(g)))
    return ret