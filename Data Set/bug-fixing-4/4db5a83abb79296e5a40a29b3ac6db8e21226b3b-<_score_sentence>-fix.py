def _score_sentence(self, feats, tags):
    score = nd.array([0])
    tags = nd.concat(nd.array([self.tag2idx[START_TAG]]), *tags, dim=0)
    for (i, feat) in enumerate(feats):
        score = ((score + self.transitions.data()[(to_scalar(tags[(i + 1)]), to_scalar(tags[i]))]) + feat[to_scalar(tags[(i + 1)])])
    score = (score + self.transitions.data()[(self.tag2idx[STOP_TAG], to_scalar(tags[int((tags.shape[0] - 1))]))])
    return score