import pandas as pd
import json
import re
from typing import List, Dict, Any, Optional
from pathlib import Path


class DataProcessor:
    """
    Handles loading and preprocessing of product data from various sources.
    """
    
    def __init__(self, data_path: Optional[str] = None):
        """Initialize the data processor with optional data path"""
        self.data_path = data_path
        self.dataframe = None
    
    def load_from_tsv(self, file_path: Optional[str] = None) -> pd.DataFrame:
        """Load product data from a TSV file"""
        path = file_path or self.data_path
        if not path:
            raise ValueError("No file path provided")
        
        self.dataframe = pd.read_csv(path, sep='\t')
        return self.dataframe
    
    def load_from_string(self, content: str) -> pd.DataFrame:
        """Load product data from a string content (TSV format)"""
        lines = content.split('\n')
        headers = lines[0].split('\t')
        
        data = []
        for i in range(1, len(lines)):
            if not lines[i].strip():
                continue
                
            values = lines[i].split('\t')
            if len(values) >= len(headers):
                row = {}
                for j, header in enumerate(headers):
                    row[header] = values[j]
                data.append(row)
        
        self.dataframe = pd.DataFrame(data)
        return self.dataframe
    
    def clean_dataframe(self) -> pd.DataFrame:
        """Clean and preprocess the dataframe"""
        if self.dataframe is None:
            raise ValueError("No data loaded yet")
        
        # Remove any duplicate products
        self.dataframe = self.dataframe.drop_duplicates(subset=['uniq_id'], keep='first')
        
        # Convert price columns to numeric
        self.dataframe['retail_price'] = pd.to_numeric(self.dataframe['retail_price'], errors='coerce')
        self.dataframe['discounted_price'] = pd.to_numeric(self.dataframe['discounted_price'], errors='coerce')
        
        # Fill missing values
        self.dataframe['product_name'] = self.dataframe['product_name'].fillna('')
        self.dataframe['description'] = self.dataframe['description'].fillna('')
        self.dataframe['brand'] = self.dataframe['brand'].fillna('Unknown')
        
        return self.dataframe
    
    def get_processed_data(self) -> pd.DataFrame:
        """Get the cleaned and processed dataframe"""
        if self.dataframe is None:
            raise ValueError("No data loaded yet")
            
        return self.clean_dataframe()