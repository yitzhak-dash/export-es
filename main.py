import os
import csv
from elasticsearch import Elasticsearch

es = Elasticsearch(['10.241.0.60'], port=9200)

file_path = 'output/data.csv'

body = {
    "query": {
        "bool": {
            "filter": [
                {
                    "bool": {
                        "must": [
                            {
                                "bool": {
                                    "must": [
                                        {
                                            "range": {
                                                "timestamp": {
                                                    "from": "2018-01-26T01:00:00.000Z",
                                                    "to": None,
                                                    "include_lower": False,
                                                    "include_upper": True,
                                                    "boost": 1
                                                }
                                            }
                                        },
                                        {
                                            "range": {
                                                "timestamp": {
                                                    "from": None,
                                                    "to": "2018-01-29T02:00:00.000Z",
                                                    "include_lower": True,
                                                    "include_upper": True,
                                                    "boost": 1
                                                }
                                            }
                                        },
                                        {
                                            "match_phrase": {
                                                "networkId": {
                                                    "query": "82ecf449b0714c609f54f5f677e9009b",
                                                    "slop": 0,
                                                    "boost": 1
                                                }
                                            }
                                        }
                                    ],
                                    "disable_coord": False,
                                    "adjust_pure_negative": True,
                                    "boost": 1
                                }
                            }
                        ],
                        "disable_coord": False,
                        "adjust_pure_negative": True,
                        "boost": 1
                    }
                }
            ],
            "disable_coord": False,
            "adjust_pure_negative": True,
            "boost": 1
        }
    },
    "_source": {
        "includes": [
            "tcr-info.active-sessions-count",
            "machine-info.id",
            "timestamp",
            "networkId",
            "customerName",
            "networkName",
            "dataCenterId"
        ],
        "excludes": []
    }
}


def write_data_to_csv(data):
    with open(file_path, 'a', newline='') as newFile:
        newFileWriter = csv.writer(newFile)
        for row in data:
            item_row = row['_source']
            newFileWriter.writerow([
                item_row['tcr-info']['active-sessions-count'],
                item_row['machine-info']['id'],
                # item_row['timestamp'],
                item_row['customerName'],
                item_row['networkName'],
                item_row['networkId'],
                item_row['dataCenterId']
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
        index='tcrraw201801',
        scroll='2m',
        size=size,
        body=body)

    sid = page['_scroll_id']
    scroll_size = page['hits']['total']

    silent_remove(file_path)

    write_header_to_csv(file_path,
                        ['active-sessions-count',
                         'id',
                         'timestamp',
                         'customerName',
                         'networkName',
                         'networkId',
                         'dataCenter'])

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


read_and_save(1000)
