"""
Requests scores for a batch of rev_ids.  Reads rev_ids from stdin.

Usage:
    request_score_batch <host> <context> <model>

Options:
    <host>     The hostname of the ORES instance to request from
    <context>  The context (wiki DB name)
    <model>    The name of the model to apply
"""
import sys

import docopt
from ores import api


def main():
    args = docopt.docopt(__doc__)
    rev_ids = (int(line) for line in sys.stdin)

    session = api.Session(
        args['<host>'], user_agent="Load testing <ahalfaker@wikimedia.org>")

    for score in session.score(args['<context>'], args['<model>'], rev_ids):
        print(score, flush=True)


if __name__ == "__main__":
    main()
