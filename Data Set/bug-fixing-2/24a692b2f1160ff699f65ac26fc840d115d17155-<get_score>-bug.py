

def get_score(self, document, index, average_idf):
    score = 0
    for word in document:
        if (word not in self.f[index]):
            continue
        idf = (self.idf[word] if (self.idf[word] >= 0) else (EPSILON * average_idf))
        score += (((idf * self.f[index][word]) * (PARAM_K1 + 1)) / (self.f[index][word] + (PARAM_K1 * ((1 - PARAM_B) + ((PARAM_B * self.corpus_size) / self.avgdl)))))
    return score
