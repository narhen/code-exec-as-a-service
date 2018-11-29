#!/bin/bash

function build_image {
    dir=$1
    cd ./$dir
    docker build -t "lang:$dir" .
    cd -
}

for dir in ./*; do
    dir=$(basename $dir)
    if [ "$dir" != "$(basename $0)" ] && [ "$dir" != "README.md" ]; then
        echo "building $dir"
        build_image $dir;
    fi
done
