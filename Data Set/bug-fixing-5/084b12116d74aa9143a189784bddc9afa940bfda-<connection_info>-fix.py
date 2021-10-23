def connection_info():
    '\n    Return a string showing the figure and connection status for the backend.\n\n    This is intended as a diagnostic tool, and not for general use.\n    '
    result = ['{fig} - {socket}'.format(fig=(manager.canvas.figure.get_label() or 'Figure {}'.format(manager.num)), socket=manager.web_sockets) for manager in Gcf.get_all_fig_managers()]
    if (not is_interactive()):
        result.append('Figures pending show: {}'.format(len(Gcf._activeQue)))
    return '\n'.join(result)