#!/bin/sh

function compile {
    dirname=$(dirname $1)
    program_name=$(basename $1)

    cd $dirname

    if [ ${program_name: -3} != ".py" ]; then
        new_fname=$program_name.py
        mv $program_name $new_fname
        program_name=$new_fname
    fi

    printf '{"status": "ok", "outfile": "%s"}\n' $program_name
}

if [ "$#" -ne 1 ]; then
    echo "Usage: build_program.sh <path to file>" >&2
    exit 1
fi

compile $1
exit 0
