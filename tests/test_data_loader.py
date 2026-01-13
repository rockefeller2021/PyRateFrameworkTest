"""
Tests for PyRate data loader module.
"""
import pytest
import os
import tempfile
import pandas as pd
import json
from pyrate.data_loader import load_dataset
from pyrate.exceptions import DataFileError
class TestCSVLoading:
    """Test CSV file loading."""
    
    def test_load_valid_csv(self):
        """Should load valid CSV file."""
        csv_content = "username,password\nuser1,pass1\nuser2,pass2"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(csv_content)
            temp_path = f.name
        
        try:
            data = load_dataset(temp_path)
            
            assert len(data) == 2
            assert data[0]["username"] == "user1"
            assert data[0]["password"] == "pass1"
            assert data[1]["username"] == "user2"
        finally:
            os.unlink(temp_path)
class TestExcelLoading:
    """Test Excel file loading."""
    
    def test_load_valid_excel(self):
        """Should load valid Excel file."""
        df = pd.DataFrame({
            "name": ["Alice", "Bob"],
            "age": [30, 25]
        })
        
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as f:
            temp_path = f.name
        
        try:
            df.to_excel(temp_path, index=False, engine='openpyxl')
            data = load_dataset(temp_path)
            
            assert len(data) == 2
            assert data[0]["name"] == "Alice"
            assert data[0]["age"] == 30
        finally:
            os.unlink(temp_path)
class TestJSONLoading:
    """Test JSON file loading."""
    
    def test_load_json_array(self):
        """Should load JSON array."""
        json_content = [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(json_content, f)
            temp_path = f.name
        
        try:
            data = load_dataset(temp_path)
            
            assert len(data) == 2
            assert data[0]["id"] == 1
            assert data[1]["name"] == "Item 2"
        finally:
            os.unlink(temp_path)
class TestErrorHandling:
    """Test error handling for data loader."""
    
    def test_file_not_found(self):
        """Should raise DataFileError when file doesn't exist."""
        with pytest.raises(DataFileError, match="Archivo no encontrado"):
            load_dataset("nonexistent_file.csv")
    
    def test_unsupported_format(self):
        """Should raise DataFileError for unsupported formats."""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as f:
            temp_path = f.name
        
        try:
            with pytest.raises(DataFileError, match="no soportado"):
                load_dataset(temp_path)
        finally:
            os.unlink(temp_path)