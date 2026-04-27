import requests
import re
import json
import os

def get_scholar_metrics(userid):
    url = f"https://scholar.google.com/citations?user={userid}&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        
        # Simple regex extraction for citations and h-index
        citations_match = re.search(r'Citations</a></td><td class="gsc_rsb_std">(\d+)</td>', html)
        hindex_match = re.search(r'h-index</a></td><td class="gsc_rsb_std">(\d+)</td>', html)
        
        metrics = {
            "citations": int(citations_match.group(1)) if citations_match else 0,
            "h_index": int(hindex_match.group(1)) if hindex_match else 0,
            "last_updated": os.environ.get("GITHUB_RUN_ID", "local")
        }
        return metrics
    except Exception as e:
        print(f"Error fetching scholar metrics: {e}")
        return None

if __name__ == "__main__":
    # Get user ID from environment or default from config (if we were parsing it)
    # For now, we take it from a known source or the user's config
    scholar_id = "-aEoZCgAAAAJ"
    
    metrics = get_scholar_metrics(scholar_id)
    if metrics:
        os.makedirs("_data", exist_ok=True)
        with open("_data/scholar_metrics.json", "w") as f:
            json.dump(metrics, f, indent=2)
        print(f"Successfully updated scholar metrics: {metrics}")
    else:
        print("Failed to update scholar metrics.")
