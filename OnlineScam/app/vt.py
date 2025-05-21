import requests
import os
import time
import base64
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("VT_API_KEY")

def url_to_vt_id(url: str) -> str:
    """
    Convert a URL to VirusTotal URL ID:
    1. Convert URL string to bytes (utf-8)
    2. Base64 encode
    3. Remove padding '=' signs
    """
    url_bytes = url.encode('utf-8')
    b64_encoded = base64.urlsafe_b64encode(url_bytes).decode('utf-8')
    return b64_encoded.strip('=')

def check_url_virustotal(url: str, max_retries=5, wait_seconds=3):
    api_url = "https://www.virustotal.com/api/v3/urls"
    headers = {
        "x-apikey": API_KEY
    }

    # Step 1: submit URL scan (raw URL)
    response = requests.post(api_url, headers=headers, data={"url": url})
    if response.status_code != 200:
        raise Exception(f"VirusTotal scan submission failed: {response.text}")

    # Step 2: Convert URL to VirusTotal URL ID (base64 encoded, no padding)
    url_id = url_to_vt_id(url)

    # Step 3: retry to get report (it may not be ready immediately)
    report_url = f"{api_url}/{url_id}"
    for attempt in range(max_retries):
        report = requests.get(report_url, headers=headers)
        if report.status_code == 404:
            # Report not ready yet, wait and retry
            time.sleep(wait_seconds)
            continue
        elif report.status_code != 200:
            raise Exception(f"VirusTotal report fetch failed: {report.text}")

        data = report.json()["data"]["attributes"]
        stats = data["last_analysis_stats"]

        total = sum(stats.values())
        if total == 0:
            time.sleep(wait_seconds)
        else:
            total_detections = stats["malicious"] + stats["suspicious"]
            return {
                "harmless": stats["harmless"],
                "malicious": stats["malicious"],
                "suspicious": stats["suspicious"],
                "undetected": stats["undetected"],
                "timeout": stats["timeout"],
                "verdict": "Scam" if total_detections > 0 else "Safe"
            }

    raise Exception("VirusTotal analysis not ready after retries")
