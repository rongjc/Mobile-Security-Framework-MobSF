import json
import yaml

# Load the JSON file
input_file = 'popular_android_libraries_with_details.json'
output_file = 'converted_libraries.yaml'

with open(input_file, 'r', encoding='utf-8') as f:
    libraries = json.load(f)

# Function to replace None and 'null' values
def replace_nulls(value):
    if value is None or value == 'null':
        return 'Not Available'
    return value

# Prepare the data for YAML conversion
yaml_data = []
for lib in libraries:
    entry = {
        'id': replace_nulls(lib.get('Group', 'N/A')),
        'message': replace_nulls(lib.get('Description', 'N/A')),
        'type': 'Regex',
        'pattern': replace_nulls(lib.get('Group', 'N/A')),
        'severity': 'Info',
        'input_case': 'exact',
        'metadata': {
            'name': replace_nulls(lib.get('Name', 'N/A')),
            'licenses': replace_nulls(lib.get('Licenses', 'N/A')),
            'description': replace_nulls(lib.get('Description', 'N/A')),
            'developers': replace_nulls(lib.get('Developers', 'N/A'))
        }
    }
    yaml_data.append(entry)

# Write the YAML file
with open(output_file, 'w', encoding='utf-8') as f:
    yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True)

print(f"Data saved to {output_file}")
