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
        },
        "Expert Systems with Applications": {
            "default": {"if": "7.5", "jcr": "Q1"}
        },
        "IEEE Journal of Biomedical and Health Informatics": {
            "default": {"if": "6.8", "jcr": "Q1"}
        }
    }
    
    updated = False
    new_data = {}
    
    for journal, year in journal_years:
        if journal not in new_data:
            new_data[journal] = {}
        
        # Pull from existing data if it's already in the new format
        if journal in existing_data and isinstance(existing_data[journal], dict):
            # Migrate old root-level keys if present
            old_if = existing_data[journal].get("if")
            old_jcr = existing_data[journal].get("jcr")
            
            for k, v in existing_data[journal].items():
                if k not in ["if", "jcr"]: # Skip the root keys we are migrating
                    new_data[journal][k] = v
            
            # If latest is missing but old root keys exist, use them
            if "latest" not in new_data[journal] or new_data[journal]["latest"].get("if") == "":
                if old_if:
                    new_data[journal]["latest"] = {"if": old_if, "jcr": old_jcr or ""}
                elif journal in metrics_repo:
                     new_data[journal]["latest"] = metrics_repo[journal].get("latest", metrics_repo[journal].get("default", {"if": "", "jcr": ""}))
                else:
                    new_data[journal]["latest"] = {"if": "", "jcr": ""}
        
        # Ensure latest exists
        if "latest" not in new_data[journal] or new_data[journal]["latest"].get("if") == "":
            if journal in metrics_repo:
                new_data[journal]["latest"] = metrics_repo[journal].get("latest", metrics_repo[journal].get("default", {"if": "", "jcr": ""}))
            else:
                new_data[journal]["latest"] = {"if": "", "jcr": ""}
            
        # Ensure specific year exists
        if year != "unknown" and (year not in new_data[journal] or new_data[journal][year].get("if") == ""):
            if journal in metrics_repo:
                new_data[journal][year] = metrics_repo[journal].get(year, metrics_repo[journal].get("default", {"if": "", "jcr": ""}))
            else:
                new_data[journal][year] = {"if": "", "jcr": ""}

    # Check if anything actually changed
    if new_data != existing_data:
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        with open(data_path, 'w') as f:
            json.dump(new_data, f, indent=2)
        print("Updated " + data_path + " with cleaned multi-year data.")
    else:
        print("No updates needed.")

if __name__ == "__main__":
    update_metrics()
