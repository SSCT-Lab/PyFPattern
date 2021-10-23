def generate_changelog(changes, plugins, fragments):
    'Generate the changelog.\n    :type changes: ChangesMetadata\n    :type plugins: list[PluginDescription]\n    :type fragments: list[ChangelogFragment]\n    '
    config = ChangelogConfig(CONFIG_PATH)
    changes.prune_plugins(plugins)
    changes.prune_fragments(fragments)
    changes.save()
    major_minor_version = '.'.join(changes.latest_version.split('.')[:2])
    changelog_path = os.path.join(CHANGELOG_DIR, ('CHANGELOG-v%s.rst' % major_minor_version))
    generator = ChangelogGenerator(config, changes, plugins, fragments)
    rst = generator.generate()
    with open(changelog_path, 'wb') as changelog_fd:
        changelog_fd.write(to_bytes(rst))