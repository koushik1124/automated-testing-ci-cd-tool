import unittest
import sys
import os
import tempfile
import json

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import process_file, process_api_response
from automation import file_automation, api_automation

class TestIntegration(unittest.TestCase):
    
    def test_file_processing_integration(self):
        """Test file automation and processing together."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json', encoding='utf-8') as temp_file:
            # Write sample data to the file
            test_data = {"name": "Integration Test", "value": 100}
            json.dump(test_data, temp_file)
            file_path = temp_file.name
        
        try:
            # Test file automation
            result = file_automation(file_path)
            self.assertTrue(result["success"])
            
            # Test file processing
            processed = process_file(file_path)
            self.assertEqual(processed["original_value"], 100)
            self.assertEqual(processed["processed_value"], 200)  # Assuming processing doubles the value
        finally:
            # Clean up temporary files
            os.unlink(file_path)
    
    def test_api_processing_integration(self):
        """Test API automation and processing together."""
        # Mock API response
        mock_response = {
            "userId": 1,
            "id": 1,
            "title": "delectus aut autem",
            "completed": False
        }
        
        # Test API processing
        processed = process_api_response(mock_response)
        self.assertIn("status", processed)
        self.assertEqual(processed["status"], "processed")

if __name__ == "__main__":
    unittest.main()