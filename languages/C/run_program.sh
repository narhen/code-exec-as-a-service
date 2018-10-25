#!/bin/bash

function run {
    dirname=$(dirname $1)
    program_name=$(basename $1)
    program_output="program_output.txt"

    cd $dirname
    ./$program_name 2>&1 >$program_output

    printf '{"outfile": "%s"}\n' $program_output
}


if [ "$#" -ne 1 ]; then
    echo "Usage: build_program.sh <path to .c file>" >&2
    exit 1
fi

run $1
