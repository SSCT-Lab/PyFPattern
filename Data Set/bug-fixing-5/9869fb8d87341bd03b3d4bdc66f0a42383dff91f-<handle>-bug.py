def handle(self, **options):
    if ((options['percent_huddles'] + options['percent_personals']) > 100):
        self.stderr.write('Error!  More than 100% of messages allocated.\n')
        return
    if options['delete']:
        clear_database()
        zulip_realm = Realm.objects.create(string_id='zulip', name='Zulip Dev', restricted_to_domain=True, invite_required=False, org_type=Realm.CORPORATE, domain='zulip.com')
        RealmAlias.objects.create(realm=zulip_realm, domain='zulip.com')
        if options['test_suite']:
            mit_realm = Realm.objects.create(string_id='mit', name='MIT', restricted_to_domain=True, invite_required=False, org_type=Realm.CORPORATE, domain='mit.edu')
            RealmAlias.objects.create(realm=mit_realm, domain='mit.edu')
        realms = {
            
        }
        for realm in Realm.objects.all():
            realms[realm.domain] = realm
        names = [('Zoe', 'ZOE@zulip.com'), ('Othello, the Moor of Venice', 'othello@zulip.com'), ('Iago', 'iago@zulip.com'), ('Prospero from The Tempest', 'prospero@zulip.com'), ('Cordelia Lear', 'cordelia@zulip.com'), ('King Hamlet', 'hamlet@zulip.com'), ('aaron', 'AARON@zulip.com')]
        for i in range(options['extra_users']):
            names.append((('Extra User %d' % (i,)), ('extrauser%d@zulip.com' % (i,))))
        create_users(realms, names)
        iago = UserProfile.objects.get(email='iago@zulip.com')
        do_change_is_admin(iago, True)
        stream_list = ['Verona', 'Denmark', 'Scotland', 'Venice', 'Rome']
        stream_dict = {
            'Verona': {
                'description': 'A city in Italy',
                'invite_only': False,
            },
            'Denmark': {
                'description': 'A Scandinavian country',
                'invite_only': False,
            },
            'Scotland': {
                'description': 'Located in the United Kingdom',
                'invite_only': False,
            },
            'Venice': {
                'description': 'A northeastern Italian city',
                'invite_only': False,
            },
            'Rome': {
                'description': 'Yet another Italian city',
                'invite_only': False,
            },
        }
        create_streams(realms, zulip_realm, stream_dict)
        recipient_streams = [Stream.objects.get(name=name, realm=zulip_realm).id for name in stream_list]
        subscriptions_to_add = []
        profiles = UserProfile.objects.select_related().all().order_by('email')
        for (i, profile) in enumerate(profiles):
            for type_id in recipient_streams[:(int(((len(recipient_streams) * float(i)) / len(profiles))) + 1)]:
                r = Recipient.objects.get(type=Recipient.STREAM, type_id=type_id)
                s = Subscription(recipient=r, user_profile=profile, color=STREAM_ASSIGNMENT_COLORS[(i % len(STREAM_ASSIGNMENT_COLORS))])
                subscriptions_to_add.append(s)
        Subscription.objects.bulk_create(subscriptions_to_add)
    else:
        zulip_realm = get_realm('zulip.com')
        recipient_streams = [klass.type_id for klass in Recipient.objects.filter(type=Recipient.STREAM)]
    user_profiles = [user_profile.id for user_profile in UserProfile.objects.all()]
    for i in range(options['num_huddles']):
        get_huddle(random.sample(user_profiles, random.randint(3, 4)))
    personals_pairs = [random.sample(user_profiles, 2) for i in range(options['num_personals'])]
    threads = options['threads']
    jobs = []
    for i in range(threads):
        count = (options['num_messages'] // threads)
        if (i < (options['num_messages'] % threads)):
            count += 1
        jobs.append((count, personals_pairs, options, self.stdout.write))
    for job in jobs:
        send_messages(job)
    if options['delete']:
        get_client('website')
        get_client('API')
        if options['test_suite']:
            testsuite_mit_users = [('Fred Sipb (MIT)', 'sipbtest@mit.edu'), ('Athena Consulting Exchange User (MIT)', 'starnine@mit.edu'), ('Esp Classroom (MIT)', 'espuser@mit.edu')]
            create_users(realms, testsuite_mit_users)
        all_realm_bots = [(bot['name'], (bot['email_template'] % (settings.INTERNAL_BOT_DOMAIN,))) for bot in settings.INTERNAL_BOTS]
        zulip_realm_bots = [('Zulip New User Bot', 'new-user-bot@zulip.com'), ('Zulip Error Bot', 'error-bot@zulip.com'), ('Zulip Default Bot', 'default-bot@zulip.com')]
        zulip_realm_bots.extend(all_realm_bots)
        create_users(realms, zulip_realm_bots, bot_type=UserProfile.DEFAULT_BOT)
        zulip_webhook_bots = [('Zulip Webhook Bot', 'webhook-bot@zulip.com')]
        create_users(realms, zulip_webhook_bots, bot_type=UserProfile.INCOMING_WEBHOOK_BOT)
        if (not options['test_suite']):
            email_gateway_bot = UserProfile.objects.get(email__iexact=settings.EMAIL_GATEWAY_BOT)
            email_gateway_bot.is_api_super_user = True
            email_gateway_bot.save()
            zulip_stream_dict = {
                'devel': {
                    'description': 'For developing',
                    'invite_only': False,
                },
                'all': {
                    'description': 'For everything',
                    'invite_only': False,
                },
                'announce': {
                    'description': 'For announcements',
                    'invite_only': False,
                },
                'design': {
                    'description': 'For design',
                    'invite_only': False,
                },
                'support': {
                    'description': 'For support',
                    'invite_only': False,
                },
                'social': {
                    'description': 'For socializing',
                    'invite_only': False,
                },
                'test': {
                    'description': 'For testing',
                    'invite_only': False,
                },
                'errors': {
                    'description': 'For errors',
                    'invite_only': False,
                },
                'sales': {
                    'description': 'For sales discussion',
                    'invite_only': False,
                },
            }
            create_streams(realms, zulip_realm, zulip_stream_dict)
            for default_stream_name in ['design', 'devel', 'social', 'support']:
                DefaultStream.objects.create(realm=zulip_realm, stream=get_stream(default_stream_name, zulip_realm))
            subscriptions_to_add = []
            profiles = UserProfile.objects.select_related().filter(realm=zulip_realm)
            for (i, stream_name) in enumerate(zulip_stream_dict):
                stream = Stream.objects.get(name=stream_name, realm=zulip_realm)
                recipient = Recipient.objects.get(type=Recipient.STREAM, type_id=stream.id)
                for profile in profiles:
                    s = Subscription(recipient=recipient, user_profile=profile, color=STREAM_ASSIGNMENT_COLORS[(i % len(STREAM_ASSIGNMENT_COLORS))])
                    subscriptions_to_add.append(s)
            Subscription.objects.bulk_create(subscriptions_to_add)
            internal_zulip_users_nosubs = [('Zulip Commit Bot', 'commit-bot@zulip.com'), ('Zulip Trac Bot', 'trac-bot@zulip.com'), ('Zulip Nagios Bot', 'nagios-bot@zulip.com')]
            create_users(realms, internal_zulip_users_nosubs, bot_type=UserProfile.DEFAULT_BOT)
        zulip_cross_realm_bots = [('Zulip Feedback Bot', 'feedback@zulip.com')]
        create_users(realms, zulip_cross_realm_bots, bot_type=UserProfile.DEFAULT_BOT)
        UserMessage.objects.all().update(flags=UserMessage.flags.read)
        self.stdout.write('Successfully populated test database.\n')