import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import pandas as pd
from sklearn.model_selection import train_test_split
from config import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, 'data')
CUSTOM_AGRI_PATH = os.path.join(DATA_DIR, 'custom_agri_messages.csv')
SUPPLEMENT_PATH = os.path.join(DATA_DIR, 'raw', 'public_fake_news_supplement.csv')
PROCESSED_DIR = os.path.join(DATA_DIR, 'processed')

def clean_and_prepare():
    """Load, clean, deduplicate and split datasets into train, val, and test sets."""
    dfs = []
    
    if os.path.exists(CUSTOM_AGRI_PATH):
        df_agri = pd.read_csv(CUSTOM_AGRI_PATH)
        dfs.append(df_agri)
        print(f"Loaded {len(df_agri)} custom agriculture records.")
        
    if os.path.exists(SUPPLEMENT_PATH):
        df_supp = pd.read_csv(SUPPLEMENT_PATH)
        dfs.append(df_supp)
        print(f"Loaded {len(df_supp)} supplementary news records.")
        
    if not dfs:
        raise FileNotFoundError("No raw data files found in data/.")
        
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Ensure text and label columns exist
    if 'text' not in combined_df.columns or 'label' not in combined_df.columns:
        raise ValueError("Dataset missing required 'text' or 'label' columns.")
        
    # Clean text and labels
    combined_df['text'] = combined_df['text'].astype(str).str.strip()
    combined_df['label'] = combined_df['label'].astype(str).str.strip().str.lower()
    
    # Filter empty texts or invalid labels
    combined_df = combined_df[combined_df['text'] != '']
    combined_df = combined_df[combined_df['label'].isin(['genuine', 'misleading'])]
    
    # Remove duplicate texts
    initial_len = len(combined_df)
    combined_df = combined_df.drop_duplicates(subset=['text']).reset_index(drop=True)
    print(f"Removed {initial_len - len(combined_df)} duplicate text entries. Total clean samples: {len(combined_df)}")
    
    # Class distribution check
    class_counts = combined_df['label'].value_counts().to_dict()
    print(f"Class distribution: {class_counts}")
    
    # Stratified train (70%), validation (15%), test (15%) split
    train_df, temp_df = train_test_split(
        combined_df, 
        test_size=0.30, 
        stratify=combined_df['label'], 
        random_state=42
    )
    
    val_df, test_df = train_test_split(
        temp_df, 
        test_size=0.50, 
        stratify=temp_df['label'], 
        random_state=42
    )
    
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    train_path = os.path.join(PROCESSED_DIR, 'train.csv')
    val_path = os.path.join(PROCESSED_DIR, 'val.csv')
    test_path = os.path.join(PROCESSED_DIR, 'test.csv')
    full_path = os.path.join(PROCESSED_DIR, 'full_dataset.csv')
    
    combined_df.to_csv(full_path, index=False)
    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    print(f"Dataset preparation complete:")
    print(f"  - Full:  {len(combined_df)} samples -> {full_path}")
    print(f"  - Train: {len(train_df)} samples -> {train_path}")
    print(f"  - Val:   {len(val_df)} samples -> {val_path}")
    print(f"  - Test:  {len(test_df)} samples -> {test_path}")

if __name__ == '__main__':
    clean_and_prepare()
