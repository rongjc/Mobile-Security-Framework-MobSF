#!/bin/bash

# Set this to 1 to enable echo statements, or 0 to disable them
ECHO=1

function log {
    if [ "$ECHO" -eq 1 ]; then
        echo "$1"
    fi
}

log "Started the script"

# Retrieve the parameters
first_hash=$1
second_hash=$2
first_file=$3
second_file=$4
output_file=$5
filte_temp_path=$6

log "Parameters received:"
log "First hash: $first_hash"
log "Second hash: $second_hash"
log "First file: $first_file"
log "Second file: $second_file"
log "Output file: $output_file"
log "Filter temporary path: $filte_temp_path"

# Define the prefix directory
prefix_directory="/path/to/your/prefix"

# Get the directory of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
log "Script directory: $SCRIPT_DIR"

# Construct the path to the Python script
PYTHON_SCRIPT="$SCRIPT_DIR/process_html.py"
log "Python script path: $PYTHON_SCRIPT"

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

log "First parameter: $first_file"
log "Second parameter: $second_file"
log "Output file: $output_file"
log "Writing 'Started the script' to $filte_temp_path"
echo "Started the script" > $filte_temp_path

# Add your script logic here
log "Removing old output file if it exists: $output_file"
rm -f $output_file

log "Changing directory to ./test"
cd ./test

log "Removing old directory: ../$first_hash-$second_hash"
rm -rf ../$first_hash-$second_hash

log "Creating new directory: $first_hash-$second_hash"
mkdir $first_hash-$second_hash

log "Changing directory to: $first_hash-$second_hash"
cd $first_hash-$second_hash

log "Copying $first_file to ./$first_hash"
cp -rf $first_file ./$first_hash

log "Copying $second_file to ./$second_hash"
cp -rf $second_file ./$second_hash

# Remove all files from each directory
for dir in "${directories[@]}"; do
    full_path="./$first_hash/$dir"
    log "Removing files from $full_path"
    rm -rf "$full_path"*

    full_path="./$second_hash/$dir"
    log "Removing files from $full_path"
    rm -rf "$full_path"*
done

log "All specified files have been removed."

log "Running nicad6cross"
nicad6cross functions java ./$first_hash ./$second_hash type3-2-report

log "Copying HTML report to $output_file"
cp "./${first_hash}_functions-blind-crossclones/${first_hash}_functions-blind-crossclones-0.30-classes-withsource.html" $output_file

log "Running Python script on $output_file"
python3 "$PYTHON_SCRIPT" "$output_file"

log "Removing directory: ../$first_hash-$second_hash"
rm -rf ../$first_hash-$second_hash

log "Removing filter temporary file: $filte_temp_path"
rm $filte_temp_path

log "Script finished"
