import unittest
import json
from pprint import pprint

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

QUERY_RAW ='''
{
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
                          "to": null,
                          "include_lower": true,
                          "include_upper": true,
                          "boost": 1
                        }
                      }
                    },
                    {
                      "range": {
                        "timestamp": {
                          "from": null,
                          "to": "2018-05-15",
                          "include_lower": true,
                          "include_upper": true,
                          "boost": 1
                        }
                      }
                    },
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
                  "disable_coord": false,
                  "adjust_pure_negative": true,
                  "boost": 1
                }
              }
            ],
            "disable_coord": false,
            "adjust_pure_negative": true,
            "boost": 1
          }
        }
      ],
      "disable_coord": false,
      "adjust_pure_negative": true,
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
      "ignore_failure": false
    },
    "field-2": {
      "script": {
        "inline": "doc['serverToClient.outgoingBytes'].value",
        "lang": "painless"
      },
      "ignore_failure": false
    },
    "field-3": {
      "script": {
        "inline": "doc['serverToClient.incomingBytes'].value",
        "lang": "painless"
      },
      "ignore_failure": false
    },
    "field-4": {
      "script": {
        "inline": "doc['clientToServer.outgoingBytes'].value",
        "lang": "painless"
      },
      "ignore_failure": false
    }
  }
}
'''

ITEM_ROW = {
    "_source": {
        "includes-1": "value-11",
        "includes-2": "value-12",
        "includes-3": "value-13"
    },
    "fields": {
        "field-1": "value-1",
        "field-2": "value-2",
        "field-3": "value-3",
        "field-4": "value-4"
    }
}


class TestColumns(unittest.TestCase):
    def setUp(self):
        pass

    def test_sanity(self):
        self.assertEqual(1, 1)

    def test_get_columns(self):
        res = query_parser.get_column_names(QUERY)
        self.assertListEqual(res,
                             ["includes-1", "includes-2", "includes-3", "field-1", "field-2", "field-3", "field-4"])

    def test_get_row(self):
        res = query_parser.get_row(QUERY, ITEM_ROW)
        self.assertListEqual(res, ["value-11", "value-12", "value-13", "value-1", "value-2", "value-3", "value-4"])

    def test_format_query(self):
        self.assertEqual(query_parser.format(QUERY_RAW), QUERY)

if __name__ == '__main__':
    unittest.main()
