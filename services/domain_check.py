import re
import json
import os
from urllib.parse import urlparse
from config import VERIFIED_DOMAINS_PATH

def check_domains(text: str) -> dict:
    """Extract URLs, domain names, and contact phone numbers for security & trust evaluation.
    
    Args:
        text (str): Input text containing potential URLs, domain names, or phone numbers.
        
    Returns:
        dict: containing detected_domain, domain_status, has_private_phone, and is_suspicious_signal.
    """
    if not text:
        return {
            "detected_domain": "",
            "domain_status": "no_domain_found",
            "has_private_phone": False,
            "is_suspicious_signal": False
        }
        
    # Check for private mobile numbers (including with +91, spaces, hyphens) or UPI payment scams.
    # Scammers frequently ask for money via UPI or personal mobile numbers.
    # Official government schemes use 1800 toll-free numbers and never request UPI transfers.
    has_upi_scam = bool(re.search(r'\b(?:upi\s*(?:no|id|number)?|gpay|paytm|phonepe)\b', text, re.IGNORECASE))
    phone_pattern = re.compile(r'(?:\+?91[\s-]?)?(?:0[\s-]?)?([1-9]\d{4}[\s-]?[1-9]\d{4}|[1-9]\d{4}[\s-]?\d{5}|[6-9]\d{9})\b')
    phone_matches = phone_pattern.findall(text)
    
    is_toll_free = bool(re.search(r'\b1800[\s-]?\d{3}[\s-]?\d{4}\b', text))
    has_private_phone = (len(phone_matches) > 0 or has_upi_scam) and not is_toll_free

    # Primary regex: URLs starting with http://, https://, or www.
    url_pattern = re.compile(
        r'(?:https?://|www\.)[a-zA-Z0-9.\-_]+(?:\.[a-zA-Z]{2,})+(?:[/?#]\S*)?',
        re.IGNORECASE
    )
    
    # Secondary regex: Standalone domain names
    domain_pattern = re.compile(
        r'\b(?:[a-zA-Z0-9\-_]+\.)+(?:gov\.[a-z]{2,3}|nic\.in|gov|org|com|net|edu|info|online|site|xyz|tech|top|in)\b',
        re.IGNORECASE
    )
    
    matches = url_pattern.findall(text)
    if not matches:
        matches = domain_pattern.findall(text)
        
    if not matches:
        return {
            "detected_domain": "",
            "domain_status": "no_domain_found",
            "has_private_phone": has_private_phone,
            "is_suspicious_signal": has_private_phone
        }
        
    first_url = matches[0].strip()
    
    # Ensure it starts with http/https for urlparse
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
            "domain_status": "no_domain_found",
            "has_private_phone": has_private_phone,
            "is_suspicious_signal": has_private_phone
        }
        
    if not host:
        return {
            "detected_domain": "",
            "domain_status": "no_domain_found",
            "has_private_phone": has_private_phone,
            "is_suspicious_signal": has_private_phone
        }
        
    if not os.path.exists(VERIFIED_DOMAINS_PATH):
        raise FileNotFoundError(f"Verified domains config file not found at {VERIFIED_DOMAINS_PATH}")
        
    with open(VERIFIED_DOMAINS_PATH, 'r', encoding='utf-8') as f:
        verified_data = json.load(f)
        
    verified_domains = [item['domain'].lower() for item in verified_data]
    
    # Check if host matches any verified official domain
    is_verified = False
    for domain in verified_domains:
        if host == domain or host.endswith('.' + domain):
            is_verified = True
            break

    # Identify URL shorteners or suspicious TLDs
    suspicious_tlds = ['.online', '.site', '.info', '.xyz', '.top', '.tech', '.win', '.vip', '.work', '.icu', '.club']
    shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'is.gd', 'buff.ly', 'rebrand.ly', 'cutt.ly', 'goo.gl']
    
    is_suspicious_link = any(host.endswith(tld) for tld in suspicious_tlds) or any(s in host for s in shorteners)
    
    return {
        "detected_domain": host,
        "domain_status": "verified" if is_verified else "not_in_list",
        "has_private_phone": has_private_phone,
        "is_suspicious_signal": has_private_phone or is_suspicious_link
    }

