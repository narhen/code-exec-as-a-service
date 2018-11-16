#!/bin/sh

function run {
    dirname=$(dirname $1)
    program_name=$(basename $1)
    program_output="program_output.txt"

    cd $dirname
    python3.7 $program_name 2>&1 >$program_output

    printf '{"status": "ok", "outfile": "%s"}\n' $program_output
}


if [ "$#" -ne 1 ]; then
    echo "Usage: build_program.sh <path to executable file>" >&2
    exit 1
fi

run $1
