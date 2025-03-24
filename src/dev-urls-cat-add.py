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

# save the json file
with open('input/urls.json', 'w') as f:
    json.dump(new_urls, f, indent=4)