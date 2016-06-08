"""
Generates revision scoring requests like ScoredRevisions does.

Usage:
    scored_revisions_demo <mw-host> <ores-host> <context> <model>
                          [--delay=<secs>]

Options:
    <mw-host>       The host of a mediawiki instance to query
    <ores-host>     The host of an ores instance to query
    <context>       The context for scoring (wiki DB name)
    <model>         The model to score with
    --delay=<secs>  The delay between requests [default: 0.5]
"""
import sys
import time

import docopt
import mwapi
import ores.api


def main():
    args = docopt.docopt(__doc__)
    context = args['<context>']
    model = args['<model>']
    delay = float(args['--delay'])

    mw_session = mwapi.Session(
        args['<mw-host>'],
        user_agent="ORES load test <ahalfaker@gmail.com>")

    ores_session = ores.api.Session(
        args['<ores-host>'], batch_size=5,
        user_agent="ORES load test <ahalfaker@gmail.com>")

    while True:
        rc_doc = mw_session.get(
            action="query", list="recentchanges", rclimit=50, rctype=[0, 1])

        rev_ids = (doc['revid'] for doc in rc_doc['query']['recentchanges'])

        for score in ores_session.score(context, model, rev_ids):
            if 'error' in score:
                sys.stderr.write("e")
            else:
                sys.stderr.write(".")
            sys.stderr.flush()

        sys.stderr.write("\n")
        time.sleep(delay)

if __name__ == "__main__":
    main()
