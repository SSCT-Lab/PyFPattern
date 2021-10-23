def _get_examples_without_label(data, label):
    count = 0
    for ex in data:
        labels = [label.split('-')[1] for label in ex.gold.ner if (label not in ('O', '-'))]
        if (label not in labels):
            count += 1
    return count