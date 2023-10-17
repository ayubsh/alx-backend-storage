#!/usr/bin/env python3
"""Log Stats"""
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """Prits log stats from nginx
    """
    print('{} logs'.format(nginx_collection.count_documents({})))
    print('Methods:')

    for method in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        req_count = len(list(nginx_collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_count))
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_checks_count))


def run():
    """Prints the stats of nginx in mongodb
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
