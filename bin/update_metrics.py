import re
import json
import os

def extract_journals_with_years(bib_file):
    results = [] # list of (journal, year)
    if not os.path.exists(bib_file):
        return results
    
    try:
        with open(bib_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except (TypeError, UnicodeDecodeError):
        with open(bib_file, 'r') as f:
            content = f.read()

    # Split into entries to keep journal/year pairs together
    entries = re.split(r'@\w+{', content)
    for entry in entries:
        journal_match = re.search(r'journal\s*=\s*[{"]([^}"]+)[}"]', entry)
        year_match = re.search(r'year\s*=\s*[{"](\d{4})[}"]', entry)
        if journal_match:
            journal = journal_match.group(1).strip()
            year = year_match.group(1).strip() if year_match else "unknown"
            results.append((journal, year))
            
    return results

def update_metrics():
    bib_path = '_bibliography/papers.bib'
    data_dir = '_data'
    data_path = os.path.join(data_dir, 'journal_metrics.json')
    
    journal_years = extract_journals_with_years(bib_path)
    
    existing_data = {}
    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            try:
                existing_data = json.load(f)
            except ValueError:
                existing_data = {}
            
    # Known metrics for various journals
    # (In a real scenario, this would fetch from an API)
    # Here we simulate some data for demonstration
    metrics_repo = {
        "Journal of Hazardous Materials": {
            "2025": {"if": "11.3", "jcr": "Q1"},
            "latest": {"if": "12.2", "jcr": "Q1"}
        },
        "Journal of Cheminformatics": {
            "2025": {"if": "5.7", "jcr": "Q1"},
            "latest": {"if": "5.7", "jcr": "Q1"}
        },
        "Journal of Pharmaceutical Analysis": {
            "default": {"if": "8.9", "jcr": "Q1"}
        }
    }
    
    updated = False
    for journal, year in journal_years:
        if journal not in existing_data:
            existing_data[journal] = {}
        
        # Ensure latest exists
        if "latest" not in existing_data[journal]:
            # Try to find in repo
            if journal in metrics_repo:
                existing_data[journal]["latest"] = metrics_repo[journal].get("latest", metrics_repo[journal].get("default", {"if": "", "jcr": ""}))
            else:
                existing_data[journal]["latest"] = {"if": "", "jcr": ""}
            updated = True
            
        # Ensure specific year exists
        if year != "unknown" and year not in existing_data[journal]:
            if journal in metrics_repo:
                existing_data[journal][year] = metrics_repo[journal].get(year, metrics_repo[journal].get("default", {"if": "", "jcr": ""}))
            else:
                existing_data[journal][year] = {"if": "", "jcr": ""}
            updated = True
                
    if updated:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(data_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        print("Updated " + data_path + " with multi-year data.")
    else:
        print("No updates needed.")

if __name__ == "__main__":
    update_metrics()
