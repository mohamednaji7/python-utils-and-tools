import json
# Load JSON data
urls = json.load(open('input/urls.json'))

def links_str_to_list(links_str):
    return [link.strip() for link in links_str.split('\n') if link.strip()]

# Add a new category
key = "Arme, albuer og hånd"
links =  links_str_to_list("""
https://smertefribevaegelse.dk/karpaltunnelsyndrom/
https://smertefribevaegelse.dk/golfalbue/
https://smertefribevaegelse.dk/tennisalbue/
https://smertefys.nu/problematikker/tennisalbue/
https://cphosteopati.com/behandling/h-ndledssmerter
https://cphosteopati.com/behandling/albuesmerter                            
        """)
scraped = [False] * len(links)

# add the new category to the dictionary in the index 3
new_urls = {}
keys = list(urls.keys())  # Get keys in order
insert_index = 3
for index, existing_key in enumerate(keys):
    if index == insert_index:  # Insert new category at index 3
        new_urls[key] = {'links': links, 'scraping_states': scraped}
    new_urls[existing_key] = urls[existing_key]  # Add existing keys

# Verify the updated dictionary
from rich.console import Console
from rich.table import Table

# Initialize the table
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Category")
table.add_column("Start")
table.add_column("End")

# Counter for indexing
i = 1
for key in new_urls:
    start = i
    end = i + len(new_urls[key]['links']) - 1
    table.add_row(key, str(start), str(end))
    i = end + 1  # Update the counter

# Print the table
console = Console()
console.print(table)