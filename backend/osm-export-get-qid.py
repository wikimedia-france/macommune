#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import csv              # CSV file manipulations


def api_call(titles):
    titles_list = ('|').join(titles)
    print(titles_list)

    api_base = "https://wikidata.org/w/api.php"

    params = [('format', 'json'),
              ('action', 'wbgetentities'),
              ('props', 'info|claims|sitelinks|labels'),
              ('sites', 'frwiki'),
              ('sitefilter', 'frwiki'),
              ('languages', 'fr'),
              ('titles', titles_list)]

    try:
        response = requests.get(api_base, params=params)
        results = json.loads(response.text)
        return results

    except 'ConnectionError':
        print('Server unreachable')

communes = []
with open('resources/extract-osm-fixed.csv', 'r') as csv_osm_extract:
    reader = csv.DictReader(csv_osm_extract)
    for row in reader:
        communes.append((row['lien-wikipedia'].strip(), {
            'insee': row['insee'].strip(),
            'titre': row['titre'].strip(),
            'qid': ''
            }))
csv_osm_extract.closed

communes_dict = dict(communes)

# print(communes)

num_communes = len(communes)
chunk_size = 50
# num_chunks = math.ceil(num_communes/chunk_size)

last = 0
missing_insee = []
mismatched_insee = []
missing_labels = []
mismatched_labels = []
wrong_titles = []

while last < num_communes:
    chunk = communes[last:last + chunk_size]

    titles = []
    for commune in chunk:
        title = commune[0].split(':')[1]
        titles.append(title)

    api_results = api_call(titles)

    entities = api_results['entities']
    for qid, data in entities.items():
        print('Fetching data for item {}'.format(qid))
        if qid[0] != 'Q':
            wrong_titles.append(data['title'])
            print('Wrong title: {}'.format(data['title']))
        else:
            wp_title = 'fr:' + data['sitelinks']['frwiki']['title']
            wd_label = data['labels']['fr']['value']
            claims = data['claims']
            try:
                wd_insee = claims['P374'][0]['mainsnak']['datavalue']['value']
            except:
                wd_insee = ''
                print('No insee claim for item {}'.format(qid))

            if wd_insee:
                dict_insee = communes_dict[wp_title]['insee']
                if dict_insee != wd_insee:
                    mismatched_insee.append((qid,
                                             wp_title,
                                             dict_insee,
                                             wd_insee))
            else:
                missing_insee.append((qid, wp_title))

            if wd_label:
                titre = communes_dict[wp_title]['titre']
                if titre != wd_label:
                    mismatched_labels.append((qid,
                                              wp_title,
                                              titre,
                                              wd_label))
            else:
                missing_labels.append((qid, wp_title))

            communes_dict[wp_title]['qid'] = qid
            print(wp_title, communes_dict[wp_title])

    # print(api_results)
    last += chunk_size

print('missing_labels: {}'.format(len(missing_labels)))
print(missing_labels)

print('===============')
print('mismatched_labels: {}'.format(len(mismatched_labels)))
print(mismatched_labels)

print('===============')
print('missing_insee: {}'.format(len(missing_insee)))
print(missing_insee)

print('===============')
print('mismatched_insee: {}'.format(len(mismatched_insee)))
print(mismatched_insee)

print('===============')
print('wrong titles: {}'.format(len(wrong_titles)))
print(wrong_titles)
