#!/bin/bash

function compile {
    dirname=$(dirname $1)
    program_name=$(basename $1)
    executable_file="program"
    error_file="compile_errors.txt"

    cd $dirname
    gcc -o $executable_file $program_name 2>&1 > $error_file
    compile_status=$?

    if [ $compile_status -eq 0 ]; then
        printf '{"status": "ok", "outfile": "%s"}\n' $executable_file
    else
        printf '{"status": "error", "outfile": "%s"}\n' $error_file
    fi
}

if [ "$#" -ne 1 ]; then
    echo "Usage: build_program.sh <path to .c file>" >&2
    exit 1
fi

compile $1
exit $compile_status
