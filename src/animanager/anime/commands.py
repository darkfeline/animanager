from .bump import main as bump

def add(args):
    from animanager.anime import add
    add.main(args.config, args.name)

    
def update(args):
    from animanager.anime import update
    update.main(args.config)


def stats(args):
    from animanager.anime import stats
    stats.main(args.config)
