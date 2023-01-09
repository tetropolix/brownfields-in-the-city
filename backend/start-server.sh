#!/bin/sh
usage() {                                 # Function: Print a help message.
  echo "Usage: $0 -h HOST -p PORT [ -e ENV FILE PATH relative to src dir ]" 1>&2 
}

exit_abnormal() {                         # Function: Exit with error.
  usage
  exit 1
}

host="127.0.0.1"
port="8000"
while getopts h:p:e: flag
do
    case "${flag}" in
        h) host=${OPTARG};;
        p) port=${OPTARG};;
        e) env_file=${OPTARG};;
        *)                                    # If unknown (any other) option:
            exit_abnormal                     # Exit abnormally.
            ;;
    esac
done


export BROWNFIELDS_ENV_FILE=$env_file
cd src && uvicorn main:app --host $host --port $port