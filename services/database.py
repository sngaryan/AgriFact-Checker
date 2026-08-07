import os
import sqlite3
import datetime
import json
import config

def get_db_connection():
    """Create and return a database connection."""
    db_path = config.DATABASE_PATH
    # Ensure the parent directory exists (e.g. instance/)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    """Initialize tables safely if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create checks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS checks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submitted_text TEXT NOT NULL,
            predicted_label TEXT NOT NULL,
            confidence REAL NOT NULL,
            influential_terms TEXT,
            detected_domain TEXT,
            domain_status TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    # Create feedback table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            check_id INTEGER NOT NULL,
            vote TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(check_id) REFERENCES checks(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_check(payload: dict) -> int:
    """Save a check result to the database.
    
    Args:
        payload (dict): containing submitted_text, predicted_label, confidence,
                         influential_terms (list), detected_domain, domain_status.
                         
    Returns:
        int: The inserted check ID.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert list of terms to comma-separated string or JSON string
    terms = json.dumps(payload.get("influential_terms", []))
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    
    cursor.execute('''
        INSERT INTO checks (
            submitted_text, predicted_label, confidence, 
            influential_terms, detected_domain, domain_status, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        payload["submitted_text"],
        payload["predicted_label"],
        payload["confidence"],
        terms,
        payload.get("detected_domain", ""),
        payload.get("domain_status", ""),
        created_at
    ))
    
    check_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return check_id

def get_recent_checks(limit: int = 20) -> list[dict]:
    """Retrieve recent check records from the database.
    
    Args:
        limit (int): Maximum number of checks to retrieve.
        
    Returns:
        list[dict]: List of checks.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, submitted_text, predicted_label, confidence,
               influential_terms, detected_domain, domain_status, created_at
        FROM checks
        ORDER BY id DESC
        LIMIT ?
    ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    checks = []
    for row in rows:
        check_dict = dict(row)
        # Parse the JSON string back into a list
        try:
            check_dict["influential_terms"] = json.loads(check_dict["influential_terms"])
        except Exception:
            check_dict["influential_terms"] = []
        checks.append(check_dict)
        
    return checks

def save_feedback(check_id: int, vote: str) -> None:
    """Save feedback (upvote/downvote) for a given check ID.
    
    Args:
        check_id (int): The associated check ID.
        vote (str): Must be 'upvote' or 'downvote'.
    """
    if vote not in ('upvote', 'downvote'):
        raise ValueError("Vote must be 'upvote' or 'downvote'")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify check_id exists
    cursor.execute("SELECT id FROM checks WHERE id = ?", (check_id,))
    if cursor.fetchone() is None:
        conn.close()
        raise ValueError(f"Check ID {check_id} does not exist.")
        
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    
    cursor.execute('''
        INSERT INTO feedback (check_id, vote, created_at)
        VALUES (?, ?, ?)
    ''', (check_id, vote, created_at))
    
    conn.commit()
    conn.close()
