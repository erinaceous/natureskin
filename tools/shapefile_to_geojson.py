#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4 expandtab
# encoding: utf-8
"""Converts an ESRI shapefile (.shp) to GeoJSON (.json) format using the
   `pyshp` library.
   Uses `pyproj` to convert between coordinate systems.
   Uses `simplify.py` to simplify polygons to reduce number of points.

   Author: Owain Jones [github.com/doomcat]
"""

import argparse
import json
import os
import pyproj

from lib import shapefile, orderedset, simplify


from_proj = None
to_proj = None


def reproject(coordinates, from_proj, to_proj):
    lon, lat = coordinates
    lon, lat = pyproj.transform(from_proj, to_proj, lon, lat)
    return (lon, lat)


def reproject_bbox(coordinates, from_proj, to_proj):
    west, north, east, south = coordinates
    west, north = pyproj.transform(from_proj, to_proj, west, north)
    east, south = pyproj.transform(from_proj, to_proj, east, south)
    return (west, north, east, south)


def reduce_wgs(coordinates, resolution):
    """Takes a set of coordinates and reduces their resolution
       (rounds them to `resolution` significant places). Duplicate
       entries are then removed.

       Arguments:
       coordinates: List of coordinates in the form [(lon, lat), ...]
       resolution: How many decimal places to round the coordinates to.

       Returns: A flattened list of coordinates, of the form
                [lon, lat, lon, lat, lon, lat, ...]
    """
    output = orderedset.OrderedSet()
    coordinates = [tuple(round(coord, resolution) for coord in point)
                   for point in coordinates]
    map(output.add, coordinates)
    coordinates = list()
    map(coordinates.extend, output)
    return coordinates


def reduce_wgs_rdp(coordinates, resolution):
    """Takes a set of coordinates (a polygon) and smooths the lines
       using the Ramer-Douglas-Peucker algorithm to reduce the number of
       vertices.

       Arguments:
       coordinates: List of coordinates in the form [(lon, lat), ...]
       resolution: Vertices reduction factor.

       Returns: A flattened list of coordinates, of the form
                [lon, lat, lon, lat, lon, lat, ...]
    """
    coordinates = [{"x": point[1], "y": point[0]}
                   for point in coordinates]
    coordinates = simplify.simplify(coordinates, resolution)
    output = list()
    for point in coordinates:
        output.extend([point['y'], point['x']])
    return output


def reduce_dummy(coordinates, resolution):
    """Doesn't actually reduce the number of coordinates. Just flattens
       the list from [(lon, lat), ...] to [lon, lat, lon, lat, ...]
    """
    new_coordinates = list()
    map(new_coordinates.extend, coordinates)
    return new_coordinates


# Give the algorithms short names so we can choose which one to use via
# the commandline
algorithms = {
    "round": reduce_wgs,
    "smoothverts": reduce_wgs_rdp,
    "dummy": reduce_dummy
}


