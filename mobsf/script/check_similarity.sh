#!/bin/bash

echo "Started the script"

# Retrieve the parameters
first_hash=$1
second_hash=$2
first_file=$3
second_file=$4
output_file=$5
filte_temp_path=$6

echo "Parameters received:"
echo "First hash: $first_hash"
echo "Second hash: $second_hash"
echo "First file: $first_file"
echo "Second file: $second_file"
echo "Output file: $output_file"
echo "Filter temporary path: $filte_temp_path"

# Define the prefix directory
prefix_directory="/path/to/your/prefix"

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Script directory: $SCRIPT_DIR"

# Construct the path to the Python script
PYTHON_SCRIPT="$SCRIPT_DIR/process_html.py"
echo "Python script path: $PYTHON_SCRIPT"

# Array of directories to remove files from
directories=(
    "com/google/"
    "androidx/"
    "okhttp2/"
    "okhttp3/"
    "com/android/"
    "com/squareup/"
    "okhttp/"
    "android/content/"
    "com/twitter/"
    "twitter4j/"
    "android/support/"
    "org/apache/"
    "oauth/signpost/"
    "android/arch/"
    "org/chromium/"
    "com/facebook/"
    "org/spongycastle/"
    "org/bouncycastle/"
    "com/amazon/identity/"
    "io/fabric/sdk/"
    "com/instabug/"
    "com/crashlytics/android/"
    "kotlinx/"
    "kotlin/"
    "com/adjust/"
    "com/bytedance/"
    "com/ironsource/"
    "com/chartboost/"
    "com/applovin/"
    "com/unity3d/"
    "com/vungle/"
    "com/appsflyer/"
)

# Example operation with the parameters
echo "First parameter: $first_file"
echo "Second parameter: $second_file"
echo "Output file: $output_file"
echo "Writing 'Started the script' to $filte_temp_path"
echo "Started the script" > $filte_temp_path

# Add your script logic here
echo "Removing old output file if it exists: $output_file"
rm -f $output_file

echo "Changing directory to ./test"
cd ./test

echo "Removing old directory: ../$first_hash-$second_hash"
rm -rf ../$first_hash-$second_hash

echo "Creating new directory: $first_hash-$second_hash"
mkdir $first_hash-$second_hash

echo "Changing directory to: $first_hash-$second_hash"
cd $first_hash-$second_hash

echo "Copying $first_file to ./$first_hash"
cp -rf $first_file ./$first_hash

echo "Copying $second_file to ./$second_hash"
cp -rf $second_file ./$second_hash

# Remove all files from each directory
for dir in "${directories[@]}"; do
    full_path="./$first_hash/$dir"
    echo "Removing files from $full_path"
    rm -rf "$full_path"*

    full_path="./$second_hash/$dir"
    echo "Removing files from $full_path"
    rm -rf "$full_path"*
done

echo "All specified files have been removed."

echo "Running nicad6cross"
nicad6cross functions java ./$first_hash ./$second_hash type3-2-report

echo "Copying HTML report to $output_file"
cp "./${first_hash}_functions-blind-crossclones/${first_hash}_functions-blind-crossclones-0.30-classes-withsource.html" $output_file

echo "Running Python script on $output_file"
python3 "$PYTHON_SCRIPT" "$output_file"

echo "Removing directory: ../$first_hash-$second_hash"
rm -rf ../$first_hash-$second_hash

echo "Removing filter temporary file: $filte_temp_path"
rm $filte_temp_path

echo "Script finished"
