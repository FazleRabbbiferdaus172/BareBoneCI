#!/bin/bash

source ./run_or_fail.sh

run_or_fail "I failed" rm -f commit_hash.txt

run_or_fail "Repo Location not found" pushd $1 1> /dev/null # 1> /dev/null removes the output of pushd

run_or_fail "Git reset failed" git reset --hard HEAD 1> /dev/null

COMMIT=$(git log -n1) # get the first line of the commit

COMMIT_ID=$(echo $COMMIT | awk {'print $2'}) # gets the first commit id, awk turns each word in text lines into positional arguments by the word seperaqtor. The default word seperator is spece, so second arg is the commit id 

run_or_fail "git pull failed" git pull 1> /dev/null

LATEST_COMMIT=$(git log -n1)
LATEST_COMMIT_ID=$(echo $LATEST_COMMIT | awk {'print $2'})

run_or_fail "directory change failed" popd 1> /dev/null

if [ $LATEST_COMMIT_ID != $COMMIT_ID ]
then
    echo $LATEST_COMMIT_ID > commit_hash.txt
fi