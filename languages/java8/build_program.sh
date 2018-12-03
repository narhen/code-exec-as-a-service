#!/bin/sh

function compile {
    dirname=$(dirname $1)
    program_name=$(basename $1)
    error_file="compile_errors.txt"

    cd $dirname

    if [ ${program_name: -5} != ".java" ]; then
        new_fname=$program_name.java
        mv $program_name $new_fname
        program_name=$new_fname
    fi

    javac $program_name 1>$error_file 2>&1
    executable_file=${program_name%.*} # remove file extension ".java"

    if [ $? -eq 0 ]; then
        printf '{"status": "ok", "outfile": "%s"}\n' $executable_file
    else
        printf '{"status": "error", "outfile": "%s"}\n' $error_file
    fi
}

if [ "$#" -ne 1 ]; then
    echo "Usage: build_program.sh <path to file>" >&2
    exit 1
fi

compile $1
exit 0
