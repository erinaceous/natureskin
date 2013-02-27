#!/bin/bash

python2.7 `dirname $0`/shapefile_to_geojson.py --reduction-method smoothverts --min-resolution=0.001 -r 0.0001 $1
