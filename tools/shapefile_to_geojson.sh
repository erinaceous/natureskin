#!/bin/bash
python2.7 ~/projects/natureskin/tools/shapefile_to_geojson.py --reduction-method smoothverts -r 0.001 $1
