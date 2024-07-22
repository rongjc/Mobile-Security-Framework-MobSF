import aiohttp
import asyncio
import requests
import pandas as pd
from tqdm import tqdm
from xml.etree import ElementTree as ET
import json

# Function to fetch popular Android libraries from Maven Central, excluding Android native packages
def fetch_maven_popular_android_libraries():
    base_url = "https://search.maven.org/solrsearch/select"
    params = {
        'q': 'android NOT g:androidx* AND NOT g:com.android*',
        'rows': 100,  # Fetch 100 results per page
        'wt': 'json',
        'sort': 'popularity desc',
        'start': 0
    }
    
    libraries = []
    total_libraries = None
    
    with tqdm(total=1, desc='Fetching Maven Central Libraries') as pbar:
        while True:
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                print("Failed to fetch data from Maven Central")
                break
            
            data = response.json()
            if total_libraries is None:
                total_libraries = data['response']['numFound']
                total_libraries = 4000
                pbar.total = total_libraries
                
            for doc in data['response']['docs']:
                libraries.append({
                    'Group': doc.get('g', 'N/A'),
                    'Artifact': doc.get('a', 'N/A'),
                    'Version': doc.get('latestVersion', 'N/A'),
                    'Packaging': doc.get('p', 'N/A'),
                    'Timestamp': doc.get('timestamp', 'N/A'),
                    'Repository': 'Maven Central',
                    'Name': None,
                    'URL': None,
                    'Licenses': None,
                    'Developers': None,
                    'Description': None  # Placeholder for description
                })
            
            params['start'] += params['rows']
            pbar.update(len(data['response']['docs']))
            
            if params['start'] >= total_libraries:
                break
    
    return libraries

# Asynchronous function to fetch POM file and extract additional fields
async def fetch_pom_details(session, library, semaphore):
    async with semaphore:
        group_path = library['Group'].replace('.', '/')
        artifact = library['Artifact']
        version = library['Version']
        url = f"https://repo1.maven.org/maven2/{group_path}/{artifact}/{version}/{artifact}-{version}.pom"
        await asyncio.sleep(0.1)  # Rate limiting: wait for 100ms between requests
        async with session.get(url) as response:
            if response.status == 200:
                try:
                    content = await response.text()
                    root = ET.fromstring(content)
                    namespace = {'m': 'http://maven.apache.org/POM/4.0.0'}
                    
                    # Extract description
                    description = root.find('m:description', namespace)
                    if description is not None and description.text is not None:
                        library['Description'] = description.text.strip()
                    else:
                        library['Description'] = "No description available"
                    
                    # Extract name
                    name = root.find('m:name', namespace)
                    if name is not None and name.text is not None:
                        library['Name'] = name.text.strip()
                    
                    # Extract URL
                    url = root.find('m:url', namespace)
                    if url is not None and url.text is not None:
                        library['URL'] = url.text.strip()
                    
                    # Extract licenses
                    licenses = root.find('m:licenses', namespace)
                    if licenses is not None:
                        library['Licenses'] = ', '.join([
                            license.find('m:name', namespace).text.strip() if license.find('m:name', namespace) is not None else "No license name"
                            for license in licenses.findall('m:license', namespace)
                        ])
                    
                    # Extract developers
                    developers = root.find('m:developers', namespace)
                    if developers is not None:
                        library['Developers'] = ', '.join([
                            developer.find('m:name', namespace).text.strip() if developer.find('m:name', namespace) is not None else "No developer name"
                            for developer in developers.findall('m:developer', namespace)
                        ])
                    
                except ET.ParseError:
                    library['Description'] = "Failed to parse POM"
                    library['Name'] = "Failed to parse POM"
                    library['URL'] = "Failed to parse POM"
                    library['Licenses'] = "Failed to parse POM"
                    library['Developers'] = "Failed to parse POM"
            else:
                library['Description'] = "Failed to fetch POM"
                library['Name'] = "Failed to fetch POM"
                library['URL'] = "Failed to fetch POM"
                library['Licenses'] = "Failed to fetch POM"
                library['Developers'] = "Failed to fetch POM"

# Main function to handle asynchronous requests with progress bar
async def fetch_all_pom_details(libraries):
    semaphore = asyncio.Semaphore(10)  # Limit concurrent requests to 10
    async with aiohttp.ClientSession() as session:
        tasks = []
        for library in libraries:
            tasks.append(fetch_pom_details(session, library, semaphore))
        
        for f in tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='Fetching POM Details'):
            await f

# Fetching libraries
android_libraries = fetch_maven_popular_android_libraries()

# Running asynchronous tasks to fetch details with progress bar
asyncio.run(fetch_all_pom_details(android_libraries))

# Save the result to a JSON file
file_path = 'popular_android_libraries_with_details.json'
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(android_libraries, f, ensure_ascii=False, indent=4)

print(f"Data saved to {file_path}")
