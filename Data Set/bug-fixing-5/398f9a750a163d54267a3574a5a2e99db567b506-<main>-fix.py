def main():
    p = argparse.ArgumentParser(usage=__doc__.lstrip())
    p.add_argument('--project', default='scipy/scipy')
    p.add_argument('milestone')
    args = p.parse_args()
    getter = CachedGet('gh_cache.json', GithubGet())
    try:
        milestones = get_milestones(getter, args.project)
        if (args.milestone not in milestones):
            msg = 'Milestone {0} not available. Available milestones: {1}'
            msg = msg.format(args.milestone, ', '.join(sorted(milestones)))
            p.error(msg)
        issues = get_issues(getter, args.project, args.milestone)
        issues.sort()
    finally:
        getter.save()
    prs = [x for x in issues if ('/pull/' in x.url)]
    issues = [x for x in issues if (x not in prs)]

    def print_list(title, items):
        print()
        print(title)
        print(('-' * len(title)))
        print()
        for issue in items:
            msg = '* `#{0} <{1}>`__: {2}'
            title = re.sub('\\s+', ' ', issue.title.strip())
            if (len(title) > 60):
                remainder = re.sub('\\s.*$', '...', title[60:])
                if (len(remainder) > 20):
                    remainder = (title[:80] + '...')
                else:
                    title = (title[:60] + remainder)
            msg = msg.format(issue.id, issue.url, title)
            print(msg)
        print()
    msg = 'Issues closed for {0}'.format(args.milestone)
    print_list(msg, issues)
    msg = 'Pull requests for {0}'.format(args.milestone)
    print_list(msg, prs)
    return 0