import logging

from animanager import mysqllib

logger = logging.getLogger(__name__)

statuses = ['plan to read', 'reading', 'complete', 'dropped', 'on hold']
output_template = """Reading: {reading}
Complete: {complete}
On Hold: {on hold}
Dropped: {dropped}
Plan to Read: {plan to read}
Total: {total}"""


def main(config):
    counts = {}
    with mysqllib.connect(**config["db_args"]) as cur:
        cur.execute('SELECT count(*) FROM manga')
        counts['total'] = cur.fetchone()[0]
        query = 'SELECT count(*) FROM manga WHERE status=%s'
        for x in statuses:
            cur.execute(query, (x,))
            counts[x] = cur.fetchone()[0]
        print(output_template.format(**counts))
