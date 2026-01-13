"""
Data loading utilities for PyRate Framework.

Supports loading test data from various formats:
- CSV files
- Excel files (.xlsx, .xls)
- JSON files
"""

import pandas as pd
import json
import os
from typing import List, Dict, Any
from .exceptions import DataFileError


def load_dataset(file_path: str) -> List[Dict[str, Any]]:
    """
    Load test data from CSV, Excel, or JSON file.
    
    Args:
        file_path: Path to the data file
        
    Returns:
        List of dictionaries, where each dictionary represents a row/record
        
    Raises:
        DataFileError: If file doesn't exist, format is unsupported, or parsing fails
        
    Examples:
        >>> # Load CSV
        >>> data = load_dataset("tests/data/users.csv")
        >>> # Returns: [{'username': 'user1', 'password': 'pass1'}, ...]
        
        >>> # Load Excel
        >>> data = load_dataset("tests/data/testdata.xlsx")
        
        >>> # Load JSON
        >>> data = load_dataset("tests/data/config.json")
    """
    if not os.path.exists(file_path):
        raise DataFileError(f"Archivo no encontrado: {file_path}")

    ext = file_path.split('.')[-1].lower()
    try:
        if ext == 'csv':
            return pd.read_csv(file_path).to_dict(orient='records')
        elif ext in ['xlsx', 'xls']:
            return pd.read_excel(file_path).to_dict(orient='records')
        elif ext == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Ensure we always return a list
            return data if isinstance(data, list) else [data]
        else:
            raise DataFileError(
                f"Formato '{ext}' no soportado. Usa .csv, .xlsx, .xls o .json"
            )
    except DataFileError:
        raise  # Re-raise our own exceptions
    except Exception as e:
        raise DataFileError(f"Error leyendo datos desde {file_path}: {str(e)}")

