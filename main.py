import os
import csv
import sys

from elasticsearch import Elasticsearch

import query_parser as parser


class ExportES:
    def __init__(self, settings):
        self.host = settings.ES_HOST
        self.file_path = settings.OUTPUT
        self.body = parser.format(settings.ES_QUERY)
        self.es_index = settings.ES_INDEX
        self.size = settings.SCROLL_SIZE

    def run(self):
        self.es = Elasticsearch([self.host], port=9200, timeout=300)
        self.main()

    def write_data_to_csv(self, data):
        with open(self.file_path, 'a', newline='') as newFile:
            newFileWriter = csv.writer(newFile)
            for row in data:
                newFileWriter.writerow(parser.get_row(self.body, row))

    def silent_remove(self, filename):
        try:
            os.remove(filename)
        except OSError:
            pass

    def write_header_to_csv(self, filename, header):
        with open(filename, 'a', newline='') as newFile:
            newFileWriter = csv.writer(newFile)
            newFileWriter.writerow(header)

    def get_page(self):
        return self.es.search(
            index=self.es_index,
            scroll='2m',
            size=self.size,
            body=self.body,
            request_timeout=30)

    def main(self):
        print("\n*********** STARTING ***********\n")
        page = self.get_page()
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']
        total_count = page['hits']['total']
        current_count = 0
        progress(current_count, total_count, 'bla')
        self.silent_remove(self.file_path)
        self.write_header_to_csv(self.file_path, parser.get_column_names(self.body))
        while (scroll_size > 0):
            page = self.es.scroll(scroll_id=sid, scroll='2m')
            sid = page['_scroll_id']
            scroll_size = len(page['hits']['hits'])
            current_count = current_count + scroll_size
            completed_percents = (current_count / total_count * 100)
            progress(current_count, total_count, 'completed')
            # print("progress: {0:.2f}%".format(completed_percents))
            self.write_data_to_csv(page['hits']['hits'])
        print("\n*********** COMPLETED ***********\n")


def progress(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 2)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()
