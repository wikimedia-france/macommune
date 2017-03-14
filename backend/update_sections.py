#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from macommune import *
import argparse
import re

if __name__ == "__main__":
    conn = db_connect()
    cur = conn.cursor()

    parser = argparse.ArgumentParser(
        description='Update the articles evaluation from Wikipedia.')
    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")

    parser.add_argument("--missing", help="only include communes \
                         not in the sections table",
                        action="store_true")
    parser.add_argument(
        "--insee", help="If included, only communes with insee number \
         starting with the value will be updated")

    parser.add_argument("--limit",
                        help="number of entries to update",
                        type=int,
                        choices=range(1, 36000))
    args = parser.parse_args()

    if args.verbose:
        VERBOSE = 1

    if args.limit:
        limit = args.limit
    else:
        limit = 0

    if args.missing:
        missing = True
    else:
        missing = False

    if args.insee:
        # Check if the value is a valid Insee code
        # (or at last the first two characters)
        regex = re.compile("^(2[AB]|[0-9]{2})[0-9]{0,3}$")

        if regex.search(args.insee) is not None:
            communes = get_communes(conn,
                                    args.insee,
                                    limit=limit,
                                    missing=missing)
        else:
            communes = get_communes(conn,
                                    limit=limit,
                                    missing=missing)
    else:
        communes = get_communes(conn,
                                limit=limit,
                                missing=missing)

    for c in communes:
        commune = Article(c)
        commune.getWikidataContent()
        commune.getWikipediaSections()

        commune.updateDB(conn)

    print('Errors:')
    print(errors)

    conn.close()