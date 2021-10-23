def _viterbi_decode(self, feats):
    backpointers = []
    vvars = nd.full((1, self.tagset_size), (- 10000.0))
    vvars[(0, self.tag2idx[START_TAG])] = 0
    for feat in feats:
        bptrs_t = []
        viterbivars_t = []
        for next_tag in range(self.tagset_size):
            next_tag_var = (vvars + self.transitions[next_tag])
            best_tag_id = argmax(next_tag_var)
            bptrs_t.append(best_tag_id)
            viterbivars_t.append(next_tag_var[(0, best_tag_id)])
        vvars = (nd.concat(*viterbivars_t, dim=0) + feat).reshape((1, (- 1)))
        backpointers.append(bptrs_t)
    terminal_var = (vvars + self.transitions[self.tag2idx[STOP_TAG]])
    best_tag_id = argmax(terminal_var)
    path_score = terminal_var[(0, best_tag_id)]
    best_path = [best_tag_id]
    for bptrs_t in reversed(backpointers):
        best_tag_id = bptrs_t[best_tag_id]
        best_path.append(best_tag_id)
    start = best_path.pop()
    assert (start == self.tag2idx[START_TAG])
    best_path.reverse()
    return (path_score, best_path)