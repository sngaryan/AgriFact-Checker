import re
import sqlite3
import config

def match_scheme(text: str) -> dict | None:
    """Scans the text and matches it to a scheme in the database using SQLite FTS5.
    
    Args:
        text (str): User submitted message text.
        
    Returns:
        dict | None: The matched scheme dictionary, or None if no match is found.
    """
    if not text or not text.strip():
        return None
        
    # Extract alphanumeric words (supporting English and Devanagari script for Hindi)
    # Devanagari Unicode block: \u0900-\u097F
    words = re.findall(r'\b[a-zA-Z0-9\u0900-\u097F]{3,}\b', text.lower())
    if not words:
        return None
        
    # Build FTS5 OR query (e.g. "gobar*" OR "kande*")
    fts_query = " OR ".join(f'"{w}*"' for w in words)
    
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        # We query the virtual FTS5 table and order by bm25 score (smaller is better match)
        cursor.execute('''
            SELECT name, name_hi, state, official_url, description, description_hi
            FROM schemes_search
            WHERE schemes_search MATCH ?
            ORDER BY bm25(schemes_search)
            LIMIT 1
        ''', (fts_query,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "name": row[0],
                "name_hi": row[1],
                "state": row[2],
                "official_url": row[3],
                "description": row[4],
                "description_hi": row[5]
            }
            
    except Exception as e:
        # Prevent database exceptions from blocking the main classification workflow
        print(f"Scheme matching error: {e}")
        
    return None
