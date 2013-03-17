#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
# encoding: utf-8
"""
   Stream a file, parse any JSON objects in it, and put them on a
   MongoDB instance.

   Author: Owain Jones [github.com/doomcat]
"""

import sys
import json
import pymongo
import argparse


def parse_file(path):
    """Parse a file and lazily parse JSON objects in it -- look for the
       first and last curly braces and cut off anything in the string
       before or after that.
    """
    data = open(path, 'r').read()
    while data.startswith('{') is False:
        data = data[1:]
    while data.endswith('}') is False:
        data = data[:-1]
    try:
        return json.loads(data)
    except ValueError as e:
        print >> sys.stderr, str(e)
        return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--database", "-d", default="natureskin",
                        help="Which mongodb database to use")
    parser.add_argument("--collection", "-c", default="areas",
                        help="Which mongodb collection to use")
    parser.add_argument("--host", "-H", default="localhost",
                        help="IP/hostname of mongodb server")
    parser.add_argument("--port", "-p", type=int, default=27017,
                        help="Port of mongodb server")
    parser.add_argument("--username", default=None,
                        help="Username (if needed)")
    parser.add_argument("--password", default=None,
                        help="Password (if needed)")
    parser.add_argument("--connection", default=None,
                        help="Custom connection string")
    args = parser.parse_args()

    connection = pymongo.MongoClient(args.host, args.port)
    db = connection[args.database]

    print "Connecting to", args.host,
    if None not in [args.username, args.password]:
        print "as", args.username,
        db.authenticate(args.username, args.password)
    print

    db = connection[args.database]
    collection = db[args.collection]

    collection.ensure_index([
        ('center', pymongo.GEO2D),
        ('name', pymongo.DESCENDING),
        ('type', pymongo.DESCENDING),
    ])

    data = parse_file(args.file)
    for key in data:
        data[key].update(data[key]['meta'])
        del data[key]['meta']
        if 'encoded' in data[key].keys() and data[key]['encoded'] != []:
            del data[key]['points']
        _id = collection.insert(data[key])
        print "Uploaded", data[key]['name'], "- ID:", _id


if __name__ == '__main__':
    main()
