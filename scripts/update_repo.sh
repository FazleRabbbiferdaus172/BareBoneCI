#!/bin/bash

source ./run_or_fail.sh

run_or_fail "I failed" echo $1

run_or_fail "Repo Location not found" pushd $1 1> /dev/null # 1> /dev/null removes the output of pushd

run_or_fail "Git reset failed" git reset --hard HEAD