def convert(input, from_proj, to_proj, min_res=1, max_res=5,
            resolution=-1, threshold=300, output_path=None,
            reduct_func=reduce_wgs, prefix="", suffix=""):
    """Takes a shapefile dataset and iterates over it, converting
       coordinates to the new projection on-the-fly.

       Arguments:
       input:       The path to the input file
       from_proj:   The map projection of the original data
       to_proj:     The new coordinate system to reproject data to
       threshold:   The number of points all polygons should try to
                    contain (this is a maximum *and* a minimum)
       min_res:     Minimum resolution of coordinates.
                    Also used to generate the 'lo_res' points list.
       max_res:     Maximum resolution of coordinates
       resolution:  If anything other than -1, overrides min_res and
                    max_res and does a "dumb" reducing of data points
                    instead of testing to see what the best resolution
                    is (which is the default operation).
       output_path: If set, the path to the file to output the JSON data
                    to. If not set, defaults to the input's path but
                    with the extension replaced with '.json'
       reduct_func: Specify a reduction function to use. Reduction
                    functions must take the arguments
                    (coordinates, resolution) where `coordinates` is a
                    list of tuples of the orm [(lon, lat), ...], and
                    must return a flattened list of coordinates of the
                    form [lon, lat, lon, lat, ...]

       Returns:     Nothing - creates a new file for the output. Default
                    is <input filename base>.json
    """
    sf = shapefile.Reader(input)

    if output_path is not None:
        output_file = open(output_path, 'w+')
    else:
        output_file = open(os.path.splitext(input)[0] + '.json', 'w+')

    output_file.write(prefix)
    output_file.write('[\n')

    for index, shape in enumerate(sf.shapes_iter()):
        # Parse the shapefile recordset for this shape's associated
        # record
        # Fields are out of order! FIX
        meta = {sf.fields[i][0].lower(): sf.records()[index][i - 1]
                for i in xrange(0, len(sf.fields) - 1)}
        try:
            del meta['deletionflag']
        except KeyError:
            pass

        # Some shapes are composed of multiple polygons (e.g. polygons
        # with holes in them), so process each part individually.
        parts = []
        lo_res = []
        sum_points = 0
        sum_lo_res = 0

        for i, part in enumerate(shape.parts):

            if i == len(shape.parts) - 1:
                end = len(shape.points) - 1
            else:
                end = shape.parts[i + 1]
            polygon = shape.points[part:end]

            # Reproject all the polygon points from BGS to WGS
            points = [reproject(point, from_proj, to_proj)
                      for point in polygon]

            # Generate low-res version of polygon
            points_lo = reduct_func(points, min_res)

            if resolution is not -1:
                points = reduct_func(points, resolution)
            else:
                # Find the polygon with the 'best' number of points.
                # This means that small areas will stay detailed whilst
                # large areas don't kill everyone's computers.
                distance = len(points)

                for i in xrange(min_res, max_res + 1):
                    cur_points = reduct_func(points, i)
                    cur_dist = abs(len(cur_points) - threshold)

                    if cur_dist < distance:
                        distance = cur_dist
                        best_points = cur_points
                        best_res = i

                points = best_points
                print best_res,

            parts.append(points)
            lo_res.append(points_lo)
            sum_points += len(points)
            sum_lo_res += len(points_lo)

        bounds = reproject_bbox(shape.bbox, from_proj, to_proj)
        output = {"meta": meta, "bounds": bounds,
                  "lo_res": lo_res, "points": parts}
        output_file.write(json.dumps(output))
        output_file.write(",\n")
        print index, len(shape.points)*2, sum_points, sum_lo_res

    output_file.write("]")
    output_file.write(suffix)
    output_file.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="+", help="Paths to input files")
    parser.add_argument("--from-proj", "-f", default='epsg:27700',
                        help="From projection (EPSG code)")
    parser.add_argument("--to-proj", "-t", default='epsg:4326',
                        help="To projection (EPSG code)")
    parser.add_argument("--resolution", "-r", type=float, default=-1,
                        help="Resolution of coordinates - what this actually" +
                        " means varies between point reduction methods - for" +
                        " the 'round' method, lower values == lower " +
                        "resolution, but for the 'smoothverts' method, " +
                        "lower values == higher resolution.")
    parser.add_argument("--min-resolution", type=float, default=1,
                        help="Minimum coordinate resolution")
    parser.add_argument("--max-resolution", type=float, default=5,
                        help="Maximum coordinate resolution")
    parser.add_argument("--points-threshold", "-p", type=int, default=300,
                        help="(Soft) maximum number of points per polygon")
    parser.add_argument("--output", "-o", default=None,
                        help="Where to save the output")
    parser.add_argument("--reduction-method", "-m", default="round",
                        help="Method to reduce number of points in shape. " +
                             "Available: %s" % ', '.join(algorithms.keys()))
    parser.add_argument("--output-prefix",
                        default="function get_polygons() { return ")
    parser.add_argument("--output-suffix",
                        default="; }")
    args = parser.parse_args()

    global from_proj, to_proj
    from_proj = pyproj.Proj(init=args.from_proj)
    to_proj = pyproj.Proj(init=args.to_proj)

    for input in args.input:
        convert(input, from_proj=from_proj, to_proj=to_proj,
                min_res=args.min_resolution, max_res=args.max_resolution,
                resolution=args.resolution, threshold=args.points_threshold,
                output_path=args.output,
                reduct_func=algorithms[args.reduction_method],
                prefix=args.output_prefix, suffix=args.output_suffix)


if __name__ == '__main__':
    main()
