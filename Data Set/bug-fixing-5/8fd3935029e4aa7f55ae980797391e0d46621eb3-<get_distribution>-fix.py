def get_distribution():
    ' return the distribution name '
    if (platform.system() == 'Linux'):
        try:
            supported_dists = (platform._supported_dists + ('arch', 'alpine'))
            distribution = platform.linux_distribution(supported_dists=supported_dists)[0].capitalize()
            if ((not distribution) and os.path.isfile('/etc/system-release')):
                distribution = platform.linux_distribution(supported_dists=['system'])[0].capitalize()
                if ('Amazon' in distribution):
                    distribution = 'Amazon'
                else:
                    distribution = 'OtherLinux'
        except:
            distribution = platform.dist()[0].capitalize()
    else:
        distribution = None
    return distribution