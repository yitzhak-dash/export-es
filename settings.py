ES_HOST = "es1.teridion.net"

ES_INDEX = "tcrtrafficrep201805"

OUTPUT = "./output/data.csv"

SCROLL_SIZE = 10000

ES_QUERY = {
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
            "networkName",
            "sourceTcrId",
            "timestamp"
        ],
        "excludes": []
    },
    "script_fields": {
        "upload1": {
            "script": {
                "inline": "doc['clientToServer.incomingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        },
        "download1": {
            "script": {
                "inline": "doc['serverToClient.outgoingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        },
        "upload2": {
            "script": {
                "inline": "doc['serverToClient.incomingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        },
        "download2": {
            "script": {
                "inline": "doc['clientToServer.outgoingBytes'].value",
                "lang": "painless"
            },
            "ignore_failure": False
        }
    }
}
