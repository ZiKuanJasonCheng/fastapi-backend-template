from elasticsearch import Elasticsearch
from .. import config

def query(start_timestamp, end_timestamp, param1="value1", param2="value2", param3="value3", index="index"):
    es = Elasticsearch([(config.elasticsearch["host"])], scheme="http", port=config.elasticsearch["port"])
    es_query = {
        "size": 1,
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "param1.raw": param1
                        }
                    },
                    {
                        "term": {
                            "param2.raw": param2
                        }
                    },
                    {
                        "terms": {
                            "param3.raw": [
                                param3
                            ]
                        }
                    },
                    {
                        "terms": {
                            "_type": [
                                "duration"
                            ]
                        }
                    },
                    {
                        "range": {
                            "evt_dt": {
                                "from": start_timestamp,
                                "to": end_timestamp,
                                "include_lower": True,
                                "include_upper": False
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "terms_based": {
                "range": {
                    "field": "evt_dt",
                    "ranges": [
                        {
                            "from": start_timestamp,
                            "to": end_timestamp
                        }
                    ]
                },
                "aggs": {
                    "color": {
                        "terms": {
                            "field": "color.raw",
                            "size": 20,
                            "order": {
                                "_term": "asc"
                            }
                        },
                        "aggs": {
                            "duration_sum": {
                                "sum": {
                                    "field": "Duration"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
    if param1 is None:
        es_query['query']['bool']['must'].pop(0)  # Remove the query dict: { "term": { "param1.raw": param1 } }
    if param2 is None:
        es_query['query']['bool']['must'].pop(1)  # Remove the query dict: { "term": { "param2.raw": param2 } }
    if param3 is None:
        es_query['query']['bool']['must'].pop(2)  # Remove the query dict: { "term": { "param3.raw": [param3] } }
    
    return es.search(index=index, body=es_query)