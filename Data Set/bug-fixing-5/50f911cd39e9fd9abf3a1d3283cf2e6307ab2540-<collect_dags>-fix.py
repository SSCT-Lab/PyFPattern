def collect_dags(self, dag_folder=None, only_if_updated=True):
    '\n        Given a file path or a folder, this method looks for python modules,\n        imports them and adds them to the dagbag collection.\n\n        Note that if a .airflowignore file is found while processing,\n        the directory, it will behaves much like a .gitignore does,\n        ignoring files that match any of the regex patterns specified\n        in the file.\n        '
    start_dttm = datetime.now()
    dag_folder = (dag_folder or self.dag_folder)
    stats = []
    FileLoadStat = namedtuple('FileLoadStat', 'file duration dag_num task_num dags')
    if os.path.isfile(dag_folder):
        self.process_file(dag_folder, only_if_updated=only_if_updated)
    elif os.path.isdir(dag_folder):
        patterns = []
        for (root, dirs, files) in os.walk(dag_folder, followlinks=True):
            ignore_file = [f for f in files if (f == '.airflowignore')]
            if ignore_file:
                f = open(os.path.join(root, ignore_file[0]), 'r')
                patterns += [p for p in f.read().split('\n') if p]
                f.close()
            for f in files:
                try:
                    filepath = os.path.join(root, f)
                    if (not os.path.isfile(filepath)):
                        continue
                    (mod_name, file_ext) = os.path.splitext(os.path.split(filepath)[(- 1)])
                    if ((file_ext != '.py') and (not zipfile.is_zipfile(filepath))):
                        continue
                    if (not any([re.findall(p, filepath) for p in patterns])):
                        ts = datetime.now()
                        found_dags = self.process_file(filepath, only_if_updated=only_if_updated)
                        td = (datetime.now() - ts)
                        td = (td.total_seconds() + (float(td.microseconds) / 1000000))
                        stats.append(FileLoadStat(filepath.replace(dag_folder, ''), td, len(found_dags), sum([len(dag.tasks) for dag in found_dags]), str([dag.dag_id for dag in found_dags])))
                except Exception as e:
                    logging.warning(e)
    Stats.gauge('collect_dags', (datetime.now() - start_dttm).total_seconds(), 1)
    Stats.gauge('dagbag_size', len(self.dags), 1)
    Stats.gauge('dagbag_import_errors', len(self.import_errors), 1)
    self.dagbag_stats = sorted(stats, key=(lambda x: x.duration), reverse=True)