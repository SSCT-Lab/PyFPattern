

def connection_info():
    '\n    Return a string showing the figure and connection status for\n    the backend. This is intended as a diagnostic tool, and not for general\n    use.\n\n    '
    result = []
    for manager in Gcf.get_all_fig_managers():
        fig = manager.canvas.figure
        result.append('{0} - {0}'.format((fig.get_label() or 'Figure {0}'.format(manager.num)), manager.web_sockets))
    if (not is_interactive()):
        result.append('Figures pending show: {0}'.format(len(Gcf._activeQue)))
    return '\n'.join(result)
