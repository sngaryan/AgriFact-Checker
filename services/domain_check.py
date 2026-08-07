import re
import json
import os
from urllib.parse import urlparse
from config import VERIFIED_DOMAINS_PATH

def check_domains(text: str) -> dict:
    """Extract the first URL host and return its trust-list state.
    
    Args:
        text (str): Input text containing potential URLs.
        
    Returns:
        dict: containing detected_domain and domain_status.
    """
    # Regex to find URLs starting with http://, https://, or www.
    url_pattern = re.compile(
        r'(?:https?://|www\.)[a-zA-Z0-9.\-_]+(?:\.[a-zA-Z]{2,})+(?:[/?#]\S*)?',
        re.IGNORECASE
    )
    
    matches = url_pattern.findall(text)
    if not matches:
        return {
            "detected_domain": "",
            "domain_status": "no_domain_found"
        }
        
    first_url = matches[0]
    
    # Ensure it starts with http/https for urlparse to parse correctly
    if not (first_url.startswith('http://') or first_url.startswith('https://')):
        url_to_parse = 'http://' + first_url
    else:
        url_to_parse = first_url
        
    try:
        parsed = urlparse(url_to_parse)
        host = parsed.netloc.lower()
        if ':' in host:
            host = host.split(':')[0]
        if host.startswith('www.'):
            host = host[4:]
    except Exception:
        return {
            "detected_domain": "",
            "domain_status": "no_domain_found"
        }
        
    if not host:
        return {
            "detected_domain": "",
            "domain_status": "no_domain_found"
        }
        
    if not os.path.exists(VERIFIED_DOMAINS_PATH):
        raise FileNotFoundError(f"Verified domains config file not found at {VERIFIED_DOMAINS_PATH}")
        
    with open(VERIFIED_DOMAINS_PATH, 'r', encoding='utf-8') as f:
        verified_data = json.load(f)
        
    verified_domains = [item['domain'].lower() for item in verified_data]
    
    # Validate against trust list
    is_verified = False
    for domain in verified_domains:
        if host == domain or host.endswith('.' + domain):
            is_verified = True
            break
            
    return {
        "detected_domain": host,
        "domain_status": "verified" if is_verified else "not_in_list"
    }
