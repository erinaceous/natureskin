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
import os
import re


def normalize(input, merge_keys, remap_keys, lower_urls=True):
    """Normalize a JSON file. Merge objects if two or more have
       identical values associated with the dictionary keys defined in
       merge_keys.

       Arguments:
       input:       The path to the file to read.
       merge_keys:  A comma-seperated string, or a list, of keys that,
                    if have identical in two or more objects, mean that
                    those objects should be merged into a single object.
       remap_keys:  A comma-seperated string, or a list, of key=new_key
                    associations - e.g. to rename all 'nnr_name' keys
                    to 'name', do 'nnr_name=name'.
       lower_urls:  If True, check to see if string properties are URLs,
                    and if they are, transform them to lowercase
                    (lots of the datasets have URLs in UPPERCASE)

       Returns:     The structure in dictionary form, normalized.
    """
    # TODO: This.
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",
                        help="The input file to operate on.")
    parser.add_argument("merge_keys", default="",
                        help="Comma-seperated list of keys, that, if have " +
                             "identical values in two or more objects, mean " +
                             "that those objects should be merged into a " +
                             "single object.")
    parser.add_argument("remap_keys", default="",
                        help="Comma-seperated list of key=new_key mappings " +
                             "- to rename all 'nnr_name' keys to 'name', " +
                             "you would have nnr_name=name in here.")
    parser.add_argument("--lower-urls", "-l", action="store_true",
                        default=False,
                        help="If True, check to see if string properties are" +
                        " URLs, and if they are, transform them to lowercase.")
    args = parser.parse_args()

    normalize(input=args.input, merge_keys=args.merge_keys,
              remap_keys=args.remap_keys, lower_urls=args.lower_urls)
