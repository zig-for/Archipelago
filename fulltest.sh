#!/bin/bash

printf "Testing %s DR with %s Tests (intensity=%d)\n" 2 vanilla 3
./testsuite.sh 2 vanilla > results.txt 2> errors.txt
printf "Testing %s DR with %s Tests (intensity=%d)\n" 5 basic 1
./testsuite.sh 5 basic 1 >> results.txt 2>> errors.txt
printf "Testing %s DR with %s Tests (intensity=%d)\n" 5 basic 2
./testsuite.sh 5 basic 2 >> results.txt 2>> errors.txt
printf "Testing %s DR with %s Tests (intensity=%d)\n" 5 basic 3
./testsuite.sh 5 basic 3 >> results.txt 2>> errors.txt
printf "Testing %s DR with %s Tests (intensity=%d)\n" 10 crossed 1
./testsuite.sh 10 crossed 1 >> results.txt 2>> errors.txt
printf "Testing %s DR with %s Tests (intensity=%d)\n" 10 crossed 2
./testsuite.sh 10 crossed 2 >> results.txt 2>> errors.txt
printf "Testing %s DR with %s Tests (intensity=%d)\n" 10 crossed 3
./testsuite.sh 10 crossed 3 >> results.txt 2>> errors.txt