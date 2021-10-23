def _forward_alg(self, feats):
    alphas = [([(- 10000.0)] * self.tagset_size)]
    alphas[0][self.tag2idx[START_TAG]] = 0.0
    alphas = nd.array(alphas)
    for feat in feats:
        alphas_t = []
        for next_tag in range(self.tagset_size):
            emit_score = feat[next_tag].reshape((1, (- 1)))
            trans_score = self.transitions.data()[next_tag].reshape((1, (- 1)))
            next_tag_var = ((alphas + trans_score) + emit_score)
            alphas_t.append(log_sum_exp(next_tag_var))
        alphas = nd.concat(*alphas_t, dim=0).reshape((1, (- 1)))
    terminal_var = (alphas + self.transitions.data()[self.tag2idx[STOP_TAG]])
    alpha = log_sum_exp(terminal_var)
    return alpha