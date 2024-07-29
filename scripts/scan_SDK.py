import os
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Load the JSON file with SDK details
json_file = 'popular_android_libraries_with_details.json'
with open(json_file, 'r', encoding='utf-8') as f:
    sdk_details = json.load(f)

# Function to detect SDKs from import statements in a single file
def detect_sdks_in_file(file_path, sdk_details):
    detected_sdks = {}
    import_pattern = re.compile(r'^\s*import\s+([\w\.]+)', re.MULTILINE)

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        imports = import_pattern.findall(content)
        for imp in imports:
            for sdk in sdk_details:
                if imp.startswith(sdk['Group']):
                    if sdk['Group'] not in detected_sdks:
                        detected_sdks[sdk['Group']] = sdk
    return detected_sdks

# Function to detect SDKs from source code files in parallel
def detect_sdks_from_source_code(root_dir, sdk_details):
    detected_sdks = {}
    files_to_scan = []

    # Traverse the directory structure to find source code files
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(('.java', '.kt', '.xml')):  # Add other source code file extensions if needed
                file_path = os.path.join(subdir, file)
                files_to_scan.append(file_path)

    # Use ThreadPoolExecutor to scan files in parallel
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(detect_sdks_in_file, file, sdk_details): file for file in files_to_scan}
        for future in tqdm(as_completed(futures), total=len(futures), desc='Scanning source code files'):
            result = future.result()
            for group, sdk in result.items():
                if group not in detected_sdks:
                    detected_sdks[group] = sdk

    return detected_sdks

# Specify the root directory of the source code
root_directory = '/Users/jrong/.MobSF/uploads/053ea86baad0f19b3b0af9e840b86ffc/java_source'

# Detect SDKs from the source code
detected_sdks = detect_sdks_from_source_code(root_directory, sdk_details)

# Save the detected SDKs to a JSON file
output_file = 'detected_sdks.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(detected_sdks, f, ensure_ascii=False, indent=4)

print(f"Data saved to {output_file}")
