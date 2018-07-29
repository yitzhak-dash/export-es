import os
import csv
from elasticsearch import Elasticsearch

import query_parser as parser


class ExportES:
    def __init__(self, settings):
        self.settings = settings

    def run(self):
        self.es = Elasticsearch([self.settings.ES_HOST], port=9200, timeout=300)

        self.file_path = self.settings.OUTPUT
        self.body = parser.format(self.settings.ES_QUERY)
        self.es_index = self.settings.ES_INDEX
        self.size = self.settings.SCROLL_SIZE

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

    def main(self):
        page = self.es.search(
            index=self.es_index,
            scroll='2m',
            size=self.size,
            body=self.body,
            request_timeout=30)
        sid = page['_scroll_id']
        scroll_size = page['hits']['total']
        self.silent_remove(self.file_path)
        self.write_header_to_csv(self.file_path, parser.get_column_names(self.body))
        while (scroll_size > 0):
            print("Scrolling...")
            page = self.es.scroll(scroll_id=sid, scroll='2m')
            sid = page['_scroll_id']
            scroll_size = len(page['hits']['hits'])
            print("scroll size: " + str(scroll_size))
            self.write_data_to_csv(page['hits']['hits'])
        print("************** completed **************")

