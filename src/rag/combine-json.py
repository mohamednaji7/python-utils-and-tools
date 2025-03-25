import json 
import os
     
def save_json(json_path, json_data, indent=4):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=indent, ensure_ascii=False)

def remove_duplicates(data, unique_key='url'):
    """
    Remove duplicate entries based on a specified unique key.
    
    :param data: List of dictionaries to deduplicate
    :param unique_key: Key to use for identifying unique entries
    :return: List of unique entries
    """
    seen = {}
    
    for item in data:
        # Use the value of the unique key to identify duplicates
        identifier = item.get(unique_key)
        
        if identifier not in seen:
            # First time seeing this identifier
            # Create a new entry with 'cat' as a list
            seen_item = item.copy()  # Create a copy to avoid modifying original
            seen_item['cat'] = [item['subdir']]
            seen[identifier] = seen_item
        else:
            # We've seen this identifier before
            # Add the new subdir to the existing 'cat' list
            if 'cat' not in seen[identifier]:
                seen[identifier]['cat'] = []
            
            # Only append if not already in the list
            if item['subdir'] not in seen[identifier]['cat']:
                seen[identifier]['cat'].append(item['subdir'])

    # Convert dictionary back to list for consistency
    return list(seen.values())

# Combine JSON files from the scraped_data_json folder
results = []
output_dir = "scraped_data_json"
for filename in os.listdir(output_dir):
    json_path = f"{output_dir}/{filename}"
    print(json_path)
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results.extend(data)

# Remove duplicates
deduplicated_results = remove_duplicates(results)

# Print out some statistics
print(f"Total entries before deduplication: {len(results)}")
print(f"Total entries after deduplication: {len(deduplicated_results)}")

# Save the deduplicated results
save_json("results_deduplicated.json", deduplicated_results, indent=2)
