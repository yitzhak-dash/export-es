from main import ExportES


class Config:
    ### CONFIGURATION

    ES_HOST = "es1.teridion.net"

    ES_INDEX = "tcrtrafficagg"

    OUTPUT = "./output/data.csv"

    SCROLL_SIZE = 1000

    ES_QUERY = '''
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
    
                "networkName",
    
                "sourceTcrId",
    
                "timestamp",
    
                "sourceDatacenter"
    
            ],
    
            "excludes": []
    
        },
    
        "script_fields": {
    
            "upload1": {
    
                "script": {
    
                    "inline": "doc['clientToServer.incomingBytes'].value",
    
                    "lang": "painless"
    
                },
    
                "ignore_failure": false
    
            },
    
            "download1": {
    
                "script": {
    
                    "inline": "doc['serverToClient.outgoingBytes'].value",
    
                    "lang": "painless"
    
                },
    
                "ignore_failure": false
    
            },
    
            "upload2": {
    
                "script": {
    
                    "inline": "doc['serverToClient.incomingBytes'].value",
    
                    "lang": "painless"
    
                },
                "ignore_failure": false
            },
            "download2": {
                "script": {
                    "inline": "doc['clientToServer.outgoingBytes'].value",
                    "lang": "painless"
                },
                "ignore_failure": false
            }
        }
    }
    '''

    ### END CONFIGURATION


if __name__ == '__main__':
    ExportES(Config()).run()
