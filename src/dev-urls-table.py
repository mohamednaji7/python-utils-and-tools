import json
from rich.console import Console
from rich.table import Table

# Load JSON data
urls = json.load(open('input/urls.json'))

# Initialize the table
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Category")
table.add_column("Start")
table.add_column("End")

# Counter for indexing
i = 1
for key in urls:
    start = i
    end = i + len(urls[key]['links']) - 1
    table.add_row(key, str(start), str(end))
    i = end + 1  # Update the counter

# Print the table
console = Console()
console.print(table)
