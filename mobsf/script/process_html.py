import sys
from bs4 import BeautifulSoup
import re

def process_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        
        # Change the title inside the head tag
        if soup.head and soup.head.title:
            soup.head.title.string = "Similarity Report"
        elif soup.head:
            new_title = soup.new_tag('title')
            new_title.string = "Similarity Report"
            soup.head.append(new_title)
        else:
            new_head = soup.new_tag('head')
            new_title = soup.new_tag('title')
            new_title.string = "Similarity Report"
            new_head.append(new_title)
            soup.html.insert(0, new_head)
        
        # Remove content between <h2> tags
        for h2 in soup.find_all('h2'):
            h2.clear()

        # Remove the second row of the first table under body
        if soup.body:
            first_table = soup.body.find('table')
            if first_table:
                rows = first_table.find_all('tr')
                if len(rows) > 1:
                    rows[1].decompose()
                    rows[0].decompose()
            # Regular expression to find the pattern and replace it
        pattern = r'(\d+) fragments, nominal size (\d+) lines, similarity (\d+)%'
        replacement = r'Code with similarity(\2 lines, \3% Similar)'
        for match in re.finditer(pattern, str(soup)):
            soup = re.sub(pattern, replacement, str(soup))


    # Save the modified HTML
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_html.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    process_html(html_file)
    print(f"Processed {html_file} successfully.")
