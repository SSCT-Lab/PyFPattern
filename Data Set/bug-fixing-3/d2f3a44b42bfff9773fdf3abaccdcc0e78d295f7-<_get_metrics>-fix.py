def _get_metrics(component):
    if (component == 'parser'):
        return ('las', 'uas', 'token_acc', 'sent_f')
    elif (component == 'tagger'):
        return ('tags_acc',)
    elif (component == 'ner'):
        return ('ents_f', 'ents_p', 'ents_r')
    elif (component == 'sentrec'):
        return ('sent_f', 'sent_p', 'sent_r')
    return ('token_acc',)