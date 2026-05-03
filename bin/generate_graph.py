import re
import json
import os

def normalize_name(name):
    # Remove braces
    name = name.replace('{', '').replace('}', '').strip()
    # Remove HTML tags
    name = re.sub(r'<[^>]+>', '', name)
    # Remove parenthetical notes like (†)
    name = re.sub(r'\([^)]+\)', '', name)
    # Normalize spacing
    name = re.sub(r'\s+', ' ', name).strip()
    
    if ',' in name:
        parts = [p.strip() for p in name.split(',')]
        if len(parts) == 2:
            name = f"{parts[1]} {parts[0]}"
            
    # Normalize user's name variant
    if "Doan Hieu Nguyen" in name or "Nguyen Doan Hieu" in name:
        name = "Nguyen Doan Hieu Nguyen"
        
    return name.strip()

def generate_graph():
    bib_file = '_bibliography/papers.bib'
    data_dir = '_data'
    out_file = os.path.join(data_dir, 'coauthors_graph.json')
    
    if not os.path.exists(bib_file):
        print(f"File {bib_file} not found.")
        return
        
    try:
        with open(bib_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except (TypeError, UnicodeDecodeError):
        with open(bib_file, 'r') as f:
            content = f.read()

    # Match individual bib entries
    entries = re.split(r'@\w+{', content)
    
    # Let's define target user
    me = "Nguyen Doan Hieu Nguyen"
    
    # Store co-authorship counts
    coauthor_counts = {}
    
    for entry in entries:
        if not entry.strip():
            continue
            
        # Extract author field
        author_match = re.search(r'author\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE | re.DOTALL)
        if author_match:
            author_str = author_match.group(1)
            # Normalize internal newlines/tabs
            author_str = re.sub(r'\s+', ' ', author_str)
            # Split authors
            raw_authors = re.split(r'\s+and\s+', author_str, flags=re.IGNORECASE)
            
            # Normalize each author name
            normalized_authors = [normalize_name(a) for a in raw_authors if a.strip()]
            
            # Is "me" in this paper?
            if me in normalized_authors:
                for author in normalized_authors:
                    if author != me:
                        coauthor_counts[author] = coauthor_counts.get(author, 0) + 1

    # Total papers for me
    my_paper_count = 0
    for entry in entries:
        if not entry.strip():
            continue
        author_match = re.search(r'author\s*=\s*[{"]([^}"]+)[}"]', entry, re.IGNORECASE | re.DOTALL)
        if author_match:
            author_str = author_match.group(1)
            author_str = re.sub(r'\s+', ' ', author_str)
            raw_authors = re.split(r'\s+and\s+', author_str, flags=re.IGNORECASE)
            normalized_authors = [normalize_name(a) for a in raw_authors if a.strip()]
            if me in normalized_authors:
                my_paper_count += 1

    # Construct nodes and links
    nodes = []
    links = []
    
    # Add me as the central node
    nodes.append({
        "id": me,
        "name": me,
        "symbolSize": 50,  # larger size for center
        "value": my_paper_count,
        "category": 0
    })
    
    for author, count in coauthor_counts.items():
        nodes.append({
            "id": author,
            "name": author,
            "symbolSize": 15 + count * 6,  # dynamic sizing
            "value": count,
            "category": 1
        })
        
        links.append({
            "source": me,
            "target": author,
            "value": count
        })
        
    categories = [{"name": "Self"}, {"name": "Co-authors"}]
    
    graph_data = {
        "nodes": nodes,
        "links": links,
        "categories": categories
    }
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated graph network data to {out_file}.")

if __name__ == "__main__":
    generate_graph()
