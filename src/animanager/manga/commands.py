def imp(args):
    from animanager.manga import imp
    imp.main(args.config, args.file)


def bump(args):
    from animanager.manga import bump
    bump.main(args.config, args.name)


def add(args):
    from animanager.manga import add
    add.main(args.config, args.name)


def hold(args):
    from animanager.manga import hold
    hold.main(args.config, args.name)


def drop(args):
    from animanager.manga import drop
    drop.main(args.config, args.name)


def update(args):
    from animanager.manga import update
    update.main(args.config)


def stats(args):
    from animanager.manga import stats
    stats.main(args.config)
