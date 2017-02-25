#!/bin/bash
tools_path=$(dirname $(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}"))
cd $tools_path

git pull

[ -e last_update ] || echo 0 > last_update 
last_update=`cat last_update`

cd migrations
for update in *; do
  if [ $update -gt $last_update ]; then
    echo "Running $update"
    ./$update
  fi
done
cd $tools_path

[ -n "$update" ] && echo $update > last_update

service probemon restart
