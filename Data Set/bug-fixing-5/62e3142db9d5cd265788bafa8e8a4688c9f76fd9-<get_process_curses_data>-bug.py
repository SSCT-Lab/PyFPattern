def get_process_curses_data(self, p, first, args):
    'Get curses data to display for a process.'
    ret = [self.curse_new_line()]
    if (('cpu_percent' in p) and (p['cpu_percent'] is not None) and (p['cpu_percent'] != '')):
        if (args.disable_irix and (self.nb_log_core != 0)):
            msg = '{0:>6.1f}'.format((p['cpu_percent'] / float(self.nb_log_core)))
        else:
            msg = '{0:>6.1f}'.format(p['cpu_percent'])
        ret.append(self.curse_add_line(msg, self.get_alert(p['cpu_percent'], header='cpu')))
    else:
        msg = '{0:>6}'.format('?')
        ret.append(self.curse_add_line(msg))
    if (('memory_percent' in p) and (p['memory_percent'] is not None) and (p['memory_percent'] != '')):
        msg = '{0:>6.1f}'.format(p['memory_percent'])
        ret.append(self.curse_add_line(msg, self.get_alert(p['memory_percent'], header='mem')))
    else:
        msg = '{0:>6}'.format('?')
        ret.append(self.curse_add_line(msg))
    if (('memory_info' in p) and (p['memory_info'] is not None) and (p['memory_info'] != '')):
        msg = '{0:>6}'.format(self.auto_unit(p['memory_info'][1], low_precision=False))
        ret.append(self.curse_add_line(msg, optional=True))
        msg = '{0:>6}'.format(self.auto_unit(p['memory_info'][0], low_precision=False))
        ret.append(self.curse_add_line(msg, optional=True))
    else:
        msg = '{0:>6}'.format('?')
        ret.append(self.curse_add_line(msg))
        ret.append(self.curse_add_line(msg))
    msg = '{0:>6}'.format(p['pid'])
    ret.append(self.curse_add_line(msg))
    if ('username' in p):
        msg = ' {0:9}'.format(str(p['username'])[:9])
        ret.append(self.curse_add_line(msg))
    else:
        msg = ' {0:9}'.format('?')
        ret.append(self.curse_add_line(msg))
    if ('nice' in p):
        nice = p['nice']
        if (nice is None):
            nice = '?'
        msg = '{0:>5}'.format(nice)
        if (isinstance(nice, int) and ((WINDOWS and (nice != 32)) or ((not WINDOWS) and (nice != 0)))):
            ret.append(self.curse_add_line(msg, decoration='NICE'))
        else:
            ret.append(self.curse_add_line(msg))
    else:
        msg = '{0:>5}'.format('?')
        ret.append(self.curse_add_line(msg))
    if ('status' in p):
        status = p['status']
        msg = '{0:>2}'.format(status)
        if (status == 'R'):
            ret.append(self.curse_add_line(msg, decoration='STATUS'))
        else:
            ret.append(self.curse_add_line(msg))
    else:
        msg = '{0:>2}'.format('?')
        ret.append(self.curse_add_line(msg))
    if self.tag_proc_time:
        try:
            delta = timedelta(seconds=sum(p['cpu_times']))
        except (OverflowError, TypeError) as e:
            logger.debug('Cannot get TIME+ ({0})'.format(e))
            self.tag_proc_time = False
        else:
            (hours, minutes, seconds, microseconds) = convert_timedelta(delta)
            if hours:
                msg = '{0:>4}h'.format(hours)
                ret.append(self.curse_add_line(msg, decoration='CPU_TIME', optional=True))
                msg = '{0}:{1}'.format(str(minutes).zfill(2), seconds)
            else:
                msg = '{0:>4}:{1}.{2}'.format(minutes, seconds, microseconds)
    else:
        msg = '{0:>10}'.format('?')
    ret.append(self.curse_add_line(msg, optional=True))
    if ('io_counters' in p):
        io_rs = int(((p['io_counters'][0] - p['io_counters'][2]) / p['time_since_update']))
        if (io_rs == 0):
            msg = '{0:>6}'.format('0')
        else:
            msg = '{0:>6}'.format(self.auto_unit(io_rs, low_precision=True))
        ret.append(self.curse_add_line(msg, optional=True, additional=True))
        io_ws = int(((p['io_counters'][1] - p['io_counters'][3]) / p['time_since_update']))
        if (io_ws == 0):
            msg = '{0:>6}'.format('0')
        else:
            msg = '{0:>6}'.format(self.auto_unit(io_ws, low_precision=True))
        ret.append(self.curse_add_line(msg, optional=True, additional=True))
    else:
        msg = '{0:>6}'.format('?')
        ret.append(self.curse_add_line(msg, optional=True, additional=True))
        ret.append(self.curse_add_line(msg, optional=True, additional=True))
    cmdline = p['cmdline']
    try:
        if (cmdline and (cmdline != [''])):
            (path, cmd, arguments) = split_cmdline(cmdline)
            if (os.path.isdir(path) and (not args.process_short_name)):
                msg = (' {0}'.format(path) + os.sep)
                ret.append(self.curse_add_line(msg, splittable=True))
                ret.append(self.curse_add_line(cmd, decoration='PROCESS', splittable=True))
            else:
                msg = ' {0}'.format(cmd)
                ret.append(self.curse_add_line(msg, decoration='PROCESS', splittable=True))
            if arguments:
                msg = ' {0}'.format(arguments)
                ret.append(self.curse_add_line(msg, splittable=True))
        else:
            msg = ' {0}'.format(p['name'])
            ret.append(self.curse_add_line(msg, splittable=True))
    except UnicodeEncodeError:
        ret.append(self.curse_add_line('', splittable=True))
    if (first and ('extended_stats' in p)):
        xpad = (' ' * 13)
        if (('cpu_affinity' in p) and (p['cpu_affinity'] is not None)):
            ret.append(self.curse_new_line())
            msg = (((xpad + 'CPU affinity: ') + str(len(p['cpu_affinity']))) + ' cores')
            ret.append(self.curse_add_line(msg, splittable=True))
        if (('memory_info' in p) and (p['memory_info'] is not None)):
            ret.append(self.curse_new_line())
            msg = (xpad + 'Memory info: ')
            for (k, v) in iteritems(p['memory_info']._asdict()):
                if ((k not in ['rss', 'vms']) and (v is not None)):
                    msg += (((k + ' ') + self.auto_unit(v, low_precision=False)) + ' ')
            if (('memory_swap' in p) and (p['memory_swap'] is not None)):
                msg += ('swap ' + self.auto_unit(p['memory_swap'], low_precision=False))
            ret.append(self.curse_add_line(msg, splittable=True))
        msg = ''
        if (('num_threads' in p) and (p['num_threads'] is not None)):
            msg += (('threads ' + str(p['num_threads'])) + ' ')
        if (('num_fds' in p) and (p['num_fds'] is not None)):
            msg += (('files ' + str(p['num_fds'])) + ' ')
        if (('num_handles' in p) and (p['num_handles'] is not None)):
            msg += (('handles ' + str(p['num_handles'])) + ' ')
        if (('tcp' in p) and (p['tcp'] is not None)):
            msg += (('TCP ' + str(p['tcp'])) + ' ')
        if (('udp' in p) and (p['udp'] is not None)):
            msg += (('UDP ' + str(p['udp'])) + ' ')
        if (msg != ''):
            ret.append(self.curse_new_line())
            msg = ((xpad + 'Open: ') + msg)
            ret.append(self.curse_add_line(msg, splittable=True))
        if (('ionice' in p) and (p['ionice'] is not None)):
            ret.append(self.curse_new_line())
            msg = (xpad + 'IO nice: ')
            k = 'Class is '
            v = p['ionice'].ioclass
            if WINDOWS:
                if (v == 0):
                    msg += (k + 'Very Low')
                elif (v == 1):
                    msg += (k + 'Low')
                elif (v == 2):
                    msg += 'No specific I/O priority'
                else:
                    msg += (k + str(v))
            elif (v == 0):
                msg += 'No specific I/O priority'
            elif (v == 1):
                msg += (k + 'Real Time')
            elif (v == 2):
                msg += (k + 'Best Effort')
            elif (v == 3):
                msg += (k + 'IDLE')
            else:
                msg += (k + str(v))
            if (hasattr(p['ionice'], 'value') and (p['ionice'].value != 0)):
                msg += (' (value %s/7)' % str(p['ionice'].value))
            ret.append(self.curse_add_line(msg, splittable=True))
    return ret