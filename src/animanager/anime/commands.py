def imp(args):
    """import"""
    from animanager.anime import imp
    imp.main(args.config, args.file)


def bump(args):
    from animanager.anime import bump
    bump.main(args.config, args.name)


def add(args):
    from animanager.anime import add
    add.main(args.config, args.name)


def hold(args):
    from animanager.anime import hold
    hold.main(args.config, args.name)


def drop(args):
    from animanager.anime import drop
    drop.main(args.config, args.name)


def update(args):
    from animanager.anime import update
    update.main(args.config)


def stats(args):
    from animanager.anime import stats
    stats.main(args.config)
