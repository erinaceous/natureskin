#!/bin/bash

python2 `dirname $0`/shapefile_to_geojson.py \
   --reduction-method dummy --also-polyencode --resolution 0 \
   $1
