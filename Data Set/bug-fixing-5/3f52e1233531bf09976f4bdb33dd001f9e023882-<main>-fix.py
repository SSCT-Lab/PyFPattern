@plac.annotations(lang='ISO language code', in_dir='Location of input directory', out_loc='Location of output file', n_workers=('Number of workers', 'option', 'n', int), size=('Dimension of the word vectors', 'option', 'd', int), window=('Context window size', 'option', 'w', int), min_count=('Min count', 'option', 'm', int), negative=('Number of negative samples', 'option', 'g', int), nr_iter=('Number of iterations', 'option', 'i', int))
def main(lang, in_dir, out_loc, negative=5, n_workers=4, window=5, size=128, min_count=10, nr_iter=5):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    nlp = spacy.blank(lang)
    corpus = Corpus(in_dir, nlp)
    model = Word2Vec(sentences=corpus, size=size, window=window, min_count=min_count, workers=n_workers, sample=1e-05, negative=negative)
    model.save(out_loc)