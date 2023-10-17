#!/usr/bin/env python3
"""find by query"""


def schools_by_topic(mongo_collection, topic):
    """finds schools by topics
    """
    return [schools for schools in mongo_collection.find({'topics': topic})]
