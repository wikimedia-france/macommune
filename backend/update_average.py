#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from macommune import *
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Update the averages sizes of sections.')

    fields = ['title',
              'importance',
              'number',
              'mean_size']
    query = "select s.title as title, c.importance as importance, \
              COUNT(s.qid) AS number, \
              ROUND(AVG(s.size)) AS mean_size FROM sections s, \
              communes c WHERE c.qid=s.qid  GROUP BY title, \
              importance ORDER BY number DESC;"

    cnx = db_connect()
    cursor = cnx.cursor()
    cnx.autocommit(False)

    try:
        cursor.execute(query)
        results = [dict(zip(fields, c)) for c in cursor]

        # delete previous results
        query = "DELETE FROM section_stats;"
        cursor.execute(query)

        for r in results:
            cursor.execute("INSERT INTO section_stats \
                            (section_title, number, mean_size, importance) \
                            VALUES(%(section_title)s, %(number)s, \
                            %(mean_size)s, %(importance)s);",
                           {'section_title': r['title'],
                            'number': r['number'],
                            'mean_size': r['mean_size'],
                            'importance': r['importance']})

        cnx.commit()
    except Exception as e:
        print('Error:', e)
        cnx.rollback()
