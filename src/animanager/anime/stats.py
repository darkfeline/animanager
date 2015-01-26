import logging

from animanager import mysqllib

logger = logging.getLogger(__name__)

statuses = ['plan to watch', 'watching', 'complete', 'dropped', 'on hold']
output_template = """Watching: {watching}
Complete: {complete}
On Hold: {on hold}
Dropped: {dropped}
Plan to Watch: {plan to watch}
Total: {total}"""


def main(args):
    config = args.config
    counts = {}
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute('SELECT count(*) FROM anime')
        counts['total'] = cur.fetchone()[0]
        query = 'SELECT count(*) FROM anime WHERE status=%s'
        for x in statuses:
            cur.execute(query, (x,))
            counts[x] = cur.fetchone()[0]
        print(output_template.format(**counts))
