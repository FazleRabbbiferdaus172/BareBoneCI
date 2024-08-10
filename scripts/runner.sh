#!/bin/bash

REPO=$1
COMMIT=$2

source ./run_or_fail.sh

run_or_fail "Repo location not found" pushd "$REPO" 1> /dev/null

run_or_fail "Could not call git pull" git pull

run_or_fail "Could not update to given commit hash" git reset --hard "$COMMIT"

# echo 'hello ok'