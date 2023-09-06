import os
import re
from datetime import datetime

# Define a function to parse frontmatter data
def parse_frontmatter(md_content):
    frontmatter = {}
    match = re.match(r'---(.*?)---', md_content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        lines = frontmatter_text.strip().split('\n')
        for line in lines:
            key, value = map(str.strip, line.split(':', 1))
            frontmatter[key] = value
    return frontmatter

# Initialize data structures to store categorized OFEPs
status_to_ofeps = {
    'Approved': [],
    'Rejected': [],
    'Withdrawn': [],
}

root_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Define the source and script directories
source_directory = os.path.join(root_directory, 'OFEP')
script_directory = os.path.join(root_directory, 'docs', 'source')

if not os.path.exists(script_directory):
    os.makedirs(script_directory)

# Get the list of OFEP files in the source directory
ofep_files = [file for file in os.listdir(source_directory) if file.endswith('.md') and file != 'OFEP-template.md']

# Generate the toctree for index.rst
content = 'OpenFeature Enhancement Proposals\n========================================\n .. toctree::\n   :titlesonly:\n   :maxdepth: 1\n   :hidden:\n   :caption: OFEP Documentation\n\n   '

content += '\n   '.join([ofep_file[:-3] for ofep_file in ofep_files])

# Iterate through the files in the OFEP directory
index_content = "\n\nOFEP Index\n===========\n\n"

for filename in os.listdir(source_directory):
     if filename.endswith('.md') and filename != 'OFEP-template.md':
        with open(os.path.join(source_directory, filename), 'r') as file:
            md_content = file.read()
            frontmatter = parse_frontmatter(md_content)
            ofep_status = frontmatter.get('status', 'Unknown')

            if ofep_status in status_to_ofeps:
                date_str = frontmatter.get('date', '1970-01-01')
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                authors_list = ', '.join([author.strip() for author in re.findall(r'\[(.*?)\]', frontmatter.get('authors', ''))])
                tags_list = ', '.join([tag.strip() for tag in re.findall(r'\[(.*?)\]', frontmatter.get('tags', ''))])
                status_to_ofeps[ofep_status].append((date_obj, frontmatter['title'], authors_list, tags_list, filename))

# Sort OFEPs in each category by date
for status, ofeps in status_to_ofeps.items():
    status_to_ofeps[status] = sorted(ofeps, key=lambda x: x[0], reverse=True)

# Generate the index content with the table
index_content += "\n"

for status, ofeps in status_to_ofeps.items():
    index_content += f"{status}\n{'=' * len(status)}\n\n"
    index_content += ".. list-table::\n"
    index_content += "   :header-rows: 1\n"
    index_content += "   :widths: auto\n"
    index_content += "\n"
    index_content += "   * - Last Modified\n"
    index_content += "     - Title\n"
    index_content += "     - Authors\n"
    index_content += "     - Tags\n"

    for date_obj, title, authors_list, tags_list, filename in ofeps:
        formatted_date = date_obj.strftime('%dth %b %Y')  # Format as "25th May 2023"
        title_link = f"`{title} <{filename.replace('.md', '.html')}>`_"
        index_content += f"   * - {formatted_date}\n"
        index_content += f"     - {title_link}\n"
        index_content += f"     - {authors_list}\n"
        index_content += f"     - {tags_list}\n"

    index_content += "\n"

# Write the index to a file
index_path = os.path.join(script_directory, 'index.rst')
if os.path.exists(index_path):
    os.remove(index_path)
with open(index_path, 'w') as index_file:
    index_file.write(content)
    index_file.write(index_content)

print(f"Index generated successfully at {index_path}.")
