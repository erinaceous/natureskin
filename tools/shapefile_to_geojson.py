#!/usr/bin/env python
"""Converts an ESRI shapefile (.shp) to GeoJSON (.json) format using the
   `pyshp` library.
   Uses `pyproj` to convert between coordinate systems."""

import argparse
import json
import os
import pyproj

from lib import shapefile


from_proj = None
to_proj = None


def reproject(coordinates, from_proj, to_proj):
    lon, lat = coordinates
    lon, lat = pyproj.transform(from_proj, to_proj, lon, lat)
    return (lon, lat)


def reduce_wgs(coordinates, resolution):
    """Takes a set of coordinates and reduces their resolution
       (rounds them to `resolution` significant places). Duplicate
       entries are then removed."""
    output = set()
    coordinates = [tuple(round(coord, resolution) for coord in point)
                   for point in coordinates]
    map(output.add, coordinates)
    coordinates = list()
    map(coordinates.extend, output)
    return coordinates


def convert(input, from_proj, to_proj, resolution):
    """Takes a shapefile dataset and iterates over it, converting
       coordinates to the new projection on-the-fly.

       Arguments:
       input:       The path to the input file
       from_proj:   The map projection of the original data
       to_proj:     The new coordinate system to reproject data to
       max_points:  The maximum number of points a polygon can contain.
    """
    sf = shapefile.Reader(input)
    output_file = open(os.path.splitext(input)[0] + '.json', 'w+')
    output_file.write('[\n')
    for index, polygon in enumerate(sf.shapes_iter()):
        print index, len(polygon.points),
        points = [reproject(point, from_proj, to_proj)
                  for point in polygon.points]
        # Fields are out of order! FIX
        #meta = {sf.fields[i][0]: sf.records()[index][i-1]
        #        for i in xrange(0, len(sf.fields)-1)}
        #del meta['DeletionFlag']
        #print meta,
        meta = {}
        points = reduce_wgs(points, resolution)
        print len(points)
        output = {"index": index, "meta": meta, "points": points}
        output_file.write(json.dumps(output))
        output_file.write(",\n")
    output_file.write("]")
    output_file.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="+", help="Paths to input files")
    parser.add_argument("--from-proj", "-f", default='epsg:27700',
                        help="From projection (EPSG code)")
    parser.add_argument("--to-proj", "-t", default='epsg:4326',
                        help="To projection (EPSG code)")
    parser.add_argument("--resolution", "-r", type=int, default=3,
                        help="Resolution of coordinates")
    args = parser.parse_args()

    global from_proj, to_proj
    from_proj = pyproj.Proj(init=args.from_proj)
    to_proj = pyproj.Proj(init=args.to_proj)

    for input in args.input:
        convert(input, from_proj=from_proj,
                to_proj=to_proj, resolution=args.resolution)


if __name__ == '__main__':
    main()
