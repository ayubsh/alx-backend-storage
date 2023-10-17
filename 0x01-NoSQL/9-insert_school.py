#!/usr/bin/env python3
"""Insert document"""


def insert_school(mongo_collection, **kwargs):
    """ inserts a document into school collection
    """
    rs = mongo_collection.insert_one(kwargs)
    return rs.inserted_id
