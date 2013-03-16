#!/bin/bash
# General purpose script for converting ESRI shapefiles to JSON format.

usage="$0 file output [plural] [type] [merge key] [remap keys] [remove keys] [prefix] [suffix]"

file=$1
temp=`dirname $file`/`basename $file .shp`.json
output=$2
plural=$3
kind=$4
merge_key=${5:-'name'}
remap_keys=$6
remove_keys=$7
prefix=${8:-"'database.load_from_file(\"$plural\", '"}
suffix=${9:-"');'"}

if [ "$#" -lt 4 ]; then
   echo $usage
   exit 2
fi

python2 `dirname $0`/shapefile_to_geojson.py \
   --reduction-method dummy --also-polyencode --resolution 0 \
   --preview $file

read -p "Hit return to continue"

python2 `dirname $0`/shapefile_to_geojson.py \
   --reduction-method dummy --also-polyencode --resolution 0 \
   $file

echo

command="python2 `dirname $0`/normalize_metadata.py -l -s -t --prefix $prefix "
command+="--suffix $suffix --add-centers --add_keys 'type=$kind' -- $temp "
command+="'$merge_key' '$remap_keys' '$remove_keys'"
echo "$command > $output"
read -p "Hit return to continue"
$command > $output

rm $temp
