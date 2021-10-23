def _get_legend_handles_labels(axs, legend_handler_map=None):
    '\n    Return handles and labels for legend, internal method.\n\n    '
    handles = []
    labels = []

    def _in_handles(h, l):
        for (f_h, f_l) in zip(handles, labels):
            if (f_l != l):
                continue
            if (type(f_h) != type(h)):
                continue
            try:
                if (f_h.get_color() != h.get_color()).any():
                    continue
            except AttributeError:
                pass
            try:
                if (f_h.get_facecolor() != h.get_facecolor()).any():
                    continue
            except AttributeError:
                pass
            try:
                if (f_h.get_edgecolor() != h.get_edgecolor()).any():
                    continue
            except AttributeError:
                pass
            return True
        return False
    for handle in _get_legend_handles(axs, legend_handler_map):
        label = handle.get_label()
        if (label and (not label.startswith('_')) and (not _in_handles(handle, label))):
            handles.append(handle)
            labels.append(label)
    return (handles, labels)