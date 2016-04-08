import csv

longest_name = ''
longest_wp_title = ''

with open('resources/france-communes-data.csv', 'r') as csvfile:
    content = csv.DictReader(csvfile, delimiter=',', quotechar='"')

    for row in content:
        if len(row['wp_title']) > len(longest_wp_title):
            longest_wp_title = row['wp_title']

        if len(row['title']) > len(longest_name):
            longest_name = row['title']

print(longest_name, len(longest_name))
print(longest_wp_title, len(longest_wp_title))
