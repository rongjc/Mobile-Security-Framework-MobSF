#!/bin/bash

# Retrieve the parameters
first_hash=$1
second_hash=$2
first_file=$3
second_file=$4
output_file=$5
filte_temp_path=$6

# Example operation with the parameters
echo "First parameter: $first_file"
echo "Second parameter: $second_file"
echo "output_file: $output_file" 
echo "Started the script" > $filte_temp_path
# Add your script logic here
rm $output_file
cd ./test
mkdir $first_hash-$second_hash
cd $first_hash-$second_hash
cp -rf $first_file ./$first_hash
cp -rf $second_file ./$second_hash
nicad6cross functions java ./$first_hash ./$second_hash type3-2-report
cp "./${first_hash}_functions-blind-crossclones/${first_hash}_functions-blind-crossclones-0.30-classes-withsource.html" $output_file
rm -rf ../$first_hash-$second_hash
rm $filte_temp_path
