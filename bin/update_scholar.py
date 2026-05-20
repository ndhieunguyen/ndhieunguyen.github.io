import requests
import re
import json
import os

def update_scholar_data(userid):
    url = f"https://scholar.google.com/citations?user={userid}&hl=en&cstart=0&pagesize=100"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        
        # 1. Extract total metrics (citations, h-index)
        citations_match = re.search(r'Citations</a></td><td class="gsc_rsb_std">(\d+)</td>', html)
        hindex_match = re.search(r'h-index</a></td><td class="gsc_rsb_std">(\d+)</td>', html)
        
        metrics = {
            "citations": int(citations_match.group(1)) if citations_match else 0,
            "h_index": int(hindex_match.group(1)) if hindex_match else 0,
            "last_updated": os.environ.get("GITHUB_RUN_ID", "local")
        }
        
        # Save user-level metrics
        os.makedirs("_data", exist_ok=True)
        with open("_data/scholar_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        print(f"Successfully updated scholar metrics: {metrics}")
        
        # 2. Extract individual paper citations
        citations_dict = {}
        rows = re.findall(r'<tr class="gsc_a_tr">.*?</tr>', html, re.DOTALL)
        for row in rows:
            id_match = re.search(r'citation_for_view=[a-zA-Z0-9_-]+?:([a-zA-Z0-9_-]+)', row)
            cite_match = re.search(r'class="gsc_a_ac[^"]*">([\d]+)</a>', row)
            
            if id_match:
                paper_id = id_match.group(1)
                citations = int(cite_match.group(1)) if cite_match else 0
                citations_dict[paper_id] = citations
        
        # Save paper-level citations
        with open("_data/scholar_citations.json", "w") as f:
            json.dump(citations_dict, f, indent=2)
        print(f"Successfully updated scholar citations for {len(citations_dict)} papers.")
        return True
        
    except Exception as e:
        print(f"Error fetching scholar metrics: {e}")
        return False

if __name__ == "__main__":
    scholar_id = "-aEoZCgAAAAJ"
    update_scholar_data(scholar_id)
