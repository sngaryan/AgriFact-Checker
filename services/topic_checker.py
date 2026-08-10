import re

# Comprehensive list of agriculture, farming, crop, livestock, weather, and scheme-related terms in English and Hindi
AGRICULTURAL_KEYWORDS = {
    # English terms
    "agri", "agriculture", "agricultural", "farm", "farmer", "farmers", "farming", "crop", "crops",
    "soil", "fertilizer", "fertilizers", "pesticide", "pesticides", "insecticide", "irrigation",
    "harvest", "harvesting", "yield", "seed", "seeds", "sowing", "kisan", "krishi", "subsidy",
    "subsidies", "subsidized", "scheme", "schemes", "mandi", "apmc", "msp", "monsoon", "drought",
    "rainfall", "weather", "livestock", "dairy", "cattle", "cow", "buffalo", "poultry", "goat",
    "sheep", "tractor", "pump", "pumps", "solar", "drone", "drones", "nabard", "icar", "kvk",
    "pmkisan", "pm-kisan", "kusum", "acabc", "smam", "rkvy", "soil-health", "organic", "horticulture",
    "floriculture", "sericulture", "pisciculture", "aquaculture", "paddy", "wheat", "rice", "maize",
    "cotton", "sugarcane", "pulses", "mustard", "soybean", "millet", "jowar", "bajra", "rabi", "kharif",
    "zaid", "manure", "vermicompost", "drip", "sprinkler", "greenhouse", "polyhouse", "warehouse",
    "cold-storage", "loan", "kcc", "credit-card", "crop-insurance", "pmfby", "fasal", "bima",

    # Hindi terms (Devanagari)
    "कृषि", "किसान", "खेती", "फसल", "फसलों", "बीज", "खाद", "उर्वरक", "कीटनाशक", "सिंचाई",
    "कटाई", "बुवाई", "पैदावार", "मंडी", "सब्सिडी", "योजना", "योजनाओं", "ऋण", "लोन", "मौसम",
    "बारिश", "मानसून", "सूखा", "पशुपालन", "डेयरी", "गाय", "भैंस", "ट्रैक्टर", "पंप", "सोलर",
    "ड्रोन", "एमएसपी", "पीएम-किसान", "केसीसी", "बीमा", "फसल-बीमा", "मिट्टी", "उवर्रक", "सिंचाई",
    "गेहूं", "धान", "चावल", "मक्का", "कपास", "गन्ना", "दलहन", "सरसों", "सोयाबीन", "बाजरा",
    "ज्वार", "रबी", "खरीफ", "जैविक", "बागवानी", "गोदाम", "कोल्ड-स्टोरेज", "क्रेडिट-कार्ड"
}

def check_agricultural_relevance(text: str) -> dict:
    """Check if the provided text contains agricultural or farming-related context.
    
    Args:
        text (str): Input claim or OCR text.
        
    Returns:
        dict: containing 'is_relevant' (bool), 'matched_terms' (list), and 'score' (float).
    """
    if not text or not text.strip():
        return {
            "is_relevant": False,
            "matched_terms": [],
            "score": 0.0
        }
        
    # Extract lowercased word tokens (English and Devanagari)
    words = re.findall(r'[\w-]+', text.lower())
    if not words:
        return {
            "is_relevant": False,
            "matched_terms": [],
            "score": 0.0
        }
        
    matched = []
    seen = set()
    
    for word in words:
        # Direct match or hyphenated/compound match
        if word in AGRICULTURAL_KEYWORDS and word not in seen:
            seen.add(word)
            matched.append(word)
        else:
            # Substring check for compound terms like 'pmkisan' or 'agri-business'
            for kw in ["agri", "kisan", "krishi", "pmkisan", "kusum", "pmfby"]:
                if kw in word and word not in seen:
                    seen.add(word)
                    matched.append(word)
                    break

    score = len(matched) / float(len(words)) if words else 0.0
    
    # Text is considered relevant if at least one distinct agricultural keyword is found
    is_relevant = len(matched) > 0
    
    return {
        "is_relevant": is_relevant,
        "matched_terms": matched,
        "score": round(score, 4)
    }
