import sys, os, time, csv, math, subprocess
from config import CHROME_PATH, URL
field = {'index': 'index', 'title': 'title', 'description': 'descrizione', 'topic': 'topic'}
global TOT_LINES
TOT_LINES = 0

def readCsv(name):
    global TOT_LINES
    with open(name, mode='r') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        rows = []
        for row in csv_reader:
            if line_count == 0:
                print('\n')
                line_count += 1
            else:
                rows.append({field['index']: line_count, field['title']: row[5], field['description']: row[6], field['topic']: row[2]})
                line_count += 1
        print('Processed '+str(line_count)+' lines.')
        TOT_LINES = line_count
        return rows

def progress(count, total, last):
    percent = (count*100)/total
    if (percent%10)==0:
        if math.ceil(percent) == last:
            pass
        else:
            print(str(percent))
            last = percent
    else:
        pass
    return last


def searchCsv(relases, text):
    perc = 0
    found = []
    last = 0
    text = text.lower()
    for relase in relases:
        if text in relase[field['title']].lower():
            found.append(relase)
        perc+=1
        last = progress(perc, TOT_LINES, last)
    return found


if __name__ == '__main__':
    # MAIN LOOP
    # 2. Ogni entry e' un oggetto
    # 3. Risultato ricerca
    # 4. Apertura chrome alla pagina del topic con WaybackMachine di InternetArchive

    # SCELTA UTENTE - 1. Search for category 2. Search for title
    print('=====================')
    print('=====TNT VILLAGE=====')
    print('=====================')
    print('\nCerca il titolo:')
    text = raw_input()

    # 1. Lettura file csv
    found = searchCsv(readCsv('dump.csv'), str(text))

    print('Found %i entries:' % len(found))
    for i in range(len(found)):
        print('%i) %s - %s (%s)' % (i, found[i][field['title']], found[i][field['description']], found[i][field['topic']]))
    c = input('>')
    url = URL+str(found[c][field['topic']])
    subprocess.call([CHROME_PATH, url])