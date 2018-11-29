#!/bin/sh

function run {
    input_file=$2
    dirname=$(dirname $1)
    program_name=$(basename $1)
    program_output="program_output.txt"

    cd $dirname
    cat $input_file | python3.7 $program_name 2>&1 >$program_output

    printf '{"status": "ok", "outfile": "%s"}\n' $program_output
}


if [ "$#" -ne 2 ]; then
    echo "Usage: run_program.sh <path to executable file> <path to input file>" >&2
    exit 1
fi

run $1 $2
