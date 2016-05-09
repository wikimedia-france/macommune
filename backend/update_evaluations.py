#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from macommune import *
import argparse


def query_category(category, cmcontinue='', retries=0):
    params = [('format', 'json'),
              ('action', 'query'),
              ('list', 'categorymembers'),
              ('cmlimit', 500),
              ('cmnamespace', 1),
              ('cmtitle', category)]

    if cmcontinue:
        params.append(('cmcontinue', cmcontinue))

    try:
        response = requests.get(WP_API_BASE, params=params, timeout=1)
        return json.loads(response.text)
    except requests.exceptions.RequestException as e:
        print('Server unreachable - {}'.format(e))
        if retries < 5:
            retries += 1
            return query_category(category, cmcontinue)


def getEvaluations(basename, cats):
    """Gets the evaluation in all the categories named <basename> <cat>"""

    communes_eval = []
    for c in cats:
        communes_data = query_category(basename + c)
        if 'query' in communes_data:
            if 'categorymembers' in communes_data['query']:
                new_communes = extract_communes_data(
                    communes_data['query']['categorymembers'],
                    c)
                communes_eval += new_communes

        while 'continue' in communes_data:
            cmcontinue = communes_data['continue']['cmcontinue']
            communes_data = query_category(basename + c, cmcontinue)
            if type(communes_data == 'dict') and 'query' in communes_data:
                if 'categorymembers' in communes_data['query']:
                    new_communes = extract_communes_data(
                        communes_data['query']['categorymembers'],
                        c)
                    communes_eval += new_communes
            if VERBOSE:
                print('continue for {}'.format(c))
        else:
            if VERBOSE:
                print('OK for {}'.format(c))

    return communes_eval

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Update the articles evaluation from Wikipedia.')
    parser.add_argument("--verbose", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    if args.verbose:
        VERBOSE = 1

    conn = db_connect()

    cur = conn.cursor()

    # Importance
    imp_base = "Category:Article sur les communes de France d'importance "
    imp_cats = ["maximum",
                "élevée",
                "moyenne",
                "faible",
                "inconnue"]
    communes_importance = dict(getEvaluations(imp_base, imp_cats))

    # if VERBOSE:
    #   print(communes_importance)

    # Progress
    prog_base = "Category:Article sur les communes de France d'avancement "
    prog_cats = ["A",
                 "AdQ",
                 "B",
                 "BA",
                 "BD",
                 "ébauche",
                 "homonymie",
                 "inconnu"]
    communes_progress = dict(getEvaluations(prog_base, prog_cats))

    # if VERBOSE:
    #    print(communes_progress)

    communes = get_communes(conn)

    for c in communes:
        commune = Article(c)

        evaluation = {}
        if commune.wp_title_no_prefix in communes_importance:
            importance = communes_importance[commune.wp_title_no_prefix]
            if importance != commune.importance:
                evaluation['importance'] = importance
        else:
            errors.append("Missing importance for {}".format(commune.wp_title))

        if commune.wp_title_no_prefix in communes_progress:
            progress = communes_progress[commune.wp_title_no_prefix]
            if progress != commune.progress:
                evaluation['progress'] = progress
        else:
            errors.append("Missing progress for {}".format(commune.wp_title))

        commune.updateEval(conn, evaluation)

    conn.close()

    if VERBOSE:
        print('Errors:')
        print(errors)
