#!/bin/bash

function print_help {
  echo "Path and suite must be set!"
  echo "usage: RunParseMTRTests.sh [-p <path>] [-s <suite>]"
  echo "OPTIONS"
  echo "  -p <path>  - path to the MariaDB source (e.g. /home/user/MariaDB/server/)"
  echo "  -s <suite>  - suite in mysql-test directory (e.g. main)"
  echo "Example: RunParseMTRTests.sh -p /home/user/MariaDB/server/ -s main"
  exit 0
}

while getopts p:s: flag
do
    case "${flag}" in
        p) path=${OPTARG};;
        s) suite=${OPTARG};;
    esac
done

if [ -z "$path" ]; then
  print_help
elif [ -z "$suite" ]; then
  print_help
fi

echo "Path: $path";
echo "Suite: $suite";

new_suit_name=$suite"_upd"

if [[ "$suite" == "main" ]]; then
  full_path="$path/mysql-test/$suite/"
  new_full_path="$path/mysql-test/suite/$new_suit_name/"
else
  full_path="$path/mysql-test/suite/$suite/t"
  new_full_path="$path/mysql-test/suite/$new_suit_name/t"
fi
  echo "Full path: $full_path";

for entry in "$full_path"/*.test
do
  new_name=$new_full_path/$(basename $entry .test)"_upd.test"
  python3 ParseMTRTests.py -i $entry -o $new_name
done