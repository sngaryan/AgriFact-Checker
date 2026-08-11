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
        
    # Check for private 10-digit mobile numbers (Indian mobile numbers starting with 6, 7, 8, 9)
    # Scammers use 10-digit mobile numbers for "helpline/whatsapp/contact", whereas Govt uses 1800 toll-free numbers.
    private_phone_pattern = re.compile(r'\b[6-9]\d{9}\b')
    phone_matches = private_phone_pattern.findall(text)
    
    # Exclude toll-free numbers (e.g. 1800-180-1551 or 18002005142)
    has_private_phone = len(phone_matches) > 0 and not ("1800" in text or "1800-" in text)

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

