import json


def get_column_names(query):
    source_names = list(query['_source']['includes'])
    query_names = list(query['script_fields'].keys())
    return source_names + query_names


def get_row(query, item_row):
    columns = get_column_names(query)
    res = []
    for column in columns:
        if column in item_row["_source"]:
            res.append(item_row["_source"][column])
        elif column in item_row["fields"]:
            res.append(str(item_row["fields"][column]).replace("[", "").replace("]", ""))
    return res


def format(query):
    if not isinstance(query, str):
        raise ValueError('You surprise me. The query param should be string')
    return json.loads(query)
