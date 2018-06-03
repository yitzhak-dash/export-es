import unittest

import query_parser

QUERY = {
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
                                                    "from": "2018-05-01",
                                                    "to": None,
                                                    "include_lower": True,
                                                    "include_upper": True,
                                                    "boost": 1
                                                }
                                            }
                                        },
                                        {
                                            "range": {
                                                "timestamp": {
                                                    "from": None,
                                                    "to": "2018-05-15",
                                                    "include_lower": True,
                                                    "include_upper": True,
                                                    "boost": 1
                                                }
                                            }},
                                        {
                                            "match_phrase": {
                                                "networkName": {
                                                    "query": "BoxUL",
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
            "includes-1",
            "includes-2",
            "includes-3"
        ],
        "excludes": []
    },
    "script_fields": {
        "field-1": {
            "script": {
                "inline": "doc['clientToServer.incomingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        },
        "field-2": {
            "script": {
                "inline": "doc['serverToClient.outgoingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        },
        "field-3": {
            "script": {
                "inline": "doc['serverToClient.incomingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        },
        "field-4": {
            "script": {
                "inline": "doc['clientToServer.outgoingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        }
    }
}


class TestColumns(unittest.TestCase):
    def setUp(self):
        pass

    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_get_columns(self):
        res = query_parser.get_columns()
        self.assertEqual(res, ['field-1', 'filed-2', 'filed-3', 'filed-4'])
        pass


if __name__ == '__main__':
    unittest.main()
