#!/usr/bin/env python3
"""List docs"""


def list_all(mongo_collection):
    """ List all documents in
    collection
    """
    return [docs for docs in mongo_collection.find()]
