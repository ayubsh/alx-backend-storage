#!/usr/bin/env python3
"""update collection"""


def update_topics(mongo_collection, name, topics):
    """update topics of school documents
    based on name
    """
    mongo_collection.update_one({'name': name}, {'$set': {'topics': topics}})
