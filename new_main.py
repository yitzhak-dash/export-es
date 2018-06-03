import os
import csv
from elasticsearch import Elasticsearch

import settings

es = Elasticsearch([settings.ES_HOST], port=9200, timeout=300)

file_path = settings.OUTPUT

body = settings.ES_QUERY


def write_data_to_csv(data):
    with open(file_path, 'a', newline='') as newFile:
        newFileWriter = csv.writer(newFile)
        for row in data:
            item_row = row
            newFileWriter.writerow([
                item_row['_source']['networkName'],
                item_row['_source']['sourceTcrId'],
                item_row['_source']['timestamp'],
                item_row['fields']['upload1'],
                item_row['fields']['upload2'],
                item_row['fields']['download1'],
                item_row['fields']['download2']
            ])


def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError:
        pass


def write_header_to_csv(filename, header):
    with open(filename, 'a', newline='') as newFile:
        newFileWriter = csv.writer(newFile)
        newFileWriter.writerow(header)


def read_and_save(size):
    page = es.search(
        index=settings.ES_INDEX,
        scroll='2m',
        size=size,
        body=body, request_timeout=30)
    sid = page['_scroll_id']
    scroll_size = page['hits']['total']
    silent_remove(file_path)
    write_header_to_csv(file_path,
                        ['networkName',
                         'sourceTcrId',
                         'timestamp',
                         'upload1',
                         'upload2',
                         'download1',
                         'download2'
                         ])

    # Start scrolling
    while (scroll_size > 0):
        print("Scrolling...")
        page = es.scroll(scroll_id=sid, scroll='2m')
        # Update the scroll ID
        sid = page['_scroll_id']
        # Get the number of results that we returned in the last scroll
        scroll_size = len(page['hits']['hits'])
        print("scroll size: " + str(scroll_size))
        # Do something with the obtained page
        write_data_to_csv(page['hits']['hits'])

    print("************** completed **************")


read_and_save(10000)
