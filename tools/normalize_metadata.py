#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
# encoding: utf-8
"""
   Takes a JSON file (as outputted by shapefile_to_json.py) and
   normalizes metadata - keys get renamed, polygons with the same
   identifier (e.g. the full name, a OS grid reference, or some other
   sort of ID) get merged, and the script prints out the normalized json
   to stdout.

   Author: Owain Jones [github.com/doomcat]
"""

import argparse
import json
import sys
import re


def normalize(input, merge_key, remap_keys, remove_keys,
              strip=True, lower_urls=True, prefix="", suffix=""):
    """Normalize a JSON file. Merge objects if two or more have
       identical values associated with the dictionary keys defined in
       merge_keys.

       Arguments:
       input:       The path to the file to read.
       merge_key:   The key that, if the value of which is identical for
                    two or more objects, mean that those objects should
                    be merged into a single object.
       remap_keys:  A comma-seperated string, or a list, of key=new_key
                    associations - e.g. to rename all 'nnr_name' keys
                    to 'name', do 'nnr_name=name'.
       remove_keys: A comma-seperated string, or a list, of keys to
                    remove from the final (merged) JSON objects.
       lower_urls:  If True, check to see if string properties are URLs,
                    and if they are, transform them to lowercase
                    (lots of the datasets have URLs in UPPERCASE).
                    If a list object is passed to lower_urls, it
                    forces those fields specifically to be lowercased
                    without first checking if they're URLS.
       strip:       If True, get rid of fields that are just whitespace.
       prefix:      String to prepend to output.
       suffix:      String to append to output.

       Returns:     Nothing. Prints the results to screen though.
    """
    input = open(input, 'r')

    print prefix,

    if type(remap_keys) == str:
        remap_keys = remap_keys.split(',')
    if type(remove_keys) == str:
        remove_keys = remove_keys.split(',')
    if remap_keys == ['']:
        remap_keys = []
    if remove_keys == ['']:
        remove_keys = []

    objects = {}
    duplicates = 0
    lineNr = 0
    for line in input:
        lineNr += 1
        line = line.strip().replace("\n", "").replace("\r", "")
        line = re.sub(",$", "", line)
        try:
            object = json.loads(line)
        except ValueError as e:
            print >> sys.stderr, "%d:" % lineNr, str(e)
            continue

        for remap_key in remap_keys:
            remap_key_from, remap_key_to = remap_key.split('=')
            try:
                object['meta'][remap_key_to] = object['meta'][remap_key_from]
                del object['meta'][remap_key_from]
            except:
                pass

        key = object['meta'][merge_key]
        if key not in objects.keys():
            objects[key] = object
        else:
            objects[key]['points'].extend(object['points'])
            objects[key]['bounds'] = rebound(
                objects[key]['bounds'], object['bounds']
            )
            duplicates += 1
        for remove_key in remove_keys:
            try:
                del objects[key]['meta'][remove_key]
            except:
                pass
        if strip:
            for strip_key in objects[key]['meta'].keys():
                if type(objects[key]['meta'][strip_key]) in [str, unicode]:
                    if re.match('^\W*$', objects[key]['meta'][strip_key])\
                    is not None:
                        del objects[key]['meta'][strip_key]

        if objects[key]['lo_res']:
            if objects[key]['lo_res'] == []:
                del objects[key]['lo_res']

    print json.dumps(objects, sort_keys=True, separators=(',', ':')),
    print suffix
    print >> sys.stderr, "Duplicates merged: %d" % duplicates


def rebound(orig, new):
    """Takes two sets of lat/lon bounds (of the form [N, W, S, E]) and
       calculates a new bounding box that covers all their area.
    """
    return [
        max([orig[0], new[0]]),
        min([orig[1], new[1]]),
        min([orig[2], new[2]]),
        max([orig[3], new[3]])
    ]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",
                        help="The input file to operate on.")
    parser.add_argument("merge_key", default="",
                        help="The key, that, if identical for two or more " +
                             "objects, means that those objects should be " +
                             "merged into a single object.")
    parser.add_argument("remap_keys", default="",
                        help="Comma-seperated list of key=new_key mappings " +
                             "- to rename all 'nnr_name' keys to 'name', " +
                             "you would have nnr_name=name in here.")
    parser.add_argument("remove_keys", default="",
                        help="Comma-seperated list of keys to remove from " +
                             "the final (merged) JSON objects.")
    parser.add_argument("--lower-urls", "-l", action="store_true",
                        default=False,
                        help="If True, check to see if string properties are" +
                        " URLs, and if they are, transform them to lowercase.")
    parser.add_argument("--strip", "-s", action="store_true", default=False,
                        help="If True, check for blank fields (all " +
                             "whitespace), and remove them.")
    parser.add_argument("--prefix", default="")
    parser.add_argument("--suffix", default="")
    args = parser.parse_args()

    normalize(input=args.input, merge_key=args.merge_key,
              remap_keys=args.remap_keys, remove_keys=args.remove_keys,
              strip=args.strip, lower_urls=args.lower_urls,
              prefix=args.prefix, suffix=args.suffix)
